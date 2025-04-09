# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StudentsMasterData(Document):
    pass

# class StudentsMasterData(Document):
#     def after_insert(self):
#         # Get the exam_id from the current Student Master document
#         imported_batch_id = self.exam_id

#         if imported_batch_id:
#             # Count the number of students in Student Master with the same imported_batch_id
#             count = frappe.db.count('Students Master Data', {'exam_id': imported_batch_id})

#             try:
#                 # Fetch the corresponding Student Exam document using exam_id (matching the name)
#                 student_exam_doc = frappe.get_doc('Student Exam', imported_batch_id)
                
#                 # Update the actual_count field in Student Exam with the count of matching students
#                 student_exam_doc.actual_count = count
#                 student_exam_doc.save()

#             except frappe.DoesNotExistError:
#                 # If no Student Exam is found with the matching exam_id
#                 frappe.throw(f"No Student Exam found with name {imported_batch_id}")
#         else:
#             frappe.throw("exam_id is missing in the Student Master record")



# class StudentsMasterData(Document):
    # def after_insert(self):
    #     # Get the imported_batch_id from the current Student Master document
    #     imported_batch_id = self.exam_id

    #     if imported_batch_id:
    #         # Count the number of students in Student Master with the same imported_batch_id
    #         count = frappe.db.count('Students Master Data', {'exam_id': imported_batch_id})

    #         try:
    #             # Fetch the corresponding Student Exam document using imported_batch_id (matching the name)
    #             student_exam_doc = frappe.get_doc('Student Exam', imported_batch_id)
                
    #             # Update the actual_count field in Student Exam with the count of matching students
    #             student_exam_doc.actual_candidates = count
    #             student_exam_doc.start_rank = 1
    #             # Fetch the highest rank (DESC order) for the given imported_batch_id
    #             highest_rank = frappe.db.get_value(
    #                 'Students Master Data',
    #                 {'exam_id': imported_batch_id},
    #                 'rank',
    #                 order_by='rank desc'
    #             )

    #             if highest_rank:
    #                 # Store the highest rank in the last_rank field of Student Exam
    #                 student_exam_doc.last_rank = highest_rank
    #             else:
    #                 frappe.throw(f"No rank found for exam_id {imported_batch_id}")

    #             # Save the updated Student Exam document
    #             student_exam_doc.save()

    #         except frappe.DoesNotExistError:
    #             # If no Student Exam is found with the matching imported_batch_id
    #             frappe.throw(f"No Student Exam found with name {imported_batch_id}")
    #     else:
    #         frappe.throw("exam_id is missing in the Student Master record")




# ################ Below code is to fetch the unchecked(unimported Records and store it into the DOctype #################)
import frappe

