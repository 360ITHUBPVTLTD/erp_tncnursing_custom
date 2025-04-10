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
        {"label": "CPS", "fieldname": "cps", "fieldtype": "Float", "width": 100},
        # {"label": "PDF URL", "fieldname": "pdf_url", "fieldtype": "Small Text", "width": 500},
    ]

# ----------------------------------------------
# Report Data
# ----------------------------------------------
def get_data(filters):
    where_clause, query_filters = get_common_conditions(filters)

    # query = f"""
    #     SELECT 
    #         sr.student_id,
    #         sr.student_name,
    #         sr.student_mobile,
    #         COUNT(sr.name) AS total_exams,
    #         SUM(CASE WHEN sr.rank_color = 'G' THEN 1 ELSE 0 END) AS green_count,
    #         SUM(CASE WHEN sr.rank_color = 'Y' THEN 1 ELSE 0 END) AS yellow_count,
    #         SUM(CASE WHEN sr.rank_color = 'R' THEN 1 ELSE 0 END) AS red_count
    #     FROM `tabStudent Results` sr
    #     WHERE sr.rank_color IS NOT NULL AND sr.rank_color != ''
    #     {f'AND {where_clause[6:]}' if where_clause else ''}
    #     GROUP BY sr.student_id
    # """
    query = f"""
    SELECT
        sr.student_id,
        sr.student_name,
        sr.student_mobile,
        os.encryption_key,  -- Include the encryption_key from Online Student
        COUNT(sr.name) AS total_exams,
        SUM(CASE WHEN sr.rank_color = 'G' THEN 1 ELSE 0 END) AS green_count,
        SUM(CASE WHEN sr.rank_color = 'Y' THEN 1 ELSE 0 END) AS yellow_count,
        SUM(CASE WHEN sr.rank_color = 'R' THEN 1 ELSE 0 END) AS red_count
    FROM `tabStudent Results` sr
    LEFT JOIN `tabOnline Student` os ON sr.student_id = os.name  -- LEFT JOIN with Online Student table
    WHERE sr.rank_color IS NOT NULL AND sr.rank_color != ''
    {f'AND {where_clause[6:]}' if where_clause else ''}
    GROUP BY sr.student_id
"""


    results = frappe.db.sql(query, query_filters, as_dict=True)
    admin_settings = frappe.get_cached_doc("Admin Settings", "Admin Settings")

    green_weight = admin_settings.green or 1.0
    yellow_weight = admin_settings.yellow or 0.3
    red_weight = admin_settings.red or 1.5

    base_url = get_url()

    for row in results:
        print(row)
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
        
        # row.pdf_url = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Online%20Student&name={row.student_id}&format=Student%20Results%20Top%20Performer&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en"


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
##################################### Below whatsApp functionality will be started ########################

import frappe, json
import requests,time
from frappe import _
from frappe.utils import get_url

@frappe.whitelist()
def create_bulk_whatsapp_entry_from_report(filters):
    if isinstance(filters, str):
        filters = json.loads(filters)
    
    # Create a new Bulk WhatsApp Sharing Results document,
    # storing the report filters (as JSON) in the 'report_filters' field.
    bulk_doc = frappe.new_doc("Bulk whatsapp Sharing Results")
    test_series= filters.get("exam_name")
    # filters["exam_name"] = ["in", test_series_list]
    # bulk_doc.filters=filters
    # for ts in test_series_list:
    bulk_doc.append("test_series", {"test_series": test_series})
    # bulk_doc.report_filters = frappe.as_json(filters)
    bulk_doc.status = "Draft"
    bulk_doc.insert()
    frappe.db.commit()
    
    # Calculate the number of messages that would be sent.
    # get_data() is a function that fetches student records based on the filters.
    student_data = get_data(filters)  # You must define get_data(filters) as needed.
    count = len(student_data) if student_data else 0
    
    return {"count": count, "bulk_docname": bulk_doc.name}

