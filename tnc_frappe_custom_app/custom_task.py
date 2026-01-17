import frappe
from webtoolex_whatsapp.webtoolex_whatsapp.doctype.whatsapp_instance.whatsapp_instance import send_custom_whatsapp_message

def custom_task_notification_on_insert(doc, method):
    # Only notify if assigned to someone else

    queue_notification(doc)

def custom_task_notification_on_update(doc, method):
    before_doc = doc.get_doc_before_save()
    if not before_doc:
        return

    # Only notify if the owner CHANGED to someone else
    if before_doc.task_owner != doc.task_owner and doc.task_owner:
        queue_notification(doc)

def queue_notification(doc):
    """
    Push to queue ONLY if the transaction commits successfully.
    """
    frappe.enqueue(
        method="tnc_frappe_custom_app.custom_task.async_send_whatsapp",
        queue="short",
        enqueue_after_commit=True,  # <--- THIS IS THE KEY FOR V15
        # Pass primitive data types (str, int), avoid passing whole 'doc' objects to queue
        task_owner=doc.task_owner,
        task_id=doc.name,
        subject=doc.subject,
        task_name=doc.name
    )

def async_send_whatsapp(task_owner, task_id, subject, task_name):
    """
    This runs in background. 
    Because of enqueue_after_commit=True, we know the Task exists and is saved.
    """
    
    # 1. Fetch Employee from User ID
    # Note: Using get_value is faster than get_doc if we just need one field, 
    # but we need name and cell_number, so let's get the doc or value dict.
    employee_details = frappe.db.get_value(
        "Employee", 
        {"user_id": task_owner}, 
        ["name", "employee_name", "cell_number"], 
        as_dict=True
    )

    if not employee_details:
        # User is not an employee, stop.
        return

    if not employee_details.cell_number:
        frappe.log_error(
            title="WhatsApp Notification Failed", 
            message=f"Employee {employee_details.employee_name} ({employee_details.name}) has no mobile number for Task {task_name}"
        )
        return

    # 2. Construct Message
    message = f"""Dear {employee_details.employee_name},

You have been assigned a new task: ({task_id})
{subject}

Regards 
TNC Admin
"""

    # 3. Send via WhatsApp API
    try:
        resp = send_custom_whatsapp_message(employee_details.cell_number, message)
    except Exception as e:
        frappe.log_error(title="WhatsApp API Error", message=f"{str(e)} | Task: {task_name}")