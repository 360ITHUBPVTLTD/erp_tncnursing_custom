import frappe
from frappe.utils import strip_html, formatdate, get_fullname
import re
# -------------------------------------------------------------------------
# HOOKS
# -------------------------------------------------------------------------

def custom_task_notification_on_insert(doc, method):
    """
    On Creation: Notify Task Owner + All Other Assignees
    """
    recipients = set()
    # if doc.other_assignees:

    #     for row in doc.other_assignees:
    #         user_child_table_row = doc.append("custom_other_assignee_user", {})
    #         user_child_table_row.user = row.user
    #     doc.save()
    #     doc.reload()
    #     frappe.db.commit()


    # 1. Add Main Task Owner
    if doc.task_owner:
        recipients.add(doc.task_owner)

    # 2. Add All Other Assignees
    for row in doc.get("other_assignees") or []:
        if row.user:
            recipients.add(row.user)

    # 3. Send WhatsApp
    if recipients:
        queue_notification_for_users(recipients, doc)

    # 4. Send System Notification (Bell Icon)
    if recipients:
        create_system_notification(
            recipients=recipients,
            doc=doc,
            message=f"You have been assigned a new task: {doc.subject}",
        )




def custom_task_notification_on_update(doc, method):
    """
    On Update: Notify if Task Owner Changed, New Assignee Added, or Status Changed
    """
    before_doc = doc.get_doc_before_save()
    if not before_doc:
        return

    assignment_recipients = set()

    # 1. Check if Main Owner Changed — notify the NEW owner
    if before_doc.task_owner != doc.task_owner and doc.task_owner:
        assignment_recipients.add(doc.task_owner)

    # 2. Check for NEWly added Other Assignees
    old_users = set(row.user for row in before_doc.get("other_assignees") or [] if row.user)
    new_users = set(row.user for row in doc.get("other_assignees") or [] if row.user)

    added_users = new_users - old_users
    assignment_recipients.update(added_users)

    # 3. Send WhatsApp for assignment changes
    if assignment_recipients:
        queue_notification_for_users(assignment_recipients, doc)

    # 4. Send System Notification for assignment changes (Bell Icon)
    if assignment_recipients:
        create_system_notification(
            recipients=assignment_recipients,
            doc=doc,
            message=f"You have been assigned to task: {doc.subject}",
        )

    # 5. Check if Task Status Changed — notify task_owner + all other_assignees
    if before_doc.status != doc.status:
        status_recipients = set()
        if doc.task_owner:
            status_recipients.add(doc.task_owner)
        for row in doc.get("other_assignees") or []:
            if row.user:
                status_recipients.add(row.user)

        # Remove the user who made the change (they already know)
        status_recipients.discard(frappe.session.user)

        if status_recipients:
            create_system_notification(
                recipients=status_recipients,
                doc=doc,
                message=f"Task status changed to {doc.status}: {doc.subject}",
            )

# -------------------------------------------------------------------------
# SYSTEM NOTIFICATION (BELL ICON) + FCM PUSH
# -------------------------------------------------------------------------

def create_system_notification(recipients, doc, message):
    """
    Create Frappe Notification Log entries that appear in the bell icon
    for each recipient, and also trigger an FCM push notification.
    """
    sender = frappe.session.user

    for user in recipients:
        # Skip sending notification to the person who triggered the action
        if user == sender:
            continue

        try:
            notification_doc = frappe.get_doc({
                "doctype": "Notification Log",
                "for_user": user,
                "from_user": sender,
                "subject": message,
                "type": "Alert",
                "document_type": "Task",
                "document_name": doc.name,
                "email_content": message,
            })
            notification_doc.insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(
                title="System Notification Error",
                message=f"Failed to create notification for {user} on Task {doc.name}: {str(e)}"
            )

        # Also send FCM push notification
        send_fcm_push_notification(
            user_email=user,
            title=f"Task: {doc.subject}",
            body=message,
            doc=doc,
        )


