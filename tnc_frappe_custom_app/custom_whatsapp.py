############################### Below code is sending the whatsapp message with particular subject only ###################################
import frappe
import requests
from frappe.utils import now

@frappe.whitelist()
def send_whatsapp_pdf_message(name, mobile_number, student_name, message):
    # Fetch the instance_id from the "Admin Settings" doctype
    base_url = frappe.utils.get_url()
    admin_settings = frappe.get_doc('Admin Settings')
    instance_id = admin_settings.instance_id

    # Construct the API URL
    try:
        # Make the API request
        base_url = frappe.utils.get_url()
        # response = requests.get(api_url)
        # link = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/{student_name}pdf"
        link = f"{base_url}method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/TNC REPORT CARD.pdf"
        # link = "https://online.lsaoffice.com/api/method/frappe.utils.print_format.download_pdf?doctype=Sales%20Order&name=SAL-ORD-2023-00262&format=Sales%20Order%20Format&no_letterhead=0&letterhead=LSA&settings=%7B%7D&_lang=en/Invoice.pdf"

        url = "https://wts.vision360solutions.co.in/api/sendFileWithCaption"
        params_1 = {
            "token": instance_id,
            "phone": f"91{mobile_number}",
            "message": message,
            "link": link
        } 
        response = requests.post(url, params=params_1)
        response_data = response.json()  # Parse the JSON response
        # print(response_data)

        # Check for success based on the response data
        if response_data.get('status') == 'success':
            message_status = "Success"
            message_ids = response_data.get('data', {}).get('messageIDs', [])
            frappe.logger().info(f"WhatsApp message sent successfully to {mobile_number}")
        else:
            message_status = "Failed"
            message_ids = []
            frappe.logger().error(f"Failed to send WhatsApp message to {mobile_number}. Response: {response_data}")
    except Exception as e:
        frappe.logger().error(f"Error sending WhatsApp message to {mobile_number}: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "WhatsApp Message Sending Failed")
        message_status = "Failed"
        message_ids = []
    # Log the message in WhatsApp Message Log doctype
    try:
        frappe.get_doc({
            'doctype': 'WhatsApp Message Log',
            'sender': frappe.session.user,   # Sender is the logged-in user
            'send_date': now(),              # Send date is the current time
            'message_type': 'Custom',        # Set custom message type
            'message': message,              # Message from the client script
            'student_id': name,              # Student ID passed from client
            'status': message_status,        # Log the status (Success/Failed)
            'message_id': ', '.join(message_ids)  # Join message IDs if any
        }).insert(ignore_permissions=True)
        
        frappe.logger().info(f"WhatsApp message log created for student {name} with status {message_status}")
    except Exception as log_error:
        frappe.log_error(frappe.get_traceback(), "Failed to create WhatsApp Message Log")

    # return {'status': message_status}
    return {"status": 'success', "msg": "WhatsApp message sent successfully!"}