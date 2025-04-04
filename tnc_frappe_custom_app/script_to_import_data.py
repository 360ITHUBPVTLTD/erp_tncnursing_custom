# import frappe
# import os
# from datetime import datetime
from tnc_frappe_custom_app.tnc_custom_app.doctype.student_exam.student_exam import student_process_data
# import pandas as pd
# def process_excel_to_create_a_student_exam(file_path, batch_size=5000):
#     try:
#         # Read CSV file into DataFrame
#         df = pd.read_csv(file_path)

#         if df.empty:
#             frappe.throw("Uploaded CSV file is empty.")

#         # Extract exam details
#         exam_name = df.iloc[0]['Exam Name']  # Assume same exam name for all rows
#         exam_date = datetime.today().strftime('%Y-%m-%d')  # Set today's date

#         # Extract filename without extension for exam title
#         exam_title_name = os.path.splitext(os.path.basename(file_path))[0]

#         # Check if Student Exam already exists
#         existing_exam = frappe.db.exists('Student Exam', {'exam_title_name': exam_title_name})
#         if existing_exam:
#             frappe.throw(f"Student Exam with title '{exam_title_name}' already exists.")
        
#         # Create Student Exam document
#         student_exam = frappe.get_doc({
#             'doctype': 'Student Exam',
#             'exam_name': exam_name,
#             'exam_title_name': exam_title_name,  # Corrected filename extraction
#             'exam_date': exam_date,
#         })
#         student_exam.insert()
#         frappe.db.commit()

#         # Get newly created Student Exam ID (docname)
#         student_exam_id = student_exam.name

#         # Update the 'Exam ID' column for all rows that have data
#         df['Exam ID'] = student_exam_id

#         # Clean the data by replacing NaN values with defaults
#         numeric_columns = ['Rank', 'Total Marks', 'Percentage', 'Total Right', 'Total Wrong', 'Total Skip']
#         for column in numeric_columns:
#             df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)  # Replace NaN with 0 for numeric columns

#         text_columns = ['Student Name', 'Mobile', 'District', 'State']
#         for column in text_columns:
#             df[column] = df[column].fillna("")  # Replace NaN with empty string for text columns

#         # Iterate over the rows and insert data into Student Master Data doctype
#         for index, row in df.iterrows():
#             student_master_data = frappe.get_doc({
#                 'doctype': 'Students Master Data',
#                 'exam_id': student_exam_id,
#                 'student_name': row['Student Name'],
#                 'mobile': row['Mobile'],
#                 'district': row['District'],
#                 'state': row['State'],
#                 'rank': row['Rank'],
#                 'total_marks': row['Total Marks'],
#                 'total_right': row['Total Right'],
#                 'total_wrong': row['Total Wrong'],
#                 'total_skip': row['Total Skip'],
#                 'percentage': row['Percentage'],
#             })
#             student_master_data.insert()

#         frappe.db.commit()

#         # Optional: Save the modified DataFrame back to a CSV (for debugging purposes)
#         modified_file_path = file_path.replace(".csv", "_modified.csv")
#         df.to_csv(modified_file_path, index=False)

#         # Optionally, enqueue a function to process the data after insertion
#         student_process_data(student_exam_id, limit=1)

#         return f"Student Exam '{exam_title_name}' created and data inserted successfully."

#     except Exception as e:
#         # Log the error in case of failure
#         frappe.log_error(f"Error processing student results: {str(e)}")
#         raise e




# @frappe.whitelist()
# def process_excel_to_create_a_student_exam_from_client_script(file_id):
#     try:
#         # Fetch file document
#         file_doc = frappe.get_doc("File", file_id)
#         file_url = file_doc.file_url.strip('/')  # Remove leading/trailing slashes
#         print("File URL:", file_url)  # Debugging

#         # Determine file path
#         if file_url.startswith("files/"):
#             file_path = frappe.get_site_path("public", "files", os.path.basename(file_url))
#         elif file_url.startswith("private/files/"):
#             file_path = frappe.get_site_path("private", "files", os.path.basename(file_url))
#         else:
#             raise FileNotFoundError(f"Invalid file URL: {file_url}")

#         print("Resolved File Path:", file_path)  # Debugging

#         # Check if file exists before processing
#         if not os.path.exists(file_path):
#             raise FileNotFoundError(f"File not found at {file_path}")

#         # Enqueue background job
#         enqueue(
#             process_excel_to_create_a_student_exam,
#             queue="long",
#             timeout=6000,
#             job_name="process_student_results",
#             file_path=file_path,
#             batch_size=5000
#         )
#         return "Data processing started. Check the Job logs for updates."

