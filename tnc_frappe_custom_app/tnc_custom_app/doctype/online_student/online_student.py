# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

################### Below code give the Actual count of OnlineStudent Master Data to the OnlineStudent Exam based on their ID #################################################################

class OnlineStudent(Document):
    # def validate(self):
    # def before_insert(self):
    #     self.check_duplicate_mobile()

    def check_duplicate_mobile(self):
        if self.mobile:
            # Check if any other online_student has the same mobile number
            existing_online_student = frappe.db.exists("Online Student", {"mobile": self.mobile, "name": ["!=", self.name]})
            
            if existing_online_student:
                # Raise an error if a duplicate is found
                frappe.throw(f"Mobile number {self.mobile} is already registered with another online_student.")


######################################## Send bulk whatsapp results sharing to Students ####################################################################



import frappe
import requests

@frappe.whitelist()
def send_bulk_student_results_to_students():
    # Hardcoded test mobile numbers (Uncomment the next line to send only to test numbers)
    # test_mobiles = ["7893913248", "9513777002"]

    # Fetch all students
    students = frappe.get_all('Online Student', fields=['mobile', 'student_name', 'name'])

    # Uncomment the next line to restrict sending to test mobiles only
    # students = [s for s in students if s.mobile in test_mobiles]

    wa_config = frappe.get_doc('WhatsApp Message Configuration', 'WA-Config-01')
    api_url = f"{wa_config.wa_server}/send"
    headers = {
        "apikey": wa_config.get_password('api_key'),
        "Content-Type": "application/json"
    }
    
    count = 0
    for student in students:
        if count >= 2:  # Limit to 5 for testing  ## comment before to production
            break                                 ## comment before to production
        if not student.mobile:  # Skip if mobile is missing
            continue

        base_url = frappe.utils.get_url()
        docname = student.name
        mobile = student.mobile

        print(f"Processing Student: {student.student_name}, Mobile: {mobile}, Doc: {docname}")
        count += 1
        print(f"Total processed students: {count}")

        wa_message = f"""Dear {student.student_name},

Please Check your Results Summary

Best regards,
TNC Administration"""

        payload = {
            "userid": wa_config.user_id,
            "msg": wa_message,
            "wabaNumber": wa_config.waba_number,
            "output": "json",
            "mobile": "919513777002",
            # "mobile": f"91{mobile}",
            "sendMethod": "quick",
            "msgType": "media",
            
            ### Uncomment below code before production
            # "mediaUrl" : f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Online Student&name={student.name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en",
            "mediaUrl": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",  # Placeholder PDF
            "mediaType": "document",
            "templateName": "student_sharing_results_template"
        }

        # Uncomment to enable actual sending
        try:
            response = requests.post(api_url, json=payload, headers=headers)
            # print("RESPONSEEEEEEEEEEEEEEEEEEWWWWWWWWWWWWWWW", response.json())
            response.raise_for_status()
            # pass
        except requests.exceptions.RequestException as e:
            frappe.log_error(f"WhatsApp Message Failed: {str(e)}", "WhatsApp API Error")

    return {"status": "Success", "message": f"Results sent to {count} students"}

