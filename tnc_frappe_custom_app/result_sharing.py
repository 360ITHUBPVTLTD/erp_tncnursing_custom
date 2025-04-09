import frappe





# @frappe.whitelist(allow_guest=True)
# def secure_student_pdf(token):
#     student = frappe.get_value("Online Student", {"encryption_key": token}, "name")
#     if not student:
#         frappe.throw("Invalid or expired link")
 
#     return frappe.utils.print_format.download_pdf(
#         doctype="Online Student",
#         name=student,
#         format="Student Results Top Performer"
#     )


# @frappe.whitelist(allow_guest=True)
# def secure_student_pdf(token):
#     student = frappe.get_value("Online Student", {"encryption_key": token}, "name")
#     if not student:
#         frappe.throw("Invalid or expired link")

#     # Use frappe.get_print to generate PDF output
#     pdf_data = frappe.get_print(
#         doctype="Online Student",
#         name=student,
#         print_format="Student Results Top Performer",
#         as_pdf=True
#     )
#     return pdf_data


# @frappe.whitelist(allow_guest=True)
# def download_result_by_key(encryption_key):
#     # Find the student by encryption_key
#     student = frappe.get_value("Online Student", {"encryption_key": encryption_key}, "name")
#     if not student:
#         frappe.throw("Invalid or expired key")
 
#     # Return the PDF response
#     return frappe.utils.print_format.download_pdf(
#         doctype="Online Student",
#         name=student,
#         format="Student Results Top Performer",
#         no_letterhead=0,
#         letterhead="TNC Logo",
#         settings={},
#         _lang="en"
#     )


# from frappe.utils.print_format import download_pdf
 
# @frappe.whitelist(allow_guest=True)
# def download_result_by_key(encryption_key):
#     # Step 1: Get student name based on encryption key
#     student_name = frappe.get_value("Online Student", {"encryption_key": encryption_key}, "name")
#     if not student_name:
#         frappe.throw("Invalid or expired key")
 
#     # Step 2: Call the correct print function
#     return download_pdf(
#         doctype="Online Student",
#         name=student_name,
#         format="Student Results Top Performer",
#         no_letterhead=0,
#         letterhead="TNC Logo",
#         # settings={},
#         # _lang="en"
#     )
from frappe.utils.print_format import download_pdf
from frappe import _

# @frappe.whitelist(allow_guest=True)
# def download_result_by_key(encryption_key):
#     try:
#         enqueue_pdf_generation_for_students_manual_s3()
#         # Step 1: Validate the encryption key
#         student_name = frappe.get_value("Online Student", {"encryption_key": encryption_key}, "name")
#         if not student_name:
#             # Return a generic error without traceback
#             frappe.local.response.http_status_code = 403
#             return {"status": "error", "message": _("Invalid or expired link.")}

#         # Step 2: Generate and return the PDF
        
#         return download_pdf(
#             doctype="Online Student",
#             name=student_name,
#             format="Student Results Top Performer",
#             no_letterhead=0,
#             letterhead="TNC Logo"
#         )

#     except Exception:
#         # Catch unexpected issues and respond safely
#         frappe.local.response.http_status_code = 500
#         return {"status": "error", "message": _("Something went wrong while processing your request.")}



# Script to enqueue PDF generation (Run via `bench execute` or create a Server Script)
import frappe
from frappe.utils.background_jobs import enqueue

import boto3
import frappe,traceback


# def enqueue_pdf_generation_for_students():
#     # Define criteria for students needing PDFs (adjust filter as needed)
#     students = frappe.get_all("Online Student", filters={"docstatus": 1, "some_relevant_filter": "value"}, fields=["name", "encryption_key"])

#     count = 0
#     for student in students:
#         # Enqueue the generation task for each student
#         enqueue(
#             "tnc_frappe_custom_app.result_sharing.generate_and_save_student_pdf", # Path to your generation function
#             queue="long", # Use 'long' queue for potentially lengthy PDF jobs
#             timeout=1800, # Increase timeout (e.g., 30 mins)
#             student_name=student.name,
#             encryption_key=student.encryption_key # Pass if needed for filename
#         )
#         count += 1
#     frappe.log_info(f"Enqueued PDF generation for {count} students.", "PDF Pre-generation")

# Call the function to start enqueueing
# enqueue_pdf_generation_for_students()


# In tnc_frappe_custom_app.result_sharing (or another appropriate place)
# The actual function that runs in the background for EACH student
# import frappe
# from frappe.utils.pdf import get_pdf
# from frappe.core.doctype.file.file import save_file

