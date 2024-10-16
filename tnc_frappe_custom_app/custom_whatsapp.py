##################Below code is sending the whatsapp message with particular subject only (Sending PDF Dynamically) ###################################
import frappe
import requests
from frappe.utils import now

@frappe.whitelist()
def send_whatsapp_pdf_message(name, mobile_number, student_name, message):
    # Fetch the instance_id from the "Admin Settings" doctype
    base_url = frappe.utils.get_url()
    admin_settings = frappe.get_doc('Admin Settings')
    instance_id = admin_settings.instance_id

    # quota, connected_number = check_credits_and_connection(instance_id) 

    # if not connected_number:
    #     frappe.throw("Your instance is not connected.")
    
    # # Check if there are sufficient credits
    # if quota <= 0:
    #     frappe.throw("Insufficient credits to send the message.")
        
    # Step 1: Check if credits and connection are valid
    quota, connected_number = check_credits_and_connection(instance_id)
    
    if quota > 0:

    # Construct the API URL
        try:
            # Make the API request
            base_url = frappe.utils.get_url()
            # response = requests.get(api_url)
        # link = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/TNC_REPORT_CARD.pdf"
            # link = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/TncResult.pdf"
            link = 'https://tourism.gov.in/sites/default/files/2019-04/dummy-pdf_2.pdf'
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
    else:# Throw error if credits are 0
        frappe.throw("No credits available to send WhatsApp message.")
        return {'status': 'Failed', 'msg': 'No credits available'}

    




# ###################### Below code is to send the message to students of the Government Results ##########################

# @frappe.whitelist()
# def send_whatsapp_custom_message(name, mobile_number, student_name, message):
#     # Fetch the instance_id from the "Admin Settings" doctype
#     base_url = frappe.utils.get_url()
#     admin_settings = frappe.get_doc('Admin Settings')
#     instance_id = admin_settings.instance_id
#     # Construct the API URL
#     try:
#         # Make the API request
#         base_url = frappe.utils.get_url()
#         # response = requests.get(api_url)
#        # link = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/TNC_REPORT_CARD.pdf"
#         # link = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/TncResult.pdf"
#         # link = 'https://tourism.gov.in/sites/default/files/2019-04/dummy-pdf_2.pdf'
#         # print(link)
#         url = "https://wts.vision360solutions.co.in/api/sendText"
#         params_1 = {
#             "token": instance_id,
#             "phone": f"91{mobile_number}",
#             "message": message,
#             # "link": link
#         } 
#         response = requests.post(url, params=params_1)
#         response_data = response.json()  # Parse the JSON response
#         # print(response_data)

#         # Check for success based on the response data
#         if response_data.get('status') == 'success':
#             message_status = "Success"
#             message_ids = response_data.get('data', {}).get('messageIDs', [])
#             frappe.logger().info(f"WhatsApp message sent successfully to {mobile_number}")
#         else:
#             message_status = "Failed"
#             message_ids = []
#             frappe.logger().error(f"Failed to send WhatsApp message to {mobile_number}. Response: {response_data}")
#     except Exception as e:
#         frappe.logger().error(f"Error sending WhatsApp message to {mobile_number}: {str(e)}")
#         frappe.log_error(frappe.get_traceback(), "WhatsApp Message Sending Failed")
#         message_status = "Failed"
#         message_ids = []
#     # Log the message in WhatsApp Message Log doctype
#     try:
#         frappe.get_doc({
#             'doctype': 'WhatsApp Message Log',
#             'sender': frappe.session.user,   # Sender is the logged-in user
#             'send_date': now(),              # Send date is the current time
#             'message_type': 'Custom',        # Set custom message type
#             'message': message,              # Message from the client script
#             'student_id': name,              # Student ID passed from client
#             'status': message_status,        # Log the status (Success/Failed)
#             'message_id': ', '.join(message_ids)  # Join message IDs if any
#         }).insert(ignore_permissions=True)
        
#         frappe.logger().info(f"WhatsApp message log created for student {name} with status {message_status}")
#     except Exception as log_error:
#         frappe.log_error(frappe.get_traceback(), "Failed to create WhatsApp Message Log")

#     return {'status': message_status}
#     # return {"status": 'success', "msg": "WhatsApp message sent successfully!"}



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


########################################################################################################################################


######################### Below code is the query to get the Choose Template Button #################################

import frappe