#     except Exception as e:
#         frappe.log_error(f"Error in import_student_results_sql_student_master_data: {str(e)}")
#         raise e



################ Above code is Single File Parsing ################



############### Below code is Bulk ######################

import frappe
import os
import pandas as pd
from datetime import datetime

@frappe.whitelist()
def process_all_csv_files_in_folder():
    """
    Fetch all CSV files from 'Bulk Upload' in File List and process them.
    """
    try:
        # Get all CSV files in 'Bulk Upload' folder
        files = frappe.get_all(
            "File",
            filters={"folder": "Home/Bulk Upload", "file_name": ["like", "%.csv"]},
            fields=["file_url", "file_name"]
        )

        if not files:
            frappe.throw("No CSV files found in 'Bulk Upload'!")

        processed_files = []

        for file in files:
            file_url = file["file_url"]

            # Ensure we correctly resolve the file path
            if file_url.startswith("/private/files/"):
                file_path = frappe.get_site_path("private", "files", file_url.replace("/private/files/", ""))
            elif file_url.startswith("/public/files/"):
                file_path = frappe.get_site_path("public", "files", file_url.replace("/public/files/", ""))
            else:
                frappe.throw(f"Invalid file path: {file_url}")

            # Check if file exists
            if not os.path.exists(file_path):
                frappe.throw(f"File not found: {file_path}")

            # Enqueue processing function for each file asynchronously
            frappe.enqueue(process_excel_to_create_a_student_exam, file_path=file_path)
            processed_files.append(file["file_name"])

        return f"Processing started for {len(processed_files)} files: {', '.join(processed_files)}"

    except Exception as e:
        frappe.log_error(f"Error processing bulk uploads: {str(e)}")
        return f"Error: {str(e)}"

import frappe
import os
import pandas as pd
from datetime import datetime
from tnc_frappe_custom_app.tnc_custom_app.doctype.student_exam.student_exam import student_process_data
import numpy as np

@frappe.whitelist()
def process_excel_to_create_a_student_exam(file_path):
    """
    Reads a CSV file, creates a Student Exam, inserts student records,
    and then processes the exam data.
    """
    try:
        if not os.path.exists(file_path):
            frappe.throw(f"File '{file_path}' does not exist.")

        df = pd.read_csv(file_path)

        if df.empty:
            frappe.throw(f"Uploaded CSV file '{file_path}' is empty.")

        # Extract exam details
        exam_name = df.iloc[0].get('Exam Name', '').strip()
        if not exam_name:
            frappe.throw("Exam Name is missing in the CSV file.")
        
        exam_date = datetime.today().strftime('%Y-%m-%d')
        exam_title_name = os.path.splitext(os.path.basename(file_path))[0]

        # Check if Student Exam already exists
        if frappe.db.exists('Student Exam', {'exam_title_name': exam_title_name}):
            frappe.throw(f"Student Exam '{exam_title_name}' already exists.")

        # Create Student Exam
        student_exam = frappe.get_doc({
            'doctype': 'Student Exam',
            'exam_name': exam_name,
            'exam_title_name': exam_title_name,
            'exam_date': exam_date,
        })
        student_exam.insert(ignore_permissions=True)
        
        student_exam_id = student_exam.name

        # Convert numeric columns safely
        numeric_columns = ['Rank', 'Total Marks', 'Percentage', 'Total Right', 'Total Wrong', 'Total Skip']
        for column in numeric_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)

        # Replace NaN values with None
        df = df.where(pd.notna(df), None)

        # Insert student data
        for _, row in df.iterrows():
            student_data = {
                'doctype': 'Students Master Data',
                'exam_id': student_exam_id,
                'student_name': row.get('Student Name', ''),
                'mobile': row.get('Mobile', ''),
                'district': row.get('District', ''),
                'state': row.get('State', ''),
                'rank': row.get('Rank', 0),
                'total_marks': row.get('Total Marks', 0),
                'total_right': row.get('Total Right', 0),
                'total_wrong': row.get('Total Wrong', 0),
                'total_skip': row.get('Total Skip', 0),
                'percentage': row.get('Percentage', 0),
            }
            student_master_data = frappe.get_doc(student_data)
            student_master_data.insert(ignore_permissions=True)
            # break  # Only insert the first row
        # ✅ Commit before processing to ensure data is saved
        frappe.db.commit()
        frappe.log_error(f"Calling student_process_data for Exam ID: {student_exam_id}")
        # student_process_data(student_exam_id)  # Direct function call

        # ✅ Enqueue `student_process_data`
        frappe.enqueue(student_process_data, name=student_exam_id, limit=1,bulk_file_read=True, queue="long", timeout=3000)
    
        return f"Student Exam '{exam_title_name}' created successfully and processing started."

    except Exception as e:
        frappe.log_error(f"Error processing CSV file {file_path}: {str(e)}")
        return f"Error: {str(e)}"





























































































































