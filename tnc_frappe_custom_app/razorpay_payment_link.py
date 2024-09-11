
############################# Below code is generating a payment link and storing it into  a another doctype "PaymentLink Log" #################################################################

# import frappe
# import requests
# import base64
# from frappe import _

# @frappe.whitelist()
# def generate_payment_link(student_id, amount, description):
#     try:
#         # Check if a payment link with status "Created" or "Paid" already exists for this student
#         existing_link = frappe.get_all('Razorpay Payment Links', filters={
#             'student_id': student_id,
#             'status': ['in', ['Created', 'Paid']]
#         })
        
#         if existing_link:
#             frappe.throw(_("A payment link already exists for this student. Please check the Razorpay Payment Links doctype."))

#         # Fetch API settings from Admin Settings
#         admin_settings = frappe.get_doc('Admin Settings')
#         razorpay_base_url = admin_settings.razorpay_base_url
#         razorpay_key_id = admin_settings.razorpay_api_key
#         razorpay_key_secret = admin_settings.get_password('razorpay_secret')
#         razorpay_api_url = razorpay_base_url + "payment_links"
        
#         # Encode API key and secret in base64
#         auth_string = f"{razorpay_key_id}:{razorpay_key_secret}"
#         base64_auth_string = base64.b64encode(auth_string.encode()).decode()
        
#         headers = {
#             "Authorization": f"Basic {base64_auth_string}",
#             "Content-Type": "application/json"
#         }
        
#         data = {
#             "amount": int(amount) * 100,  # Razorpay expects amount in paise
#             "currency": "INR",
#             "description": description,
#             "callback_url": "https://www.youtube.com/"
#         }
        
#         response = requests.post(razorpay_api_url, headers=headers, json=data)
#         response_data = response.json()
        
#         if response.status_code == 200:
#             short_url = response_data.get("short_url")
#             link_id = response_data.get("id")

#             # Store payment link details in Razorpay Payment Links doctype
#             student = frappe.get_doc('Student', student_id)
#             payment_link_doc = frappe.new_doc('Razorpay Payment Links')
#             payment_link_doc.student_id = student_id
#             payment_link_doc.student_name = student.student_name
#             # payment_link_doc.mobile_number = student.mobile_number
#             payment_link_doc.payment_link = short_url
#             payment_link_doc.link_id = link_id
#             payment_link_doc.status = 'Created'
#             payment_link_doc.insert()

#             return {
#                 "short_url": short_url
#             }
#         else:
#             frappe.throw(_("Failed to create payment link: {0}".format(response_data.get("error", {}).get("description", "Unknown error"))))
    
#     except Exception as e:
#         frappe.throw(_("An error occurred: {0}".format(str(e))))


######################### Below code is after generating the payment link it send the payment link through whatsapp #########################

import frappe
import requests
import base64
from frappe import _

@frappe.whitelist()
def generate_payment_link(student_id, amount, description):
    try:
        # Check if a payment link with status "Created" or "Paid" already exists for this student
        existing_link = frappe.get_all('Razorpay Payment Links', filters={
            'student_id': student_id,
            'status': ['in', ['Created', 'Paid']]
        })
        
        if existing_link:
            frappe.throw(_("A payment link already exists for this student. Please check the Razorpay Payment Links doctype."))

        # Fetch API settings from Admin Settings
        admin_settings = frappe.get_doc('Admin Settings')
        razorpay_base_url = admin_settings.razorpay_base_url
        razorpay_key_id = admin_settings.razorpay_api_key
        razorpay_key_secret = admin_settings.get_password('razorpay_secret')
        razorpay_api_url = razorpay_base_url + "payment_links"
        
        # Encode API key and secret in base64
        auth_string = f"{razorpay_key_id}:{razorpay_key_secret}"
        base64_auth_string = base64.b64encode(auth_string.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {base64_auth_string}",
            "Content-Type": "application/json"
        }
        
        data = {
            "amount": int(amount) * 100,  # Razorpay expects amount in paise
            "currency": "INR",
            "description": description,
            "callback_url": "https://www.youtube.com/"  # Replace with your actual callback URL
        }
        
        response = requests.post(razorpay_api_url, headers=headers, json=data)
        response_data = response.json()
        
        if response.status_code == 200:
            short_url = response_data.get("short_url")
            link_id = response_data.get("id")

            # Store payment link details in Razorpay Payment Links doctype
            student = frappe.get_doc('Student', student_id)
            payment_link_doc = frappe.new_doc('Razorpay Payment Links')
            payment_link_doc.student_id = student_id
            payment_link_doc.student_name = student.student_name
            # payment_link_doc.mobile_number = student.mobile_number
            payment_link_doc.payment_link = short_url
            payment_link_doc.link_id = link_id
            payment_link_doc.status = 'Created'
            payment_link_doc.insert()

            # Send WhatsApp message
            send_whatsapp_message(student.mobile, short_url)

            return {
                "short_url": short_url
            }
        else:
            frappe.throw(_("Failed to create payment link: {0}".format(response_data.get("error", {}).get("description", "Unknown error"))))
    
    except Exception as e:
        frappe.throw(_("An error occurred: {0}".format(str(e))))