# This function will be called by the background worker
# def generate_and_save_student_pdf(student_name, encryption_key):
#     try:
#         student_doc = frappe.get_doc("Online Student", student_name)

#         # Check if PDF already exists to avoid re-generation (optional but good)
#         if student_doc.result_pdf_attachment:
#              print(f"Skipping {student_name}, PDF already exists: {student_doc.result_pdf_attachment}")
#              # frappe.log_info(f"Skipping {student_name}, PDF already exists: {student_doc.result_pdf_attachment}", "PDF Pre-generation")
#              return

#         print(f"Generating PDF for {student_name}...")
#         # frappe.log_info(f"Generating PDF for {student_name}...", "PDF Pre-generation")

#         # Generate PDF content (similar to download_pdf but gets bytes)
#         pdf_content = get_pdf(
#             doctype="Online Student",
#             name=student_name,
#             format="Student Results Top Performer",
#             no_letterhead=0,
#             letterhead="TNC Logo",
#             # as_pdf=True # get_pdf returns bytes directly
#         )

#         # Define filename
#         # Using encryption_key ensures uniqueness if student names aren't unique
#         # Make sure encryption_key is safe for filenames (alphanumeric)
#         safe_key = ''.join(filter(str.isalnum, encryption_key))
#         file_name = f"student_result_{safe_key}_{student_name}.pdf"

#         # Save the file using Frappe's file manager (handles S3 if configured)
#         file_doc = save_file(
#             fname=file_name,
#             content=pdf_content,
#             doctype="Online Student",
#             docname=student_name,
#             folder="Attachments", # Or a specific folder like "Student Results"
#             is_private=1, # Make private if results are sensitive
#             # attach_to_field='result_pdf_attachment' # Link to the field if using Attach type
#         )

#         # Update the student record with the file path/URL
#         # If 'result_pdf_attachment' is type Attach, save_file might handle linking it automatically
#         # If it's type Data, store file_doc.file_url
#         student_doc.db_set("result_pdf_attachment", file_doc.file_url) # Or file_doc.name if Attach field links automatically

#         # frappe.db.commit() # Background jobs usually commit automatically, but double-check documentation if needed

#         print(f"Successfully generated and saved PDF for {student_name} at {file_doc.file_url}")
#         # frappe.log_info(f"Successfully generated and saved PDF for {student_name} at {file_doc.file_url}", "PDF Pre-generation")

#     except Exception as e:
#         print(f"Failed to generate PDF for {student_name}: {str(e)}")
#         # frappe.log_error(f"Failed PDF generation for {student_name}", "PDF Pre-generation")
#         # Log the full traceback for debugging
#         frappe.log_error(frappe.get_traceback(), f"PDF Generation Error: {student_name}")


# @frappe.whitelist()
# def check_s3_connection_from_doctype():
#     """
#     Checks S3 connection using credentials from the 'Admin Settings' DocType.
#     Assumes the script is run for a specific site (site name needs to be set below).
#     """
#     # site_name = "your_site_name_here"  # <--- MODIFY THIS WITH YOUR SITE NAME

#     try:
#         # frappe.init(site=site_name)
#         # frappe.connect()

#         admin_settings = frappe.get_doc("Admin Settings") # Assuming only one 'Admin Settings' document

#         bucket_name = admin_settings.bucket
#         region_name = admin_settings.region_name
#         access_key = admin_settings.access_key
#         secret_key = admin_settings.secret_key

#         if not all([bucket_name, region_name, access_key, secret_key]):
#             print("Error: Incomplete S3 credentials in 'Admin Settings' DocType.")
#             return False

#         s3_client = boto3.client(
#             's3',
#             aws_access_key_id=access_key,
#             aws_secret_access_key=secret_key,
#             region_name=region_name
#         )

#         try:
#             # Attempt a simple operation: list objects in the bucket (limited to 1 to be quick)
#             response = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
#             print(response)
#             print(f"S3 Connection to bucket '{bucket_name}' in region '{region_name}' successful for site !")
#             return True

#         except Exception as e:
#             print(f"Error connecting to S3: {e}")
#             print(traceback.format_exc())
#             return False

#     except frappe.exceptions.DoesNotExistError:
#         print("Error: 'Admin Settings' DocType not found or document named 'Admin Settings' does not exist.")
#         print(traceback.format_exc())
#         return False
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         print(traceback.format_exc())
#         return False

