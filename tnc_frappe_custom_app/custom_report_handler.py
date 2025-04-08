import frappe

@frappe.whitelist()
def handle_report_before_save(doc, method):
    report_existd = frappe.db.exists("Report", doc.report_name)
    if report_existd:
        if doc.prepared_report == 1:
            doc.prepared_report = 0
            doc.save()