@frappe.whitelist()  # Makes the function callable from the client side
def get_template_options(doctype, txt, searchfield, start, page_len, filters):
    """
    This function returns a list of WhatsApp Templates based on the user's input.
    The `txt` argument contains the user's input text, and the query fetches templates that match this text.
    """
    # SQL query to fetch matching WhatsApp templates from the database
    template_list = frappe.db.sql("""
        SELECT name FROM `tabWhatsApp Templates`
        WHERE name LIKE %s
        ORDER BY name ASC
        LIMIT %s, %s
    """, ("%%%s%%" % txt, start, page_len))
    
    template_dict = frappe.get_all("WhatsApp Templates", 
                                #    filters={},
                                   fields=["name","template_name","attach_image"])
    template_list = [(template.name,template.template_name,template.attach_image) for template in template_dict]
    return template_list



############# Below code is to fetch the message using the template ID and it return the message to the prompt #############


@frappe.whitelist()
def get_template_message(template_id):
    # print(template_id)
    # Fetch the message field from WhatsApp Templates doctype using the template ID
    template = frappe.get_doc('WhatsApp Templates', {'template_name': template_id})
    
    # Return the message field
    if template:
        return template.message, template.attach_image
    return ''

################## Below code is to send the WhatsApp message whether it is File,Image or Normal Text also #########################



# import os
# from frappe.utils.file_manager import save_file, get_files_path

# @frappe.whitelist()
# def send_whatsapp_Image_message(name, mobile_number, student_name, message, image=None):
    
#     # Fetch the instance_id from the "Admin Settings" doctype
#     base_url = frappe.utils.get_url()
#     admin_settings = frappe.get_doc('Admin Settings')
#     instance_id = admin_settings.instance_id

#     # If the image is provided, handle the image sending process
#     if image:
#         # Check if the file already exists in the File Manager
#         existing_file = frappe.db.exists("File", {"file_url": image})

#         if existing_file:
#             saved_file = frappe.get_doc("File", existing_file)  # Retrieve the existing file
#         else:
#             # Save the image to Frappe's file system
#             saved_file = frappe.get_doc({
#                 "doctype": "File",
#                 "file_name": os.path.basename(image),
#                 "file_url": image,
#                 "attached_to_doctype": "Student",  # Adjust this if needed
#                 "attached_to_name": name,          # Adjust this if needed
#                 "is_private": 0
#             })
#             saved_file.save()

#         # Get the absolute path of the saved file
#         file_path = os.path.join(get_files_path(), os.path.basename(saved_file.file_url))

#         # Check if the file exists at the file_path
#         if not os.path.exists(file_path):
#             frappe.throw(('File not found at path {0}. Make sure the file is public.').format(file_path))


#         # Send the image via WhatsApp API
#         api_url = 'https://wts.vision360solutions.co.in/api/sendFileWithCaption'
#         params = {
#             'token': instance_id,  # Use your API token from the "Admin Settings" doctype
#             'phone': f'91{mobile_number}',  # Mobile number prefixed with country code
#             'message': message              # Message content
#         }

#         # Open the saved file and pass it as a file parameter
#         with open(file_path, 'rb') as image_file:
#             files = {
#                 'file': image_file
#             }

#             # Send the request to the WhatsApp API
#             response = requests.post(api_url, params=params, files=files)
#             response_data = response.json()  # Parse the JSON response
#     else:
#         # Call the fallback function to send a text-only message if no image is provided
#         return send_whatsapp_Template_message(name, mobile_number, student_name, message)

#     # Check for success based on the response data
#     if response_data.get('status') == 'success':
#         # Extract the messageID(s) from the response
#         message_ids = response_data.get('data', {}).get('messageIDs', [])
#         message_status = 'Success'

#         # Log the message in WhatsApp Message Log doctype
#         frappe.get_doc({
#             'doctype': 'WhatsApp Message Log',
#             'sender': frappe.session.user,            # Sender is the logged-in user
#             'send_date': frappe.utils.now(),          # Send date is the current time
#             'message_type': 'Message with File/Image',               # Set custom message type
#             'message': message,                       # Message from the client script
#             'student_id': name,                       # Student ID passed from client
#             'status': message_status,                 # Log the status (Success/Failed)
#             'message_id': ', '.join(message_ids)      # Join message IDs into a string (if multiple IDs)
#         }).insert(ignore_permissions=True)

#         frappe.logger().info(f"WhatsApp message sent successfully to {mobile_number} with messageID: {', '.join(message_ids)}")
#     else:
#         message_status = 'Failed'
#         message_ids = []
#         frappe.logger().error(f"Failed to send WhatsApp message to {mobile_number}. Response: {response_data}")

#     # Return the status of the message
#     return {'status': message_status}

