# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

import frappe,urllib
from frappe.model.document import Document
from frappe import _
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class ContactFormSubmission(Document):
	pass

def parse_form_data(form_data):
    parsed_data = urllib.parse.parse_qs(form_data)
    name = parsed_data.get("name", [None])[0]
    email = parsed_data.get("email", [None])[0]
    mobile = parsed_data.get("mobile", [None])[0]
    message = parsed_data.get("message", [None])[0]
    return name, email, mobile, message


def create_contact_form_submission(name, email, mobile, message, url):
    custom_data_doc = frappe.new_doc("Contact Form Submission")
    custom_data_doc.name1 = name
    custom_data_doc.email = email
    custom_data_doc.mobile = mobile
    custom_data_doc.message = message
    custom_data_doc.url = url
    custom_data_doc.insert(ignore_permissions=True)


def get_admin_settings():
    return frappe.get_doc("Admin Settings", "Admin Settings")


def build_email(sender_email, recipient_email, subject, body, cc_emails_str=""):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    if cc_emails_str:
        msg['CC'] = cc_emails_str

    msg.attach(MIMEText(body, 'html'))
    return msg


import smtplib

def send_email(name, email, message, url):
    doc = get_admin_settings()

    sender_email = doc.admin_email
    sender_password = doc.email_app_password
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    send_mail_to_user = doc.send_mail_to_user
    send_mail_to_admin = doc.send_mail_to_admin

    submitter_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Thank You for Contacting Us</title>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; margin: 0; padding: 0; background-color: #f9f9f9; }}
            .email-container {{ width: 100%; max-width: 600px; margin: 20px auto; background-color: #ffffff; padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); }}
            h3 {{ color: #4CAF50; font-size: 24px; margin-bottom: 10px; }}
            p {{ font-size: 16px; line-height: 1.6; margin: 10px 0; }}
            .footer {{ font-size: 14px; color: #777; text-align: center; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <h3>Hello {name},</h3>
            <p>Thank you for submitting your contact form. We have received your message:</p>
            <p><strong>Your Message:</strong><br>{message}</p>
            <p>Our team will get back to you as soon as possible. If you have any further questions, feel free to reach out.</p>
            <p>Best regards,<br>360ITHUB</p>
            <div class="footer">
                <p>If you didn't expect this email, please ignore it.</p>
            </div>
        </div>
    </body>
    </html>
    """

    receiver_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Contact Form Submission</title>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; margin: 0; padding: 0; background-color: #f9f9f9; }}
            .email-container {{ width: 100%; max-width: 600px; margin: 20px auto; background-color: #ffffff; padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); }}
            h3 {{ color: #4CAF50; font-size: 24px; margin-bottom: 10px; }}
            p {{ font-size: 16px; line-height: 1.6; margin: 10px 0; }}
            .footer {{ font-size: 14px; color: #777; text-align: center; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <h3>New Contact Form Submission</h3>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Message:</strong><br>{message}</p>
            <p>Review the submission and get back to the submitter as necessary.</p>
            <p>Best regards,<br>360ITHUB</p>
            <div class="footer">
                <p>If you didn't expect this email, please ignore it.</p>
            </div>
        </div>
    </body>
    </html>
    """

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  
            server.login(sender_email, sender_password)

            if send_mail_to_user == 1:
                
                msg_submitter = build_email(sender_email, email, "Thank You for Contacting Us", submitter_body)
                server.sendmail(sender_email, email, msg_submitter.as_string())
            else:
                print("Emails are not sent to user")

            if send_mail_to_admin == 1:
                
                receiver_email = doc.cc.split(",")[0] if doc.cc else None
                cc_emails_str = ', '.join(doc.cc.split(",")[1:]) if doc.cc else ""
                msg_receiver = build_email(sender_email, receiver_email, "New Contact Form Submission", receiver_body, cc_emails_str)
                server.sendmail(sender_email, receiver_email, msg_receiver.as_string())
            else:
                print("Emails are not sent to admin")

            print("Emails sent successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")


@frappe.whitelist(allow_guest=True)
def process_form_data(form_data, url):
    name, email, mobile, message = parse_form_data(form_data)

    create_contact_form_submission(name, email, mobile, message, url)

    send_email(name, email, message, url)

    return {"message": "success"}

