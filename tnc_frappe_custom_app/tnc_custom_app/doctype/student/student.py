# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

import frappe

class Student(Document):
    # def validate(self):
    def before_insert(self):
        self.check_duplicate_mobile()

    def check_duplicate_mobile(self):
        if self.mobile:
            # Check if any other student has the same mobile number
            existing_student = frappe.db.exists("Student", {"mobile": self.mobile, "name": ["!=", self.name]})
            
            if existing_student:
                # Raise an error if a duplicate is found
                frappe.throw(f"Mobile number {self.mobile} is already registered with another student.")
