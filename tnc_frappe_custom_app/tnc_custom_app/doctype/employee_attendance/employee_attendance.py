# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import getdate


class EmployeeAttendance(Document):
	pass


# your_custom_app/api.py


@frappe.whitelist()
def get_active_employees(attendance_date):
    """
    Fetches all active employees.

    :param attendance_date: Date for which attendance is being marked.
    :return: List of active employees with necessary details.
    """
    try:
        employees = frappe.get_all(
            "Employee",
            filters={"status": "Active"},
            fields=["name", "employee_name"]
        )
        return employees
    except Exception as e:
        frappe.log_error(message=str(e), title="Get Active Employees Error")
        frappe.throw(_("An error occurred while fetching active employees."))

@frappe.whitelist()
def submit_employee_attendance(attendance_date, attendance_list):
    """
    Creates Attendance records in ERPNext based on the submitted attendance data.
    :param attendance_date: Date of attendance.
    :param attendance_list: List of dictionaries with employee_id and status.
    :return: "OK" if successful.
    """
    try:
        attendance_list = frappe.parse_json(attendance_list)
        if not attendance_date:
            frappe.throw(_("Attendance date is required."))

        # Validate attendance_date format
        try:
            attendance_date = getdate(attendance_date)
        except ValueError:
            frappe.throw(_("Invalid date format for Attendance Date."))

        # Check if attendance is already marked for the date
        

        for entry in attendance_list:
            employee_name = entry.get('employee_id')  # Correct key access
            status = entry.get('status')              # Correct key access

            if not employee_name:
                frappe.throw(_("Employee ID is missing in the attendance entry."))

            employee = frappe.db.get_value("Employee", employee_name, ["name", "status"])
            if not employee:
                frappe.throw(_("Employee with ID {0} does not exist.").format(employee_name))
            if employee[1] != "Active":
                frappe.throw(_("Employee {0} is not active.").format(employee[0]))

            # Check if Attendance record already exists
            existing_attendance = frappe.db.exists(
                "Attendance",
                {
                    "employee": employee[0],
                    "attendance_date": attendance_date
                }
            )
            if existing_attendance:
                frappe.throw(_("Attendance for Employee {0} on {1} already exists.").format(employee[0], attendance_date))

            # Create Attendance record
            attendance_doc = frappe.get_doc({
                "doctype": "Attendance",
                "employee": employee[0],
                "attendance_date": attendance_date,
                "status": status,
                "in_time": "",
                "out_time": "",
                "remarks": ""
            })
            attendance_doc.insert(ignore_permissions=True)
            attendance_doc.submit()
        
		

        frappe.db.commit()
        frappe.logger().debug(f"Attendance successfully submitted for date: {attendance_date}")
        return "OK"
    except frappe.ValidationError:
        # Re-throw validation errors
        raise
    except Exception as e:
        frappe.log_error(message=str(e), title="Submit Employee Attendance Error")
        frappe.throw(_("An error occurred while submitting attendance. Please check the logs."))

@frappe.whitelist()
def get_existing_attendance(attendance_date):
    """
    Fetches existing attendance records for a given date.

    :param attendance_date: Date for which attendance is being viewed.
    :return: List of attendance records with employee details.
    """
    try:
        frappe.logger().debug(f"Fetching existing attendance for date: {attendance_date}")
        attendance_records = frappe.get_all(
            "Attendance",
            filters={"attendance_date": attendance_date},
            fields=["employee","employee_name", "status"]
        )
        # Enhance records with employee details
        enhanced_records = []
        for record in attendance_records:
            
            enhanced_records.append({
                "employee_id": record.employee,  # Using 'name' as ID
                "employee_name": record.employee_name,
                "status": record.status
            })
        frappe.logger().debug(f"Fetched Attendance Records: {enhanced_records}")
        return enhanced_records
    except Exception as e:
        frappe.log_error(message=str(e), title="Get Existing Attendance Error")
        frappe.throw(_("An error occurred while fetching attendance records."))