# In tnc_frappe_custom_app.result_sharing (or another appropriate place)
import frappe
from frappe.utils.pdf import get_pdf
import boto3
import io
import traceback
import logging

# Configure logging for background task debugging
logger = logging.getLogger("pdf_generation_s3")
# You might want to configure file logging in production if needed

# This function will be called by the background worker
# @frappe.whitelist()
# def generate_and_save_student_pdf_manual_s3(student_name, encryption_key):
#     """
#     Generates a student result PDF, uploads it directly to S3 using boto3,
#     and stores the public S3 URL in the student's record.
#     Credentials fetched from 'Admin Settings' Singleton DocType.
#     """
#     try:
#         student_doc = frappe.get_doc("Online Student", student_name)

#         # --- Check if PDF URL already exists ---
#         if student_doc.result_pdf_attachment and student_doc.result_pdf_attachment.startswith('https://'):
#             logger.info(f"Skipping {student_name}, S3 URL already exists: {student_doc.result_pdf_attachment}")
#             return

#         logger.info(f"Starting PDF generation for {student_name}...")

#         # --- Get S3 Credentials ---
#         try:
#             admin_settings = frappe.get_single("Admin Settings") # Use get_single for Singletons
#             bucket_name = admin_settings.bucket
#             region_name = admin_settings.region_name
#             access_key = admin_settings.get_password("access_key") # Use get_password for Password fields
#             secret_key = admin_settings.get_password("secret_key")

#             if not all([bucket_name, region_name, access_key, secret_key]):
#                 raise ValueError("Incomplete S3 credentials in 'Admin Settings'")

#         except Exception as cred_err:
#             logger.error(f"Failed to get S3 credentials for {student_name}: {cred_err}", exc_info=True)
#             # Optionally update student doc status to indicate failure?
#             # student_doc.db_set("some_status_field", "PDF Generation Failed - Credential Error")
#             raise # Re-raise to mark the background job as failed

#         # --- Generate PDF Content ---
#         pdf_content = get_pdf(
#             doctype="Online Student",
#             name=student_name,
#             format="Student Results Top Performer",
#             no_letterhead=0,
#             letterhead="TNC Logo",
#             # as_pdf=True # get_pdf returns bytes
#         )
#         logger.info(f"PDF content generated for {student_name} ({len(pdf_content)} bytes)")

#         # --- Define S3 Key (File Path/Name in S3) ---
#         # Ensure the key is unique and doesn't contain problematic characters
#         safe_key_part = ''.join(filter(str.isalnum, encryption_key))
#         s3_key = f"student_results/{safe_key_part}_{student_name.replace(' ', '_')}.pdf"
#         logger.info(f"Generated S3 key for {student_name}: {s3_key}")


#         # --- Upload to S3 using Boto3 ---
#         try:
#             s3_client = boto3.client(
#                 's3',
#                 aws_access_key_id=access_key,
#                 aws_secret_access_key=secret_key,
#                 region_name=region_name
#             )

#             pdf_stream = io.BytesIO(pdf_content)

#             s3_client.upload_fileobj(
#                 Fileobj=pdf_stream,
#                 Bucket=bucket_name,
#                 Key=s3_key,
#                 ExtraArgs={
#                     'ContentType': 'application/pdf',
#                     'ACL': 'public-read' # Make the object publicly readable via its URL
#                 }
#             )
#             logger.info(f"Successfully uploaded PDF to S3 for {student_name} at Key: {s3_key}")

#         except Exception as s3_err:
#             logger.error(f"Failed to upload PDF to S3 for {student_name}: {s3_err}", exc_info=True)
#             # student_doc.db_set("some_status_field", "PDF Generation Failed - S3 Upload Error")
#             raise # Re-raise to mark the background job as failed

#         # --- Construct the Public S3 URL ---
#         # Standard URL format: https://<bucket-name>.s3.<region-name>.amazonaws.com/<key>
#         # Adjust if using a custom domain or different S3 endpoint (e.g., DigitalOcean Spaces)
#         s3_url = f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{s3_key}"
#         logger.info(f"Constructed S3 URL for {student_name}: {s3_url}")


#         # --- Update the student record with the S3 URL ---
#         student_doc.db_set("result_pdf_attachment", s3_url)
#         # frappe.db.commit() # Background jobs usually commit automatically per job

#         logger.info(f"Successfully processed and saved S3 URL for {student_name}")

