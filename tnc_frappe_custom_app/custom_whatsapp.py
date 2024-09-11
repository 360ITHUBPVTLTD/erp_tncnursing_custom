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

# import frappe
# import requests
# from frappe.utils import now

# @frappe.whitelist()
# def send_whatsapp_pdf_message(name, mobile_number, student_name, message):
#     # Fetch the instance_id from the "Admin Settings" doctype
#     base_url = frappe.utils.get_url()
#     admin_settings = frappe.get_doc('Admin Settings')
#     instance_id = admin_settings.instance_id
    

#     # Prepend +91 to the mobile number if not already present
#     if not mobile_number.startswith("91"):
#         mobile_number = "91" + mobile_number

#     # Generate the dynamic file URL
#     # file_url = "https://tourism.gov.in/sites/default/files/2019-04/dummy-pdf_2.pdf"
#     file_url = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/{student_name}.pdf"
#     text_message = f"Dear {student_name}, Check your results."

#     # Construct the API URL
#     api_url = f"https://wts.vision360solutions.co.in/api/sendFileWithCaption?token={instance_id}&phone={mobile_number}&link={file_url}&message={text_message}"    


    # Prepend +91 to the mobile number if not already present
    if not mobile_number.startswith("91"):
        mobile_number = "91" + mobile_number

    # Generate the dynamic file URL
    # file_url = "https://tourism.gov.in/sites/default/files/2019-04/dummy-pdf_2.pdf"
    file_url = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/{student_name}.pdf"

    text_message = f"Dear {student_name}, Check your results."

    # file_url = f"http://3.111.226.95/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/{student_name}.pdf"
#     file_url = "http://3.111.226.95/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name=TNC-Student-00072286&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/TNC-Student-00072286.pdf"


    # Construct the API URL
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



#     try:
#         # Make the API request
#         response = requests.get(api_url)
#         response_data = response.json()  # Parse the JSON response
#         print(response_data)

#         # Check for success based on the response data
#         if response_data.get('status') == 'success':
#             message_status = "success"
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

        
        frappe.logger().info(f"WhatsApp message log created for student {name} with status {message_status}")
    except Exception as log_error:
        frappe.log_error(frappe.get_traceback(), "Failed to create WhatsApp Message Log")

    # return {'status': message_status}
    return {"status": 'success', "msg": "WhatsApp message sent successfully!"}


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




















# import frappe
# import requests
# from frappe.utils import now

# @frappe.whitelist()
# def send_bulk_whatsapp_messages(message_text):
#     # Ensure the message_text is provided
#     if not message_text:
#         frappe.throw("Message text is required.")

#     # Fetch the admin settings to get the instance ID
#     admin_settings = frappe.get_doc('Admin Settings')
#     instance_id = admin_settings.instance_id
    
#     # Fetch the students and their mobile numbers
#     students = frappe.get_all('Student', fields=['name', 'mobile','student_name'])
#     base_url = frappe.utils.get_url()
    
#     # Loop through each student to prepare and send the message
#     for student in students:
#         mobile = student.mobile
#         name = student.name
#         student_name = student.student_name
#         # print(mobile)
#         # print(name)
#         # print(student_name)

        
#         # Check if the mobile number starts with country code 91
#         if not mobile.startswith('91'):
#             # Add country code 91 if it's missing
#             mobile = '91' + mobile
        
#         # Generate the PDF URL dynamically (replace with your actual URL)
#         file_url = "https://tourism.gov.in/sites/default/files/2019-04/dummy-pdf_2.pdf"
#         # file_url = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name={name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en/{student_name}.pdf"

        
#         # WhatsApp API endpoint and payload
#         api_url = f"https://wts.vision360solutions.co.in/api/sendFiles?token={instance_id}&phone={mobile}&link={file_url}&message={message_text}"
        
#         # Send the request to the WhatsApp API
#         try:
#             response = requests.get(api_url)
#             response_data = response.json()  # Get the response JSON
            