############################# Below script is upload the Student Results doctype #############################


# import frappe
# import pandas as pd
# from rq import Queue
# from redis import Redis
# import math
# import numpy as np

# # Initialize Redis connection and RQ queue
# redis_conn = Redis()
# queue = Queue('default', connection=redis_conn)

# # Function to process the batch of records and upload to the "Student Results" doctype
# def upload_batch(batch_data_list):
#     try:
#         count = 0
#         # Iterate over the batch data
#         for row in batch_data_list:
#             # Replace NaN values with None
#             row = {key: (None if isinstance(value, float) and np.isnan(value) else value) for key, value in row.items()}
            
#             # Create a new record in the 'Student Results' Doctype
#             doc = frappe.get_doc({
#                 "doctype": "Student Results",
#                 "old_id": row.get("ID"),
#                 "student_name": row.get("Student Name"),
#                 "student_mobile": row.get("Student Mobile"),
#                 "exam_date": row.get("Exam Date"),
#                 "exam_id": row.get("Exam ID"),
#                 "exam_name": row.get("Exam Name"),
#                 "exam_title_name": row.get("Exam Title Name"),
#                 "percentage": row.get("Percentage"),
#                 "total_wrong": row.get("Total Wrong"),
#                 "total_skip": row.get("Total Skip"),
#                 "total_right": row.get("Total Right"),
#                 "total_marks": row.get("Total Marks"),
#                 "system_imported": row.get("System Imported"),
#                 "student_id": row.get("Student ID"),
#                 "rank_color": row.get("Rank Color"),
#                 "rank": row.get("Rank")
#             })

#             # Insert the document into the database
#             doc.insert()
#             count += 1
#             print("Student Results", count)

#         # Commit changes to the database
#         frappe.db.commit()

#         # Log success for this batch
#         frappe.log_error(f"Batch uploaded successfully with {len(batch_data_list)} records.")
    
#     except Exception as e:
#         # Rollback changes in case of any errors and log the error
#         frappe.db.rollback()
#         frappe.log_error(f"Error uploading batch: {str(e)}")
#         raise e

# # Function to read the Excel file, divide it into batches, and enqueue each batch for processing
# def process_excel_in_batches(file_path, batch_size=1000):
#     try:
#         # Load the Excel file into a pandas DataFrame
#         data = pd.read_excel(file_path)

#         # Total number of rows in the Excel file
#         total_rows = len(data)

#         # Calculate the number of batches
#         num_batches = math.ceil(total_rows / batch_size)

#         # Enqueue each batch
#         for batch_num in range(num_batches):
#             # Slice the DataFrame to get the batch data
#             start_idx = batch_num * batch_size
#             end_idx = min((batch_num + 1) * batch_size, total_rows)
#             batch_data = data[start_idx:end_idx]

#             # Convert batch_data (DataFrame) to a list of dictionaries
#             batch_data_list = batch_data.to_dict(orient="records")
#             print(batch_data_list) 

#             # Enqueue the batch job to the 'long' queue
#             # Pass batch_data_list as a single argument, and 'queue' as a keyword argument
#             frappe.enqueue('tnc_frappe_custom_app.script_to_import_data.upload_batch', batch_data_list=batch_data_list, queue='long')
            
#         frappe.log_error(f"Total {num_batches} batches enqueued for processing.")
#         return f"Total {num_batches} batches enqueued for processing."

#     except Exception as e:
#         frappe.log_error(f"Error processing Excel file: {str(e)}")
#         raise e


# # Usage Example
# @frappe.whitelist()
# def import_student_results():
#     file_path = "/home/pankaj/Documents/Student Results Xlxs.xlsx"
#     """
#     Function to import student results in batches.
#     :param file_path: Path to the Excel file
#     """
#     return process_excel_in_batches(file_path)





#################################### Student Master Data Migration code ######################################################################
import frappe
import pandas as pd
import math
from frappe import enqueue


