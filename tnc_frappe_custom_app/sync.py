# import frappe

# @frappe.whitelist()
# def sync_data():
#     # Fetch all records from Students Master Data where imported is not checked
#     students_master_data = frappe.get_all('Students Master Data', filters={'imported': 0}, fields=[
#         'student_name', 'mobile', 'district', 'state', 
#         'exam_type', 'date', 'exam_code', 'exam_name', 
#         'rank', 'total_marks', 'total_right', 
#         'total_wrong', 'total_skip', 'percentage'
#     ])
    
#     for student_data in students_master_data:
#         # Check if student already exists in Student doctype by mobile number
#         existing_student = frappe.db.exists('Student', {'mobile': student_data['mobile']})
        
#         if not existing_student:
#             # Create a new student record in the Student doctype
#             new_student = frappe.get_doc({
#                 'doctype': 'Student',
#                 'student_name': student_data['student_name'],
#                 'mobile': student_data['mobile'],
#                 'district': student_data['district'],
#                 'state': student_data['state']
#             })
#             new_student.insert()
#             frappe.db.commit()  # Save the new student
#             student_id = new_student.name
#         else:
#             # Fetch the existing student's ID
#             student_id = frappe.get_value('Student', {'mobile': student_data['mobile']}, 'name')

#         # Create a new Student Results record
#         new_test_series_result = frappe.get_doc({
#             'doctype': 'Student Results',
#             # 'test_series_type_id': student_data['exam_type'],  # Assuming exam_type corresponds to test_series_type_id
#             'student_id': student_id,
#             'student_name': student_data['student_name'],
#             'student_mobile': student_data['mobile'],
#             'exam_name': student_data['exam_name'],
#             'exam_date': student_data['date'],
#             'exam_code': student_data['exam_code'],
#             'rank': student_data['rank'],
#             'total_marks': student_data['total_marks'],
#             'total_right': student_data['total_right'],
#             'total_wrong': student_data['total_wrong'],
#             'total_skip': student_data['total_skip'],
#             'percentage': student_data['percentage']
#         })
#         new_test_series_result.insert()
    
#     # Mark all processed records as imported
#     frappe.db.sql("""
#         UPDATE `tabStudents Master Data`
#         SET imported = 1
#         WHERE name IN (%s)
#     """ % ','.join(["'%s'" % d.name for d in students_master_data]))
    
#     frappe.db.commit()
    
#     return "success"


############################## ABOVE CODE IS WORKING FINE ###########################

import frappe

@frappe.whitelist()
def sync_data():
    # Fetch all records from Students Master Data where imported is not checked
    students_master_data = frappe.get_all('Students Master Data', filters={'imported': 0}, fields=[
        'name',  # Include 'name' field to identify records
        'student_name', 'mobile', 'district', 'state', 
        'exam_type', 'date', 'exam_code', 'exam_name', 
        'rank', 'total_marks', 'total_right', 
        'total_wrong', 'total_skip', 'percentage','exam_title_name'
    ])
    
    for student_data in students_master_data:
        # Check if student already exists in Student doctype by mobile number
        existing_student = frappe.db.exists('Student', {'mobile': student_data['mobile']})
        
        if not existing_student:
            # Create a new student record in the Student doctype
            new_student = frappe.get_doc({
                'doctype': 'Student',
                'student_name': student_data['student_name'],
                'mobile': student_data['mobile'],
                'district': student_data['district'],
                'state': student_data['state'],
                'system_imported': 1
            })
            new_student.insert()
            student_id = new_student.name
        else:
            # Fetch the existing student's ID
            student_id = frappe.get_value('Student', {'mobile': student_data['mobile']}, 'name')

        # Fetch the correct exam_name reference from the 'Test Series Type' doctype
        exam_type_name = frappe.db.get_value('Test Series Type', {'name1': student_data['exam_name']}, 'name')

        if not exam_type_name:
            frappe.throw(f"Could not find Exam Name: {student_data['exam_name']} in Test Series Type")

        # Create a new Student Results record
        new_test_series_result = frappe.get_doc({
            'doctype': 'Student Results',
            'student_id': student_id,
            'student_name': student_data['student_name'],
            'student_mobile': student_data['mobile'],
            'exam_name': exam_type_name,  # Use the correct linked name
            'exam_date': student_data['date'],
            'exam_code': student_data['exam_code'],
            'rank': student_data['rank'],
            'total_marks': student_data['total_marks'],
            'total_right': student_data['total_right'],
            'total_wrong': student_data['total_wrong'],
            'total_skip': student_data['total_skip'],
            'percentage': student_data['percentage'],
            'exam_title_name': student_data['exam_title_name'],  # Include the exam title name for better understanding in reports and dashboards  # Add new field 'exam_title_name' in Students Master Data and Student Results doctype to store this information for better understanding in reports and dashboards
            'system_imported': 1
        })
        new_test_series_result.insert()

        # Mark the student record in Students Master Data as imported
        frappe.db.set_value('Students Master Data', student_data['name'], 'imported', 1)
    
    frappe.db.commit()
    
    return "success"

#################### Below code is for Deleting the data in the doctype after successfully imported #####################

import frappe

@frappe.whitelist()
def delete_data():
    try:
        # Delete all records in the "Students Master Data" doctype
        frappe.db.delete('Students Master Data')
        frappe.db.commit()
        return "success"
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Delete Students Master Data Error')
        return "error"

###################################### Below code is check the data present in the doctype or not to show the Intial value of button #####################
@frappe.whitelist()
def check_all_imported():
    total_count = frappe.db.count('Students Master Data')
    if total_count == 0:
        return "no_data"
    
    not_imported_count = frappe.db.count('Students Master Data', filters={'imported': 0})
    
    if not_imported_count == 0:
        return "all_imported"
    else:
        return "not_imported"