#             # Extract the message status and message IDs from the API response
#             message_status = response_data.get('status', 'Failed')  # Default to 'Failed' if no status
#             message_ids = ', '.join(response_data.get('data', {}).get('messageIDs', []))  # Get messageIDs
            
#             # Check for success status
#             if response.status_code == 200 and message_status == "success":
#                 frappe.logger().info(f"Message sent to {mobile} successfully.")
#             else:
#                 frappe.logger().error(f"Failed to send message to {mobile}. Status code: {response.status_code}, Status: {message_status}")
#                 message_status = "Failed"
#         except Exception as e:
#             frappe.logger().error(f"Error sending message to {mobile}: {str(e)}")
#             frappe.log_error(frappe.get_traceback(), "WhatsApp Message Sending Failed")
#             message_status = "Failed"
#             message_ids = ''  # No message IDs if it failed

#         # Log the message in "WhatsApp Message Log" doctype
#         try:
#             frappe.get_doc({
#                 'doctype': 'WhatsApp Message Log',
#                 'sender': frappe.session.user,  # Sender is the logged-in user
#                 'send_date': now(),             # Send date is the current time
#                 'message_type': 'Bulk',         # Set message type to 'Bulk'
#                 'message': message_text,        # The message that was sent
#                 'student_id': student.name,     # The student ID
#                 'mobile_number': mobile,        # The mobile number the message was sent to
#                 'status': message_status,       # Log the status (Success/Failed)
#                 'message_id': message_ids      # Log the message IDs from the response
#             }).insert(ignore_permissions=True)
            
#             frappe.logger().info(f"WhatsApp message log created for student {student.name}")
#         except Exception as log_error:
#             frappe.log_error(frappe.get_traceback(), "Failed to create WhatsApp Message Log")
    
#     return {'message': 'Bulk WhatsApp messages sent successfully!'}






#################################### Batch wise queue whatsapp messages #########################

# import frappe
# from frappe import enqueue
# from math import ceil

# @frappe.whitelist()
# def send_bulk_whatsapp_messages(message_text):
#     if not message_text:
#         frappe.throw("Message text is required.")

#     students = frappe.get_all('Student', fields=['name', 'mobile', 'student_name'])
#     batch_size = 100
#     num_batches = ceil(len(students) / batch_size)

#     for i in range(num_batches):
#         batch = students[i * batch_size:(i + 1) * batch_size]
#         enqueue(
#             send_messages_batch,
#             batch,
#             timeout=600,  # adjust the timeout if needed
#             queue='default'  # you can create different queues if needed
#         )
    
#     return {'message': 'Bulk WhatsApp messages enqueued successfully!'}




# import frappe
# import requests
# from frappe.utils import now

# def send_messages_batch(batch):
#     for student in batch:
#         mobile = student['mobile']
#         name = student['name']
#         student_name = student['student_name']

#         # Add country code 91 if it's missing
#         if not mobile.startswith('91'):
#             mobile = '91' + mobile

#         # Generate the PDF URL dynamically
#         file_url = "https://tourism.gov.in/sites/default/files/2019-04/dummy-pdf_2.pdf"
        
#         # WhatsApp API endpoint and payload
#         instance_id = frappe.get_doc('Admin Settings').instance_id
#         api_url = f"https://wts.vision360solutions.co.in/api/sendFiles?token={instance_id}&phone={mobile}&link={file_url}&message={message_text}"
        
#         try:
#             response = requests.get(api_url)
#             response_data = response.json()  # Get the response JSON
            
#             message_status = response_data.get('status', 'Failed')
#             message_ids = ', '.join(response_data.get('data', {}).get('messageIDs', []))
            
#             if response.status_code == 200 and message_status == "success":
#                 frappe.logger().info(f"Message sent to {mobile} successfully.")
#             else:
#                 frappe.logger().error(f"Failed to send message to {mobile}. Status code: {response.status_code}, Status: {message_status}")
#                 message_status = "Failed"
#         except Exception as e:
#             frappe.logger().error(f"Error sending message to {mobile}: {str(e)}")
#             frappe.log_error(frappe.get_traceback(), "WhatsApp Message Sending Failed")
#             message_status = "Failed"
#             message_ids = ''

