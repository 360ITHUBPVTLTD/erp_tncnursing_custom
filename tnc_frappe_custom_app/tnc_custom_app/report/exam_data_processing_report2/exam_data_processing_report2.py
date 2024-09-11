# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

from frappe import _
import frappe
import json

def execute(filters=None):
    columns, data = [], []

    # Define columns for the report
    columns = [
        {"label": "Exam ID", "fieldname": "exam_id", "fieldtype": "Link", "options": "Student Exam", "width": 150},
        {"label": "Total Master Data", "fieldname": "student_master_count", "fieldtype": "Int", "width": 200},
        {"label": "Imported Master Data", "fieldname": "student_master_imported_count", "fieldtype": "Int", "width": 200},
        {"label": "Student Created", "fieldname": "student_created_count", "fieldtype": "Int", "width": 200},
        {"label": "Student Results Created", "fieldname": "student_results_count", "fieldtype": "Int", "width": 200},
    ]

    # Fetch data for the report
    data = get_exam_performance_data(filters)

    return columns, data

def get_exam_performance_data(filters):
    exam_id = filters.get("exam_id") if filters else None
    
    data = []

    # Get all Student Exam data
    student_exams = frappe.get_all(
        "Student Exam",
        fields=["name"]
    )

    for exam in student_exams:
        # Count records for 'Students Master Data' for the given exam
        student_master_data_count = frappe.db.count('Students Master Data', {'imported_batch_id': exam.name})
        
        # Count records for 'Students Master Data' where 'imported' is set to 1
        student_master_data_imported_count = frappe.db.count('Students Master Data', {'imported_batch_id': exam.name, 'imported': 1})

        # Count records for students created from 'Student' where batch ID matches
        student_created_count = frappe.db.count('Student', {'student_batch_id': exam.name})

        # Count records for student results from 'Student Results' where batch ID matches
        student_results_count = frappe.db.count('Student Results', {'batch_id': exam.name})

        # Add data to the report
        data.append({
            "exam_id": exam.name,
            "student_master_count": student_master_data_count,
            "student_master_imported_count": student_master_data_imported_count,
            "student_created_count": student_created_count,
            "student_results_count": student_results_count,
        })

    return data
