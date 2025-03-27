# Copyright (c) 2025, Administrator and contributors
# For license information, please see license.txt


# import frappe
# import math

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters or {})
#     return columns, data


# def get_columns():
#     return [
#         {"label": "Student ID", "fieldname": "student_id", "fieldtype": "Link","options": "Online Student","width": 100},
#         {"label": "Student Name", "fieldname": "student_name", "fieldtype": "Data", "width": 200},
#         {"label": "Mobile", "fieldname": "student_mobile", "fieldtype": "Data", "width": 120},
#         {"label": "Total Exams", "fieldname": "total_exams", "fieldtype": "Int", "width": 100},
#         {"label": "Green Count", "fieldname": "green_count", "fieldtype": "Int", "width": 100},
#         {"label": "Yellow Count", "fieldname": "yellow_count", "fieldtype": "Int", "width": 100},
#         {"label": "Red Count", "fieldname": "red_count", "fieldtype": "Int", "width": 100},
#         {"label": "Green %", "fieldname": "green_percent", "fieldtype": "Float", "width": 100},
#         {"label": "Yellow %", "fieldname": "yellow_percent", "fieldtype": "Float", "width": 100},
#         {"label": "Red %", "fieldname": "red_percent", "fieldtype": "Float", "width": 100},
#         # Optional: Enable if you use score-based ranking
#         # {"label": "Score", "fieldname": "score", "fieldtype": "Float", "width": 120},
#     ]


# def get_data(filters):
#     conditions = []

#     if filters.get("exam_date"):
#         from_date, to_date = filters.get("exam_date")
#         if from_date:
#             conditions.append("sr.exam_date >= %(from_date)s")
#             filters["from_date"] = from_date
#         if to_date:
#             conditions.append("sr.exam_date <= %(to_date)s")
#             filters["to_date"] = to_date

#     if filters.get("exam_name"):
#         conditions.append("sr.exam_name = %(exam_name)s")
#     if filters.get("student_id"):
#         conditions.append("sr.student_id = %(student_id)s")
#     if filters.get("exam_id"):
#         conditions.append("sr.exam_id = %(exam_id)s")

#     where_clause = " AND ".join(conditions)
#     if where_clause:
#         where_clause = "WHERE " + where_clause

#     query = f"""
#         SELECT 
#             sr.student_id,
#             sr.student_name,
#             sr.student_mobile,
#             COUNT(sr.name) AS total_exams,
#             SUM(CASE WHEN sr.rank_color = 'G' THEN 1 ELSE 0 END) AS green_count,
#             SUM(CASE WHEN sr.rank_color = 'Y' THEN 1 ELSE 0 END) AS yellow_count,
#             SUM(CASE WHEN sr.rank_color = 'R' THEN 1 ELSE 0 END) AS red_count
#         FROM `tabStudent Results` sr
#         {where_clause}
#         GROUP BY sr.student_id
#     """

#     result = frappe.db.sql(query, filters, as_dict=True)

#     for row in result:
#         total = row.total_exams or 1
#         row.green_percent = round((row.green_count / total) * 100, 2)
#         row.yellow_percent = round((row.yellow_count / total) * 100, 2)
#         row.red_percent = round((row.red_count / total) * 100, 2)

#         # Optional: calculate fair score
#         # row.score = round(row.green_percent * math.log(total + 1), 2)

#     # Sort by Green % descending (default)
#     result.sort(key=lambda x: x["green_percent"], reverse=True)

#     # Optional: Sort by score instead of green_percent
#     # result.sort(key=lambda x: x["score"], reverse=True)

#     # Apply count limit filter
#     if filters.get("count"):
#         try:
#             count = int(filters["count"])
#             result = result[:count]
#         except ValueError:
#             pass  # if invalid count, return all records

#     return result

import frappe

def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    html = get_html_summary(filters)
    return columns, data, html

# ----------------------------------------------
# Report Columns
# ----------------------------------------------
def get_columns():
    return [
        {"label": "Student ID", "fieldname": "student_id", "fieldtype": "Link", "options": "Online Student", "width": 100},
        {"label": "Student Name", "fieldname": "student_name", "fieldtype": "Data", "width": 200},
        {"label": "Mobile", "fieldname": "student_mobile", "fieldtype": "Data", "width": 120},
        {"label": "Total Exams", "fieldname": "total_exams", "fieldtype": "Int", "width": 100},
        {"label": "Green Count", "fieldname": "green_count", "fieldtype": "Int", "width": 100},
        {"label": "Yellow Count", "fieldname": "yellow_count", "fieldtype": "Int", "width": 100},
        {"label": "Red Count", "fieldname": "red_count", "fieldtype": "Int", "width": 100},
        {"label": "Green %", "fieldname": "green_percent", "fieldtype": "Float", "width": 100},
        {"label": "Yellow %", "fieldname": "yellow_percent", "fieldtype": "Float", "width": 100},
        {"label": "Red %", "fieldname": "red_percent", "fieldtype": "Float", "width": 100},
        {"label": "CPS", "fieldname": "cps", "fieldtype": "Float", "width": 100}
    ]