def upload_batch_sql_student_master_data(batch_data_tuples):
    """
    Uploads a batch of student data to the database using SQL.
    Each insert query will insert 10 rows at a time.
    """
    try:
        
        print("upload_batch_sql: Batch Data:", batch_data_tuples)  # Debugging
        
        # SQL query template for bulk insert with placeholders
        sql_query = """
            INSERT INTO `tabStudents Master Data` (
                name, exam_id, student_name, mobile, district, state,
                rank, percentage, imported, total_marks, total_right,
                total_skip, total_wrong
            ) VALUES
        """

        # Check if each batch entry has 13 values, as required by the query
        for data in batch_data_tuples:
            if len(data) != 13:
                raise ValueError(f"Invalid data row: {data}. Expected 13 values.")
            print("Data to Insert:", data)  # Debugging

        # Process data in chunks of 10 records per query
        chunk_size = 10
        for i in range(0, len(batch_data_tuples), chunk_size):
            chunk = batch_data_tuples[i:i + chunk_size]
            
            # Prepare the values part for the current chunk
            # Replace None with NULL in each record
            chunk_values = []
            for data in chunk:
                # Convert None to NULL for SQL
                converted_data = [f"NULL" if value is None else f"'{value}'" for value in data]
                chunk_values.append(f"({', '.join(converted_data)})")
            
            # Join the values to form the complete part of the query
            values = ', '.join(chunk_values)
            
            # Full query with the values inserted
            full_query = sql_query + values

            # Execute the query with the batch data
            frappe.db.sql(full_query, as_dict=False)

        ###################### single insrts #################
        # for data in batch_data_tuples:
        #     # Replace None with None (as Frappe handles NULL automatically)
        #     student_record = frappe.get_doc({
        #         'doctype': 'Students Master Data',
        #         'old_id':data[0],
        #         'exam_id': data[1] if data[1] is not None else None,  # exam_id
        #         'student_name': data[2] if data[2] is not None else None,  # student_name
        #         'mobile': data[3] if data[3] is not None else None,  # mobile
        #         'district': data[4] if data[4] is not None else None,  # district
        #         'state': data[5] if data[5] is not None else None,  # state
        #         'rank': data[6] if data[6] is not None else None,  # rank
        #         'percentage': data[7] if data[7] is not None else None,  # percentage
        #         'imported': data[8] if data[8] is not None else None,  # imported
        #         'total_marks': data[9] if data[9] is not None else None,  # total_marks
        #         'total_right': data[10] if data[10] is not None else None,  # total_right
        #         'total_skip': data[11] if data[11] is not None else None,  # total_skip
        #         'total_wrong': data[12] if data[12] is not None else None,  # total_wrong
        #     })
            
        #     # Insert the student record
        #     student_record.insert()

        # Commit the transaction
        frappe.db.commit()

    except Exception as e:
        # Rollback changes in case of errors and log the error
        frappe.db.rollback()
        frappe.log_error(f"Error uploading batch: {str(e)}")
        print("Error:", e)  # Debugging
        raise e



def process_excel_in_batches_sql_student_master_data(file_path, batch_size=5000):
    """
    Processes an Excel file in batches and uploads the data to the database.
    """
    try:
        print("Starting batch processing for file:", file_path)  # Debugging
        frappe.log_error(f"Starting batch processing for file:, {file_path}")
        
        # Load the Excel file into a pandas DataFrame
        data = pd.read_excel(file_path)

        # Replace NaN values with None
        data = data.where(pd.notnull(data), None)

        # Total number of rows in the Excel file
        total_rows = len(data)

        # Calculate the number of batches
        num_batches = math.ceil(total_rows / batch_size)
        print(f"Total rows: {total_rows}. Number of batches: {num_batches}")  # Debugging
        frappe.log_error(f"Total rows: {total_rows}. Number of batches: {num_batches}")
        

        # Process each batch
        for batch_num in range(num_batches):
            start_idx = batch_num * batch_size
            end_idx = min((batch_num + 1) * batch_size, total_rows)
            batch_data = data.iloc[start_idx:end_idx]

            # Convert batch_data to tuples
            batch_data_tuples = list(batch_data.itertuples(index=False, name=None))

            # Process the batch using SQL
            upload_batch_sql_student_master_data(batch_data_tuples)
            # break

        return f"Total {num_batches} batches processed successfully."

    except Exception as e:
        frappe.log_error(f"Error processing Excel file: {str(e)}")
        raise e


@frappe.whitelist()
def import_student_results_sql_student_master_data(file_id):
    print("1111111111111111111111111111111")
    """
    Initiates the import of student results from an Excel file in the background.
    """
    try:
        print("Initiating import for file_id:", file_id)  # Debugging
        
        # Fetch the file document using the File ID
        file_doc = frappe.get_doc("File", file_id)
        file_url = file_doc.file_url
        file_path = frappe.get_site_path(file_url.strip('/'))

        # Enqueue the background job
        frappe.enqueue(
            "tnc_frappe_custom_app.script_to_import_data.process_excel_in_batches_sql_student_master_data",
            queue="long",
            timeout=6000,
            job_id="process_student_results",  # Use job_id instead of job_name
            file_path=file_path,
            batch_size=5000,
        )

        return "Data processing started. Check the Job logs for updates."

    except Exception as e:
        frappe.log_error(f"Error in import_student_results_sql: {str(e)}")
        raise e


