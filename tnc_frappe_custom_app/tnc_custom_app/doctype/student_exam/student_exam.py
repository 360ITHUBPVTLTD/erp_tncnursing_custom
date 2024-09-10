# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

import frappe,time
from frappe.model.document import Document


class StudentExam(Document):
    pass


####################################Vatsal's Working Modified code for conditional live and enqueing bulk operations start ######
 
 
####################################Vatsal's Working Modified code for enqueing bulk operations start #########################
 
def student_and_result_validation_and_creation(student_data):
    try:
        existing_student = frappe.db.exists('Student', {'mobile': student_data['mobile']})
        if not existing_student:
            new_student = frappe.get_doc({
                'doctype': 'Student',
                'student_name': student_data['student_name'],
                'mobile': student_data['mobile'],
                'state': student_data['state'],
                'district': student_data['district'],
                'system_imported': 1,
                'student_batch_id': student_data['imported_batch_id'],
            })
            new_student.insert()
            student_id = new_student.name
        else:
            student_id = frappe.get_value('Student', {'mobile': student_data['mobile']}, 'name')
 
        new_test_series_result = frappe.get_doc({
            'doctype': 'Student Results',
            'student_id': student_id,
            'student_name': student_data['student_name'],
            'student_mobile': student_data['mobile'],
            'exam_date': student_data.get('date'),
            'exam_code': student_data.get('exam_code'),
            'rank': student_data.get('rank'),
            'total_marks': student_data.get('total_marks'),
            'total_right': student_data.get('total_right'),
            'total_wrong': student_data.get('total_wrong'),
            'total_skip': student_data.get('total_skip'),
            'percentage': student_data.get('percentage'),
            'batch_id': student_data.get('imported_batch_id'),
            'system_imported': 1
        })
        new_test_series_result.insert()
 
        frappe.db.set_value('Students Master Data', student_data['name'], 'imported', 1)
        
        # print(completed_records)
 
    except Exception as e:
        # print(e)
        frappe.log_error(frappe.get_traceback(), f"Error syncing student master data {student_data['name']} in Student Exam {student_data['student_name']}")
 
 
@frappe.whitelist()
def student_process_data(name, limit=1500):
    try:
        total_records = frappe.db.count('Students Master Data', filters={'imported': 0, 'imported_batch_id': name})
        if total_records > limit:
            # Enqueue the background job
            frappe.enqueue('tnc_frappe_custom_app.tnc_custom_app.doctype.student_exam.student_exam.process_students_in_background',
                        queue='long',
                        timeout=6000,
                        name=name,
                        # limit=limit
                        )
            return {"status":True,"enqueued":True,"msg":"Data syncing is Enqueued Successfully!"}
        else:
            response_realtime_data_processing=process_data_realtime(name)
            return response_realtime_data_processing
 
    except Exception as e:
        return {"status": False, "msg": str(e)}
    # process_students_in_background(name, start, limit)
 
 
 
