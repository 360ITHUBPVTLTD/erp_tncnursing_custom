# import frappe

# def handle_data_import_after_save(doc, method):
#     # frappe.log_error("IT is Geting errror Please see the hooks.py")
#     # Check conditions
#     exam_id=frappe.get_all("Students Master Data",filters={"exam_id":None})
#     frappe.log_error(f"Students Master Data {len(exam_id)}")
#     if doc.reference_doctype == 'Students Master Data' and doc.status == 'Success' and \
#         doc.custom_exam_id and not doc.custom_records_linked_with_exam_id:
#         # Update the exam_id field in Student Master Data
#         frappe.log_error("After condition I am getting errror")
#         frappe.db.set_value(
#             'Students Master Data',
#             filters={'exam_id': ('in',[None])},
#             fieldname='exam_id',
#             value=doc.custom_exam_id
#         )
#         print("Hello world!")
#         doc.custom_records_linked_with_exam_id = 1
      
#         print(doc.custom_exam_id)
#         frappe.db.commit()
#         frappe.log_error("After commit in the error Please check the after_commit")
#         print("File ID succefully!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#         doc.save()
#         frappe.msgprint(('Student Master Data records updated successfully.'))


import frappe

@frappe.whitelist()
def update_imported_batch_id(exam_id):
    # Find all records in Student Master Data where exam_id is empty or null
    student_records = frappe.get_all(
        'Students Master Data', 
        filters=[['exam_id', 'in', [None, '']]],
        fields=['name']
    )
    
    if not student_records:
        return {'status': 'error', 'message': 'No Student Master Data records found without exam_id.'}
    
    # Update each Student Master Data record with the provided exam_id
    for record in student_records:
        frappe.db.set_value('Students Master Data', record['name'], 'exam_id', exam_id)
    
    frappe.db.commit()
    
    return {'status': 'success', 'message': 'Student Master Data records updated successfully.'}