######################################## Students Results Migration code #########################################

import frappe
import pandas as pd
import math
from frappe import enqueue


def upload_batch_sql_student_results(batch_data_tuples):
    """
    Uploads a batch of student data to the database using SQL.
    Each insert query will insert 10 rows at a time.
    """
    try:
        
        print("upload_batch_sql: Batch Data:", batch_data_tuples)  # Debugging
        
        # SQL query template for bulk insert with placeholders
        sql_query = """
            INSERT INTO `tabStudent Results` (
                name,student_name,student_mobile,exam_date,exam_id,
                exam_name,exam_title_name,percentage,total_wrong,total_skip,total_right,
                total_marks,system_imported,student_id,rank_color,rank

            ) VALUES
        """ 

        # Check if each batch entry has 13 values, as required by the query
        for data in batch_data_tuples:
            if len(data) != 16:
                raise ValueError(f"Invalid data row: {data}. Expected 13 values.")
            print("Data to Insert:", data)  # Debugging

        # Process data in chunks of 10 records per query
        chunk_size = 10
        for i in range(0, len(batch_data_tuples), chunk_size):
            chunk = batch_data_tuples[i:i + chunk_size]
            
            # Prepare the values part for the current chunk
            # Replace None with NULL in each record
            chunk_values = []
            for data in chunk:
                # Convert None to NULL for SQL
                converted_data = [f"NULL" if value is None else f"'{value}'" for value in data]
                chunk_values.append(f"({', '.join(converted_data)})")
            
            # Join the values to form the complete part of the query
            values = ', '.join(chunk_values)
            
            # Full query with the values inserted
            full_query = sql_query + values

            # Execute the query with the batch data
            frappe.db.sql(full_query, as_dict=False)

        # Commit the transaction
        frappe.db.commit()

    except Exception as e:
        # Rollback changes in case of errors and log the error
        frappe.db.rollback()
        frappe.log_error(f"Error uploading batch: {str(e)}")
        print("Error:", e)  # Debugging
        raise e



def process_excel_in_batches_sql_student_results(file_path, batch_size=5000):
    """
    Processes an Excel file in batches and uploads the data to the database.
    """
    try:
        print("Starting batch processing for file:", file_path)  # Debugging
        frappe.log_error(f"Starting batch processing for file:, {file_path}")
        
        # Load the Excel file into a pandas DataFrame
        data = pd.read_excel(file_path)

        # Replace NaN values with None
        data = data.where(pd.notnull(data), None)

        # Total number of rows in the Excel file
        total_rows = len(data)

        # Calculate the number of batches
        num_batches = math.ceil(total_rows / batch_size)
        print(f"Total rows: {total_rows}. Number of batches: {num_batches}")  # Debugging
        frappe.log_error(f"Total rows: {total_rows}. Number of batches: {num_batches}")
        

        # Process each batch
        for batch_num in range(num_batches):
            start_idx = batch_num * batch_size
            end_idx = min((batch_num + 1) * batch_size, total_rows)
            batch_data = data.iloc[start_idx:end_idx]

            # Convert batch_data to tuples
            batch_data_tuples = list(batch_data.itertuples(index=False, name=None))

            # Process the batch using SQL
            upload_batch_sql_student_results(batch_data_tuples)
            # break

        return f"Total {num_batches} batches processed successfully."

    except Exception as e:
        frappe.log_error(f"Error processing Excel file: {str(e)}")
        raise e


@frappe.whitelist()
def import_student_results_sql_student_results(file_id):
    print("1111111111111111111111111111111")
    """
    Initiates the import of student results from an Excel file in the background.
    """
    try:
        print("Initiating import for file_id:", file_id)  # Debugging
        
        # Fetch the file document using the File ID
        file_doc = frappe.get_doc("File", file_id)
        file_url = file_doc.file_url
        file_path = frappe.get_site_path(file_url.strip('/'))

        # Enqueue the background job
        frappe.enqueue(
            "tnc_frappe_custom_app.script_to_import_data.process_excel_in_batches_sql_student_results",
            queue="long",
            timeout=6000,
            job_id="process_student_results",  # Use job_id instead of job_name
            file_path=file_path,
            batch_size=5000,
        )

        return "Data processing started. Check the Job logs for updates."

    except Exception as e:
        frappe.log_error(f"Error in import_student_results_sql: {str(e)}")
        raise e
    