#     except Exception as e:
#         logger.error(f"Overall failure in generating/uploading PDF for {student_name}: {str(e)}", exc_info=True)
#         # Log the full traceback for detailed debugging
#         # frappe.log_error(f"Failed PDF processing for {student_name}", traceback.format_exc())
#         # Consider setting a failure status on the student record here as well.



# In tnc_frappe_custom_app.result_sharing (or another appropriate place)
import frappe
from frappe.utils.pdf import get_pdf
import boto3
import io
import traceback
import logging
from frappe.utils.print_format import download_pdf

# Configure logging for background task debugging
logger = logging.getLogger("pdf_generation_s3")
# You might want to configure file logging in production if needed

# This function will be called by the background worker
# @frappe.whitelist()
# def generate_and_save_student_pdf_manual_s3(student_name, encryption_key):
#     """
#     Generates a student result PDF, uploads it directly to S3 using boto3,
#     and stores the public S3 URL in the student's record.
#     Credentials fetched from 'Admin Settings' Singleton DocType.
#     """
#     try:
#         student_doc = frappe.get_doc("Online Student", student_name)

#         # --- Check if PDF URL already exists ---
#         if student_doc.result_pdf_attachment and student_doc.result_pdf_attachment.startswith('https://'):
#             logger.info(f"Skipping {student_name}, S3 URL already exists: {student_doc.result_pdf_attachment}")
#             return

#         logger.info(f"Starting PDF generation for {student_name}...")

#         # --- Get S3 Credentials ---
#         try:
#             admin_settings = frappe.get_single("Admin Settings") # Use get_single for Singletons
#             bucket_name = admin_settings.bucket
#             region_name = admin_settings.region_name
#             # access_key = admin_settings.get_password("access_key") # Use get_password for Password fields
#             # secret_key = admin_settings.get_password("secret_key")
#             access_key = admin_settings.access_key # Use get_password for Password fields
#             secret_key = admin_settings.secret_key

#             if not all([bucket_name, region_name, access_key, secret_key]):
#                 raise ValueError("Incomplete S3 credentials in 'Admin Settings'")

#         except Exception as cred_err:
#             logger.error(f"Failed to get S3 credentials for {student_name}: {cred_err}", exc_info=True)
#             # Optionally update student doc status to indicate failure?
#             # student_doc.db_set("some_status_field", "PDF Generation Failed - Credential Error")
#             raise # Re-raise to mark the background job as failed

#         # --- Generate PDF Content ---
#         # pdf_content = get_pdf(
#         #     # doctype="Online Student",  <- REMOVE THIS LINE, it's incorrect
#         #     name=student_name,         # Use 'name' (or docname) to specify the document
#         #     format="Student Results Top Performer",
#         #     no_letterhead=0,
#         #     letterhead="TNC Logo",
#         #     # as_pdf=True # get_pdf returns bytes
#         # )
        
#         pdf_content =  download_pdf(
#             doctype="Online Student",
#             name=student_name,
#             format="Student Results Top Performer",
#             no_letterhead=0,
#             letterhead="TNC Logo"
#         )
#         # logger.info(f"PDF content generated for {student_name} ({len(pdf_content)} bytes)")

#         # --- Define S3 Key (File Path/Name in S3) ---
#         # Ensure the key is unique and doesn't contain problematic characters
#         safe_key_part = ''.join(filter(str.isalnum, encryption_key))
#         s3_key = f"student_results/{safe_key_part}_{student_name.replace(' ', '_')}.pdf"
#         logger.info(f"Generated S3 key for {student_name}: {s3_key}")


#         # --- Upload to S3 using Boto3 ---
#         try:
#             s3_client = boto3.client(
#                 's3',
#                 aws_access_key_id=access_key,
#                 aws_secret_access_key=secret_key,
#                 region_name=region_name
#             )

#             pdf_stream = io.BytesIO(pdf_content)

#             s3_client.upload_fileobj(
#                 Fileobj=pdf_stream,
#                 Bucket=bucket_name,
#                 Key=s3_key,
#                 ExtraArgs={
#                     'ContentType': 'application/pdf',
#                     # 'ACL': 'public-read' # Make the object publicly readable via its URL
#                 }
#             )
#             logger.info(f"Successfully uploaded PDF to S3 for {student_name} at Key: {s3_key}")

#         except Exception as s3_err:
#             logger.error(f"Failed to upload PDF to S3 for {student_name}: {s3_err}", exc_info=True)
#             # student_doc.db_set("some_status_field", "PDF Generation Failed - S3 Upload Error")
#             raise # Re-raise to mark the background job as failed

