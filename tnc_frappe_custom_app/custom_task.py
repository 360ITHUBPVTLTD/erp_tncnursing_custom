import frappe

# -------------------------------------------------------------------------
# HOOKS
# -------------------------------------------------------------------------

def custom_task_notification_on_insert(doc, method):
    """
    On Creation: Notify Task Owner + All Other Assignees
    """
    recipients = set()
    
    # 1. Add Main Task Owner
    if doc.task_owner:
        recipients.add(doc.task_owner)
        
    # 2. Add All Other Assignees
    for row in doc.get("other_assignees") or []:
        if row.user:
            recipients.add(row.user)
            
    # 3. Send
    if recipients:
        queue_notification_for_users(recipients, doc)


def custom_task_notification_on_update(doc, method):
    """
    On Update: Notify ONLY if Task Owner Changed OR New Assignee Added
    """
    before_doc = doc.get_doc_before_save()
    if not before_doc:
        return

    recipients = set()

    # 1. Check if Main Owner Changed
    # If changed, notify the NEW owner
    if before_doc.task_owner != doc.task_owner and doc.task_owner:
        recipients.add(doc.task_owner)

    # 2. Check for NEWly added Other Assignees
    # We use Python Sets to find the difference
    old_users = set(row.user for row in before_doc.get("other_assignees") or [] if row.user)
    new_users = set(row.user for row in doc.get("other_assignees") or [] if row.user)
    
    # "New - Old" gives us only the users that were added in this save
    added_users = new_users - old_users
    
    recipients.update(added_users)

    # 3. Send
    if recipients:
        queue_notification_for_users(recipients, doc)

# -------------------------------------------------------------------------
# QUEUE LOGIC
# -------------------------------------------------------------------------

def queue_notification_for_users(recipient_emails, doc):
    """
    Loop through the unique list of emails and enqueue a job for each.
    """
    for user_email in recipient_emails:
        frappe.enqueue(
            method="tnc_frappe_custom_app.custom_task.async_send_whatsapp",
            queue="short",
            enqueue_after_commit=True,
            # Arguments passed to the worker:
            target_user_email=user_email,
            task_id=doc.name,
            subject=doc.subject
        )

# -------------------------------------------------------------------------
# BACKGROUND WORKER
# -------------------------------------------------------------------------

def async_send_whatsapp(target_user_email, task_id, subject):
    """
    This runs in background. 
    Accepts 'target_user_email' instead of 'task_owner' to be generic.
    """
    
    # 1. Fetch Employee from User ID
    employee_details = frappe.db.get_value(
        "Employee", 
        {"user_id": target_user_email}, 
        ["name", "employee_name", "cell_number"], 
        as_dict=True
    )

    if not employee_details:
        # User is not an employee or mapped to one
        # Optional: Print warning to console for debugging
        # print(f"User {target_user_email} is not linked to an Employee")
        return

    if not employee_details.cell_number:
        frappe.log_error(
            title="WhatsApp Notification Failed", 
            message=f"Employee {employee_details.employee_name} ({employee_details.name}) has no mobile number for Task {task_id}"
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
        # Ensure this function is imported or available in this scope
        from webtoolex_whatsapp.webtoolex_whatsapp.doctype.whatsapp_instance.whatsapp_instance import send_custom_whatsapp_message
        resp = send_custom_whatsapp_message(employee_details.cell_number, message)
        # print("RRRRRRRRRRRRRRRRRRrrrrrrrrrrrrrrrrrr",resp)
        # if resp and not resp["status"]:
        #     frappe.log_error(title="WhatsApp API Response", message=f"{resp}")
        return resp
    except ImportError:
        frappe.log_error("WhatsApp Error", "send_custom_whatsapp_message function not found. Check imports.")
    except Exception as e:
        frappe.log_error(title="WhatsApp API Error", message=f"{str(e)} | Task: {task_id}")

# import frappe
# 
# def custom_task_notification_on_insert(doc, method):
#     # Only notify if assigned to someone else

#     queue_notification(doc)

# def custom_task_notification_on_update(doc, method):
#     before_doc = doc.get_doc_before_save()
#     if not before_doc:
#         return

#     # Only notify if the owner CHANGED to someone else
#     if before_doc.task_owner != doc.task_owner and doc.task_owner:
#         queue_notification(doc)

# def queue_notification(doc):
#     """
#     Push to queue ONLY if the transaction commits successfully.
#     """
#     frappe.enqueue(
#         method="tnc_frappe_custom_app.custom_task.async_send_whatsapp",
#         queue="short",
#         enqueue_after_commit=True,  # <--- THIS IS THE KEY FOR V15
#         # Pass primitive data types (str, int), avoid passing whole 'doc' objects to queue
#         task_owner=doc.task_owner,
#         task_id=doc.name,
#         subject=doc.subject,
#         task_name=doc.name
#     )

# def async_send_whatsapp(task_owner, task_id, subject, task_name):
#     """
#     This runs in background. 
#     Because of enqueue_after_commit=True, we know the Task exists and is saved.
#     """
    
#     # 1. Fetch Employee from User ID
#     # Note: Using get_value is faster than get_doc if we just need one field, 
#     # but we need name and cell_number, so let's get the doc or value dict.
#     employee_details = frappe.db.get_value(
#         "Employee", 
#         {"user_id": task_owner}, 
#         ["name", "employee_name", "cell_number"], 
#         as_dict=True
#     )

#     if not employee_details:
#         # User is not an employee, stop.
#         return

#     if not employee_details.cell_number:
#         frappe.log_error(
#             title="WhatsApp Notification Failed", 
#             message=f"Employee {employee_details.employee_name} ({employee_details.name}) has no mobile number for Task {task_name}"
#         )
#         return

#     # 2. Construct Message
#     message = f"""Dear {employee_details.employee_name},

# You have been assigned a new task: ({task_id})
# {subject}

# Regards 
# TNC Admin
# """

#     # 3. Send via WhatsApp API
#     try:
#         resp = send_custom_whatsapp_message(employee_details.cell_number, message)
#     except Exception as e:
#         frappe.log_error(title="WhatsApp API Error", message=f"{str(e)} | Task: {task_name}")