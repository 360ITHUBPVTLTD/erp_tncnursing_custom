# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StudentsMasterData(Document):
    pass

# class StudentsMasterData(Document):
#     def after_insert(self):
#         # Get the imported_batch_id from the current Student Master document
#         imported_batch_id = self.imported_batch_id

#         if imported_batch_id:
#             # Count the number of students in Student Master with the same imported_batch_id
#             count = frappe.db.count('Students Master Data', {'imported_batch_id': imported_batch_id})

#             try:
#                 # Fetch the corresponding Student Exam document using imported_batch_id (matching the name)
#                 student_exam_doc = frappe.get_doc('Student Exam', imported_batch_id)
                
#                 # Update the actual_count field in Student Exam with the count of matching students
#                 student_exam_doc.actual_count = count
#                 student_exam_doc.save()

#             except frappe.DoesNotExistError:
#                 # If no Student Exam is found with the matching imported_batch_id
#                 frappe.throw(f"No Student Exam found with name {imported_batch_id}")
#         else:
#             frappe.throw("imported_batch_id is missing in the Student Master record")



class StudentsMasterData(Document):
    def after_insert(self):
        # Get the imported_batch_id from the current Student Master document
        imported_batch_id = self.imported_batch_id

        if imported_batch_id:
            # Count the number of students in Student Master with the same imported_batch_id
            count = frappe.db.count('Students Master Data', {'imported_batch_id': imported_batch_id})

            try:
                # Fetch the corresponding Student Exam document using imported_batch_id (matching the name)
                student_exam_doc = frappe.get_doc('Student Exam', imported_batch_id)
                
                # Update the actual_count field in Student Exam with the count of matching students
                student_exam_doc.actual_candidates = count
                student_exam_doc.start_rank = 1
                # Fetch the highest rank (DESC order) for the given imported_batch_id
                highest_rank = frappe.db.get_value(
                    'Students Master Data',
                    {'imported_batch_id': imported_batch_id},
                    'rank',
                    order_by='rank desc'
                )

                if highest_rank:
                    # Store the highest rank in the last_rank field of Student Exam
                    student_exam_doc.last_rank = highest_rank
                else:
                    frappe.throw(f"No rank found for imported_batch_id {imported_batch_id}")

                # Save the updated Student Exam document
                student_exam_doc.save()

            except frappe.DoesNotExistError:
                # If no Student Exam is found with the matching imported_batch_id
                frappe.throw(f"No Student Exam found with name {imported_batch_id}")
        else:
            frappe.throw("imported_batch_id is missing in the Student Master record")




# ################ Below code is to fetch the unchecked(unimported Records and store it into the DOctype #################)
import frappe

@frappe.whitelist()
def sync_uninported_data():
    # Fetch all records from 'Student Masters Data' where 'imported' is unchecked
    student_records = frappe.get_all('Students Master Data', 
                                     filters={'imported': 0}, 
                                     fields=['imported_batch_id', 'student_name', 'mobile', 'district', 'state', 
                                             'rank', 'total_marks', 'total_right', 'total_wrong', 'total_skip', 'percentage'])
    
    if not student_records:
        return {'status': 'no_records', 'message': 'No records to sync'}
    
    # Insert the records into 'Not Imported Logs' doctype
    for record in student_records:
        new_log = frappe.get_doc({
            'doctype': 'Not Imported Logs',
            'imported_batch_id': record['imported_batch_id'],
            'student_name': record['student_name'],
            'mobile': record['mobile'],
            'district': record['district'],
            'state': record['state'],
            'rank': record['rank'],
            'total_marks': record['total_marks'],
            'total_right': record['total_right'],
            'total_wrong': record['total_wrong'],
            'total_skip': record['total_skip'],
            'percentage': record['percentage'],
        })
        new_log.insert(ignore_permissions=True)
    
    # Update the 'imported' field to checked (1) for the records that have been synced
    # frappe.db.set_value('Students Master Data', 
    #                     [record['name'] for record in student_records], 
    #                     'imported', 1)

    return {'status': 'success', 'message': 'Data synced successfully!'}
