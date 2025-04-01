# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

import frappe,time
from frappe.model.document import Document


class StudentExam(Document):
    def before_save(self):
        pass
        # self.validate_color_ranges()

    def validate_color_ranges(self):
        # Initialize variables for tracking colors
        green_end_to = None
        yellow_end_to = None
        red_end_to = 100  # The last rank from the main Student Exam doc

        # Loop through the color_generation child table
        for row in self.color_generation:
            if row.color == "Green":
                # Validate Green: starts_from should be 1
                if row.starts_from != 1:
                    frappe.throw(("Green should start from 1."))

                # Store Green's end_to for later validation of Yellow
                green_end_to = row.end_to

            elif row.color == "Yellow":
                # Ensure Green's end_to is already set
                if green_end_to is None:
                    frappe.throw(("Please define Green's range before Yellow."))

                # Validate Yellow: starts_from should be Green's end_to + 1
                if row.starts_from != green_end_to + 1:
                    frappe.throw(("Yellow should start from {0}.").format(green_end_to + 1))

                # Store Yellow's end_to for future validation of Red
                yellow_end_to = row.end_to

            elif row.color == "Red":
                # Ensure Yellow's end_to is already set
                if yellow_end_to is None:
                    frappe.throw(("Please define Yellow's range before Red."))

                # Validate Red: starts_from should be Yellow's end_to + 1
                if row.starts_from != yellow_end_to + 1:
                    frappe.throw(("Red should start from {0}.").format(yellow_end_to + 1))

                # Validate Red's end_to: it should be equal to self.last_rank
                if row.end_to != red_end_to:
                    
                    frappe.throw(("Red's end should be equal to the last rank {0}.").format(red_end_to))

        # Validate that all colors are defined correctly
        if not green_end_to:
            frappe.throw(("Please ensure that 'Green' rank range is defined."))
        if not yellow_end_to:
            frappe.throw(("Please ensure that 'Yellow' rank range is defined."))
            
    def on_update(self):
        pass
        # Ensure that exam_date is not empty before proceeding
        # if self.exam_date:
        #     # Fetch the Student Results entry where exam_id equals self.name
        #     student_result = frappe.get_value("Student Results", {"exam_id": self.name}, "name")
            
        #     if student_result:
        #         # Load the document using the name from get_value
        #         student_result_doc = frappe.get_doc("Student Results", student_result)
                
        #         # Update the exam_date in Student Results
        #         student_result_doc.exam_date = self.exam_date
        #         student_result_doc.save()
        #         # frappe.msgprint(f"Student Results updated with exam date for Batch ID: {self.name}")
        #     else:
        #         pass
        #         # frappe.msgprint(f"No Student Results found for Batch ID: {self.name}")
        # else:
        #     frappe.msgprint(f"Exam date is not set for Batch ID: {self.name}. Please add the exam date.")



####################################Vatsal's Working Modified code for conditional live and enqueing bulk operations start ######





















####################################Vatsal's Working Modified code for enqueing bulk operations start #########################


@frappe.whitelist()
def student_process_data(name, limit=1):
    try:
        students_exam_doc = frappe.get_doc('Student Exam', name)

        rq_job_for_student_exam = frappe.get_all("RQ Job",filters={"status":("in",["started","queued"])},fields=["arguments","name"])
        
        for job in rq_job_for_student_exam:
            if students_exam_doc.name in job.arguments:
                base_url = frappe.utils.get_url()
                job_url = f"{base_url}/app/rq-job/{job.name}"
                job_anchor_tag=f'<a href="{ base_url }/app/rq-job/{ job.name }">{ job.name }</a>'
                return {"status":False, "msg":f"Data processing is already in Queue {job_anchor_tag}. . . the operation will be finished in 10 minutes, Please wait for the operation to complete"}
        
        total_records = frappe.db.count('Students Master Data', filters={'imported': 0, 'exam_id': name})
        if not total_records:
            return {"status": False, "msg": f"No Student Master Data to process for this Exam {name}"}
            
        elif total_records > limit:
            # Enqueue the background job
            frappe.enqueue('tnc_frappe_custom_app.tnc_custom_app.doctype.student_exam.student_exam.process_students_in_background', 
                        queue='long', 
                        timeout=3000, 
                        name=name, 
                        # limit=limit
                        )
            students_exam_doc.status="In Queue"
            students_exam_doc.save()
            frappe.db.commit()
            return {"status":True,"enqueued":True,"msg":"Data syncing is Enqueued Successfully!"}
        else:
            response_realtime_data_processing=process_data_realtime(name)
            return response_realtime_data_processing

    except Exception as e:
        return {"status": False, "msg": str(e)}
    # process_students_in_background(name, start, limit)