def send_whatsapp_message(mobile_number, payment_link):
    # Fetch instance ID from Admin Settings
    admin_settings = frappe.get_doc('Admin Settings')
    instance_id = admin_settings.instance_id

    # Prepend +91 to the mobile number if not already present
    if not mobile_number.startswith("91"):
        mobile_number = "91" + mobile_number

    # Construct the WhatsApp API URL
    text_message = f"Here is your payment link: {payment_link}"
    api_url = f"https://wts.vision360solutions.co.in/api/sendText?token={instance_id}&phone={mobile_number}&message={text_message}"
    
    try:
        # Make the API request
        response = requests.get(api_url)
        
        # Log success or failure
        if response.status_code == 200:
            frappe.msgprint(("WhatsApp message sent successfully."))
        else:
            frappe.log_error("Failed to send WhatsApp message", "WhatsApp Message Error")
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "WhatsApp Message Sending Failed")


################ Cancel the Payment Link in the Payment Link Log doctype #################################
 
import frappe
import requests
import base64
from frappe import _

@frappe.whitelist()
def cancel_payment_link(link_id):
    try:
        # Fetch API settings from Admin Settings
        admin_settings = frappe.get_doc('Admin Settings')
        razorpay_base_url = admin_settings.razorpay_base_url
        razorpay_key_id = admin_settings.razorpay_api_key
        razorpay_key_secret = admin_settings.get_password('razorpay_secret')
        razorpay_cancel_url = f"{razorpay_base_url}payment_links/{link_id}/cancel"
        
        # Encode API key and secret in base64
        auth_string = f"{razorpay_key_id}:{razorpay_key_secret}"
        base64_auth_string = base64.b64encode(auth_string.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {base64_auth_string}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(razorpay_cancel_url, headers=headers)
        
        if response.status_code == 200:
            # Update the status in Razorpay Payment Links doctype to "Cancelled"
            payment_link_doc = frappe.get_doc('Razorpay Payment Links', {'link_id': link_id})
            payment_link_doc.status = 'Cancelled'
            payment_link_doc.save()

            # Clear the payment_link field in the associated Student doctype
            student_doc = frappe.get_doc('Student', payment_link_doc.student_id)
            student_doc.payment_link = None
            student_doc.save()

            return 'success'
        else:
            frappe.throw(_("Failed to cancel payment link: {0}".format(response.json().get("error", {}).get("description", "Unknown error"))))
    
    except Exception as e:
        frappe.throw(_("An error occurred: {0}".format(str(e))))





#################### Below is the Sync Button in the Razorpay Payment Link #################################



import requests
from requests.auth import HTTPBasicAuth
import frappe

@frappe.whitelist()
def sync_payment_links():
    # Retrieve Razorpay credentials from Admin Settings
    admin_settings = frappe.get_doc('Admin Settings')
    razorpay_base_url = admin_settings.razorpay_base_url
    razorpay_key_id = admin_settings.razorpay_api_key
    razorpay_key_secret = admin_settings.get_password('razorpay_secret')
    
    # Get all documents of type 'Razorpay Payment Links'
    payment_links = frappe.get_all('Razorpay Payment Links', fields=['name', 'link_id'])
    
    for link in payment_links:
        plink_id = link['link_id']
        
        # Endpoint URL
        url = f'{razorpay_base_url}payment_links/{plink_id}'
        
        # Make the request
        response = requests.get(url, auth=HTTPBasicAuth(razorpay_key_id, razorpay_key_secret))
        
        if response.status_code == 200:
            data = response.json()
            amount_paid = data.get('amount_paid', 0)
            status = 'Paid' if amount_paid > 0 else 'Created'
            
            # Update the status field in the document
            frappe.db.set_value('Razorpay Payment Links', link['name'], 'status', status)
        else:
            frappe.log_error(f"Failed to fetch details for link_id: {plink_id}", "Razorpay Sync Error")

    frappe.db.commit()
