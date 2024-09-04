import time
import frappe
 
@frappe.whitelist()
def test_progress():
    for i in range(1, 101):
        frappe.publish_realtime('test_progress', {'progress': i})
        time.sleep(0.1)  # Simulate a task