############################### Below code is sending the whatsapp message with particular subject only ###################################
import frappe
import requests
from frappe.utils import now

@frappe.whitelist()
def send_whatsapp_pdf_message(name, mobile_number, student_name):
    # Fetch the instance_id from the "Admin Settings" doctype
    base_url = frappe.utils.get_url()
    admin_settings = frappe.get_doc('Admin Settings')
    instance_id = admin_settings.instance_id
    message = (
        'Assessment Report by TNC Experts\n'
        'You are doing very good 👍\n\n'
        'Your score is very fantastic. According to TNC experts, you will achieve a good rank in NORCET Exam.\n\n'
        '🎯📚 Just continue your hard work and study, maximum question practice, and try to control minus marking.\n\n'
        '🎖️ We hope strongly that you are our next interviewer on our TNC YouTube channel.\n\n'
        '👍 Be confident and be consistent.\n\n'
        '💐 All the Best and Best wishes.\n\n'
        'आपकी सफलता वाली कॉल का इंतजार रहेगा।\n\n'
        'Thanks\n\n'
        'AIIMS 20+ Expert TNC TEAM\n\n'
        'If you need any help and assistance, please message us on the official number:\n'
        '7484999051\n'
        'TNC Nursing'
    )
    # Construct the API URL
    try:
        # Make the API request
        base_url = frappe.utils.get_url()
        # response = requests.get(api_url)
       # link = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/TNC_REPORT_CARD.pdf"
        link = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/TNC_REPORT_CARD.pdf"
        # link = 'https://tourism.gov.in/sites/default/files/2019-04/dummy-pdf_2.pdf'
        # print(link)
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

    return {'status': message_status}
    # return {"status": 'success', "msg": "WhatsApp message sent successfully!"}


######### Validating the button based on the 

# @frappe.whitelist()
# def valiadting_user_for_bulk_wa_msg():
#     user = frappe.session.user
#     if user=="Administrator":
#         return {"status": True, "msg": "User has the required role."}
    
#     admin_setting_doc = frappe.get_doc("Admin Settings")
#     auhenticated_users=[]
#     for i in admin_setting_doc.whatsapp_access:
#         auhenticated_users.append(i.user)
    
#     if user not in auhenticated_users :
#         return {"status": False, "msg": "User does not have the required role to send Bulk WhatsApp messages."}
#     return {"status": True, "msg": "User has the required role."}


###########################List view Button in Student doctype #################################################