############################## Below code is only sending the Template Message without Image/File #################################################################
# @frappe.whitelist()
# def send_whatsapp_Template_message(name, mobile_number, student_name, message):
#     # Fetch the instance_id from the "Admin Settings" doctype
#     base_url = frappe.utils.get_url()
#     admin_settings = frappe.get_doc('Admin Settings')
#     instance_id = admin_settings.instance_id
#     # Construct the API URL
#     try:
#         # Make the API request
#         base_url = frappe.utils.get_url()
#         url = "https://wts.vision360solutions.co.in/api/sendText"
#         params_1 = {
#             "token": instance_id,
#             "phone": f"91{mobile_number}",
#             "message": message,
#             # "link": link
#         } 
#         response = requests.post(url, params=params_1)
#         response_data = response.json()  # Parse the JSON response
#         # print(response_data)

#         # Check for success based on the response data
#         if response_data.get('status') == 'success':
#             message_status = "Success"
#             message_ids = response_data.get('data', {}).get('messageIDs', [])
#             frappe.logger().info(f"WhatsApp message sent successfully to {mobile_number}")
#         else:
#             message_status = "Failed"
#             message_ids = []
#             frappe.logger().error(f"Failed to send WhatsApp message to {mobile_number}. Response: {response_data}")
#     except Exception as e:
#         frappe.logger().error(f"Error sending WhatsApp message to {mobile_number}: {str(e)}")
#         frappe.log_error(frappe.get_traceback(), "WhatsApp Message Sending Failed")
#         message_status = "Failed"
#         message_ids = []
#     # Log the message in WhatsApp Message Log doctype
#     try:
#         frappe.get_doc({
#             'doctype': 'WhatsApp Message Log',
#             'sender': frappe.session.user,   # Sender is the logged-in user
#             'send_date': now(),              # Send date is the current time
#             'message_type': 'Template',        # Set custom message type
#             'message': message,              # Message from the client script
#             'student_id': name,              # Student ID passed from client
#             'status': message_status,        # Log the status (Success/Failed)
#             'message_id': ', '.join(message_ids)  # Join message IDs if any
#         }).insert(ignore_permissions=True)
        
#         frappe.logger().info(f"WhatsApp message log created for student {name} with status {message_status}")
#     except Exception as log_error:
#         frappe.log_error(frappe.get_traceback(), "Failed to create WhatsApp Message Log")

#     return {'status': message_status}
#     # return {"status": 'success', "msg": "WhatsApp message sent successfully!"}








####################### Below code is validation to check quota and connection status then only the pdf/image attachment will go ######


import os
import requests
import frappe
from frappe.utils.file_manager import save_file, get_files_path

# Assuming check_credits_and_connection() is defined elsewhere
def check_credits_and_connection(instance_id):
    # API call to check the balance and connection status
    url = f"https://wts.vision360solutions.co.in/api/checkBal?token={instance_id}"

    try:
        response = requests.get(url)
        response_data = response.json()

        if response.status_code == 200 and response_data.get('status') == 'success':
            # Extract the necessary fields
            quota = response_data.get('data', {}).get('quota', 0)
            connected_number = response_data.get('data', {}).get('connectedNumeber', '')

            # Check if connected number is empty or not
            if not connected_number:
                frappe.throw("Your instance is not connected.")

            # Return both quota and connected number for further checks
            return quota, connected_number

        else:
            frappe.logger().error(f"Failed to check credits. Response: {response_data}")
            return 0, ''  # Default values if the request fails
    except Exception as e:
        frappe.logger().error(f"Error checking credits: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Credit Check Failed")
        return 0, ''  # Return 0 credits and empty connection on failure

