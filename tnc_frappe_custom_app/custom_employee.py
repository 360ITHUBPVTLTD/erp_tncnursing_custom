import frappe,traceback
from frappe.utils import get_first_day, get_last_day, getdate
from datetime import timedelta, date, datetime
import logging


# Initialize logger
logger = logging.getLogger(__name__)

@frappe.whitelist()
def allocate_weekly_leaves(custom_date=None):
    try:
        # Set the current date
        if custom_date:
            pass
            # try:
            #     current_date = date(2024, 12, 1)
            #     current_date = getdate(custom_date)
            # except:
            #     frappe.throw(("Invalid date format for custom_date. Please use YYYY-MM-DD."))
        else:
            current_date = getdate()


        if current_date.day != 1:
            return
        # current_date = date(2024, 3, 1)


        weeks = get_week_ranges(current_date)

        logger.info(f"Generated weeks: {weeks}")

        # Fetch all active employees
        employees = frappe.get_all("Employee", filters={
                                                        "status": "Active",
                                                        # "name":"HR-EMP-00002"
                                                        }, fields=["name"])
        
        for employee in employees:
            # if employee.name != "HR-EMP-00002":
            #     continue
            sunady_month_start_leaves = 0
            
            for week in weeks:
                try:
                    if week[0] == week[1]:
                        sunady_month_start_leaves = 1
                        continue
                    # Prevent duplicate allocations
                    existing_allocation = frappe.get_all("Leave Allocation",
                                                        filters={
                                                            "employee": employee.name,
                                                            "from_date": week[0],
                                                            "to_date": week[1]
                                                        },
                                                        fields=["name"])
                    if existing_allocation:
                        logger.info(f"Leave Allocation already exists for {employee.name} from {week[0]} to {week[1]}")
                        continue  # Skip to prevent duplicate allocations

                    # Fetch the Leave Type configuration
                    # leave_type = frappe.get_value("Leave Allocation", {"employee": employee.name, "from_date": week['from_date'], "to_date": week['to_date']}, "leave_type")
                    # if not leave_type:
                    leave_type = "Privilege Leave"  # Default or fetch based on your logic

                    # Check if the Leave Type allows carry forward
                    leave_type_doc = frappe.get_doc("Leave Type", leave_type)
                    
                    
                    new_leaves_allocated = 1
                    if sunady_month_start_leaves: 
                        new_leaves_allocated = new_leaves_allocated + sunady_month_start_leaves
                        sunady_month_start_leaves = 0
                    
                    carry_forward = 1
                    if week[0].day == 1 and not sunady_month_start_leaves:
                        carry_forward = 0

                    # Create a new Leave Allocation
                    print(new_leaves_allocated)
                    allocation = frappe.get_doc({
                        "doctype": "Leave Allocation",
                        "employee": employee.name,
                        "leave_type": leave_type,  # Ensure this leave type exists
                        "from_date": week[0],
                        "to_date": week[1],
                        "carry_forward": carry_forward,
                        "new_leaves_allocated": new_leaves_allocated,
                        # Do not modify 'new_leaves_allocated' based on unused leaves
                        # Frappe HRMS will handle carry forward automatically
                        # "status": "Approved"  # Uncomment if your workflow requires it
                    })
                    # print(week)

                    allocation.insert(ignore_permissions=True)
                    # Optionally submit the allocation if required
                    allocation.submit()
                    frappe.db.commit()

                    logger.info(f"Allocated 1 leave to {employee.name} from {week[0]} to {week[1]} with carry_forward={allocation.carry_forward}")
                except Exception as e:
                    frappe.log_error(message = f"Error in allocating weekly leaves: {e},{traceback.format_exc()}", title = f"Leave Allocation Error for {employee.name} date:  {getdate()}")
        frappe.db.commit()
        frappe.msgprint(("Weekly leave allocations have been successfully processed."))

    except Exception as e:
        # logger.error(f"Error in allocating weekly leaves: {e}")
        frappe.log_error(message = f"Error in allocating weekly leaves: {e},{traceback.format_exc()}", title = f"Leave Allocation Error for date:  {getdate()}")
        frappe.throw(("An error occurred while allocating weekly leaves: {0}").format(str(e)))





def get_week_ranges(input_date):
    """
    Given a datetime object, return a list of tuples representing
    the week ranges for that month.

    Each tuple contains ('from_date', 'to_date') as datetime objects.
    """
    year = input_date.year
    month = input_date.month

    # Find the first and last day of the month
    first_day = datetime(year, month, 1)
    # To get the last day, add one month then subtract one day
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)

    week_ranges = []
    current_start = first_day

    while current_start <= last_day:
        if current_start == first_day:
            # Calculate the first Sunday of the month
            days_until_sunday = (6 - current_start.weekday())  # Monday=0, Sunday=6
            current_end = current_start + timedelta(days=days_until_sunday)
            if current_end > last_day:
                current_end = last_day
        else:
            # Subsequent weeks start on Monday
            # current_start is already set to Monday from the previous iteration
            current_end = current_start + timedelta(days=6)  # Sunday
            if current_end > last_day:
                current_end = last_day

        week_ranges.append((current_start, current_end))

        # Move to the next week (Monday)
        current_start = current_end + timedelta(days=1)
    print(week_ranges)
    return week_ranges