def process_students_in_background(name):
    
    try:
        students_exam_doc = frappe.get_doc('Student Exam', name)
        exam_docname = students_exam_doc.name
        students_master_data = frappe.get_all('Students Master Data', filters={
            'imported': 0, 'exam_id': name
        }, fields=['name', 'student_name', 'mobile', 'state', 'rank', 'total_marks', 'district', 
                   'total_right', 'total_wrong', 'total_skip', 'percentage', 'exam_id'], 
            # start=start,
            # limit=limit,
                     )
                     
        master_data_highest_rank = frappe.get_value('Students Master Data', filters={'exam_id': name}, fieldname='rank', order_by='rank desc')
    
        if not students_master_data:
            frappe.log_error(frappe.get_traceback(), f"No Student Master Data To process for Exam {name}")
            return {"status": False, "msg": f"No Student Master Data To process"}
    
        # completed_records = 0
    
        for student_data in students_master_data:
            student_and_result_validation_and_creation(student_data)
            
            # completed_records += 1
        students_exam_doc.reload()
        students_exam_doc.status = 'Data Synced'
        students_exam_doc.start_rank = 1
        students_exam_doc.last_rank = master_data_highest_rank
        students_exam_doc.save()
        
        frappe.db.commit()
        assign_colors(exam_docname)
        frappe.db.commit()
        # print("Data Processing completed Successfullt!!")
    
        return {"status": True, "msg": f"Data Processed Successfully"}
    except Exception as e:
        students_exam_doc = frappe.get_doc('Student Exam', name)
        students_exam_doc.status="Failed Queue"
        students_exam_doc.save()
        frappe.log_error(frappe.get_traceback(), "Error in background sync")
        return {"status": False, "msg": f"Error in Background Processing Data: {str(e)}"}

####################################Vatsal's Working Modified code for enqueing bulk operations end #########################


#################################Vatsal's Working Modified code for % based progress publish and exception handling start #######

@frappe.whitelist()
def process_data_realtime(name):
    try:
        
        students_exam_doc = frappe.get_doc('Student Exam', name)
        students_exam_doc.status="In Queue"
        students_exam_doc.save()
        frappe.db.commit()
        
        # Fetch all records from Students Master Data where imported is not checked
        students_master_data = frappe.get_all('Students Master Data', filters={
            'imported': 0, 'exam_id': name
        }, fields=['name', 'student_name', 'mobile', 'state', 'rank', 'total_marks', 'district', 'total_right', 'total_wrong', 'total_skip', 'percentage', 'exam_id'], 
        # start=start, 
        # limit=limit
        )
    
        total_records = frappe.db.count('Students Master Data', filters={'imported': 0, 'exam_id': name})
    
        if not students_master_data:
            # If no records are found, return a message indicating no data to sync
            return {"status": "no_data", "progress": 100}
    
        completed_records = 0
        publish_iteration = 0
    
        # Loop through the fetched data and sync it
        for student_data in students_master_data:
            student_and_result_validation_and_creation(student_data)
            
            completed_records += 1
            progress = int((completed_records / total_records) * 100)

            if progress > publish_iteration:
                frappe.publish_realtime("sync_progress", {
                    "completed_records": completed_records,
                    "total_records": total_records,
                    "progress": progress,
                })
                publish_iteration += 1
    
        # Update the status of the 'Student Exam' document
        students_exam_doc.status = 'Data Synced'
        students_exam_doc.save()
    
        frappe.db.commit()
    
        return {"status": True, "msg": f"Data Processed Successfully"}
    except Exception as e:
        print(e)
        students_exam_doc.status="Failed Queue"
        students_exam_doc.save()
        frappe.db.commit()
        return {"status": False, "msg": f"Error in Processing Data: {str(e)}"}

