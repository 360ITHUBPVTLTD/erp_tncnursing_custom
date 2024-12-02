# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

from frappe import _
import frappe
import json

def execute(filters=None):
    columns, data = [], []

    columns = [
        {"label": "Exam ID", "fieldname": "exam_id", "fieldtype": "Link", "options": "Student Exam", "width": 150},
        {"label": "Total Master Data", "fieldname": "student_master_count", "fieldtype": "Int", "width": 200},
        {"label": "Imported Master Data", "fieldname": "student_master_imported_count", "fieldtype": "Int", "width": 200},
        {"label": "Student Created", "fieldname": "student_created_count", "fieldtype": "Int", "width": 200},
        {"label": "Student Results Created", "fieldname": "student_results_count", "fieldtype": "Int", "width": 200},
    ]

    data = get_exam_performance_data(filters)

    return columns, data

def get_exam_performance_data(filters):
    exam_id = filters.get("exam_id")
    
    data = []

    # Get all Student Master Data for the given Exam ID
    student_exams = frappe.get_all(
        "Student Exam",
        fields=["name"],
    )

    for exam in student_exams:

		student_master_data_records = frappe.db.count('Students Master Data', {'exam_id': imported_batch_id})
        # student_master_data_records = frappe.get_all(
        #     "Students Master Data",
        #     fields=["name"],
        #     filters={"exam_id": exam.name},
        #     limit_page_length=0,  # Ensures no data is fetched, only count
        #     as_list=True
        # )
        
		student_master_data_records = frappe.db.count('Students Master Data', {'exam_id': imported_batch_id,, "imported": 1})
        # student_master_data_records_imported = frappe.get_all(
        #     "Students Master Data",
        #     fields=["name"],
        #     filters={"exam_id": exam.name, "imported": 1},
        #     limit_page_length=0,  # Ensures no data is fetched, only count
        #     as_list=True
        # )
        students_imported = frappe.db.count('Online Student', {"exam_id": exam.name})
        # students_imported = frappe.get_all(
        #     "Online Student",
        #     filters={"exam_id": exam.name},
        #     limit_page_length=0,
        #     as_list=True
        # )
        student_results_imported = frappe.db.count('Student Results', {"exam_id": exam.name})
        # student_results_imported = frappe.get_all(
        #     "Student Results",
        #     filters={"exam_id": exam.name},
        #     limit_page_length=0,
        #     as_list=True
        # )

        # Add data to the report
        data.append({
            "exam_id": exam.name,
            "student_master_count": len(student_master_data_records),
            "student_master_imported_count": len(student_master_data_records_imported),
            "student_created_count": len(students_imported),
            "student_results_count": len(student_results_imported),
        })

    return data
