# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt



import frappe
from frappe.model.document import Document

import frappe
from frappe.model.document import Document

# class StudentResults(Document):
#     def before_insert(self):
#         # Ensure that the student_mobile is provided
#         if self.student_mobile:
#             # Check if the student already exists based on the mobile number
#             student_exists = frappe.db.exists('Student', {'mobile': self.student_mobile})
            
#             if not student_exists:
#                 # If the student does not exist, create a new Student record
#                 new_student = frappe.get_doc({
#                     'doctype': 'Student',
#                     'student_name': self.student_name,
#                     'mobile': self.student_mobile
#                 })
#                 new_student.insert(ignore_permissions=True)
#                 frappe.msgprint(f"New Student created: {self.student_name}")
#                 # Link the new student's ID to the Student Results record
#                 self.student_id = new_student.name
#             else:
#                 # If the student exists, fetch the student ID and update the Student Results record
#                 student = frappe.get_doc('Student', student_exists)
#                 self.student_id = student.name
#         else:
#             frappe.throw("Student Mobile is required to create a Student record.")

#################################### Above code is previous code #####################################

# import frappe
# from frappe.model.document import Document
# from frappe import _

# class StudentResults(Document):
#     def before_insert(self):
#         self.check_duplicate_entry()

#     def check_duplicate_entry(self):
#         # Check if a record with the same exam_name, exam_date, and student_mobile already exists
#         duplicate_entry = frappe.db.exists('Student Results', {
#             'exam_name': self.exam_name,
#             'exam_date': self.exam_date,
#             'student_mobile': self.student_mobile
#         })

#         if duplicate_entry:
#             frappe.throw(_("A record with the same Exam Name, Exam Date, and Student Mobile already exists."))

########################## Below code is working good code ###########################


# import frappe
# from frappe.model.document import Document
# from frappe import _

# class StudentResults(Document):
#     def before_save(self):
#         self.check_duplicate_entry()

#     def check_duplicate_entry(self):
#         # Check if a record with the same exam_name, exam_date, and student_mobile already exists
#         duplicate_entry = frappe.db.exists('Student Results', {
#             'exam_name': self.exam_name,
#             'exam_date': self.exam_date,
#             'student_mobile': self.student_mobile,
#             'name': ['!=', self.name]  # Exclude the current document from the check
#         })

#         if duplicate_entry:
#             frappe.throw(_("A record with the same Exam Name, Exam Date, and Student Mobile already exists."))

############### Above code is validating the duplicate Student Results withexam_name,exam_date,student_mobile ##################


# import frappe
# from frappe.model.document import Document

# class StudentResults(Document):
#     def before_save(self):
#         # Ensure that the student_mobile is provided
#         if self.student_mobile:
#             # Check if the student already exists based on the mobile number
#             student_exists = frappe.db.exists('Student', {'mobile': self.student_mobile})
            
#             if not student_exists:
#                 # If the student does not exist, create a new Student record
#                 new_student = frappe.get_doc({
#                     'doctype': 'Student',
#                     'student_name': self.student_name,
#                     'mobile': self.student_mobile,
#                     # 'district': self.district,  # Add other fields if necessary
#                     # 'state': self.state
#                 })
#                 new_student.insert(ignore_permissions=True)
#                 # Log the creation of the new student
#                 frappe.msgprint(f"New Student created: {self.student_name}")
#                 # Link the new student's ID to the Student Results record
#                 self.student_id = new_student.name
#             else:
#                 # If the student exists, fetch the student ID and update the Student Results record
#                 student = frappe.get_doc('Student', student_exists)
#                 self.student_id = student.name
#         else:
#             frappe.throw("Student Mobile is required to create or link a Student record.")



############### Above code is creating a new student record in the Student Results doctype ###################


##################  Combined of aBove two codes ###############



import frappe
from frappe.model.document import Document
from frappe import _

class StudentResults(Document):
    def before_save(self):
        self.check_duplicate_entry()
        self.ensure_student_exists()

    def check_duplicate_entry(self):
        # Check if a record with the same exam_name, exam_date, and student_mobile already exists
        duplicate_entry = frappe.db.exists('Student Results', {
            'exam_name': self.exam_name,
            'exam_date': self.exam_date,
            'student_mobile': self.student_mobile,
            'name': ['!=', self.name]  # Exclude the current document from the check
        })

        if duplicate_entry:
            frappe.log_error(f"Bulk Sync fail.{self.exam_name}{self.exam_date}{self.student_mobile}")
            frappe.throw(_("A record with the same Exam Name, Exam Date, and Student Mobile already exists."))

    def ensure_student_exists(self):
        # Ensure that the student_mobile is provided
        if self.student_mobile:
            # Check if the student already exists based on the mobile number
            student_exists = frappe.db.exists('Student', {'mobile': self.student_mobile})
            
            if not student_exists:
                # If the student does not exist, create a new Student record
                new_student = frappe.get_doc({
                    'doctype': 'Student',
                    'student_name': self.student_name,
                    'mobile': self.student_mobile,
                    # 'district': self.district,  # Add other fields if necessary
                    # 'state': self.state
                })
                new_student.insert(ignore_permissions=True)
                # Log the creation of the new student
                frappe.msgprint(f"New Student created: {self.student_name}")
                # Link the new student's ID to the Student Results record
                self.student_id = new_student.name
            else:
                # If the student exists, fetch the student ID and update the Student Results record
                self.student_id = frappe.get_value('Student', {'mobile': self.student_mobile}, 'name')
        else:
            frappe.throw(_("Student Mobile is required to create or link a Student record."))