#         try:
#             frappe.get_doc({
#                 'doctype': 'WhatsApp Message Log',
#                 'sender': frappe.session.user,
#                 'send_date': now(),
#                 'message_type': 'Bulk',
#                 'message': message_text,
#                 'student_id': student['name'],
#                 'mobile_number': mobile,
#                 'status': message_status,
#                 'message_id': message_ids
#             }).insert(ignore_permissions=True)
            
#             frappe.logger().info(f"WhatsApp message log created for student {student['name']}")
#         except Exception as log_error:
#             frappe.log_error(frappe.get_traceback(), "Failed to create WhatsApp Message Log")


# import frappe
# from frappe import enqueue
# from math import ceil
# import requests
# from frappe.utils import now

# @frappe.whitelist()
# def send_bulk_whatsapp_messages(message_text):
#     if not message_text:
#         frappe.throw("Message text is required.")
    
#     # Get all students
#     students = frappe.get_all('Student', fields=['name', 'mobile', 'student_name'])
#     batch_size = 100
#     num_batches = ceil(len(students) / batch_size)
    
#     # Enqueue each batch for background processing
#     for i in range(num_batches):
#         batch = students[i * batch_size:(i + 1) * batch_size]
#         enqueue(
#             send_messages_batch,
#             batch,
#             timeout=600,  # adjust the timeout if needed
#             queue='default'  # you can create different queues if needed
#         )
    
#     return {'message': 'Bulk WhatsApp messages enqueued successfully!'}

# def send_messages_batch(batch):
#     message_text = message_text  # Placeholder, adjust according to your needs

#     for student in batch:
#         mobile = student['mobile']
#         name = student['name']
#         student_name = student['student_name']

#         # Add country code 91 if it's missing
#         if not mobile.startswith('91'):
#             mobile = '91' + mobile

#         # Generate the PDF URL dynamically
#         file_url = "https://tourism.gov.in/sites/default/files/2019-04/dummy-pdf_2.pdf"
        
#         # WhatsApp API endpoint and payload
#         instance_id = frappe.get_doc('Admin Settings').instance_id
#         api_url = f"https://wts.vision360solutions.co.in/api/sendFiles?token={instance_id}&phone={mobile}&link={file_url}&message={message_text}"
        
#         try:
#             response = requests.get(api_url)
#             response_data = response.json()  # Get the response JSON
            
#             message_status = response_data.get('status', 'Failed')
#             message_ids = ', '.join(response_data.get('data', {}).get('messageIDs', []))
            
#             if response.status_code == 200 and message_status == "success":
#                 frappe.logger().info(f"Message sent to {mobile} successfully.")
#             else:
#                 frappe.logger().error(f"Failed to send message to {mobile}. Status code: {response.status_code}, Status: {message_status}")
#                 message_status = "Failed"
#         except Exception as e:
#             frappe.logger().error(f"Error sending message to {mobile}: {str(e)}")
#             frappe.log_error(frappe.get_traceback(), "WhatsApp Message Sending Failed")
#             message_status = "Failed"
#             message_ids = ''

#         try:
#             frappe.get_doc({
#                 'doctype': 'WhatsApp Message Log',
#                 'sender': frappe.session.user,
#                 'send_date': now(),
#                 'message_type': 'Bulk',
#                 'message': message_text,
#                 'student_id': student['name'],
#                 'mobile_number': mobile,
#                 'status': message_status,
#                 'message_id': message_ids
#             }).insert(ignore_permissions=True)
            
#             frappe.logger().info(f"WhatsApp message log created for student {student['name']}")
#         except Exception as log_error:
#             frappe.log_error(frappe.get_traceback(), "Failed to create WhatsApp Message Log")
