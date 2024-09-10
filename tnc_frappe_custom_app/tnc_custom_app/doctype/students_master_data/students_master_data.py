# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StudentsMasterData(Document):
    pass

class StudentsMasterData(Document):
    def on_update(self):
        # Get the imported_batch_id from the current Student Master document
        imported_batch_id = self.imported_batch_id

        if imported_batch_id:
            # Count the number of students in Student Master with the same imported_batch_id
            count = frappe.db.count('Students Master Data', {'imported_batch_id': imported_batch_id})

            try:
                # Fetch the corresponding Student Exam document using imported_batch_id (matching the name)
                student_exam_doc = frappe.get_doc('Student Exam', imported_batch_id)
                
                # Update the actual_count field in Student Exam with the count of matching students
                student_exam_doc.actual_count = count
                student_exam_doc.save()

            except frappe.DoesNotExistError:
                # If no Student Exam is found with the matching imported_batch_id
                frappe.throw(f"No Student Exam found with name {imported_batch_id}")
        else:
            frappe.throw("imported_batch_id is missing in the Student Master record")