#         # --- Construct the Public S3 URL ---
#         # Standard URL format: https://<bucket-name>.s3.<region-name>.amazonaws.com/<key>
#         # Adjust if using a custom domain or different S3 endpoint (e.g., DigitalOcean Spaces)
#         s3_url = f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{s3_key}"
#         logger.info(f"Constructed S3 URL for {student_name}: {s3_url}")


#         # --- Update the student record with the S3 URL ---
#         student_doc.db_set("result_pdf_attachment", s3_url)
#         # frappe.db.commit() # Background jobs usually commit automatically per job

#         logger.info(f"Successfully processed and saved S3 URL for {student_name}")

#     except Exception as e:
#         logger.error(f"Overall failure in generating/uploading PDF for {student_name}: {str(e)}", exc_info=True)
#         # Log the full traceback for detailed debugging
#         # frappe.log_error(f"Failed PDF processing for {student_name}", traceback.format_exc())
#         # Consider setting a failure status on the student record here as well.

import os
import io
import boto3
import frappe


import frappe
from frappe.utils.print_format import download_pdf
import boto3
import io
import os
import traceback
import logging

logger = logging.getLogger("pdf_generation_s3")
import os
import io
import boto3
import frappe
# import logger  # Ensure logger is imported or use frappe.logger()

import frappe
from frappe.utils.pdf import get_pdf # CORRECT IMPORT
import boto3
import io
import os
import traceback
import logging

# Re-enable logging - it's essential for debugging!
logger = logging.getLogger("pdf_generation_s3")

import frappe
from frappe.utils.pdf import get_pdf # Correct: Imports the function that takes HTML
import frappe.utils.print_format # Needed for get_print
import boto3
import io
import os
import traceback
import logging

logger = logging.getLogger("pdf_generation_s3_corrected")

    # finally:
        # If you were using the local save method, keep the finally block for cleanup
        # if local_pdf_path and os.path.exists(local_pdf_path):
        #     try:
        #         os.remove(local_pdf_path)
        #         logger.info(f"Successfully deleted temporary local file: {local_pdf_path}")
        #     except Exception as delete_err:
        #         logger.error(f"Failed to delete temporary local file '{local_pdf_path}': {delete_err}", exc_info=True)
    
# @frappe.whitelist()
# def generate_and_save_student_pdf_manual_s3(student_name, encryption_key):
#     """
#     Generates a student result PDF, saves it locally to the Frappe public folder,
#     uploads it directly to S3 using boto3, and stores a pre-signed URL (valid for one week)
#     in the student's record.
#     Credentials fetched from 'Admin Settings' Singleton DocType.
#     """
#     try:
#         student_doc = frappe.get_doc("Online Student", student_name)

#         # --- Check if PDF URL already exists ---
#         if student_doc.result_pdf_attachment and student_doc.result_pdf_attachment.startswith('https://'):
#             frappe.logger().info(f"Skipping {student_name}, S3 URL already exists: {student_doc.result_pdf_attachment}")
#             return

#         frappe.logger().info(f"Starting PDF generation for {student_name}...")

#         # --- Get S3 Credentials ---
#         try:
#             admin_settings = frappe.get_single("Admin Settings")
#             bucket_name = admin_settings.bucket
#             region_name = admin_settings.region_name
#             access_key = admin_settings.access_key
#             secret_key = admin_settings.secret_key

#             if not all([bucket_name, region_name, access_key, secret_key]):
#                 raise ValueError("Incomplete S3 credentials in 'Admin Settings'")

#         except Exception as cred_err:
#             frappe.logger().error(f"Failed to get S3 credentials for {student_name}: {cred_err}", exc_info=True)
#             raise

#         # --- Generate PDF Content ---
#         pdf_content = download_pdf(
#             doctype="Online Student",
#             name=student_name,
#             format="Student Results Top Performer",
#             no_letterhead=0,
#             letterhead="TNC Logo"
#         )

#         # --- Define S3 Key (File Path/Name in S3) ---
#         safe_key_part = ''.join(filter(str.isalnum, encryption_key))
#         s3_key = f"student_results/{safe_key_part}_{student_name.replace(' ', '_')}.pdf"
#         frappe.logger().info(f"Generated S3 key for {student_name}: {s3_key}")