###########################################Vatsal's Modified code for % based progress publish and exception handling end#######


def student_and_result_validation_and_creation(student_data):
    try:
        existing_student = frappe.db.exists('Online Student', {'mobile': student_data['mobile']})
        student_id = None
        if not existing_student:
            try:
                new_student = frappe.get_doc({
                    'doctype': 'Online Student',
                    'student_name': student_data['student_name'],
                    'mobile': student_data['mobile'],
                    'state': student_data['state'],
                    'district': student_data['district'],
                    'system_imported': 1,
                    'exam_id': student_data['exam_id'],
                    'total_exams':1,
                })
                new_student.insert()
                student_id = new_student.name
            except Exception as e:
                frappe.get_doc({
                    'doctype': 'Not Imported Logs',
                    'exam_id': student_data['exam_id'],
                    'student_name': student_data['student_name'],
                    'mobile': student_data['mobile'],
                    'exam_date': student_data.get('date'),
                    'district': student_data['district'],
                    'state': student_data['state'],
                    'rank': student_data.get('rank'),
                    'total_marks': student_data.get('total_marks'),
                    'total_right': student_data.get('total_right'),
                    'total_wrong': student_data.get('total_wrong'),
                    'total_skip': student_data.get('total_skip'),
                    'percentage': student_data.get('percentage'),
                    'student_master_data_id': student_data['name'],
                }).insert()
                
                frappe.log_error(frappe.get_traceback(), f"Error in creating Student: {str(e)}")
                return

        else:
            student_doc = frappe.get_doc('Online Student', existing_student )
            old_test_series_results = frappe.get_all('Student Results',filters={"student_id":existing_student})
            student_doc.total_exams=len(old_test_series_results)+1
            student_doc.save()
            student_id = student_doc.name
        try:
            new_test_series_result = frappe.get_doc({
                'doctype': 'Student Results',
                'student_id': student_id,
                'student_name': student_data['student_name'],
                'student_mobile': student_data['mobile'],
                'exam_date': student_data.get('date'),
                'rank': student_data.get('rank'),
                'total_marks': student_data.get('total_marks'),
                'total_right': student_data.get('total_right'),
                'total_wrong': student_data.get('total_wrong'),
                'total_skip': student_data.get('total_skip'),
                'percentage': student_data.get('percentage'),
                'exam_id': student_data.get('exam_id'),
                'system_imported': 1
            })
            new_test_series_result.insert()

            frappe.db.set_value('Students Master Data', student_data['name'], 'imported', 1)
            print('Student Result Created')
            # print(completed_records)

        except Exception as e:
            # print(e)
            frappe.get_doc({
                    'doctype': 'Not Imported Logs',
                    'error_message' : frappe.get_traceback(),
                    'exam_id': student_data['exam_id'],
                    'student_name': student_data['student_name'],
                    'mobile': student_data['mobile'],
                    'exam_date': student_data.get('date'),
                    'district': student_data['district'],
                    'state': student_data['state'],
                    'rank': student_data.get('rank'),
                    'total_marks': student_data.get('total_marks'),
                    'total_right': student_data.get('total_right'),
                    'total_wrong': student_data.get('total_wrong'),
                    'total_skip': student_data.get('total_skip'),
                    'percentage': student_data.get('percentage'),
                    'student_master_data_id': student_data['name'],
                    # 'student_id': student_id if student_id else None,
                }).insert()

            frappe.log_error(frappe.get_traceback(), f"Error in creating Student Results: {str(e)}")
#    frappe.log_error(frappe.get_traceback(), f"Error syncing student master data {student_data['name']} in Student Exam {student_data['exam_id']} for student name {student_data['student_name']} with mobile number {student_data['mobile']}.")
    except Exception as e:
        # General error logging
        frappe.log_error(frappe.get_traceback(), f"Error syncing student master data {student_data['name']} in Student Exam {student_data['exam_id']} for student name {student_data['student_name']} with mobile number {student_data['mobile']}.")




############# Below code is to generate  the HTML table in the Student Exam which are not imported from the SMD #########################################################
import frappe

