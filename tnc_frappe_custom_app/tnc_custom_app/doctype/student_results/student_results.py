# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt



import frappe
from frappe.model.document import Document

import frappe
from frappe.model.document import Document

# class StudentResults(Document):
#     def before_insert(self):
#         # Ensure that the student_mobile is provided
#         if self.student_mobile:
#             # Check if the student already exists based on the mobile number
#             student_exists = frappe.db.exists('Online Student', {'mobile': self.student_mobile})
            
#             if not student_exists:
#                 # If the student does not exist, create a new Student record
#                 new_student = frappe.get_doc({
#                     'doctype': 'Online Student',
#                     'student_name': self.student_name,
#                     'mobile': self.student_mobile
#                 })
#                 new_student.insert(ignore_permissions=True)
#                 frappe.msgprint(f"New Student created: {self.student_name}")
#                 # Link the new student's ID to the Student Results record
#                 self.student_id = new_student.name
#             else:
#                 # If the student exists, fetch the student ID and update the Student Results record
#                 student = frappe.get_doc('Online Student', student_exists)
#                 self.student_id = student.name
#         else:
#             frappe.throw("Student Mobile is required to create a Student record.")

#################################### Above code is previous code #####################################

# import frappe
# from frappe.model.document import Document
# from frappe import _

# class StudentResults(Document):
#     def before_insert(self):
#         self.check_duplicate_entry()

#     def check_duplicate_entry(self):
#         # Check if a record with the same exam_name, exam_date, and student_mobile already exists
#         duplicate_entry = frappe.db.exists('Student Results', {
#             'exam_name': self.exam_name,
#             'exam_date': self.exam_date,
#             'student_mobile': self.student_mobile
#         })

#         if duplicate_entry:
#             frappe.throw(_("A record with the same Exam Name, Exam Date, and Student Mobile already exists."))

########################## Below code is working good code ###########################


# import frappe
# from frappe.model.document import Document
# from frappe import _

# class StudentResults(Document):
#     def before_save(self):
#         self.check_duplicate_entry()

#     def check_duplicate_entry(self):
#         # Check if a record with the same exam_name, exam_date, and student_mobile already exists
#         duplicate_entry = frappe.db.exists('Student Results', {
#             'exam_name': self.exam_name,
#             'exam_date': self.exam_date,
#             'student_mobile': self.student_mobile,
#             'name': ['!=', self.name]  # Exclude the current document from the check
#         })

#         if duplicate_entry:
#             frappe.throw(_("A record with the same Exam Name, Exam Date, and Student Mobile already exists."))

############### Above code is validating the duplicate Student Results withexam_name,exam_date,student_mobile ##################


# import frappe
# from frappe.model.document import Document

# class StudentResults(Document):
#     def before_save(self):
#         # Ensure that the student_mobile is provided
#         if self.student_mobile:
#             # Check if the student already exists based on the mobile number
#             student_exists = frappe.db.exists('Online Student', {'mobile': self.student_mobile})
            
#             if not student_exists:
#                 # If the student does not exist, create a new Student record
#                 new_student = frappe.get_doc({
#                     'doctype': 'Online Student',
#                     'student_name': self.student_name,
#                     'mobile': self.student_mobile,
#                     # 'district': self.district,  # Add other fields if necessary
#                     # 'state': self.state
#                 })
#                 new_student.insert(ignore_permissions=True)
#                 # Log the creation of the new student
#                 frappe.msgprint(f"New Student created: {self.student_name}")
#                 # Link the new student's ID to the Student Results record
#                 self.student_id = new_student.name
#             else:
#                 # If the student exists, fetch the student ID and update the Student Results record
#                 student = frappe.get_doc('Online Student', student_exists)
#                 self.student_id = student.name
#         else:
#             frappe.throw("Student Mobile is required to create or link a Student record.")



############### Above code is creating a new student record in the Student Results doctype ###################


##################  Combined of aBove two codes ###############



import frappe
from frappe.model.document import Document
from frappe import _