# ----------------------------------------------
# Report Data
# ----------------------------------------------
def get_data(filters):
    where_clause, query_filters = get_common_conditions(filters)

    query = f"""
        SELECT 
            sr.student_id,
            sr.student_name,
            sr.student_mobile,
            COUNT(sr.name) AS total_exams,
            SUM(CASE WHEN sr.rank_color = 'G' THEN 1 ELSE 0 END) AS green_count,
            SUM(CASE WHEN sr.rank_color = 'Y' THEN 1 ELSE 0 END) AS yellow_count,
            SUM(CASE WHEN sr.rank_color = 'R' THEN 1 ELSE 0 END) AS red_count
        FROM `tabStudent Results` sr
        WHERE sr.rank_color IS NOT NULL AND sr.rank_color != ''
        {f'AND {where_clause[6:]}' if where_clause else ''}
        GROUP BY sr.student_id
    """


    results = frappe.db.sql(query, query_filters, as_dict=True)
    admin_settings = frappe.get_cached_doc("Admin Settings", "Admin Settings")

    green_weight = admin_settings.green or 1.0
    yellow_weight = admin_settings.yellow or 0.3
    red_weight = admin_settings.red or 1.5

    for row in results:
        total = row.total_exams or 1
        row.green_percent = round((row.green_count / total) * 100, 2)
        row.yellow_percent = round((row.yellow_count / total) * 100, 2)
        row.red_percent = round((row.red_count / total) * 100, 2)

        # Compute CPS score using dynamic weights
        row.cps = round(
            (row.green_percent * green_weight) +
            (row.yellow_percent * yellow_weight) -
            (row.red_percent * red_weight),
            2
        )


    if filters.get("min_total_exams"):
        min_total = int(filters["min_total_exams"])
        results = [r for r in results if r.total_exams >= min_total]


    results = sorted(
    results,
    key=lambda x: (x.green_percent, x.total_exams),
    reverse=True
)


    if filters.get("count"):
        # Sort before slicing
        results = sorted(
            results,
            key=lambda x: (x.green_percent, x.total_exams),
            reverse=True
        )
        results = results[:int(filters["count"])]
    else:
        results = sorted(
            results,
            key=lambda x: (x.green_percent, x.total_exams),
            reverse=True
        )


    return results

# ----------------------------------------------
# Summary Number Cards (HTML)
# ----------------------------------------------
def get_html_summary(filters):
    where_clause, query_filters = get_common_conditions(filters)

    # Get Total Exams from tabStudent Exam with status = 'Data Synced'
    exam_query = """
        SELECT COUNT(DISTINCT se.exam_title_name) AS total_exams
        FROM `tabStudent Exam` se
        WHERE se.status = 'Data Synced'
    """
    exam_filters = {}

    # Apply exam_date range if provided
    if filters.get("exam_date"):
        from_date, to_date = filters.get("exam_date")
        if from_date:
            exam_query += " AND se.exam_date >= %(from_date)s"
            exam_filters["from_date"] = from_date
        if to_date:
            exam_query += " AND se.exam_date <= %(to_date)s"
            exam_filters["to_date"] = to_date

    # Apply exam_name if present
    if filters.get("exam_name"):
        exam_query += " AND se.exam_name = %(exam_name)s"
        exam_filters["exam_name"] = filters["exam_name"]

    exam_result = frappe.db.sql(exam_query, exam_filters, as_dict=True)[0]

    # Get Unique Students from tabStudent Results (as before)
    student_query = f"""
        SELECT COUNT(DISTINCT sr.student_id) AS unique_students
        FROM `tabStudent Results` sr
        {where_clause}
    """
    student_result = frappe.db.sql(student_query, query_filters, as_dict=True)[0]

    # Format values
    total_exams = format_indian_number(exam_result["total_exams"])
    unique_students = format_indian_number(student_result["unique_students"])

    html = f"""
    <div style="display: flex; gap: 20px; margin: 20px 0;">
        <div style="background: #e0f7fa; padding: 20px; border-radius: 8px; flex: 1; text-align: center;">
            <h4 style="margin: 0; font-size: 16px; color: #00796b;">Total Exams</h4>
            <div style="font-size: 24px; font-weight: bold;">{total_exams}</div>
        </div>
        <div style="background: #f1f8e9; padding: 20px; border-radius: 8px; flex: 1; text-align: center;">
            <h4 style="margin: 0; font-size: 16px; color: #558b2f;">Unique Students</h4>
            <div style="font-size: 24px; font-weight: bold;">{unique_students}</div>
        </div>
    </div>
    """
    return html


# ----------------------------------------------
# Common Filtering Logic
# ----------------------------------------------
def get_common_conditions(filters):
    conditions = []
    query_filters = {}

    if filters.get("exam_date"):
        from_date, to_date = filters.get("exam_date")
        if from_date:
            conditions.append("sr.exam_date >= %(from_date)s")
            query_filters["from_date"] = from_date
        if to_date:
            conditions.append("sr.exam_date <= %(to_date)s")
            query_filters["to_date"] = to_date

    if filters.get("exam_name"):
        conditions.append("sr.exam_name = %(exam_name)s")
        query_filters["exam_name"] = filters["exam_name"]

    if filters.get("student_id"):
        conditions.append("sr.student_id = %(student_id)s")
        query_filters["student_id"] = filters["student_id"]

    if filters.get("exam_id"):
        conditions.append("sr.exam_id = %(exam_id)s")
        query_filters["exam_id"] = filters["exam_id"]

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
    return where_clause, query_filters

# ----------------------------------------------
# Utility: Format number Indian style
# ----------------------------------------------
def format_indian_number(n):
    s = str(int(n))
    r = ''
    if len(s) > 3:
        r = ',' + s[-3:]
        s = s[:-3]
        while len(s) > 2:
            r = ',' + s[-2:] + r
            s = s[:-2]
        r = s + r
    else:
        r = s
    return r
