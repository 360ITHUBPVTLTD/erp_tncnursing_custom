# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

import random
import string



################### Below code give the Actual count of OnlineStudent Master Data to the OnlineStudent Exam based on their ID #################################################################

class OnlineStudent(Document):
    # def validate(self):
    # def before_insert(self):
    #     self.check_duplicate_mobile()
    pass
    # def check_duplicate_mobile(self):
    #     if self.mobile:
    #         # Check if any other online_student has the same mobile number
    #         existing_online_student = frappe.db.exists("Online Student", {"mobile": self.mobile, "name": ["!=", self.name]})
            
    #         if existing_online_student:
    #             # Raise an error if a duplicate is found
    #             frappe.throw(f"Mobile number {self.mobile} is already registered with another online_student.")


######################################## Send bulk whatsapp results sharing to Students ####################################################################



import frappe
import requests

@frappe.whitelist()
def send_bulk_student_results_to_students():
    # Hardcoded test mobile numbers (Uncomment the next line to send only to test numbers)
    test_mobiles = ["7893913248", "9513777001","7795194181"]

    # Fetch all students
    students = frappe.get_all('Online Student', fields=['mobile', 'student_name', 'name'])

    # Uncomment the next line to restrict sending to test mobiles only
    students = [s for s in students if s.mobile in test_mobiles]

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
            # "mobile": "919513777002",
            "mobile": f"91{mobile}",
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



############################### Selected Students only will receive the WhatsApp Messages ##########################


import frappe

@frappe.whitelist()
def get_online_students():
    students = frappe.get_all(
        "Online Student",
        fields=["name", "student_name", "mobile"],
        limit_page_length=100
    )
    return students
########################################################################
import frappe
import requests

import frappe
import json

@frappe.whitelist()
def send_results_to_selected_students(student_ids):
    print("Raw student_ids from client:", student_ids)
    
    # Ensure student_ids is a list
    if isinstance(student_ids, str):
        try:
            student_ids = json.loads(student_ids)  # Convert JSON string to list
        except json.JSONDecodeError as e:
            frappe.throw("Invalid JSON format")

    print("Processed Student IDs:", student_ids, type(student_ids))

    if not student_ids or not isinstance(student_ids, list):
        frappe.throw("Invalid or empty student list.")

    # Fetch student details
    students = frappe.get_all(
        'Online Student',
        filters=[["name", "in", student_ids]],
        fields=['mobile', 'student_name', 'name']
    )

    print("Fetched Students:", students)

    if not students:
        frappe.throw("No matching students found.")

    try:
        wa_config = frappe.get_doc('WhatsApp Message Configuration', 'WA-Config-01')
        api_url = f"{wa_config.wa_server}/send"
        headers = {
            "apikey": wa_config.get_password('api_key'),
            "Content-Type": "application/json"
        }
        base_url = frappe.utils.get_url()

        count = 0  # Initialize count
        for student in students:
            if not student.mobile:
                frappe.log_error(f"Missing mobile number for {student.student_name}", "WhatsApp Message Skipped")
                continue  # Skip students without a mobile number

            docname = student.name
            mobile = student.mobile
            print(f"Processing Student: {student.student_name}, Mobile: {mobile}, Doc: {docname}")

            wa_message = f"""Dear {student.student_name},

Please Check your Results Summary

Best regards,
TNC Administration"""

            payload = {
                "userid": wa_config.user_id,
                "msg": wa_message,
                "wabaNumber": wa_config.waba_number,
                "output": "json",
                "mobile": f"91{mobile}",
                "sendMethod": "quick",
                "msgType": "media",
                # Replace this URL in production with the actual result PDF link
                # "mediaUrl": f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Online Student&name={student.name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en",
                "mediaUrl" : "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                "mediaType": "document",
                "templateName": "student_sharing_results_template"
            }

            # Sending WhatsApp Message
            try:
                response = requests.post(api_url, json=payload, headers=headers)
                # print("sssssssssswdedgfefgeggggggggggggggggggggggggggggggg",response)
                response.raise_for_status()
                # print("WA RESPONSE",response.json())
                count += 1  # Increment success count
                # print(f"Message sent successfully to {mobile}")

            except requests.exceptions.RequestException as e:
                frappe.log_error(f"WhatsApp Message Failed for {student.student_name}: {str(e)}", "WhatsApp API Error")

        return {"status": "Success", "message": f"Results sent to {count} students"}

    except Exception as e:
        frappe.log_error(f"Unexpected error: {str(e)}", "Send WhatsApp Results Error")
        return {"status": "Failed", "message": "An unexpected error occurred. Check logs."}
    




@frappe.whitelist()
def bulk_generate_encryption_keys():
    """Bulk update encryption_key field for all Online Student documents."""
    # Fetch all documents from Online Student doctype
    students = frappe.get_all("Online Student", fields=["name"])
    
    updated_records = []
    for student in students:
        # Generate a new random encryption key
        new_key = generate_random_string(14)
        # Update the encryption_key field for this document
        frappe.db.set_value("Online Student", student.name, "encryption_key", new_key)
        updated_records.append((student.name, new_key))
    
    frappe.db.commit()  # Commit after bulk updating all records
    
    # Print feedback for each updated record
    for record in updated_records:
        print(f"Updated {record[0]} with encryption_key: {record[1]}")
    
    return f"Updated {len(updated_records)} documents."



def generate_random_string(length=14):
    """Generates a random string of given length containing upper case,
    lower case letters and digits."""
    characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return ''.join(random.choices(characters, k=length))