class StudentResults(Document):
    def before_insert(self):
        self.check_duplicate_entry()
        self.ensure_student_exists()

    def check_duplicate_entry(self):
        # Check if a record with the same exam_name, exam_date, and student_mobile already exists
        duplicate_entry = frappe.db.exists('Student Results', {
            # 'exam_name': self.exam_name,
            # 'exam_date': self.exam_date,
            # 'exam_id': self.exam_id,
            'student_id': self.student_id,
            'exam_id': self.exam_id,
            # 'exam_title_name': self.exam_title_name,
            # 'student_mobile': self.student_mobile,
            # 'name': ['!=', self.name]  # Exclude the current document from the check
        })

        if duplicate_entry:
            frappe.log_error(f"Bulk Sync fail.{self.exam_name}{self.exam_date}{self.student_mobile}")
            frappe.throw(_("A record with the same Exam Name, Exam Date, and Student Mobile already exists."))

    def ensure_student_exists(self):
        # Ensure that the student_mobile is provided
        if self.student_mobile:
            # Check if the student already exists based on the mobile number
            student_exists = frappe.db.exists('Online Student', {'mobile': self.student_mobile})
            
            if not student_exists:
                # If the student does not exist, create a new Student record
                new_student = frappe.get_doc({
                    'doctype': 'Online Student',
                    'student_name': self.student_name,
                    'mobile': self.student_mobile,
                    # 'district': self.district,  # Add other fields if necessary
                    # 'state': self.state
                })
                new_student.insert(ignore_permissions=True)
                # Log the creation of the new student
                frappe.msgprint(f"New Student created: {self.student_name}")
                # Link the new student's ID to the Student Results record
                self.student_id = new_student.name
            else:
                # If the student exists, fetch the student ID and update the Student Results record
                self.student_id = frappe.get_value('Online Student', {'mobile': self.student_mobile}, 'name')
        else:
            frappe.throw(_("Student Mobile is required to create or link a Student record."))

    # def after_delete(doc):
    #     student_id = doc.student_id
    #     student_doc = frappe.get_doc('Online Student', student_id )
    #     old_test_series_results = frappe.get_doc('Student Results',filters={"student_id":student_id})
    #     student_doc=len(old_test_series_results)+1
    #     student_doc.save()


############################## Creating a Entry in the Bulk whatsapp doctype ############################################
# File: tnc_frappe_custom_app/tnc_custom_app/doctype/student_results/student_results.py

import frappe
from frappe.model.document import Document
from frappe import _

@frappe.whitelist()
def create_bulk_whatsapp_entry_for_single_exam(exam_ids):
    if not exam_ids:
        frappe.throw(_("No Exam ID provided."))

    if isinstance(exam_ids, str):
        import json
        exam_ids = json.loads(exam_ids)

    created_docname = None
    total_students = 0

    for exam_id in exam_ids:
        exam = frappe.get_doc("Student Exam", exam_id)

        # Get students from Student Results linked to this exam
        student_results = frappe.get_all(
            "Student Results",
            filters={"exam_id": exam_id},
            fields=["student_id"]
        )

        total_students += len(student_results)

        # Create a new Bulk WhatsApp Sharing Results doc
        bulk_doc = frappe.new_doc("Bulk whatsapp Sharing Results")
        bulk_doc.student_exam_id = exam_id
        bulk_doc.status = "Draft"
        # bulk_doc.student_count = len(student_results)
        bulk_doc.save(ignore_permissions=True)
        created_docname = bulk_doc.name

    return {
        "success": True,
        "docname": created_docname,
        "student_count": total_students
    }



######################## Below code is to send the WA for selected Exams only ############################

from frappe.utils import get_url

@frappe.whitelist()
def send_results_for_single_exam(exam_ids,bulk_docname):

    resp = frappe.db.set_value("Bulk whatsapp Sharing Results", bulk_docname, "status", "Submitted")
    frappe.log_error(f"Response from frappe.db.set_value: {resp}", "Status Update")
    # Enqueue the background job
    frappe.enqueue(
        method="tnc_frappe_custom_app.tnc_custom_app.doctype.student_results.student_results.send_whatsapp_for_single_exam",  # ✅ Replace with your actual module path
        queue='default',
        timeout=600,
        exam_ids=exam_ids,
        bulk_docname=bulk_docname
    )
    # send_results_background(from_date, to_date, test_series,bulk_docname)
    return {"status": "Queued", "message": "Result sending is scheduled in background."}

########################## RQ Job for single exam sending Result #############################

import frappe
import json
import requests
from frappe import _