@frappe.whitelist()
def cancel_bulk_result(bulk_docname):
    try:
        bulk_doc = frappe.get_doc("Bulk whatsapp Sharing Results", bulk_docname)
        if bulk_doc.status == "Draft":
            bulk_doc.status = "Cancelled"
            bulk_doc.save(ignore_permissions=True)
            frappe.db.commit()
            return {"status": "Cancelled"}
        else:
            return {"status": "Cannot cancel, already processed"}
    except Exception as e:
        frappe.log_error("Cancel Bulk Result Error", str(e))
        return {"status": "Error", "message": str(e)}

@frappe.whitelist()
def send_whatsapp_from_reports_using_rq(filters, bulk_docname):
    if isinstance(filters, str):
        filters = json.loads(filters)
    
    # Enqueue the WhatsApp sending process in the background,
    # passing both the filters and the bulk_docname.
    frappe.enqueue(
        method="tnc_frappe_custom_app.tnc_custom_app.report.high_performing_students_report.high_performing_students_report.send_whatsapp",
        queue="long",
        timeout=25200,
        job_id="Send WhatsApp Bulk Messages " + bulk_docname,
        filters=filters,
        bulk_docname=bulk_docname
    )
    
    return {"status": "Queued", "message": "WhatsApp message sending is scheduled in the background."}


@frappe.whitelist()
def send_whatsapp(filters, bulk_docname):
    if isinstance(filters, str):
        filters = json.loads(filters)
    filters = frappe._dict(filters or {})

    # Update the Bulk WhatsApp doc status to Submitted
    try:
        bulk_doc = frappe.get_doc("Bulk whatsapp Sharing Results", bulk_docname)
        bulk_doc.status = "Submitted"
        bulk_doc.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error("Bulk Doc Update Error", str(e))
    
    # Get the students based on the filters
    student_data = get_data(filters)  # Define get_data(filters) per your requirements.
    frappe.log_error(title="Filtered Student Data", message=frappe.as_json(student_data))
    frappe.log_error(title="Length of Student Data", message=str(len(student_data)))

    if not student_data:
        return {"status": "No students found", "success": False}

    try:
        wa_config = frappe.get_doc('WhatsApp Message Configuration', 'WA-Config-02')
    except frappe.DoesNotExistError:
        frappe.log_error("WA Config not found", "WhatsApp Send Error")
        return {"status": "WhatsApp config missing", "success": False}

    api_url = f"{wa_config.wa_server}/send"
    headers = {
        "apikey": wa_config.get_password('api_key'),
        "Content-Type": "application/json"
    }
    admin_doc = frappe.get_doc("Admin Settings")
    bulk_wa_test_mobile_no = admin_doc.bulk_wa_test_mobile_no

    failed = []
    count = 0
    mobile_no_s = bulk_wa_test_mobile_no.split(",")

    unsuccessfull_wa = frappe.get_all("Unsuccessful Whatsapp Log")
    unsuccessfull_wa_list = [i.name for i in unsuccessfull_wa]
        
    for student in student_data:
        mobile = student.get("student_mobile")
        if not mobile:
            frappe.log_error(f"Missing mobile number for {student.get('student_name')}", "WhatsApp Skipped")
            failed.append(student.get("student_id"))
            continue

        if mobile not in unsuccessfull_wa_list:
            continue

        # iteration_start = time.time()

        student_name = student.get("student_name")
        exam_name = "NORCET 8.0 Prelims"
        # second_variable = "TNC Test Series"
        # third_variable = "TNC"
        # fourth_variable = "TNC Nursing"
        # student_name = "Mohan Raj"
        file_encryption_key = student.get("encryption_key")

        # file_encryption_key = mobile_no_s[count]

        base_url = get_url()  # Get the site's base URL
        file_url = f"{base_url}/api/method/tnc_frappe_custom_app.result_sharing.download_result_by_key?encryption_key={file_encryption_key}"


        
        wa_message = f"""Dear {student_name} ji ,

Before the upcoming {exam_name} Exam, we are sharing the TNC Test Series Performance Report based on daily test results.
This report provides an overview of academic progress and is intended to support better preparation for the final exam.

Thank you for your trust in TNC.

Your Success is Our Concern.

TNC Nursing
Official Number: Call / WhatsApp: 7484999051

Download Your Result from here 👉🏻
{file_url}"""


        payload = {
            "userid": wa_config.user_id,
            "msg": wa_message,
            "wabaNumber": wa_config.waba_number,
            "output": "json",
            "mobile": f"91{mobile}",
            "sendMethod": "quick",
            "msgType": "text",
            "templateName": "exem_result_final_3"
        }
        
        try:
            response = requests.post(api_url, json=payload, headers=headers)
            frappe.log_error(title="WhatsApp Response", message=f"Response: {response.json()}\nPayload:{payload}")


            # frappe.log_error(title="WhatsApp Payload", message=f"Payload: {payload}")
            count += 1
     
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to send WhatsApp to {student_name} ({mobile}): {str(e)}"
            frappe.log_error("WhatsApp API Error", error_msg)
            failed.append(student.get("student_id"))
        # iteration_end = time.time()
        # duration = iteration_end - iteration_start
        # frappe.log_error(
        #     title="WhatsApp Iteration Time",
        #     message=f"Duration for {student_name} ({mobile}): {duration} seconds"
        # )
        # break

    # Update the Bulk WhatsApp doc with the results
    try:
        bulk_doc = frappe.get_doc("Bulk whatsapp Sharing Results", bulk_docname)
        bulk_doc.sent = 1
        bulk_doc.count = count
        bulk_doc.failed_count = len(failed)
        bulk_doc.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.log_error("WhatsApp Results Summary", f"Successfully sent results to {count} students.")
    except Exception as e:
        frappe.log_error("Bulk Doc Final Update Error", str(e))

    return {
        "success": count > 0,
        "sent_count": count,
        "failed_count": len(failed),
        "failed_ids": failed
    }




