import frappe
from webtoolex_whatsapp.webtoolex_whatsapp.doctype.whatsapp_instance.whatsapp_instance import send_custom_whatsapp_message


def custom_task_notification_on_insert(doc,method):
    if doc.owner != doc.task_owner:
        employee = frappe.db.get_value("Employee",{"user_id":doc.task_owner},"name")
        if employee:

            send_task_notification(doc,employee)




def custom_task_notification_on_update(doc, method):
    before_doc = doc.get_doc_before_save()
    if not before_doc:
        return

    if before_doc.task_owner != doc.task_owner:
        if doc.task_owner:
            frappe.share.add(
                "Task",
                doc.name,
                doc.task_owner,
                read=1,
                write=1,
                share=1,
                notify=0
            )
            employee = frappe.db.get_value("Employee",{"user_id":doc.task_owner},"name")
            if employee:
                send_task_notification(doc,employee)

        if before_doc.task_owner:
            frappe.share.remove("Task", doc.name, before_doc.task_owner)



def send_task_notification(task, employee):

    emp_doc = frappe.get_doc("Employee",employee)
    if not emp_doc.cell_number:
        frappe.log_error(title = "Error sending task assignment WA", message = f"Employee {emp_doc.name} has no mobile number for notify regarding task {task.name} assignment")
        return {"status":False,"msg":f"Employee {emp_doc.name} has no mobile number for notify regarding task {task.name} assignment"}
    
    
    message = f"""Dear {emp_doc.employee_name},

You have been assigned a new task: {task.subject}

Regards 
TNC Admin
"""
    
    mobile_number = emp_doc.cell_number
    # mobile_number = "9098543046"
    resp = send_custom_whatsapp_message(mobile_number, message)
    frappe.log_error(title = "sending task assignment WA", message = f"Response from send_custom_whatsapp_message: {resp}")
    return resp

            