@frappe.whitelist()
def fetch_unimported_logs(imported_batch_id):
    logs = frappe.get_all('Not Imported Logs', filters={'exam_id': imported_batch_id}, fields=['exam_id', 'student_name', 'mobile', 'district', 'state', 'rank', 'total_marks', 'total_right', 'total_wrong', 'total_skip', 'percentage','student_master_data_id','name','status'])
    return logs








################################Delete the specific exam ID in the Student Results doctype #################################

import frappe

@frappe.whitelist()
def delete_student_results(exam_id):
    # Get all Student Results records where exam_id matches the exam_name
    student_results = frappe.get_all('Student Results', filters={'exam_id': exam_id})

    if student_results:
        # Delete each result
        for result in student_results:
            frappe.delete_doc('Student Results', result['name'])
        
        return f"Deleted {len(student_results)} student results for Exam {exam_id}"
    else:
        pass
        # return f"No student results found for Exam {exam_id}"





################### assigning Ranks color to the Student Results ##############################


@frappe.whitelist()
def assign_colors(exam_name):
    try:
        # Fetch the Student Exam document
        exam_doc = frappe.get_doc('Student Exam', exam_name)
        # print("Exam opened for color assigment",exam_name)
        
        # Fetch total number of students
        total_students = float(exam_doc.last_rank)

        # Calculate the actual counts for each color range based on the percentage
        green_end = int(total_students * (exam_doc.green_ends_to / 100))

        yellow_end = int(total_students * (exam_doc.yellow_ends_to / 100))
        
        print(green_end,yellow_end)
        # Fetch the Student Results for the current exam, ordered by rank
        student_results = frappe.get_all('Student Results', filters={'exam_id': exam_name}, fields=['name', 'rank'], order_by='rank asc')
        # print(student_results)
        # Initialize a counter to track the current student's position
        # counter = 1

        # Iterate over the student results and assign colors based on rank
        for student_result in student_results:
            if student_result.rank <= green_end:
                # Assign green color
                frappe.db.set_value('Student Results', student_result.name, 'rank_color', 'G')
            elif student_result.rank <= yellow_end:
                # Assign yellow color
                frappe.db.set_value('Student Results', student_result.name, 'rank_color', 'Y')
            else:
                # Assign red color
                frappe.db.set_value('Student Results', student_result.name, 'rank_color', 'R')
            
            # counter += 1

        # After assigning colors, set the "colors_assigned" field to checked
        exam_doc.colors_assigned = 1  # Set it to checked (True)
        exam_doc.save()
        frappe.db.commit()

        return {'message': 'Colors assigned successfully'}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"Error in Color assignement for Exam: {exam_name}")
        return {"status": False, "msg": f"Error in Color assignement for Exam {exam_name}"}


############################### IT is for bulk assigning the colors #########################

@frappe.whitelist()
def bulk_assign_colors(green_end,yellow_end):

    try:
        student_exams = frappe.get_all('Student Exam', filters={"colors_assigned":0,'status': ("not in",["Pending to Process Data","In Queue","Failed Queue"])})
        # print(student_exams)
        for exam in student_exams:
            try:
                student_exam_result_last_rank = frappe.get_all('Student Results', filters={"exam_id":exam.name},fields=["rank"],order_by="rank desc",limit=1)
                student_exam_doc = frappe.get_doc('Student Exam',exam.name)
                student_exam_doc.green_starts_from = 0
                student_exam_doc.yellow_starts_from = int(green_end)+1
                student_exam_doc.red_starts_from = int(yellow_end)+1
                student_exam_doc.green_ends_to = int(green_end)
                student_exam_doc.yellow_ends_to = int(yellow_end)
                student_exam_doc.red_ends_to = 100

                student_exam_doc.start_rank = 1
                student_exam_doc.last_rank = student_exam_result_last_rank[0].rank
                student_exam_doc.actual_candidates = student_exam_doc.actual_count

                student_exam_doc.save()
                
                response1=assign_colors(student_exam_doc.name)
                # print(response1)
                frappe.log_error(frappe.get_traceback(), f"Color assignement for Exam {exam.name} done Successfully")
            except Exception as e:
                # print(e)
                frappe.log_error(frappe.get_traceback(), f"Error in Color assignement for Exam {exam.name}")

        return {"status": True, "msg": f"Bulk Color assignement for all Exam done Successfully"}
    except Exception as e:

        frappe.log_error(frappe.get_traceback(), "Error in Bulk Color assignement for All Exam")
        return {"status": False, "msg": f"Error in Bulk Color assignement for All Exam"}

































































