@frappe.whitelist()
def send_whatsapp_media(filters, bulk_docname):
    if isinstance(filters, str):
        filters = json.loads(filters)
    filters = frappe._dict(filters or {})

    # Update the Bulk WhatsApp doc status to Submitted
    try:
        bulk_doc = frappe.get_doc("Bulk whatsapp Sharing Results", bulk_docname)
        bulk_doc.status = "Submitted"
        bulk_doc.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error("Bulk Doc Update Error", str(e))
    
    # Get the students based on the filters
    student_data = get_data(filters)  # Define get_data(filters) per your requirements.
    frappe.log_error(title="Filtered Student Data", message=frappe.as_json(student_data))
    frappe.log_error(title="Length of Student Data", message=str(len(student_data)))

    if not student_data:
        return {"status": "No students found", "success": False}

    try:
        wa_config = frappe.get_doc('WhatsApp Message Configuration', 'WA-Config-02')
    except frappe.DoesNotExistError:
        frappe.log_error("WA Config not found", "WhatsApp Send Error")
        return {"status": "WhatsApp config missing", "success": False}

    api_url = f"{wa_config.wa_server}/send"
    headers = {
        "apikey": wa_config.get_password('api_key'),
        "Content-Type": "application/json"
    }
    admin_doc = frappe.get_doc("Admin Settings")
    bulk_wa_test_mobile_no = admin_doc.bulk_wa_test_mobile_no

    failed = []
    count = 0
    mobile_no_s = bulk_wa_test_mobile_no.split(",")
    for student in student_data:
        mobile = student.get("student_mobile")
        if not mobile:
            frappe.log_error(f"Missing mobile number for {student.get('student_name')}", "WhatsApp Skipped")
            failed.append(student.get("student_id"))
            continue
        iteration_start = time.time()

        student_name = student.get("student_name")
        exam_name = "NORCET 8.0 Prelims"
        second_variable = "TNC Test Series"
        third_variable = "TNC"
        fourth_variable = "TNC Nursing"
        # student_name = "Mohan Raj"
        file_encryption_key = student.get("encryption_key")

        # file_encryption_key = mobile_no_s[count]

        base_url = get_url()  # Get the site's base URL
        file_url = f"{base_url}/api/method/tnc_frappe_custom_app.result_sharing.download_result_by_key?encryption_key={file_encryption_key}"
        # Compose the media WhatsApp message