def process_students_in_background(name):
    # print("Function Calleddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
    try:
        students_exam_doc = frappe.get_doc('Student Exam', name)
        students_master_data = frappe.get_all('Students Master Data', filters={
            'imported': 0, 'imported_batch_id': name
        }, fields=['name', 'student_name', 'mobile', 'state', 'rank', 'total_marks', 'district',
                   'total_right', 'total_wrong', 'total_skip', 'percentage', 'imported_batch_id'],
            # start=start,
            # limit=limit,
                     )
        # print(students_master_data)
    
        total_records = frappe.db.count('Students Master Data', filters={'imported': 0, 'imported_batch_id': name})
    
        if not students_master_data:
            return {"status": "no_data"}
    
        completed_records = 0
    
        for student_data in students_master_data:
            student_and_result_validation_and_creation(student_data)
            # try:
            #     existing_student = frappe.db.exists('Student', {'mobile': student_data['mobile']})
            #     if not existing_student:
            #         new_student = frappe.get_doc({
            #             'doctype': 'Student',
            #             'student_name': student_data['student_name'],
            #             'mobile': student_data['mobile'],
            #             'state': student_data['state'],
            #             'district': student_data['district'],
            #             'system_imported': 1,
            #             'student_batch_id': student_data['imported_batch_id'],
            #         })
            #         new_student.insert()
            #         student_id = new_student.name
            #     else:
            #         student_id = frappe.get_value('Student', {'mobile': student_data['mobile']}, 'name')
    
            #     new_test_series_result = frappe.get_doc({
            #         'doctype': 'Student Results',
            #         'student_id': student_id,
            #         'student_name': student_data['student_name'],
            #         'student_mobile': student_data['mobile'],
            #         'exam_date': student_data.get('date'),
            #         'exam_code': student_data.get('exam_code'),
            #         'rank': student_data.get('rank'),
            #         'total_marks': student_data.get('total_marks'),
            #         'total_right': student_data.get('total_right'),
            #         'total_wrong': student_data.get('total_wrong'),
            #         'total_skip': student_data.get('total_skip'),
            #         'percentage': student_data.get('percentage'),
            #         'batch_id': student_data.get('imported_batch_id'),
            #         'system_imported': 1
            #     })
            #     new_test_series_result.insert()
    
            #     frappe.db.set_value('Students Master Data', student_data['name'], 'imported', 1)
                
            #     # print(completed_records)
    
            # except Exception as e:
            #     # print(e)
            #     frappe.log_error(frappe.get_traceback(), f"Error syncing student master data {student_data['name']} in Student Exam {name}")
            #     continue
            completed_records += 1
    
        students_exam_doc.status = 'Data Synced'
        students_exam_doc.save()
    
        frappe.db.commit()
        # print("Data Processing completed Successfullt!!")
    
        return {"status": True, "msg": f"Data Processed Successfully"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in background sync")
        return {"status": False, "msg": f"Error in Background Processing Data: {str(e)}"}
 
####################################Vatsal's Working Modified code for enqueing bulk operations end #########################
 
 
#################################Vatsal's Working Modified code for % based progress publish and exception handling start #######
 
@frappe.whitelist()
def process_data_realtime(name):
    try:
        students_exam_doc = frappe.get_doc('Student Exam', name)
        # Fetch all records from Students Master Data where imported is not checked
        students_master_data = frappe.get_all('Students Master Data', filters={
            'imported': 0, 'imported_batch_id': name
        }, fields=['name', 'student_name', 'mobile', 'state', 'rank', 'total_marks', 'district', 'total_right', 'total_wrong', 'total_skip', 'percentage', 'imported_batch_id'],
        # start=start,
        # limit=limit
        )
    
        total_records = frappe.db.count('Students Master Data', filters={'imported': 0, 'imported_batch_id': name})
    
        if not students_master_data:
            # If no records are found, return a message indicating no data to sync
            return {"status": "no_data", "progress": 100}
    
        completed_records = 0
        publish_iteration = 0
    
        # Loop through the fetched data and sync it
        for student_data in students_master_data:
            student_and_result_validation_and_creation(student_data)
            # try:
            #     # Check if the student already exists in the 'Student' doctype by mobile number
            #     existing_student = frappe.db.exists('Student', {'mobile': student_data['mobile']})
            #     if not existing_student:
            #         # Create a new student record in the 'Student' doctype
            #         new_student = frappe.get_doc({
            #             'doctype': 'Student',
            #             'student_name': student_data['student_name'],
            #             'mobile': student_data['mobile'],
            #             'state': student_data['state'],
            #             'district': student_data['district'],
            #             'system_imported': 1,
            #             'student_batch_id': student_data['imported_batch_id'],
            #         })
            #         new_student.insert()
            #         student_id = new_student.name
            #     else:
            #         # Fetch the existing student's ID
            #         student_id = frappe.get_value('Student', {'mobile': student_data['mobile']}, 'name')
    
            #     # Create a new 'Student Results' record
            #     new_test_series_result = frappe.get_doc({
            #         'doctype': 'Student Results',
            #         'student_id': student_id,
            #         'student_name': student_data['student_name'],
            #         'student_mobile': student_data['mobile'],
            #         'exam_date': student_data.get('date'),
            #         'exam_code': student_data.get('exam_code'),
            #         'rank': student_data.get('rank'),
            #         'total_marks': student_data.get('total_marks'),
            #         'total_right': student_data.get('total_right'),
            #         'total_wrong': student_data.get('total_wrong'),
            #         'total_skip': student_data.get('total_skip'),
            #         'percentage': student_data.get('percentage'),
            #         'batch_id': student_data.get('imported_batch_id'),
            #         'system_imported': 1
            #     })
            #     new_test_series_result.insert()
    
            #     # Mark the student record in 'Students Master Data' as imported
            #     frappe.db.set_value('Students Master Data', student_data['name'], 'imported', 1)
    
            # except Exception as e:
            #     print(e)
            #     # Log the error in Frappe's error log with proper context
            #     frappe.log_error(frappe.get_traceback(), f"Error syncing student {student_data['name']} in Student Exam {name}")
            #     continue  # Continue to the next student even if an error occurs
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
        return {"status": False, "msg": f"Error in Processing Data: {str(e)}"}
 
###########################################Vatsal's Modified code for % based progress publish and exception handling end#######
####################################Vatsal's Working Modified code for conditional live and enqueing bulk operations end ######


# @frappe.whitelist()
# def student_process_data(name, start=0, limit=10000):
#     try:
#         students_exam_doc = frappe.get_doc('Student Exam', name)
        
#         # Fetch records from Students Master Data where imported is not checked
#         students_master_data = frappe.get_all('Students Master Data', filters={
#             'imported': 0, 'imported_batch_id': name
#         }, fields=['name', 'student_name', 'mobile', 'state', 'rank', 'total_marks', 'district', 'total_right', 'total_wrong', 'total_skip', 'percentage', 'imported_batch_id'], start=start, limit=limit)
        
#         total_records = frappe.db.count('Students Master Data', filters={'imported': 0, 'imported_batch_id': name})

#         # If no records are found, return a message indicating no data to sync
#         if not students_master_data:
#             return {"status": "no_data", "progress": 100}
        
#         completed_records = start
#         publish_iteration = 0

#         # Loop through the fetched data and sync it
#         for student_data in students_master_data:
#             try:
#                 # Check if the student already exists in the 'Student' doctype by mobile number
#                 existing_student = frappe.db.exists('Student', {'mobile': student_data['mobile']})
#                 if not existing_student:
#                     # Create a new student record in the 'Student' doctype
#                     new_student = frappe.get_doc({
#                         'doctype': 'Student',
#                         'student_name': student_data['student_name'],
#                         'mobile': student_data['mobile'],
#                         'state': student_data['state'],
#                         'district': student_data['district'],
#                         'system_imported': 1,
#                         'student_batch_id': student_data['imported_batch_id'],
#                     })
#                     new_student.insert()
#                     student_id = new_student.name
#                 else:
#                     # Fetch the existing student's ID
#                     student_id = frappe.get_value('Student', {'mobile': student_data['mobile']}, 'name')

#                 # Create a new 'Student Results' record
#                 new_test_series_result = frappe.get_doc({
#                     'doctype': 'Student Results',
#                     'student_id': student_id,
#                     'student_name': student_data['student_name'],
#                     'student_mobile': student_data['mobile'],
#                     'exam_date': student_data.get('date'),
#                     'exam_code': student_data.get('exam_code'),
#                     'rank': student_data.get('rank'),
#                     'total_marks': student_data.get('total_marks'),
#                     'total_right': student_data.get('total_right'),
#                     'total_wrong': student_data.get('total_wrong'),
#                     'total_skip': student_data.get('total_skip'),
#                     'percentage': student_data.get('percentage'),
#                     'batch_id': student_data.get('imported_batch_id'),
#                     'system_imported': 1
#                 })
#                 new_test_series_result.insert()

#                 # Mark the student record in 'Students Master Data' as imported
#                 frappe.db.set_value('Students Master Data', student_data['name'], 'imported', 1)

#                 completed_records += 1
#                 progress = int((completed_records / total_records) * 100)

#                 if progress > publish_iteration:
#                     frappe.publish_realtime("sync_progress", {
#                         "completed_records": completed_records,
#                         "total_records": total_records,
#                         "progress": progress,
#                     })
#                     publish_iteration += 1

#             except Exception as e:
#                 # Log the error but allow the process to continue for other records
#                 frappe.log_error(frappe.get_traceback(), f"Error syncing student {student_data['name']} in Student Exam {name}")
#                 continue

#         # Update the status of the 'Student Exam' document after syncing is complete
#         students_exam_doc.status = 'Data Synced'
#         students_exam_doc.save()

#         return {"status": "success", "progress": 100}

#     except Exception as e:
#         # Log the error if the entire function fails
#         frappe.log_error(frappe.get_traceback(), f"Error processing student data for exam {name}")
#         return {"status": "error", "message": str(e), "progress": 0}
