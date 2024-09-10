############################### Below code is sending the whatsapp message with particular subject only ###################################

import frappe
import requests

@frappe.whitelist()
def send_whatsapp_pdf_message(name, mobile_number, student_name):
    # Fetch the instance_id from the "Admin Settings" doctype
    print(name)
    base_url = frappe.utils.get_url()
    print(base_url)
    admin_settings = frappe.get_doc('Admin Settings')
    instance_id = admin_settings.instance_id
    

    # Prepend +91 to the mobile number if not already present
    if not mobile_number.startswith("91"):
        mobile_number = "91" + mobile_number

    # API details
    # file_url = "https://tourism.gov.in/sites/default/files/2019-04/dummy-pdf_2.pdf"
    file_url = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/{student_name}.pdf"
    # file_url = f"http://3.111.226.95/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/{student_name}.pdf"
#     file_url = "http://3.111.226.95/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name=TNC-Student-00072286&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/TNC-Student-00072286.pdf"
    text_message = f"Dear {student_name},Check your results"

    # Construct API URL
    api_url = f"https://wts.vision360solutions.co.in/api/sendFileWithCaption?token={instance_id}&phone={mobile_number}&link={file_url}&message={text_message}"    
#     print(mobile_number)
#     print("Hello world!")
#     print(name)
#     # Prepend +91 to the mobile number if not already present
#     if not mobile_number.startswith("91"):
#         mobile_number = "91" + mobile_number


    # API details
#     file_url = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/{student_name}.pdf"


    
#     # file_url = f"http://3.111.226.95/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/{student_name}.pdf"
#     text_message = f"Dear {student_name},Check your results"

#     # Construct API URL
#     api_url = f"https://wts.vision360solutions.co.in/api/sendFileWithCaption?token={instance_id}&phone={mobile_number}&link={file_url}&message={text_message}"    
#     print(mobile_number)
#     print("Hello world!")
#     print(name)

    
    try:
        # Make the API request
        response = requests.get(api_url)
        print(response.json())
        
        # Check for success status
        if response.status_code == 200:
            return "Success"
        else:
            return "Failed"
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "WhatsApp Message Sending Failed")
        return "Failed"








#########################################################################
# import frappe

# @frappe.whitelist()
# def fetch_student_mobiles():
#     # Fetch the students and their mobile numbers
#     students = frappe.get_all('Student', fields=['name', 'mobile'])
    
#     # Prepare the details to return and log to the console
#     details = ""
#     for student in students:
#         line = f"Student: {student.name}, Mobile: {student.mobile}"
#         details += line + "<br>"
#         print(student.mobile)
        
#         # Log each student's mobile number to the server console
#         frappe.logger().info(line)
    
#     return {'message': details}


import frappe
import requests

@frappe.whitelist()
def send_bulk_whatsapp_messages():
    # Fetch the admin settings to get the instance ID
    admin_settings = frappe.get_doc('Admin Settings')
    instance_id = admin_settings.instance_id
    
    # Fetch the students and their mobile numbers
    students = frappe.get_all('Student', fields=['name', 'mobile'])
    text_message = "Hello Student!"
    
    # Loop through each student to prepare and send the message
    for student in students:
        mobile = student.mobile
        
        # Check if the mobile number starts with country code 91
        if not mobile.startswith('91'):
            # Add country code 91 if it's missing
            mobile = '91' + mobile
        
        # Generate the PDF URL dynamically
        # file_url = f"http://test.local:8010/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={student.name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en"
        file_url = "https://tourism.gov.in/sites/default/files/2019-04/dummy-pdf_2.pdf"
        
        # WhatsApp API endpoint and payload
        api_url = f"https://wts.vision360solutions.co.in/api/sendFiles?token={instance_id}&phone={mobile}&link={file_url}&message={text_message}"
        
        # Send the request to the WhatsApp API
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                frappe.logger().info(f"Message sent to {mobile} successfully.")
            else:
                frappe.logger().error(f"Failed to send message to {mobile}. Status code: {response.status_code}")
        except Exception as e:
            frappe.logger().error(f"Error sending message to {mobile}: {str(e)}")

    return {'message': 'Bulk WhatsApp messages sent successfully!'}