#         wa_message = f"""Dear {student_name},


# Please Check your Results Summary

# Best regards,
# TNC Administration"""
        
#         wa_message = f"""Dear {student_name} ji ,

# Before the upcoming {exam_name} Exam, we are sharing the TNC Test Series Performance Report based on daily test results.
# This report provides an overview of academic progress and is intended to support better preparation for the final exam.

# Thank you for your trust in TNC.
# Your Success is Our Concern.

# TNC Nursing
# Official Number: Call / WhatsApp: 7484999051"""
#         wa_message = f"""नमस्कार !
# आपले मत आमच्यासाठी खूप महत्वाचे आहे. फक्त 30 सेकंड लागेल.
# *खालील दिलेल्या लिंक वर क्लिक करून एक फॉर्म उघडेल ज्याच्यात आपले अमूल्य मत मांडावेत.*
# धन्यवाद"""
        wa_message = f"""Dear {student_name}ji ,

Before the upcoming {exam_name} Exam, we are sharing the {second_variable} Performance Report based on daily test results.
This report provides an overview of academic progress and is intended to support better preparation for the final exam.

Thank you for your trust in {third_variable}.
Your Success is Our Concern.

{fourth_variable}
Official Number: Call / WhatsApp: 7484999051"""

        wa_message = f"""Dear {student_name} ji ,

Before the upcoming {exam_name} Exam, we are sharing the {second_variable} Performance Report based on daily test results.
This report provides an overview of academic progress and is intended to support better preparation for the final exam.

Thank you for your trust in {third_variable}.
Your Success is Our Concern.

{fourth_variable}
Official Number: Call / WhatsApp: 7484999051"""
        
#         wa_message = f"""Dear {student_name} ji ,

# Before the upcoming {exam_name} Exam, we are sharing the TNC Test Series Performance Report based on daily test results.
# This report provides an overview of academic progress and is intended to support better preparation for the final exam.

# Thank you for your trust in TNC.
# Your Success is Our Concern.

# TNC Nursing
# Official Number: Call / WhatsApp: 7484999051

# Result: {file_url}"""


        payload = {
            "userid": wa_config.user_id,
            "msg": wa_message,
            "wabaNumber": wa_config.waba_number,
            "output": "json",
            # "mobile": f"91{mobile}",
            "mobile": "919441395592",
            # "mobile": f"91{mobile_no_s[count]}",
            "sendMethod": "quick",
            "msgType": "media",
            # "msgType": "text",
            # For production, generate a dynamic mediaUrl if needed.
            # "mediaUrl": f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Online%20Student&name={student.get('student_id')}&format=Student%20Results%20Top%20Performer&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en",
            # "mediaUrl": f"https://tnc.360ithub.com/api/method/frappe.utils.print_format.download_pdf?doctype=Online%20Student&name=TNC-Student-00074203&format=Student%20Results%20Top%20Performer&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en",
            # "media_url" : f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Student%20Results&name={docname}&format=Dynamic%20Student%20Print%20Format&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en",
            "mediaUrl":"https://tnc.360ithub.com/files/TNC-Student-00082650.pdf",
            "mediaType": "document",
            "documentName": f'{student_name.lower().replace(" ", "_")}.pdf',
            "templateName": "exam_result"
            # "templateName": "exem_result_final"
        }
        
        try:
            response = requests.post(api_url, json=payload, headers=headers)
            frappe.log_error(title="WhatsApp Response", message=f"Response: {response.json()}\nPayload:{payload}")


            # frappe.log_error(title="WhatsApp Payload", message=f"Payload: {payload}")
            count += 1
            # if count == len(mobile_no_s):
            if True:
                break

            
            
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to send WhatsApp to {student_name} ({mobile}): {str(e)}"
            frappe.log_error("WhatsApp API Error", error_msg)
            failed.append(student.get("student_id"))
        iteration_end = time.time()
        duration = iteration_end - iteration_start
        frappe.log_error(
            title="WhatsApp Iteration Time",
            message=f"Duration for {student_name} ({mobile}): {duration} seconds"
        )
        # break

    # Update the Bulk WhatsApp doc with the results
    try:
        bulk_doc = frappe.get_doc("Bulk whatsapp Sharing Results", bulk_docname)
        bulk_doc.sent = 1
        bulk_doc.count = count
        bulk_doc.failed_count = len(failed)
        bulk_doc.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.log_error("WhatsApp Results Summary", f"Successfully sent results to {count} students.")
    except Exception as e:
        frappe.log_error("Bulk Doc Final Update Error", str(e))

    return {
        "success": count > 0,
        "sent_count": count,
        "failed_count": len(failed),
        "failed_ids": failed
    }