#         # --- Save the PDF locally in the Frappe site's public folder ---
#         public_files_path = frappe.get_site_path("public", "files")
#         if not os.path.exists(public_files_path):
#             os.makedirs(public_files_path)
#         local_pdf_filename = f"{safe_key_part}_{student_name.replace(' ', '_')}.pdf"
#         print(local_pdf_filename)
#         local_pdf_path = os.path.join(public_files_path, local_pdf_filename)

#         with open(local_pdf_path, "wb") as f:
#             f.write(pdf_content)
#         frappe.logger().info(f"PDF saved locally for {student_name} at {local_pdf_path}")

#         # --- Upload to S3 using Boto3 ---
#         try:
#             s3_client = boto3.client(
#                 's3',
#                 aws_access_key_id=access_key,
#                 aws_secret_access_key=secret_key,
#                 region_name=region_name
#             )

#             pdf_stream = io.BytesIO(pdf_content)
#             s3_client.upload_fileobj(
#                 Fileobj=pdf_stream,
#                 Bucket=bucket_name,
#                 Key=s3_key,
#                 ExtraArgs={
#                     'ContentType': 'application/pdf'
#                 }
#             )
#             frappe.logger().info(f"Successfully uploaded PDF to S3 for {student_name} at Key: {s3_key}")

#         except Exception as s3_err:
#             frappe.logger().error(f"Failed to upload PDF to S3 for {student_name}: {s3_err}", exc_info=True)
#             raise

#         # --- Generate a Pre-signed URL with an expiry time of 1 week (604800 seconds) ---
#         presigned_url = s3_client.generate_presigned_url(
#             'get_object',
#             Params={
#                 'Bucket': bucket_name,
#                 'Key': s3_key,
#                 'ResponseContentType': 'application/pdf'
#             },
#             ExpiresIn=604800  # 7 days = 604800 seconds
#         )
#         frappe.logger().info(f"Generated pre-signed URL for {student_name}: {presigned_url}")

#         # --- Update the student record with the pre-signed URL ---
#         student_doc.db_set("result_pdf_attachment", presigned_url)
#         # frappe.db.commit() # Typically, background jobs commit automatically per job

#         frappe.logger().info(f"Successfully processed and saved pre-signed S3 URL for {student_name}")

#     except Exception as e:
#         frappe.logger().error(f"Overall failure in generating/uploading PDF for {student_name}: {str(e)}", exc_info=True)
#         # Optionally update student doc status or log error details for future debugging.


# import boto3
# import frappe




# def download_file_from_s3_from_admin_settings(s3_key, local_filename):
#     """
#     Downloads a file from S3 using credentials from Frappe's Admin Settings,
#     and saves it to the local system.

#     Parameters:
#     - s3_key: The S3 object key (path/filename) to download.
#     - local_filename: The local filename where the S3 file will be saved.
#     """
#     try:
#         # --- Get S3 Credentials from Admin Settings ---
#         admin_settings = frappe.get_single("Admin Settings")
#         bucket_name = admin_settings.bucket
#         region_name = admin_settings.region_name
#         access_key = admin_settings.access_key
#         secret_key = admin_settings.secret_key

#         if not all([bucket_name, region_name, access_key, secret_key]):
#             raise ValueError("Incomplete S3 credentials in 'Admin Settings'")
        
#         # --- Initialize the S3 client with your credentials ---
#         s3_client = boto3.client(
#             's3',
#             aws_access_key_id=access_key,
#             aws_secret_access_key=secret_key,
#             region_name=region_name
#         )

#         # --- Retrieve the object from S3 ---
#         response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
#         file_content = response['Body'].read()

#         # --- Write the file content to a local file ---
#         with open(local_filename, 'wb') as f:
#             f.write(file_content)

#         frappe.logger().info(f"File downloaded successfully and saved as '{local_filename}'.")
#         print(f"File downloaded successfully and saved as '{local_filename}'.")
        
#     except Exception as e:
#         error_message = f"Error downloading file from S3: {e}"
#         frappe.logger().error(error_message, exc_info=True)
#         print(error_message)


    # Replace this with your actual S3 key as used during upload.





