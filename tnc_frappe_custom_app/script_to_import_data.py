

import frappe
import pandas as pd

@frappe.whitelist()
def import_online_students():
    """
    Import data from a CSV file into the 'Online Student' Doctype.
    """
    try:
        file_path = "/home/pankaj/Documents/Book1(Onlinie student test).xlsx"
        
        # Load the CSV file
        data = pd.read_excel(file_path)

        # Replace NaN values with None (or another default value if necessary)
        data = data.apply(lambda x: x.map(lambda v: None if isinstance(v, float) and pd.isna(v) else v))
        count = 0
        # Iterate over rows in the dataframe
        for _, row in data.iterrows():
            # Check if 'student_name' or 'mobile' is missing, and skip the row if necessary
            # if pd.isna(row.get("Student Name")) or pd.isna(row.get("Mobile")):
            #     # Log or skip the row if mandatory fields are missing
            #     frappe.log_error(f"Skipping record due to missing mandatory fields: {row}")
            #     continue  # Skipping the row with missing fields

            # Create a new record in the 'Online Student' Doctype
            doc = frappe.get_doc({
                "doctype": "Online Student",
                "docname": row.get("ID"),
                "student_name": row.get("Student Name"),
                "mobile": row.get("Mobile"),
                "state": row.get("State"),
                "district": row.get("District"),
                "exam_id": row.get("Exam ID"),
                "total_exams": row.get("Total Exams"),
                "system_imported": row.get("System Imported"),
                "payment_link": row.get("Payment Link")
            })

            # Insert the record into the database
            
            doc.insert()
            count += 1
            print("Student",count,row.get("ID"))

        # Commit changes to the database
        frappe.db.commit()
        return "Data imported successfully!"

    except Exception as e:
        # Rollback changes in case of any errors
        frappe.db.rollback()
        frappe.throw(f"An error occurred: {e}")



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
    