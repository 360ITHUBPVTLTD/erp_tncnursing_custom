# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StudentsMasterData(Document):
    pass




######## It is creating a BatchID with the same record #########

# import frappe
# from datetime import datetime

# # Global variable to hold the current batch timestamp
# current_batch_timestamp = None

# def before_insert(doc, method):
#     global current_batch_timestamp

#     # Check if it's the first record in the batch (i.e., timestamp is not set)
#     if not current_batch_timestamp:
#         # Assign the current date and time (including milliseconds)
#         current_batch_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

#     # Set the imported_batch_id field to the batch timestamp
#     doc.imported_batch_id = current_batch_timestamp