####################################Vatsal's Working Modified code for conditional live and enqueing bulk operations end ######


# import frappe
# @frappe.whitelist()
# def student_process_data(name):
#     students_exam_doc = frappe.get_doc('Student Exam',name)
#     # Fetch all records from Students Master Data where imported is not checked
#     students_master_data = frappe.get_all('Students Master Data', filters={'imported': 0,'exam_id':name}, fields=[
#         'name',  # Include 'name' field to identify records
#         'student_name', 'mobile', 'state', 'rank', 'total_marks', 'district',
#         'total_right', 'total_wrong', 'total_skip', 'percentage', 'exam_id'
#     ])
    
#     if not students_master_data:
#         # If no records are found, return a message indicating no data to sync
#         return "no_data"
    
#     total_records = len(students_master_data)
#     completed_records = 0
 
#     # Loop through the fetched data and sync it
#     for student_data in students_master_data:
#         # Debugging: print the student data to check available fields
#         frappe.log_error(f"Student Data: {student_data}", "Sync Data Debug")
 
#         # Check if student already exists in Student doctype by mobile number
#         existing_student = frappe.db.exists('Online Student', {'mobile': student_data['mobile']})
        
#         if not existing_student:
#         # if True:
#             # Create a new student record in the Student doctype
#             new_student = frappe.get_doc({
#                 'doctype': 'Online Student',
#                 'student_name': student_data['student_name'],
#                 'mobile': student_data['mobile'],
#                 'state': student_data['state'],
#                 'district': student_data['district'],
#                 'system_imported': 1,
#                 'exam_id': student_data['exam_id'],
#                 'total_exams':1,
#             })
#             new_student.insert()
#             student_id = new_student.name
#         else:
            # Fetch the existing student's ID
            # student_id = frappe.get_value('Online Student', {'mobile': student_data['mobile']}, 'name')
            # student_doc = frappe.get_doc('Online Student', student_id )
            # old_test_series_results = frappe.get_doc('Student Results',filters={"student_id":student_id})
            # student_doc=len(old_test_series_results)+1
            # student_doc.save()
 
#         # Check if the result already exists to avoid duplication
#         # existing_result = frappe.db.exists('Student Results', {
#         #     'student_id': student_id,
#         #     'exam_id': student_data.get('exam_id'),
#         #     # 'exam_date': student_data.get('date')
#         # })
 
#         # if not existing_result:
#         if True:
#             # Create a new Student Results record
#             new_test_series_result = frappe.get_doc({
#                 'doctype': 'Student Results',
#                 'student_id': student_id,
#                 'student_name': student_data['student_name'],
#                 'student_mobile': student_data['mobile'],
#                 'exam_date': student_data.get('date'),
#                 'exam_code': student_data.get('exam_code'),
#                 'rank': student_data.get('rank'),
#                 'total_marks': student_data.get('total_marks'),
#                 'total_right': student_data.get('total_right'),
#                 'total_wrong': student_data.get('total_wrong'),
#                 'total_skip': student_data.get('total_skip'),
#                 'percentage': student_data.get('percentage'),
#                 'exam_id': student_data.get('exam_id'),
#                 'system_imported': 1
#             })
#             new_test_series_result.insert()
#         completed_records+=1
#         # Mark the student record in Students Master Data as imported
#         frappe.db.set_value('Students Master Data', student_data['name'], 'imported', 1)
#         progress=int((completed_records/total_records)*100)
#         frappe.publish_realtime("sync_progress", {
#                                             "completed_records":completed_records,
#                                             "total_records":total_records,
#                                             "progress":progress,

#                                         })
    
#     students_exam_doc.status = 'Data Synced'
#     students_exam_doc.save()
    
#     frappe.db.commit()
    
#     return "success"










