# your_custom_app/your_module_name/doctype/student_master_data/student_master_data.py

import frappe

@frappe.whitelist()
def delete_all_records():
    try:
        frappe.db.sql("DELETE FROM `tabStudents Master Data`")
        frappe.db.commit()
        return 'success'
    except Exception as e:
        frappe.log_error(message=str(e), title="Error in Deleting Student Master Data")
        return 'error'

@frappe.whitelist()
def delete_all_records_in_student_results():
    try:
        frappe.db.sql("DELETE FROM `tabStudent Results`")
        frappe.db.commit()
        return 'success'
    except Exception as e:
        frappe.log_error(message=str(e), title="Error in Deleting Student Master Data")
        return 'error'
    
    delete_all_records_in_student

@frappe.whitelist()
def delete_all_records_in_student():
    try:
        frappe.db.sql("DELETE FROM `tabStudent`")
        frappe.db.commit()
        return 'success'
    except Exception as e:
        frappe.log_error(message=str(e), title="Error in Deleting Student Master Data")
        return 'error'
    


import frappe

@frappe.whitelist()
def uncheck_imported():
    try:
        # Uncheck the imported field for all records
        frappe.db.sql("""
            UPDATE `tabStudents Master Data`
            SET imported = 0
        """)
        frappe.db.commit()
        return "success"
    except Exception as e:
        frappe.log_error(f"Error unchecking imported field: {e}")
        return "error"
