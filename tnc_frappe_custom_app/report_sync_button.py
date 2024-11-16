import frappe

import frappe

# @frappe.whitelist()
# def sync_data(report_name):
#     # Print report_name for debugging
#     print(f"Report Name: {report_name}")

#     # Fetch the exam_title_name from Student Exam doctype using report_name
#     exam_title_name = frappe.get_value('Student Exam', {'exam_title_name': report_name}, 'name')
    
#     if not exam_title_name:
#         # If no exam_title_name found, return an error message
#         return {"status": "no_exam_title_name"}

#     # Fetch all records from Students Master Data where imported is not checked
#     students_master_data = frappe.get_all('Students Master Data', filters={'imported': 0, 'exam_id': exam_title_name}, fields=[
#         'name',  # Include 'name' field to identify records
#         'student_name', 'mobile', 'state', 'rank', 'total_marks', 'district', 
#         'total_right', 'total_wrong', 'total_skip', 'percentage', 'exam_id'
#     ])
    
#     if not students_master_data:
#         # If no records are found, return a message indicating no data to sync
#         return {"status": "no_data"}

#     # Loop through the fetched data and sync it
#     for student_data in students_master_data:
#         # Debugging: print the student data to check available fields
#         frappe.log_error(f"Student Data: {student_data}", "Sync Data Debug")

#         # Check if student already exists in Student doctype by mobile number
#         existing_student = frappe.db.exists('Online Student', {'mobile': student_data['mobile']})
        
#         if not existing_student:
#             # Create a new student record in the Student doctype
#             new_student = frappe.get_doc({
#                 'doctype': 'Online Student',
#                 'student_name': student_data['student_name'],
#                 'mobile': student_data['mobile'],
#                 'state': student_data['state'],
#                 'district': student_data['district'],
#                 'system_imported': 1,
#                 'exam_id': student_data['exam_id'],
#             })
#             new_student.insert()
#             student_id = new_student.name
#         else:
#             # Fetch the existing student's ID
#             student_id = frappe.get_value('Online Student', {'mobile': student_data['mobile']}, 'name')

#         # Check if the result already exists to avoid duplication
#         existing_result = frappe.db.exists('Student Results', {
#             'student_id': student_id,
#             'exam_code': student_data.get('exam_code'),
#             'exam_date': student_data.get('date')
#         })

#         if not existing_result:
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
#                 'batch_id': student_data.get('exam_id'),
#                 'system_imported': 1
#             })
#             new_test_series_result.insert()

#         # Mark the student record in Students Master Data as imported
#         frappe.db.set_value('Students Master Data', student_data['name'], 'imported', 1)
    
#     frappe.db.commit()
    
#     return {"status": "success"}


import frappe

@frappe.whitelist()
def sync_data(report_name):
    # Print report_name for debugging
    print(f"Report Name: {report_name}")

    # Fetch the exam_title_name from Student Exam doctype using report_name
    exam_title_name = frappe.get_value('Student Exam', {'exam_title_name': report_name}, 'name')
    
    if not exam_title_name:
        # If no exam_title_name found, return an error message
        return {"status": "no_exam_title_name"}

    # Fetch all records from Students Master Data where imported is not checked
    students_master_data = frappe.get_all('Students Master Data', filters={'imported': 0, 'exam_id': exam_title_name}, fields=[
        'name',  # Include 'name' field to identify records
        'student_name', 'mobile', 'state', 'rank', 'total_marks', 'district', 
        'total_right', 'total_wrong', 'total_skip', 'percentage', 'exam_id'
    ])
    
    if not students_master_data:
        # If no records are found, return a message indicating no data to sync
        return {"status": "no_data"}

    # Loop through the fetched data and sync it
    for student_data in students_master_data:
        # Debugging: print the student data to check available fields
        frappe.log_error(f"Student Data: {student_data}", "Sync Data Debug")

        # Check if student already exists in Student doctype by mobile number
        existing_student = frappe.db.exists('Online Student', {'mobile': student_data['mobile']})
        
        if not existing_student:
            # Create a new student record in the Student doctype
            new_student = frappe.get_doc({
                'doctype': 'Online Student',
                'student_name': student_data['student_name'],
                'mobile': student_data['mobile'],
                'state': student_data['state'],
                'district': student_data['district'],
                'system_imported': 1,
                'exam_id': student_data['exam_id'],
            })
            new_student.insert()
            student_id = new_student.name
        else:
            # Fetch the existing student's ID
            student_id = frappe.get_value('Online Student', {'mobile': student_data['mobile']}, 'name')

        # Check if the result already exists to avoid duplication
        existing_result = frappe.db.exists('Student Results', {
            'student_id': student_id,
            'exam_code': student_data.get('exam_code'),
            'exam_date': student_data.get('date')
        })

        if not existing_result:
            # Create a new Student Results record
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
                'exam_id': student_data.get('exam_id'),
                'system_imported': 1
            })
            new_test_series_result.insert()

        # Mark the student record in Students Master Data as imported
        frappe.db.set_value('Students Master Data', student_data['name'], 'imported', 1)
    
    # Update status in Student Exam to "Data Synced"
    update_status(exam_title_name)

    frappe.db.commit()
    
    return {"status": "success"}

def update_status(exam_title_name):
    # Update the status to "Data Synced"
    # Here, exam_title_name is the ID for the Student Exam
    if exam_title_name:
        frappe.db.set_value('Student Exam', exam_title_name, 'status', 'Data Synced')
    else:
        # Log an error if the exam_title_name is not found
        frappe.log_error(f"Could not find exam_title_name for report_name: {exam_title_name}", "Sync Data Debug")






# import frappe

# @frappe.whitelist()
# def check_data_availability(exam_title_name):
#     # Step 1: Find the corresponding 'name' in Student Exam doctype using 'exam_title_name'
#     student_exam = frappe.get_value('Student Exam', {'exam_title_name': exam_title_name}, 'name')
    
#     if not student_exam:
#         return {"status": "no_exam_title_name"}  # Return if no corresponding exam exists

#     # Step 2: Fetch records from Student Master Data where imported is not checked
#     students_master_data = frappe.get_all(
#         'Students Master Data',
#         filters={'imported': 0, 'exam_id': student_exam},
#         fields=['name']
#     )

#     # Return status based on whether data is available
#     if students_master_data:
#         return {"status": "data_available"}
#     else:
#         return {"status": "no_data"}


