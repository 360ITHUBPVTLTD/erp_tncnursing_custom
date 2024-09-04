# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

import frappe,time
from frappe.model.document import Document


class StudentExam(Document):
	pass


@frappe.whitelist()
def sync_data(name):
    students_master_data = frappe.get_all('Students Master Data', filters={'imported': 0, 'imported_batch_id': name}, fields=[
        'name', 'student_name', 'mobile', 'state', 'rank', 'total_marks', 'district',
        'total_right', 'total_wrong', 'total_skip', 'percentage', 'imported_batch_id'
    ])

    if not students_master_data:
        return "no_data"

    total_records = len(students_master_data)
    completed_records = 0

    for i, student_data in enumerate(students_master_data):
        try:
            # Processing each student record
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

            existing_result = frappe.db.exists('Student Results', {
                'student_id': student_id,
                'exam_code': student_data.get('exam_code'),
                'exam_date': student_data.get('date')
            })

            if not existing_result:
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

            # Mark student data as imported
            frappe.db.set_value('Students Master Data', student_data['name'], 'imported', 1)

        except Exception as e:
            frappe.log_error(f"Error syncing data: {e}")
        
        completed_records += 1
        
        # Simulate delay
        # time.sleep(2)
        
        # Publish progress to clients
        progress_data = {
            'total': total_records,
            'completed': completed_records
        }
        frappe.publish_progress('sync_progress', progress_data)

        # Log progress to check if it's working
    frappe.log_error(f"Progress Update: {completed_records}/{total_records} | Data: {progress_data}")
    
    frappe.db.commit()
    return "success"













# @frappe.whitelist()
# def vatsal_sync(student_exam_id):
    
#     student_exam_doc = frappe.get_doc("Student Exam",student_exam_id)
#     all_imported_data = frappe.get_all("Students Master Data",
#                                      filters={
#                                          'imported_batch_id': student_exam_id,
#                                         #  'imported': 0,
#                                      },
#                                      fields=[
#                                                 'name', 'student_name', 'mobile', 'state', 'rank', 'total_marks', 'district',
#                                                 'total_right', 'total_wrong', 'total_skip', 'percentage', 'imported_batch_id'
#                                             ]
#                                     )

    
#     if all_imported_data:
#         total_imported_data=len(all_imported_data)
#         in_progress_imported_data=0
#         for imported_data in all_imported_data:
#             try:

#                 existing_student = frappe.db.exists('Student', {'mobile': imported_data['mobile']})
#                 if not existing_student:
#                     new_student = frappe.get_doc({
#                         'doctype': 'Student',
#                         'student_name': imported_data['student_name'],
#                         'mobile': imported_data['mobile'],
#                         'state': imported_data['state'],
#                         'district': imported_data['district'],
#                         'system_imported': 1,
#                         'student_batch_id': imported_data['imported_batch_id'],
#                     })
#                     new_student.insert()
#                     new_student.reload()
                
#                 new_student_result = frappe.get_doc({
#                     'doctype': 'Student Results',
#                     'student_id': new_student.name,
#                     'student_name': imported_data['student_name'],
#                     'student_mobile': imported_data['mobile'],
#                     # 'exam_date': student_exam_doc.,
#                     # 'exam_code': student_exam_doc.,
#                     # 'rank': imported_data['rank'],
#                     'total_marks': imported_data['total_marks'],
#                     'total_right': imported_data['total_right'],
#                     'total_wrong': imported_data['total_wrong'],
#                     'total_skip': imported_data['total_skip'],
#                     'percentage': imported_data['percentage'],
#                     'batch_id': imported_data['imported_batch_id'],
#                     # 'system_imported': 1
#                 })
#                 new_student_result.insert()
                    
                    
#             except Exception as er:
#                 frappe.log_error(f"An error occurred in bulk processing of Student Import Data: {er}")
#             in_progress_imported_data+=1
#             # frappe.publish_realtime("progress", {
#             #                                 "total": total_imported_data,
#             #                                 "created": in_progress_imported_data,
#             #                             }, user=frappe.session.user)
#             progress = int(in_progress_imported_data / total_imported_data * 100)
        
#             # Update the progress bar on the client-side
#             frappe.publish_realtime('bulk_creation_progress', progress, user=frappe.session.user)
    

# @frappe.whitelist()
# def test_progress():
#     for i in range(1, 101):
#         frappe.publish_realtime('test_progress', {'progress': i})
#         time.sleep(0.1)  # Simulate a task
