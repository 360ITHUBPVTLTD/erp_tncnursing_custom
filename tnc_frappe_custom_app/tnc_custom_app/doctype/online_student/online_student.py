# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

################### Below code give the Actual count of OnlineStudent Master Data to the OnlineStudent Exam based on their ID #################################################################

class OnlineStudent(Document):
    # def validate(self):
    # def before_insert(self):
    #     self.check_duplicate_mobile()

    def check_duplicate_mobile(self):
        if self.mobile:
            # Check if any other online_student has the same mobile number
            existing_online_student = frappe.db.exists("Online Student", {"mobile": self.mobile, "name": ["!=", self.name]})
            
            if existing_online_student:
                # Raise an error if a duplicate is found
                frappe.throw(f"Mobile number {self.mobile} is already registered with another online student.")
