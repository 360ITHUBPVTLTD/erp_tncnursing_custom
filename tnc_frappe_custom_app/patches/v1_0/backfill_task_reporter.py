# import frappe


# def execute():
# 	frappe.reload_doctype("Task")

# 	frappe.db.sql("""
# 		UPDATE `tabTask` t
# 		JOIN `tabUser` u ON u.name = t.owner
# 		SET t.task_reporter = t.owner, t.task_reporter_name = u.full_name
# 		WHERE t.task_reporter IS NULL OR t.task_reporter = ''
# 	""")
