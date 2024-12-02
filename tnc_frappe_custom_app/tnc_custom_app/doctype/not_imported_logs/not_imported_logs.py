# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class NotImportedLogs(Document):
	pass


import frappe

@frappe.whitelist()
def check_mobile_exists(mobile):
    student = frappe.get_value('Online Student', {'mobile': mobile}, 'name')
    if student:
        return True
    return False

@frappe.whitelist()
def create_student(student_name, mobile,imported_batch_id):
    doc = frappe.new_doc('Online Student')
    doc.student_name = student_name
    doc.mobile = mobile
    doc.exam_id = imported_batch_id
    doc.insert()
    return doc.name

@frappe.whitelist()
def create_student_result(student_id, exam_id, student_name, mobile, rank, total_right, total_wrong, total_marks, total_skip, percentage):
    # Create new Student Results record
    doc = frappe.new_doc('Student Results')
    doc.student_id = student_id
    doc.exam_id = exam_id
    doc.student_name = student_name
    doc.mobile = mobile
    doc.rank = rank
    doc.total_right = total_right
    doc.total_wrong = total_wrong
    doc.total_marks = total_marks
    doc.total_skip = total_skip
    doc.percentage = percentage
    doc.insert()

    return doc.name