@frappe.whitelist()
def send_whatsapp_for_single_exam(exam_ids,bulk_docname):

    try:
        # Get the exam title from the first exam ID
        exam_title_name = frappe.db.get_value('Student Exam', exam_ids, 'exam_title_name')


        # Fetch unique students who appeared in that exam title
        # Fetch students from Student Results using the exam ID directly
        results = frappe.get_all(
            "Student Results",
            filters={"exam_id": exam_ids},
            fields=["student_id", "student_name", "student_mobile", "name"],
            distinct=True
        )
    # Check if any results were found
        if not results:
            return {"status": "No students found for this exam title"}

        # WhatsApp Configuration
        wa_config = frappe.get_doc('WhatsApp Message Configuration', 'WA-Config-01')
        api_url = f"{wa_config.wa_server}/send"
        headers = {
            "apikey": wa_config.get_password('api_key'),
            "Content-Type": "application/json"
        }
        base_url = frappe.utils.get_url()

        count = 0
        for student in results:
            mobile = student.get("student_mobile")
            student_name = student.get("student_name")
            student_id = student.get("student_id")
            docname = student.get("name")

            if not mobile:
                frappe.log_error(f"Missing mobile number for {student_name}", "WhatsApp Message Skipped")
                continue

            wa_message = f"""Dear {student_name},

Please Check your Results Summary

Best regards,
TNC Administration"""

            # You can dynamically build the PDF link later
            # media_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
            media_url = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Student%20Results&name={docname}&format=Student%20Results%20Sharing&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en"

            payload = {
                "userid": wa_config.user_id,
                "msg": wa_message,
                "wabaNumber": wa_config.waba_number,
                "output": "json",
                "mobile": f"91{mobile}",
                "sendMethod": "quick",
                "msgType": "media",
                "mediaUrl": media_url,
                "mediaType": "document",
                "templateName": "student_sharing_results_template"
            }

            try:
                response = requests.post(api_url, json=payload, headers=headers)
                response.raise_for_status()
                # print("WhatsaAPAP REsponse",response.json())
                count += 1
                # print(f"[SUCCESS] Sent WhatsApp to {student_name} ({mobile})")

            except requests.exceptions.RequestException as e:
                frappe.log_error(f"WhatsApp Message Failed for {student_name}: {str(e)}", "WhatsApp API Error")


        bulk_wa = frappe.get_doc('Bulk whatsapp Sharing Results', bulk_docname)
        bulk_wa.sent = 1
        bulk_wa.count = count
        bulk_wa.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.log_error("WhatsApp Results Summary", f"Successfully sent results to {count} students.")

        return {"status": "Success", "message": f"Results sent to {count} students"}

    except Exception as e:
        frappe.log_error(f"Unexpected error: {str(e)}", "Send WhatsApp Results Error")
        return {"status": "Failed", "message": "An unexpected error occurred. Check logs."}


######################## Save it into the doctype Bulk whatsapp functionality for result shariing ####################
import frappe
import json

@frappe.whitelist()
def create_bulk_whatsapp_entry(from_date, to_date, test_series):
    print("Raw test_series:", test_series)  # e.g., '["NORCET 7.0"]'
    test_series_list = json.loads(test_series)  # now a Python list
    print("Parsed test_series_list:", test_series_list)

    filters = {"exam_date": ["between", [from_date, to_date]]}
    
    if test_series_list:
        filters["exam_name"] = ["in", test_series_list]

    results = frappe.get_all(
        "Student Results",
        filters=filters,
        fields=["name", "student_id", "student_name", "student_mobile", "exam_name"],
        distinct=True
    )
    print("Results found:", results)

    if not results:
        frappe.log_error("No students found for WhatsApp sharing", "WhatsApp Results Skipped")
        return {"success": False, "message": "No students found."}

    doc = frappe.new_doc("Bulk whatsapp Sharing Results")
    doc.from_date = from_date
    doc.to_date = to_date
    doc.status = "Draft"

    for series in test_series_list:
        doc.append("test_series", {
            "test_series": series
        })

    doc.insert()
    frappe.db.commit()

    student_count = len(results)

    return {
        "success": True,
        "docname": doc.name,
        "student_count": student_count
    }

############################################## Cancel Bulk Result ################################

