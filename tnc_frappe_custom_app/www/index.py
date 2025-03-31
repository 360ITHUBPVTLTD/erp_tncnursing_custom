import frappe


def get_context(context):
    # Fetch the single Doctype "Public Website Settings"
    public_website_settings = frappe.get_doc("TNC Public Website Settings")
    context.public_website_settings = public_website_settings
    return context