import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def download_result_by_key(encryption_key):
    """
    Retrieves a pre-generated S3 pre-signed URL based on the encryption key
    and redirects the user's browser to it for direct download from S3.
    Returns simple errors on failure without tracebacks.
    """
    try:
        # Step 1: Attempt to retrieve the stored S3 URL
        student_info = frappe.db.get_value(
            "Online Student",
            {"encryption_key": encryption_key},
            ["result_pdf_attachment"], # Fetch only the field containing the S3 URL
            as_dict=True
        )

        # Step 2: Validate if the student and URL exist
        if not student_info:
            # Invalid encryption key - Student not found
            frappe.local.response.http_status_code = 403 # Forbidden
            return {"status": "error", "message": _("Invalid or expired link.")}

        s3_presigned_url = student_info.get("result_pdf_attachment")

        if not s3_presigned_url or not s3_presigned_url.startswith('https://'):
            # Student found, but the URL is missing or invalid
            frappe.local.response.http_status_code = 404 # Not Found
            return {"status": "error", "message": _("Result PDF not available yet. Please try again later.")}

        # Step 3: If valid, perform the redirect
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = s3_presigned_url
        # No explicit return value is sent when redirecting

    except Exception:
        # Catch any other unexpected issues (database down, etc.)
        frappe.local.response.http_status_code = 500 # Internal Server Error
        return {"status": "error", "message": _("Something went wrong while processing your request.")}




# Script to enqueue PDF generation (Run via `bench execute` or create a Server Script)
import frappe
from frappe.utils.background_jobs import enqueue
import logging

logger = logging.getLogger("pdf_generation_s3")

@frappe.whitelist()
def enqueue_pdf_generation_for_students_manual_s3():
    """Enqueues background jobs for PDF generation and manual S3 upload."""
    # Define criteria for students needing PDFs (adjust filter as needed)
    # Filter for students *without* a result PDF URL yet
    students = frappe.get_all(
        "Online Student",
        filters={
            # "docstatus": 1,
            "result_pdf_attachment": ["is", "not set"],
            # Add any other relevant filters, e.g., specific academic year, batch etc.
            # "academic_year": "2023-24"
        },
        fields=["name", "encryption_key"]
    )

    count = 0
    total = len(students)
    logger.info(f"Found {total} students needing PDF generation.")

    for student in students:
        if not student.encryption_key:
            logger.warning(f"Skipping student {student.name} due to missing encryption key.")
            continue

        # Enqueue the generation task for each student
        enqueue(
            "tnc_frappe_custom_app.result_sharing.generate_and_save_student_pdf_manual_s3", # Path to your NEW background function
            queue="long",      # Use 'long' queue for potentially lengthy jobs
            timeout=1800,      # Increase timeout (e.g., 30 mins)
            student_name=student.name,
            encryption_key=student.encryption_key
        )
        count += 1
        if count % 100 == 0: # Log progress every 100 students
             logger.info(f"Enqueued {count}/{total} PDF generation jobs...")
        break

    logger.info(f"Finished enqueueing PDF generation for {count} students.")
    print(f"Finished enqueueing PDF generation for {count} students.") # Also print for bench execute

# To run this from bench console:
# bench --site [your.site.name] execute tnc_frappe_custom_app.result_sharing.enqueue_pdf_generation_for_students_manual_s3