def send_fcm_push_notification(user_email, title, body, doc):
    """
    Look up the Employee's custom_fcm_token by user_id and send
    an FCM push notification via the fcm_360ithub app.
    """
    try:
        fcm_token = frappe.db.get_value(
            "Employee",
            {"user_id": user_email},
            "custom_fcm_token"
        )

        if not fcm_token:
            # No FCM token for this user — skip silently
            return

        send_fcm_notification = frappe.get_attr("fcm_360ithub.fcm_functions.send_fcm_notification")

        send_fcm_notification(
            token=fcm_token,
            title=title,
            body=body,
            doctype="Task",
            task_id=doc.name,
            user_doctype="Employee",
            user=user_email,
            notification_type="Task Notification",
        )
    except Exception as e:
        frappe.log_error(
            title="FCM Push Notification Error",
            message=f"Failed to send FCM for {user_email} on Task {doc.name}: {str(e)}"
        )

# -------------------------------------------------------------------------
# COMMENT NOTIFICATION
# -------------------------------------------------------------------------

def notify_on_task_comment(doc, method):
    """
    Triggered after a Comment is inserted.
    If the comment is on a Task, notify task_owner + other_assignees.
    """
    # Only handle comments on Task documents
    if doc.reference_doctype != "Task" or not doc.reference_name:
        return

    # Only handle actual user comments (not system-generated logs)
    if doc.comment_type != "Comment":
        return

    task_doc = frappe.get_doc("Task", doc.reference_name)

    recipients = set()

    # Add task owner
    if task_doc.task_owner:
        recipients.add(task_doc.task_owner)

    # Add all other assignees
    for row in task_doc.get("other_assignees") or []:
        if row.user:
            recipients.add(row.user)

    # Remove the commenter (they already know)
    recipients.discard(frappe.session.user)

    if recipients:
        commenter_name = get_fullname(frappe.session.user)
        create_system_notification(
            recipients=recipients,
            doc=task_doc,
            message=f"{commenter_name} commented on task: {task_doc.subject}",
        )

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


def clean_html_for_whatsapp(html_text):
    if not html_text:
        return ""

    # 1. Handle List items: Add a bullet point and a newline
    html_text = html_text.replace("</li>", "\n")
    html_text = html_text.replace("<li", "\n• <li")

    # 2. Handle Paragraphs and Divisions: Replace closing tags with newlines
    html_text = html_text.replace("</p>", "\n")
    html_text = html_text.replace("</div>", "\n")
    html_text = html_text.replace("<br>", "\n")
    html_text = html_text.replace("<br/>", "\n")

    # 3. Now strip all remaining tags (like <span>, <strong>, etc.)
    clean_text = strip_html(html_text)

    # 4. Clean up: remove leading/trailing whitespace on each line
    # and limit consecutive newlines to maximum 2
    lines = [line.strip() for line in clean_text.split("\n")]
    clean_text = "\n".join(lines)

    # Remove excessive empty lines
    clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text).strip()

    return clean_text

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
    task_doc = frappe.get_doc("Task", task_id)

    clean_description = clean_html_for_whatsapp(task_doc.description or "No description provided")
    formatted_date = formatdate(task_doc.exp_end_date) if task_doc.exp_end_date else "Not Set"

    assigned_by = frappe.db.get_value(
        "Employee",
        {"user_id": task_doc.modified_by},
        ["name", "employee_name"],
        as_dict=True
    )

    # 2. Construct Message
    message = f"""Dear {employee_details.employee_name},

You have been assigned a new task:
📌 *{task_doc.subject}*({formatted_date})
🔥 *Priority*: {task_doc.priority}

📝*Description*:
{clean_description}

👤 *Assigned By*: {assigned_by.employee_name if assigned_by else task_doc.modified_by}


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
        # frappe.log_error(title="WhatsApp Error", message=f"{message}")
    except ImportError:
        frappe.log_error(title="WhatsApp Error", message="send_custom_whatsapp_message function not found. Check imports.")
    except Exception as e:
        frappe.log_error(title="WhatsApp API Error", message=f"{str(e)} | Task: {task_id}")


def custom_task_before_save(doc, method):
    old_doc = doc.get_doc_before_save()
    admin_roles = {"Administrator", "System Manager", "TNC Super Admin"}

    is_being_completed = (
        doc.status == "Completed"
        and old_doc
        and old_doc.status != "Completed"
    )

    is_creator = doc.owner == frappe.session.user
    is_admin = bool(admin_roles & set(frappe.get_roles()))

    if is_being_completed and not (is_creator or is_admin):
        frappe.throw("You need to be creator of the task to mark it as completed.")

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
