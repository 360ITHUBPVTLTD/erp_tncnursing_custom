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


from frappe.utils.print_format import download_pdf
 
@frappe.whitelist(allow_guest=True)
def download_result_by_key(encryption_key):
    # Step 1: Get student name based on encryption key
    student_name = frappe.get_value("Online Student", {"encryption_key": encryption_key}, "name")
    if not student_name:
        frappe.throw("Invalid or expired key")
 
    # Step 2: Call the correct print function
    return download_pdf(
        doctype="Online Student",
        name=student_name,
        format="Student Results Top Performer",
        no_letterhead=0,
        letterhead="TNC Logo",
        # settings={},
        # _lang="en"
    )




