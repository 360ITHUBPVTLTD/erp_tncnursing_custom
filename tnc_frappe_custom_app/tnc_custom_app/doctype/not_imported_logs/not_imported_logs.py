# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class NotImportedLogs(Document):
	pass


import frappe

@frappe.whitelist()
def check_mobile_exists(mobile):
    student = frappe.get_value('Student', {'mobile': mobile}, 'name')
    if student:
        return True
    return False

@frappe.whitelist()
def create_student(student_name, mobile,imported_batch_id):
    doc = frappe.new_doc('Student')
    doc.student_name = student_name
    doc.mobile = mobile
    doc.student_batch_id = imported_batch_id
    doc.insert()
    return doc.name

@frappe.whitelist()
def create_student_result(student_id, batch_id, student_name, mobile, rank, total_right, total_wrong, total_marks, total_skip, percentage):
    # Create new Student Results record
    doc = frappe.new_doc('Student Results')
    doc.student_id = student_id
    doc.batch_id = batch_id
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