@frappe.whitelist()
def sync_uninported_data():
    # Fetch all records from 'Student Masters Data' where 'imported' is unchecked
    student_records = frappe.get_all('Students Master Data', 
                                     filters={'imported': 0}, 
                                     fields=['exam_id', 'student_name', 'mobile', 'district', 'state', 
                                             'rank', 'total_marks', 'total_right', 'total_wrong', 'total_skip', 'percentage'])
    
    if not student_records:
        return {'status': 'no_records', 'message': 'No records to sync'}
    
    # Insert the records into 'Not Imported Logs' doctype
    for record in student_records:
        new_log = frappe.get_doc({
            'doctype': 'Not Imported Logs',
            'exam_id': record['exam_id'],
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


@frappe.whitelist()
def remove_duplicate_student_results(exam_id=None):
    """
    Optimized removal of duplicate records in the Student Results doctype for a given exam_id.
    Duplicates are defined by the combination of student_mobile and exam_id.
    Uses GROUP_CONCAT to fetch record IDs in order, deletes all but the oldest record,
    and finally updates the Student Exam's processed_candidates field.
    
    :param exam_id: The exam ID to filter records on. (Required)
    """
    if not exam_id:
        return "Error: exam_id parameter is required."
    
    # Aggregate duplicate records by student_mobile for the specified exam_id.
    duplicate_groups = frappe.db.sql("""
        SELECT student_mobile, exam_id,
               GROUP_CONCAT(name ORDER BY creation ASC) AS names,
               COUNT(*) AS cnt
        FROM `tabStudent Results`
        WHERE exam_id = %s
        GROUP BY student_mobile, exam_id
        HAVING cnt > 1
    """, exam_id, as_dict=1)
    
    if not duplicate_groups:
        # Even if no duplicates exist, update the processed count.
        processed_count = frappe.db.count("Student Results", {"exam_id": exam_id})
        try:
            exam_doc = frappe.get_doc("Student Exam", exam_id)
            exam_doc.processed_candidates = processed_count
            exam_doc.save()
            frappe.db.commit()
        except Exception as e:
            print(f"Error updating Student Exam record: {e}")
        return f"No duplicate records found for exam_id: {exam_id}"
    
    # Process each duplicate group: keep the oldest, delete the rest.
    for group in duplicate_groups:
        record_ids = group.names.split(',')
        # Retain the oldest; mark the rest for deletion.
        duplicates_to_delete = record_ids[1:]
        
        for rec_id in duplicates_to_delete:
            try:
                frappe.delete_doc("Student Results", rec_id)
            except Exception as e:
                print(f"Error deleting record {rec_id}: {e}")
        # Commit the deletions for this group.
        frappe.db.commit()
        print(f"Deleted duplicates for mobile: {group.student_mobile} and exam: {group.exam_id}. Kept record: {record_ids[0]}")
    
    # After processing, count the remaining records and update the Student Exam.
    processed_count = frappe.db.count("Student Results", {"exam_id": exam_id})
    try:
        exam_doc = frappe.get_doc("Student Exam", exam_id)
        exam_doc.processed_candidates = processed_count
        exam_doc.save()
        frappe.db.commit()
        print(f"Updated Student Exam {exam_id} processed_candidates to {processed_count}")
    except Exception as e:
        print(f"Error updating Student Exam record: {e}")
    
    return f"Duplicate removal for Student Results with exam_id '{exam_id}' completed."



@frappe.whitelist()
def remove_duplicate_students_master_data(exam_id=None):
    """
    Optimized removal of duplicate records in the Students Master Data doctype for a given exam_id.
    Duplicates are defined by the combination of mobile and exam_id.
    Uses GROUP_CONCAT to aggregate record IDs (ordered by creation), deletes all but the oldest,
    and updates the Student Exam's actual_candidates field.
    
    :param exam_id: The exam ID to filter records on. (Required)
    """

    if not exam_id:
        return "Error: exam_id parameter is required."
    
    # Aggregate duplicate records by mobile for the specified exam_id.
    duplicate_groups = frappe.db.sql("""
        SELECT mobile, exam_id,
               GROUP_CONCAT(name ORDER BY creation ASC) AS names,
               COUNT(*) AS cnt
        FROM `tabStudents Master Data`
        WHERE exam_id = %s
        GROUP BY mobile, exam_id
        HAVING cnt > 1
    """, exam_id, as_dict=1)
    
    if not duplicate_groups:
        # Even if no duplicates exist, update the actual count.
        actual_count = frappe.db.count("Students Master Data", {"exam_id": exam_id})
        try:
            exam_doc = frappe.get_doc("Student Exam", exam_id)
            exam_doc.actual_candidates = actual_count
            exam_doc.save()
            frappe.db.commit()
        except Exception as e:
            print(f"Error updating Student Exam record: {e}")
        return f"No duplicate records found for exam_id: {exam_id}"
    
    for group in duplicate_groups:
        record_ids = group.names.split(',')
        # Keep the first (oldest) and mark the rest for deletion.
        duplicates_to_delete = record_ids[1:]
        
        for rec_id in duplicates_to_delete:
            try:
                frappe.delete_doc("Students Master Data", rec_id)
            except Exception as e:
                print(f"Error deleting record {rec_id}: {e}")
        # Commit deletions for this group.
        frappe.db.commit()
        print(f"Deleted duplicates for mobile: {group.mobile} and exam: {group.exam_id}. Kept record: {record_ids[0]}")
    
    # After processing, count the remaining records and update the Student Exam.
    actual_count = frappe.db.count("Students Master Data", {"exam_id": exam_id})
    try:
        exam_doc = frappe.get_doc("Student Exam", exam_id)
        exam_doc.actual_candidates = actual_count
        exam_doc.save()
        frappe.db.commit()
        print(f"Updated Student Exam {exam_id} actual_candidates to {actual_count}")
    except Exception as e:
        print(f"Error updating Student Exam record: {e}")
    
    return f"Duplicate removal for Students Master Data with exam_id '{exam_id}' completed."