@frappe.whitelist()
def generate_and_save_student_pdf_manual_s3(student_name, encryption_key):
    """
    Generates a student result PDF using the CORRECT two-step process:
    1. frappe.get_print to get HTML.
    2. frappe.utils.pdf.get_pdf to convert HTML to PDF bytes.
    Uploads to S3, stores pre-signed URL, returns JSON status.
    """
    local_pdf_path = None # Initialize for finally block (if using local save)
    try:
        student_doc = frappe.get_doc("Online Student", student_name)

        # --- Check if PDF URL already exists ---
        if student_doc.result_pdf_attachment and student_doc.result_pdf_attachment.startswith('https://'):
            # ... (skipped logic) ...
            return {'status': 'skipped', 'message': f"Skipping {student_name}, URL exists."}

        logger.info(f"Starting PDF generation process for {student_name}...")

        # --- Get S3 Credentials ---
        # ... (same as before) ...
        try:
            admin_settings = frappe.get_single("Admin Settings")
            bucket_name = admin_settings.bucket
            region_name = admin_settings.region_name
            access_key = admin_settings.get_password("access_key")
            secret_key = admin_settings.get_password("secret_key")
            if not all([bucket_name, region_name, access_key, secret_key]):
                raise ValueError("Incomplete S3 credentials")
        except Exception as cred_err:
            error_message = f"Failed to get S3 credentials for {student_name}: {cred_err}"
            logger.error(error_message, exc_info=True)
            return {'status': 'error', 'message': error_message}

        # --- CORRECTED PDF GENERATION ---
        # --- Step 1: Generate Print Format HTML ---
        try:
            print_format_name = "Student Results Top Performer"
            letterhead_name = "TNC Logo"
            logger.info(f"Generating HTML using frappe.get_print for Doc: {student_name}, Format: {print_format_name}")

            # Use frappe.get_print to render the HTML
            # It takes doctype, name, print_format name, and other options
            generated_html = frappe.get_print(
                doctype="Online Student",
                name=student_name,
                print_format=print_format_name,
                doc=student_doc, # Pass the loaded doc for context
                no_letterhead=(letterhead_name is None), # Set no_letterhead based on letterhead_name
                letterhead=letterhead_name,
                # Add other options if needed, e.g., print_settings, lang
            )

            if not generated_html:
                 raise ValueError("frappe.get_print did not return any HTML content.")
            logger.info(f"HTML generated successfully for {student_name}")

        except Exception as html_gen_err:
             error_message = f"Failed to generate HTML content for {student_name} using print format '{print_format_name}': {html_gen_err}"
             logger.error(error_message, exc_info=True)
             # Check if print format exists, if wkhtmltopdf path is correct etc.
             return {'status': 'error', 'message': error_message}

        # --- Step 2: Generate PDF Bytes from HTML using get_pdf ---
        try:
            logger.info(f"Generating PDF bytes from HTML for {student_name} using get_pdf...")
            # Pass the generated HTML to the actual get_pdf function
            pdf_content_bytes = get_pdf(html=generated_html, options={}) # Pass empty options or customize if needed

            if not isinstance(pdf_content_bytes, bytes) or len(pdf_content_bytes) < 100:
                 raise ValueError(f"get_pdf returned invalid content from HTML. Size: {len(pdf_content_bytes) if isinstance(pdf_content_bytes, bytes) else 'Not bytes'}")
            logger.info(f"PDF content bytes generated for {student_name} ({len(pdf_content_bytes)} bytes)")

        except Exception as pdf_gen_err:
             error_message = f"Failed to generate PDF bytes from HTML for {student_name}: {pdf_gen_err}"
             logger.error(error_message, exc_info=True)
             return {'status': 'error', 'message': error_message}


        # --- Define S3 Key ---
        safe_key_part = ''.join(filter(str.isalnum, encryption_key))
        s3_key = f"student_results/{safe_key_part}_{student_name.replace(' ', '_')}_test_again.pdf"
        logger.info(f"Generated S3 key: {s3_key}")

        # --- Upload to S3 using BytesIO ---
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region_name
            )
            pdf_stream = io.BytesIO(pdf_content_bytes) # Use the bytes generated in Step 2
            s3_client.upload_fileobj(
                Fileobj=pdf_stream,
                Bucket=bucket_name,
                Key=s3_key,
                ExtraArgs={'ContentType': 'application/pdf'}
            )
            logger.info(f"Successfully uploaded PDF stream to S3 Key: {s3_key}")
        except Exception as s3_err:
            error_message = f"Failed to upload PDF stream to S3 for {student_name}: {s3_err}"
            logger.error(error_message, exc_info=True)
            return {'status': 'error', 'message': error_message}


        # --- Generate Pre-signed URL ---
        # ... (same as before) ...
        try:
            presigned_url = s3_client.generate_presigned_url(
                ClientMethod='get_object',        # The S3 operation
                Params={                          # Parameters for the 'get_object' operation
                    'Bucket': bucket_name,
                    'Key': s3_key,
                    'ResponseContentType': 'application/pdf' # Hint for browser download
                },
                ExpiresIn=604800                  # URL validity duration in seconds (7 days)
            )
            logger.info(f"Generated pre-signed URL: {presigned_url}")
        except Exception as presigned_url_err:
            # ... error handling ...
            return {'status': 'error', 'message': f"Failed pre-signed URL: {presigned_url_err}"}


        # --- Update Student Record ---
        # ... (same as before) ...
        try:
             student_doc.db_set("result_pdf_attachment", presigned_url)
        except Exception as db_update_err:
            # ... error handling ...
            return {'status': 'error', 'message': f"Failed DB update: {db_update_err}"}


        # --- Return Success ---
        success_message = f"Successfully processed using get_print/get_pdf for {student_name}"
        logger.info(success_message)
        return {'status': 'success', 'message': success_message, 'url': presigned_url}

    except Exception as e:
        # Catch any unexpected errors
        error_message = f"Overall failure (corrected method) for {student_name}: {str(e)}"
        logger.error(error_message, exc_info=True)
        return {'status': 'error', 'message': error_message}
