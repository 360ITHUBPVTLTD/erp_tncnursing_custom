# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

import frappe,time
from frappe.model.document import Document


class StudentExam(Document):
	pass



import frappe
@frappe.whitelist()
def student_process_data(name):
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
    
    total_records = len(students_master_data)
    completed_records = 0
 
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
        completed_records+=1
        # Mark the student record in Students Master Data as imported
        frappe.db.set_value('Students Master Data', student_data['name'], 'imported', 1)
        progress=int((completed_records/total_records)*100)
        frappe.publish_realtime("sync_progress", {
                                            "completed_records":completed_records,
                                            "total_records":total_records,
                                            "progress":progress,

                                        })
    
    students_exam_doc.status = 'Data Synced'
    students_exam_doc.save()
    
    frappe.db.commit()
    
    return "success"