# @frappe.whitelist()
# def send_whatsapp(filters):
#     if isinstance(filters, str):
#         filters = json.loads(filters)  # Convert JSON string to dict

#     filters = frappe._dict(filters or {})

#     student_data = get_data(filters)
#     # ✅ Correct function: frappe.log_error
#     frappe.log_error(title="Filtered Student Data", message=frappe.as_json(student_data))

#     # ✅ Convert length to string before logging
#     frappe.log_error(title="Length of Student Data", message=str(len(student_data)))

#     if not student_data:
#         return {"status": "No students found", "success": False}

#     try:
#         wa_config = frappe.get_doc('WhatsApp Message Configuration', 'WA-Config-01')
#     except frappe.DoesNotExistError:
#         frappe.log_error("WA Config not found", "WhatsApp Send Error")
#         return {"status": "WhatsApp config missing", "success": False}


#     api_url = f"{wa_config.wa_server}/send"
#     headers = {
#         "apikey": wa_config.get_password('api_key'),
#         "Content-Type": "application/json"
#     }

    
#     failed =[]
#     count = 0
#     for student in student_data:
#         mobile = student.get("student_mobile")
#         if mobile != "9098543046":
#             continue

#         student_name = student.get("student_name")
        
#         if not mobile:
#             frappe.log_error(f"Missing mobile number for {student_name}", "WhatsApp Skipped")
#             failed.append(student.get("student_id"))
#             continue  # Skip this iteration

#         wa_message = f"""🎉 *Congratulations, Star Achievers!* 🌟

# Dear {student_name},

# Your hard work, dedication, and perseverance have truly paid off! Securing a place among the Top 100 Students is no small feat—it’s a testament to your brilliance and relentless effort. 🌟

# Once again, kudos on this remarkable milestone! 🏆 Keep shining and inspiring those around you.

# With pride &amp; best wishes,

# TNC Nursing"""

#         payload = {
#             "userid": wa_config.user_id,
#             "msg": wa_message,
#             "wabaNumber": wa_config.waba_number,
#             "output": "json",
#             "mobile": f"91{mobile}",
#             "sendMethod": "quick",
#             "msgType": "text",
#             # "mediaType": "document",
#             "templateName": "top_students_inspiration_template_new",
#             "footer": "Thank you"
#         }

#         try:
#             response = requests.post(api_url, json=payload, headers=headers)
#             # response.raise_for_status()
#             frappe.log_error(title="WhatsApp Response in Reports",message= f"test: {response.json()}")
#             frappe.log_error("WhatsApp Sent", f"{student_name} ({mobile}) ✅\nResponse: {response.json()}")
#             count += 1  # ✅ Increment only after success
#         except requests.exceptions.RequestException as e:
#             error_msg = f"Failed to send WhatsApp to {student_name} ({mobile}): {str(e)}"
#             frappe.error_log("WhatsApp API Error", error_msg)
#             failed.append(student.get("student_id"))

#     # ✅ Ensure correct response
#     return {
#         "success": count > 0,  # ✅ Return True if any messages were sent
#         "sent_count": count,
#         "failed_count": len(failed),
#         "failed_ids": failed
#     }



@frappe.whitelist()
def get_whatsapp_count(filters):
    import json
    if isinstance(filters, str):
        filters = json.loads(filters)
        
    # Assume get_data is the function that returns student records
    student_data = get_data(filters)
    count = len(student_data) if student_data else 0
    
    return {"count": count}

