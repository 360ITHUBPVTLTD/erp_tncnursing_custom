# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WhatsAppInstance(Document):
	pass

######################### Login Instance (connect now button) ###################################

import frappe
import requests
from frappe.model.document import Document
import json

@frappe.whitelist()
def storing_the_qrcode(name=None):
    if True:
        whatsapp_demo = frappe.get_doc("WhatsApp Instance",name)
        instance_id=whatsapp_demo.instance_id
        try:
            
            api_endpoint = 'https://wts.vision360solutions.co.in/api/qrCodeLink?token={{instance_id}}'
            api_endpoint = api_endpoint.replace('{{instance_id}}', instance_id)

            # Make a GET request to the API endpoint
            response = requests.get(api_endpoint)
            response.raise_for_status()  # Raise an error for HTTP errors (status codes other than 2xx)

            # Parse the JSON response
            json_data = response.json()
            
            # Extract the URL from the JSON response
            qr_code_url = json_data.get('data')
            # print(qr_code_url)

            return qr_code_url  # Return the URL
        except requests.RequestException as e:
            frappe.log_error(f"Error generating QR code link: {e}")
            return None
        


############################## Logout Instance code (Disconnect Now Button)#######################################

@frappe.whitelist()
def logout_instance(name):
    try:
        whatsapp_demo = frappe.get_doc("WhatsApp Instance",name)
        instance_id=whatsapp_demo.instance_id

        # Attempt to disconnect the instance
        url = "https://wts.vision360solutions.co.in/api/logout"
        params = {"token": instance_id}
        response = requests.post(url, params=params)
        # print(response.status_code)
        
        response.raise_for_status() # Raise an error for HTTP errors (status codes other than 2xx)
        response=response.json()
        # print(response)
        # Check if the instance is already disconnected
        #  {'status': 'success', 'message': 'Instance 609bc2d1392a635870527076 disconnected successfully'}

        if "disconnected successfully" in response["message"]:
            whatsapp_demo.connection_status = 0
            whatsapp_demo.save()
            return {"message": "Instance disconnected successfully."}
        else:
            return {"message": "Error disconnecting."}
    
    except requests.RequestException as e:
        frappe.logger().error(f"Error sending WhatsApp message: {e}")
        raise

############################## Sync Button ###################################

import frappe
import requests
from datetime import datetime

@frappe.whitelist()
def storing_the_instance_data(name):
    try:
        whatsapp_demo = frappe.get_doc("WhatsApp Instance",name)
        instance_id=whatsapp_demo.instance_id
        # print(instance_id)
        # Define the API endpoint URL with the token placeholder
        api_endpoint = 'https://wts.vision360solutions.co.in/api/qrCodeLink?token={{instance_id}}'

        # Replace {{instance_id}} with the actual token
        api_endpoint = api_endpoint.replace('{{instance_id}}', instance_id)

        # Make a GET request to the API endpoint
        response = requests.get(api_endpoint)
        response.raise_for_status()  # Raise an error for HTTP errors (status codes other than 2xx)

        # Parse the JSON response
        json_data = response.json()
        # print(json_data)

        # Extract data from JSON
        instance_data = json_data['data']
        # print(type(instance_data))
        # print("Hello")
        creation_time_formatted=None
        expiry_date_formatted=None

        # Convert the datetime string to the correct format
        if (type(instance_data) == dict):
            creation_time = datetime.strptime(instance_data['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
            creation_time_formatted = creation_time.strftime('%Y-%m-%d %H:%M:%S')
            expiry_date = datetime.strptime(instance_data['quotaValidity'], '%Y-%m-%dT%H:%M:%S.%fZ')
            expiry_date_formatted = expiry_date.strftime('%Y-%m-%d %H:%M:%S')

            whatsapp_demo.connected_number = instance_data['connectedNumeber'] ##
            print(whatsapp_demo.connected_number,whatsapp_demo.assigned_mobile_number)
            if whatsapp_demo.connected_number != whatsapp_demo.assigned_mobile_number:
                instance_id=whatsapp_demo.instance_id

                # Attempt to disconnect the instance
                url = "https://wts.vision360solutions.co.in/api/logout"
                params = {"token": instance_id}
                response = requests.post(url, params=params)
                # print(response.status_code)
                
                # response.raise_for_status() # Raise an error for HTTP errors (status codes other than 2xx)
                # response=response.json()
                # print(response)
                # # Check if the instance is already disconnected
                # #  {'status': 'success', 'message': 'Instance 609bc2d1392a635870527076 disconnected successfully'}

                # if "disconnected successfully" in response["message"]:
                #     whatsapp_demo.connection_status = 0
                #     whatsapp_demo.save()
                    # return {"message": "Instance disconnected successfully."}
                # else:
                #     # return {"message": "Error disconnecting."}
                return {'status':False,"error": "You are connecting WhatsApp API with Invalid Number."}
            # whatsapp_demo.connected_number = "919513777002"
            whatsapp_demo.instance_name = instance_data['name']  ##
            whatsapp_demo.remaining_credits = instance_data['quota'] ##
            whatsapp_demo.webhook = instance_data['webhookEnabled'] ##
            # whatsapp_demo.instance_name = instance_data['profileName']
            whatsapp_demo.expiry_date = expiry_date_formatted ##
            whatsapp_demo.creation_time = creation_time_formatted ##
            whatsapp_demo.credits_usage = instance_data['instanceUsage'] ##
            whatsapp_demo.connection_status = instance_data['isLoggedIn'] ##
            whatsapp_demo.today_credits_usage = instance_data['todayUsage'] ##
            # whatsapp_demo.active = 1 if instance_data['isLoggedIn'] else 0 
            whatsapp_demo.save()
        else:
            whatsapp_demo.connection_status = 0 ##
            # whatsapp_demo.active = 0
            whatsapp_demo.save()


        return {"message": "Data stored successfully."}
    except requests.RequestException as e:
        frappe.log_error(f"Error in a storing data: {e}")
        return {"message": "Failed to store  data."}
