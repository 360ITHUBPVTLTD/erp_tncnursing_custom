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


############################## Below CODE IS WORKING FINE ###########################


# import frappe

# @frappe.whitelist()
# def sync_data(name):
#     # Fetch all records from Students Master Data where imported is not checked
#     print(name)
#     students_master_data = frappe.get_all('Students Master Data', filters={'imported': 0,'imported_batch_id':name}, fields=[
#         'name',  # Include 'name' field to identify records
#         'student_name', 'mobile', 'state', 'rank', 'total_marks', 'district', 
#         'total_right', 'total_wrong', 'total_skip', 'percentage', 'imported_batch_id'
#     ])
    
#     for student_data in students_master_data:
#         # Debugging: print the student data to check available fields
#         frappe.log_error(f"Student Data: {student_data}", "Sync Data Debug")

#         # Check if student already exists in Student doctype by mobile number
#         existing_student = frappe.db.exists('Student', {'mobile': student_data['mobile']})
        
#         if not existing_student:
#             # Create a new student record in the Student doctype
#             new_student = frappe.get_doc({
#                 'doctype': 'Student',
#                 'student_name': student_data['student_name'],
#                 'mobile': student_data['mobile'],
#                 'state': student_data['state'],
#                 'district': student_data['district'],
#                 'system_imported': 1,
#                 'student_batch_id': student_data['imported_batch_id'],
#             })
#             new_student.insert()
#             student_id = new_student.name
#         else:
#             # Fetch the existing student's ID
#             student_id = frappe.get_value('Student', {'mobile': student_data['mobile']}, 'name')

#         # Assuming no exam_name reference is needed, so this part is removed

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
#                 'batch_id': student_data.get('imported_batch_id'),
#                 'system_imported': 1
#             })
#             new_test_series_result.insert()

#         # Mark the student record in Students Master Data as imported
#         frappe.db.set_value('Students Master Data', student_data['name'], 'imported', 1)
    
#     frappe.db.commit()
    
#     return "success"


#################### working code #################################





import frappe

@frappe.whitelist()
def sync_data(name):
    students_exam_doc = frappe.get_doc('Student Exam',name)
    # Fetch all records from Students Master Data where imported is not checked
    students_master_data = frappe.get_all('Students Master Data', filters={'imported': 0,'imported_batch_id':name}, fields=[
        'name',  # Include 'name' field to identify records
        'student_name', 'mobile', 'state', 'rank', 'total_marks', 'district', 
        'total_right', 'total_wrong', 'total_skip', 'percentage', 'imported_batch_id'
    ])
    
    if not students_master_data:
        # If no records are found, return a message indicating no data to sync
        return "no_data"

    # Loop through the fetched data and sync it
    for student_data in students_master_data:
        # Debugging: print the student data to check available fields
        frappe.log_error(f"Student Data: {student_data}", "Sync Data Debug")

        # Check if student already exists in Student doctype by mobile number
        existing_student = frappe.db.exists('Student', {'mobile': student_data['mobile']})
        
        if not existing_student:
        # if True:
            # Create a new student record in the Student doctype
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
            # Fetch the existing student's ID
            student_id = frappe.get_value('Student', {'mobile': student_data['mobile']}, 'name')

        # Check if the result already exists to avoid duplication
        # existing_result = frappe.db.exists('Student Results', {
        #     'student_id': student_id,
        #     'batch_id': student_data.get('imported_batch_id'),
        #     # 'exam_date': student_data.get('date')
        # })

        # if not existing_result:
        if True:
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
                'batch_id': student_data.get('imported_batch_id'),
                'system_imported': 1
            })
            new_test_series_result.insert()

        # Mark the student record in Students Master Data as imported
        frappe.db.set_value('Students Master Data', student_data['name'], 'imported', 1)
    
    students_exam_doc.status = 'Data Synced'
    students_exam_doc.save()
    
    frappe.db.commit()
    
    return "success"























































# import frappe

# @frappe.whitelist()
# def sync_data(name):
#     students_master_data = frappe.get_all('Students Master Data', filters={'imported': 0, 'imported_batch_id': name}, fields=[
#         'name', 'student_name', 'mobile', 'state', 'rank', 'total_marks', 'district',
#         'total_right', 'total_wrong', 'total_skip', 'percentage', 'imported_batch_id'
#     ])

#     if not students_master_data:
#         return "no_data"

#     total_records = len(students_master_data)
#     success_count = 0

#     for index, student_data in enumerate(students_master_data):
#         try:
#             existing_student = frappe.db.exists('Student', {'mobile': student_data['mobile']})
#             if not existing_student:
#                 new_student = frappe.get_doc({
#                     'doctype': 'Student',
#                     'student_name': student_data['student_name'],
#                     'mobile': student_data['mobile'],
#                     'state': student_data['state'],
#                     'district': student_data['district'],
#                     'system_imported': 1,
#                     'student_batch_id': student_data['imported_batch_id'],
#                 })
#                 new_student.insert()
#                 student_id = new_student.name
#             else:
#                 student_id = frappe.get_value('Student', {'mobile': student_data['mobile']}, 'name')

#             existing_result = frappe.db.exists('Student Results', {
#                 'student_id': student_id,
#                 'exam_title_name': student_data.get('imported_batch_id'),

                # 'exam_code': student_data.get('exam_code'),
                # 'exam_date': student_data.get('date')
#             })

#             if not existing_result:
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

#             frappe.db.set_value('Students Master Data', student_data['name'], 'imported', 1)
#             success_count += 1

#             # Publish progress
#             frappe.publish_realtime("progress", {
#                 "total": total_records,
#                 "created": success_count
#             }, user=frappe.session.user)

#         except Exception as e:
#             frappe.log_error(f"Error syncing data: {e}")

#     frappe.db.commit()
#     return "success"


