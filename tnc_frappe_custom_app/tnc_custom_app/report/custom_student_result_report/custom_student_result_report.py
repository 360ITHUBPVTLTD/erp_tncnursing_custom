# # Copyright (c) 2024, Administrator and contributors
# # For license information, please see license.txt

# # import frappe
# from frappe import _


# def execute(filters: dict | None = None):
# 	"""Return columns and data for the report.

# 	This is the main entry point for the report. It accepts the filters as a
# 	dictionary and should return columns and data. It is called by the framework
# 	every time the report is refreshed or a filter is updated.
# 	"""
# 	columns = get_columns()
# 	data = get_data()

# 	return columns, data


# def get_columns() -> list[dict]:
# 	"""Return columns for the report.

# 	One field definition per column, just like a DocType field definition.
# 	"""
# 	return [
# 		{
# 			"label": _("Column 1"),
# 			"fieldname": "column_1",
# 			"fieldtype": "Data",
# 		},
# 		{
# 			"label": _("Column 2"),
# 			"fieldname": "column_2",
# 			"fieldtype": "Int",
# 		},
# 	]


# def get_data() -> list[list]:
# 	"""Return data for the report.

# 	The report data is a list of rows, with each row being a list of cell values.
# 	"""
# 	return [
# 		["Row 1", 1],
# 		["Row 2", 2],
# 	]




# import frappe

# def execute(filters=None):
#     columns = [
#         {"label": "Batch ID", "fieldname": "batch_id", "fieldtype": "Data", "width": 120},
#         {"label": "Student ID", "fieldname": "student_id", "fieldtype": "Link", "options": "Student", "width": 120},
#         {"label": "Student Name", "fieldname": "student_name", "fieldtype": "Data", "width": 150},
#         {"label": "Student Mobile", "fieldname": "student_mobile", "fieldtype": "Data", "width": 120},
#         {"label": "Exam Name", "fieldname": "exam_name", "fieldtype": "Link", "options": "Student Exam", "width": 150},
#         {"label": "Exam Title Name", "fieldname": "exam_title_name", "fieldtype": "Data", "width": 150},
#         {"label": "Exam Date", "fieldname": "exam_date", "fieldtype": "Date", "width": 120},
#         {"label": "Rank", "fieldname": "rank", "fieldtype": "Int", "width": 100},
#         {"label": "Total Marks", "fieldname": "total_marks", "fieldtype": "Float", "width": 120},
#         {"label": "Total Right", "fieldname": "total_right", "fieldtype": "Int", "width": 100},
#         {"label": "Total Wrong", "fieldname": "total_wrong", "fieldtype": "Int", "width": 100},
#         {"label": "Total Skip", "fieldname": "total_skip", "fieldtype": "Int", "width": 100},
#         {"label": "Percentage", "fieldname": "percentage", "fieldtype": "Percent", "width": 100},
#     ]

#     data = get_data(filters)
#     return columns, data

# def get_data(filters):
#     conditions = []

#     if filters.get("exam_name"):
#         conditions.append("exam_name = %(exam_name)s")

#     if filters.get("exam_title_name"):
#         conditions.append("exam_title_name = %(exam_title_name)s")

#     conditions_str = " AND ".join(conditions)
    
#     if conditions_str:
#         conditions_str = "WHERE " + conditions_str

#     query = f"""
#         SELECT
#             batch_id, student_id, student_name, student_mobile,
#             exam_name, exam_title_name, exam_date, rank,
#             total_marks, total_right, total_wrong, total_skip, percentage
#         FROM
#             `tabStudent Results`
#         {conditions_str}
#         ORDER BY
#             rank 
#     """

#     return frappe.db.sql(query, filters, as_dict=True)

import frappe

def execute(filters=None):
    # Define the columns for the report
    columns = [
        {"label": "Batch ID", "fieldname": "batch_id", "fieldtype": "Data", "width": 120},
        {"label": "Student ID", "fieldname": "student_id", "fieldtype": "Link", "options": "Student", "width": 120},
        {"label": "Student Name", "fieldname": "student_name", "fieldtype": "Data", "width": 150},
        {"label": "Student Mobile", "fieldname": "student_mobile", "fieldtype": "Data", "width": 120},
        {"label": "Exam Name", "fieldname": "exam_name", "fieldtype": "Link", "options": "Test Series Type", "width": 150},
        {"label": "Exam Title Name", "fieldname": "exam_title_name", "fieldtype": "Link", "options": "Student Exam", "width": 150},
        {"label": "Exam Date", "fieldname": "exam_date", "fieldtype": "Date", "width": 120},
        {"label": "Rank", "fieldname": "rank", "fieldtype": "Int", "width": 100},
        {"label": "Total Marks", "fieldname": "total_marks", "fieldtype": "Float", "width": 120},
        {"label": "Total Right", "fieldname": "total_right", "fieldtype": "Int", "width": 100},
        {"label": "Total Wrong", "fieldname": "total_wrong", "fieldtype": "Int", "width": 100},
        {"label": "Total Skip", "fieldname": "total_skip", "fieldtype": "Int", "width": 100},
        {"label": "Percentage", "fieldname": "percentage", "fieldtype": "Percent", "width": 100},
    ]

    # Get data based on filters
    data,total_count = get_data(filters)
        # Create an HTML snippet to display the total count
    html_card = f"""
    <div style="padding: 10px; font-weight: bold;">
        <h4>Actual Count: {total_count}</h4>
    </div>
    """

    return columns, data, html_card


def get_data(filters):
    # Define the conditions based on the filters
    conditions = []
    if filters.get("exam_name"):
        conditions.append("exam_name = %(exam_name)s")
    if filters.get("exam_title_name"):  # exam_title_name filter corresponds to batch_id in Student Results
        conditions.append("batch_id = %(exam_title_name)s")

    # Build the WHERE clause
    conditions_str = " AND ".join(conditions)

    if conditions_str:
        conditions_str = f"WHERE {conditions_str}"

    # SQL query to fetch data from the Student Results doctype
    query = f"""
        SELECT
            batch_id, student_id, student_name, student_mobile,
            exam_name, exam_title_name, exam_date, rank,
            total_marks, total_right, total_wrong, total_skip, percentage
        FROM
            `tabStudent Results`
        {conditions_str}
        ORDER BY
            rank
    """

    # Fetch the filtered data
    data = frappe.db.sql(query, filters, as_dict=True)

    total_count = len(data)

    return data, total_count