@frappe.whitelist()
def send_whatsapp_Image_message(name, mobile_number, student_name, message, image=None):
    # Fetch the instance_id from the "Admin Settings" doctype
    base_url = frappe.utils.get_url()
    admin_settings = frappe.get_doc('Admin Settings')
    instance_id = admin_settings.instance_id

    # Step 1: Check if credits and connection are valid
    quota, connected_number = check_credits_and_connection(instance_id)

    if quota <= 0:
        frappe.throw("No credits available to send WhatsApp message.")
    
    # If the image is provided, handle the image sending process
    if image:
        # Check if the file already exists in the File Manager
        existing_file = frappe.db.exists("File", {"file_url": image})

        if existing_file:
            saved_file = frappe.get_doc("File", existing_file)  # Retrieve the existing file
        else:
            # Save the image to Frappe's file system
            saved_file = frappe.get_doc({
                "doctype": "File",
                "file_name": os.path.basename(image),
                "file_url": image,
                "attached_to_doctype": "Student",  # Adjust this if needed
                "attached_to_name": name,          # Adjust this if needed
                "is_private": 0
            })
            saved_file.save()

        # Get the absolute path of the saved file
        file_path = os.path.join(get_files_path(), os.path.basename(saved_file.file_url))

        # Check if the file exists at the file_path
        if not os.path.exists(file_path):
            frappe.throw(('File not found at path {0}. Make sure the file is public.').format(file_path))

        # Send the image via WhatsApp API
        api_url = 'https://wts.vision360solutions.co.in/api/sendFileWithCaption'
        params = {
            'token': instance_id,  # Use your API token from the "Admin Settings" doctype
            'phone': f'91{mobile_number}',  # Mobile number prefixed with country code
            'message': message              # Message content
        }

        # Open the saved file and pass it as a file parameter
        with open(file_path, 'rb') as image_file:
            files = {
                'file': image_file
            }

            # Send the request to the WhatsApp API
            response = requests.post(api_url, params=params, files=files)
            response_data = response.json()  # Parse the JSON response
    else:
        # Call the fallback function to send a text-only message if no image is provided
        return send_whatsapp_Template_message(name, mobile_number, student_name, message)

    # Check for success based on the response data
    if response_data.get('status') == 'success':
        # Extract the messageID(s) from the response
        message_ids = response_data.get('data', {}).get('messageIDs', [])
        message_status = 'Success'

        # Log the message in WhatsApp Message Log doctype
        frappe.get_doc({
            'doctype': 'WhatsApp Message Log',
            'sender': frappe.session.user,            # Sender is the logged-in user
            'send_date': frappe.utils.now(),          # Send date is the current time
            'message_type': 'Message with File/Image',               # Set custom message type
            'message': message,                       # Message from the client script
            'student_id': name,                       # Student ID passed from client
            'status': message_status,                 # Log the status (Success/Failed)
            'message_id': ', '.join(message_ids)      # Join message IDs into a string (if multiple IDs)
        }).insert(ignore_permissions=True)

        frappe.logger().info(f"WhatsApp message sent successfully to {mobile_number} with messageID: {', '.join(message_ids)}")
    else:
        message_status = 'Failed'
        message_ids = []
        frappe.logger().error(f"Failed to send WhatsApp message to {mobile_number}. Response: {response_data}")

    # Return the status of the message
    return {'status': message_status}

################# Below code will check the quota and connection status if true then only the message will go ###################

import requests
import frappe

# def check_credits_and_connection(instance_id):
#     # API call to check the balance and connection status
#     url = f"https://wts.vision360solutions.co.in/api/checkBal?token={instance_id}"
    
#     try:
#         response = requests.get(url)
#         response_data = response.json()

#         if response.status_code == 200 and response_data.get('status') == 'success':
#             # Extract the necessary fields
#             quota = response_data.get('data', {}).get('quota', 0)
#             connected_number = response_data.get('data', {}).get('connectedNumeber', '')

#             # Check if connected number is empty or not
#             if not connected_number:
#                 frappe.throw("Your instance is not connected.")
            
#             # Return both quota and connected number for further checks
#             return quota, connected_number
        
#         else:
#             frappe.logger().error(f"Failed to check credits. Response: {response_data}")
#             return 0, ''  # Default values if the request fails
#     except Exception as e:
#         frappe.logger().error(f"Error checking credits: {str(e)}")
#         frappe.log_error(frappe.get_traceback(), "Credit Check Failed")
#         return 0, ''  # Return 0 credits and empty connection on failure

@frappe.whitelist()
def send_whatsapp_Template_message(name, mobile_number, student_name, message):
    # Fetch the instance_id from the "Admin Settings" doctype
    base_url = frappe.utils.get_url()
    admin_settings = frappe.get_doc('Admin Settings')
    instance_id = admin_settings.instance_id
    
    # Step 1: Check if credits and connection are valid
    quota, connected_number = check_credits_and_connection(instance_id)
    
    if quota > 0:
        # Proceed with sending the message if credits are available and connected number is valid
        try:
            # Make the API request to send the WhatsApp message
            url = "https://wts.vision360solutions.co.in/api/sendText"
            params_1 = {
                "token": instance_id,
                "phone": f"91{mobile_number}",
                "message": message,
            }
            response = requests.post(url, params=params_1)
            response_data = response.json()

            # Check if the message was successfully sent
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
                'sender': frappe.session.user,
                'send_date': now(),
                'message_type': 'Template',
                'message': message,
                'student_id': name,
                'status': message_status,
                'message_id': ', '.join(message_ids)  # Join message IDs if any
            }).insert(ignore_permissions=True)
            
            frappe.logger().info(f"WhatsApp message log created for student {name} with status {message_status}")
        except Exception as log_error:
            frappe.log_error(frappe.get_traceback(), "Failed to create WhatsApp Message Log")
        
        return {'status': message_status}
    
    else:
        # Throw error if credits are 0
        frappe.throw("No credits available to send WhatsApp message.")
        return {'status': 'Failed', 'msg': 'No credits available'}