@frappe.whitelist()
def cancel_bulk_result(bulk_docname):
    # if not frappe.db.exists("Bulk whatsapp Sharing Results", bulk_docname):
    #     frappe.throw(_("Bulk whatsapp Sharing Results not found: {0}").format(bulk_docname))

    doc = frappe.get_doc("Bulk whatsapp Sharing Results", bulk_docname)
    if doc.status == "Draft":
        doc.status = "Cancelled"
        doc.save(ignore_permissions=True)
        frappe.db.commit()

#####################################################################################################################
# /home/pankaj/Pictures/bench-tnc-45/apps/tnc_frappe_custom_app/tnc_frappe_custom_app/tnc_custom_app/doctype/student_results/student_results.py
######################## Below is to choose the daterange functionality #####################################
import frappe
import requests
import json
from frappe import _
from frappe.utils import get_url

@frappe.whitelist()
def send_results_by_date_range(from_date, to_date, test_series,bulk_docname):
    if not from_date or not to_date:
        frappe.throw(_("From Date and To Date are required."))

    resp = frappe.db.set_value("Bulk whatsapp Sharing Results", bulk_docname, "status", "Submitted")
    frappe.log_error(f"Response from frappe.db.set_value: {resp}", "Status Update")


    # Enqueue the background job
    frappe.enqueue(
        method="tnc_frappe_custom_app.tnc_custom_app.doctype.student_results.student_results.send_results_background",  # ✅ Replace with your actual module path
        queue='default',
        timeout=600,
        from_date=from_date,
        to_date=to_date,
        test_series=test_series,
        bulk_docname=bulk_docname
    )
    # send_results_background(from_date, to_date, test_series,bulk_docname)
    return {"status": "Queued", "message": "Result sending is scheduled in background."}

import traceback
def send_results_background(from_date, to_date, test_series,bulk_docname):
    try:
        # Parse test_series if it's JSON string
        if isinstance(test_series, str):
            try:
                test_series = json.loads(test_series)
            except Exception:
                test_series = [test_series]

        filters = {"exam_date": ["between", [from_date, to_date]]}
        if test_series:
            filters["exam_name"] = ["in", test_series]

        results = frappe.get_all(
            "Student Results",
            filters=filters,
            fields=["name", "student_id", "student_name", "student_mobile", "exam_name"],
            distinct=True
        )

        if not results:
            frappe.log_error("No students found for WhatsApp sharing", "WhatsApp Results Skipped")
            return

        wa_config = frappe.get_doc('WhatsApp Message Configuration', 'WA-Config-01')
        api_url = f"{wa_config.wa_server}/send"
        headers = {
            "apikey": wa_config.get_password('api_key'),
            "Content-Type": "application/json"
        }
        base_url = get_url()
        count = 0

        for student in results:
            mobile = student.get("student_mobile")
            if not mobile:
                frappe.log_error(f"Missing mobile number for {student.get('student_name')}", "WhatsApp Skipped")
                continue

            docname = student.get("name")
            wa_message = f"""Dear {student.get('student_name')},

Please Check your Results Summary

Best regards,
TNC Administration"""

            media_url = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Student%20Results&name={docname}&Dynamic%20Student%20Print%20Format&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en"
            # media_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
            payload = {
                "userid": wa_config.user_id,
                "msg": wa_message,
                "wabaNumber": wa_config.waba_number,
                "output": "json",
                "mobile": f"91{mobile}",
                "sendMethod": "quick",
                "msgType": "media",
                "mediaUrl": media_url,
                "mediaType": "document",
                "templateName": "student_sharing_results_template"
            }

            try:
                response = requests.post(api_url, json=payload, headers=headers)
                # response.raise_for_status()
                # print("RESSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",response.json())
                frappe.log_error(title="WhatsApp Response",message= f"test: {response.json()}")
                count += 1
            except requests.exceptions.RequestException as e:
                frappe.log_error(f"WhatsApp Failed for {student.get('student_name')}: {str(e)}", "WhatsApp API Error")
    
        bulk_wa = frappe.get_doc('Bulk whatsapp Sharing Results', bulk_docname)
        # print("WAWAWAWAWAW",bulk_wa)
        bulk_wa.sent = 1
        bulk_wa.count = count
        # bulk_wa.flags.ignore_permissions = True
        bulk_wa.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.log_error("WhatsApp Results Summary", f"Successfully sent results to {count} students.")

    except Exception as e:
        frappe.log_error(title="WhatsApp Results Background Error", message=f"Unexpected error: {str(e)}{traceback.format_exc()}")

