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
    # file_url = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en"
    # file_url = f"http://3.111.226.95/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/{student_name}.pdf"
    file_url = "http://3.111.226.95/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name=TNC-Student-00072286&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/TNC-Student-00072286.pdf"
    text_message = f"Dear {student_name},Check your results"

    # Construct API URL
    api_url = f"https://wts.vision360solutions.co.in/api/sendFileWithCaption?token={instance_id}&phone={mobile_number}&link={file_url}&message={text_message}"    
    print(mobile_number)
    print("Hello world!")
    print(name)
    
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


