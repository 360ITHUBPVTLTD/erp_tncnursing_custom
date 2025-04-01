import frappe, traceback
from frappe.utils import getdate  # get_first_day, get_last_day are not needed if calculating manually
from datetime import timedelta, date, datetime
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # Ensure logger captures info level messages

# --- Configuration ---
DEFAULT_LEAVE_TYPE = "Privilege Leave"
# Rule 5: Minimum days for the last week to be considered separate
MIN_DAYS_FOR_SEPARATE_LAST_WEEK = 5

@frappe.whitelist()
def allocate_weekly_leaves(custom_date=None):
    """
    Allocates leaves weekly based on specified rules.
    - Runs daily, but proceeds only on 1st of month or Mondays.
    - Allocates 1 leave per week.
    - Merges last week if shorter than MIN_DAYS_FOR_SEPARATE_LAST_WEEK, allocating 2 leaves for the merged period.
    - Carry Forward: Allowed (1) unless the allocation period starts on the 1st of the month (0).
    """
    process_start_time = datetime.now()
    logger.info(f"--- Starting allocate_weekly_leaves run at {process_start_time} ---")

    try:
        # 1. Determine the date to process
        if custom_date:
            try:
                current_date_dt = getdate(custom_date)
                # Ensure we work with date objects internally
                current_date = current_date_dt.date() if isinstance(current_date_dt, datetime) else current_date_dt
                logger.info(f"Using custom date: {current_date}")
            except Exception as e:
                logger.error(f"Invalid custom_date format: {custom_date}. Error: {e}")
                frappe.throw(f"Invalid date format for custom_date. Please use YYYY-MM-DD. Error: {e}")
        else:
            # current_date = getdate().date() # Work with date object
            current_date = getdate()
            logger.info(f"Using system date: {current_date}")

        # 2. Rule 3: Trigger Condition Check
        is_first_of_month = current_date.day == 1
        is_monday = current_date.weekday() == 0 # Monday is 0

        if not (is_first_of_month or is_monday):
            msg = f"Skipping allocation. Today ({current_date}) is not the 1st ({is_first_of_month}) or a Monday ({is_monday})."
            logger.info(msg)
            frappe.throw(f"{is_first_of_month}{ is_monday} {current_date}")
            return msg # Exit gracefully

        logger.info(f"Proceeding with allocation for {current_date} (Is 1st: {is_first_of_month}, Is Monday: {is_monday})")

        # 3. Rule 5 (part 1): Generate weekly ranges, handling potential merge
        # get_week_ranges now returns list of tuples: (start_date, end_date, num_leaves_to_allocate)
        try:
            weeks_data = get_current_allocation_period(current_date, MIN_DAYS_FOR_SEPARATE_LAST_WEEK)
            logger.info(f"Generated allocation periods for {current_date.strftime('%Y-%m')}: {weeks_data}")
        except Exception as e:
             logger.error(f"Error generating week ranges for {current_date}: {e}\n{traceback.format_exc()}", exc_info=True)
             frappe.throw(f"Failed to generate week ranges: {e}")
             return # Stop execution if weeks can't be generated

        if not weeks_data:
            msg = f"No allocation periods generated for {current_date.strftime('%Y-%m')}. This might be unexpected."
            logger.warning(msg)
            frappe.throw(msg)
            return msg

        # 4. Fetch active employees
        employees = frappe.get_list("Employee", filters={"status": "Active"}, fields=["name"], ignore_permissions=True) # Use get_list
        if not employees:
             msg = "No active employees found. No allocations will be made."
             logger.info(msg)
             frappe.throw(msg)
             return msg

        logger.info(f"Found {len(employees)} active employees.")

        allocation_count = 0
        skip_count = 0
        error_count = 0
        processed_employees = set() # Track employees processed in this run

        # 5. Loop through employees and allocation periods
        for employee_dict in employees:
            employee_name = employee_dict.name
            processed_employees.add(employee_name)

            # Rule 1 & Rule 5 (part 2): Iterate through generated periods
            for week_start_date, week_end_date, leaves_for_this_period in weeks_data:
                try:
                    # Basic validation
                    if week_start_date > week_end_date:
                         logger.warning(f"Skipping invalid period for {employee_name}: Start {week_start_date} > End {week_end_date}")
                         continue
                    if leaves_for_this_period <= 0:
                         logger.warning(f"Skipping period with zero leaves for {employee_name}: {week_start_date} to {week_end_date}")
                         continue

                    # Format dates for filter query
                    from_date_str = week_start_date.strftime('%Y-%m-%d')
                    to_date_str = week_end_date.strftime('%Y-%m-%d')

                    # Check for existing *submitted* allocation for this specific period
                    existing_allocation = frappe.get_list("Leave Allocation", filters={
                        "employee": employee_name,
                        "leave_type": DEFAULT_LEAVE_TYPE,
                        "from_date": from_date_str,
                        "to_date": to_date_str,
                        "docstatus": 1 # Check only submitted documents
                    }, fields=["name"], limit=1, ignore_permissions=True)

                    if existing_allocation:
                        logger.info(f"Skipping: Allocation already exists for {employee_name} from {from_date_str} to {to_date_str}")
                        skip_count += 1
                        continue

                    # Rule 4: Determine Carry Forward flag
                    # Carry forward is 0 ONLY if the allocation period starts on the 1st day of the month
                    # Rule 2 (Monthly Expiry) is primarily enforced by the allocation's from/to dates.
                    # The carry_forward flag here controls balance calculation *between* these weekly allocations within the month.
                    carry_forward_flag = 0 if week_start_date.day == 1 else 1

                    # Rule 1 & 5: Set number of leaves for this specific allocation doc
                    new_leaves_to_allocate = leaves_for_this_period

                    # Create description for clarity
                    description = f"Weekly allocation: {from_date_str} to {to_date_str}."
                    if leaves_for_this_period > 1:
                        description += f" Includes merged short final week ({leaves_for_this_period} leaves total)."

                    # Create and Submit Leave Allocation Document
                    allocation_doc = frappe.new_doc("Leave Allocation")
                    allocation_doc.employee = employee_name
                    allocation_doc.leave_type = DEFAULT_LEAVE_TYPE
                    allocation_doc.from_date = week_start_date
                    allocation_doc.to_date = week_end_date
                    allocation_doc.new_leaves_allocated = new_leaves_to_allocate
                    allocation_doc.carry_forward = carry_forward_flag
                    allocation_doc.description = description
                    # Add any other mandatory fields if necessary

                    allocation_doc.insert(ignore_permissions=True) # Insert first
                    allocation_doc.submit() # Then submit

                    allocation_count += 1
                    logger.info(f"SUCCESS: Allocated {new_leaves_to_allocate} leave(s) to {employee_name} ({from_date_str} to {to_date_str}), CarryForward={carry_forward_flag}")

                except Exception as e:
                    error_count += 1
                    # Rollback is crucial if commit is outside loop and one allocation fails
                    frappe.db.rollback()
                    logger.error(
                        f"ERROR allocating leave for {employee_name} ({week_start_date} to {week_end_date}): {e}\n{traceback.format_exc()}",
                        exc_info=True
                    )
                    # Decide whether to stop for this employee or continue with next week/employee
                    # For robustness, let's log the error and continue to the next period/employee
                    continue # Continue to next iteration

        # 6. Final Commit & Report
        if allocation_count > 0 or error_count == 0: # Commit if successful allocations or no errors occurred
             frappe.db.commit()
             final_msg = (
                 f"Weekly leave allocation run finished. "
                 f"Processed {len(processed_employees)} employees. "
                 f"Successful Allocations: {allocation_count}. "
                 f"Skipped (Duplicates): {skip_count}. "
                 f"Errors: {error_count}."
             )
             logger.info(final_msg)
             frappe.msgprint(final_msg, title="Allocation Summary", indicator="green" if error_count == 0 else "orange")
             return final_msg
        else: # Only errors occurred or nothing to process
             frappe.db.rollback() # Ensure no partial changes are committed
             final_msg = (
                 f"Weekly leave allocation run finished. No successful allocations made. "
                 f"Processed {len(processed_employees)} employees. "
                 f"Skipped (Duplicates): {skip_count}. "
                 f"Errors: {error_count}."
            )
             logger.warning(final_msg)
             # Don't show msgprint if nothing happened unless debugging
             # frappe.msgprint(final_msg, title="Allocation Summary", indicator="red")
             return final_msg


    except Exception as e:
        frappe.db.rollback() # Rollback any potential changes from before the main loop
        process_end_time = datetime.now()
        logger.error(
            f"--- CRITICAL ERROR in allocate_weekly_leaves (Duration: {process_end_time - process_start_time}) ---"
            f"\nError: {e}\n{traceback.format_exc()}",
            exc_info=True
        )
        # frappe.throw will log the error in scheduler logs properly
        frappe.throw(f"A critical error occurred during weekly leave allocation: {str(e)}, {traceback.format_exc()}")

import frappe, traceback
from frappe.utils import getdate
from datetime import timedelta, date, datetime
import logging

# Assume logger is initialized elsewhere or initialize it here if needed
logger = logging.getLogger(__name__)
# You might need to set the level for logger to capture info messages
# logger.setLevel(logging.INFO)

def get_current_allocation_period(input_date, min_days_for_separate_last_week=5):
    """
    Calculates the specific allocation period (week or merged week) that
    contains the given input_date.

    Handles merging of the last week into the penultimate one if it's shorter
    than min_days_for_separate_last_week.

    Args:
        input_date (date or datetime): The date for which to find the allocation period.
        min_days_for_separate_last_week (int): Min days for the last period to remain separate.

    Returns:
        list: A list containing exactly ONE tuple:
              (start_date (date), end_date (date), leaves_to_allocate (int))
              representing the period containing input_date.
              Returns an empty list if input is invalid, calculation fails,
              or the input_date doesn't fall into any calculated period.
    """
    if not isinstance(input_date, (date, datetime)):
        logger.error(f"get_current_allocation_period received invalid input type: {type(input_date)}")
        return []

    # Ensure we work with date objects for comparison
    if isinstance(input_date, datetime):
        target_date = input_date.date()
    else:
        target_date = input_date

    year = target_date.year
    month = target_date.month

    try:
        # --- Step 1: Calculate all potential periods for the month (including merge) ---

        # Find the first and last day of the month as date objects
        first_day_of_month = date(year, month, 1)
        if month == 12:
            last_day_of_month = date(year, 12, 31)
        else:
            first_day_next_month = date(year, month + 1, 1)
            last_day_of_month = first_day_next_month - timedelta(days=1)

        # Generate raw weekly ranges (Mon-Sun or partial) within the month
        raw_weeks = []
        current_start = first_day_of_month
        while current_start <= last_day_of_month:
            days_until_sunday = 6 - current_start.weekday()
            current_end = current_start + timedelta(days=days_until_sunday)
            if current_end > last_day_of_month:
                current_end = last_day_of_month
            if current_start <= current_end:
                 raw_weeks.append((current_start, current_end))
            current_start = current_end + timedelta(days=1)

        # Process raw weeks to create final periods with merge logic and leaf count
        all_periods_data = []
        num_raw_weeks = len(raw_weeks)

        if num_raw_weeks == 0:
            logger.warning(f"No raw weeks calculated for {year}-{month}.")
            return []

        if num_raw_weeks > 1:
            last_week_start, last_week_end = raw_weeks[-1]
            days_in_last_week = (last_week_end - last_week_start).days + 1

            if days_in_last_week < min_days_for_separate_last_week:
                # Merge needed
                for i in range(num_raw_weeks - 2):
                    start, end = raw_weeks[i]
                    all_periods_data.append((start, end, 1)) # Add non-merged weeks

                penultimate_start, _ = raw_weeks[-2]
                merged_start = penultimate_start
                merged_end = last_week_end # End date is the end of the short last week
                all_periods_data.append((merged_start, merged_end, 2)) # Add merged period
                logger.info(f"Calculated potential merged period for {year}-{month}: {merged_start} to {merged_end}, 2 leaves.")
            else:
                # No merge needed
                for start, end in raw_weeks:
                    all_periods_data.append((start, end, 1))
                logger.info(f"Calculated potential separate periods for {year}-{month}. Last week ({days_in_last_week} days) is long enough.")

        elif num_raw_weeks == 1:
             start, end = raw_weeks[0]
             all_periods_data.append((start, end, 1)) # Only one period

        # --- Step 2: Find the specific period containing the input_date ---
        for start_date, end_date, leaves in all_periods_data:
            if start_date <= target_date <= end_date:
                logger.info(f"Input date {target_date} falls within period: {start_date} to {end_date}, leaves: {leaves}")
                # Return list containing only the matching tuple
                return [(start_date, end_date, leaves)]

        # If loop completes without finding a match (should not happen for valid dates within the month)
        logger.warning(f"Input date {target_date} did not fall into any calculated allocation period for {year}-{month}. Periods calculated: {all_periods_data}")
        return []

    except Exception as e:
        logger.error(f"Error calculating allocation period for {target_date}: {e}\n{traceback.format_exc()}", exc_info=True)
        return [] # Return empty list on error

# def get_week_ranges(input_date, min_days_for_separate_last_week=5):
#     """
#     Calculates allocation periods (weeks) for the month of the input_date.
#     Merges the last week into the penultimate one if it's shorter than
#     min_days_for_separate_last_week.

#     Args:
#         input_date (date): The date defining the month and year to process.
#         min_days_for_separate_last_week (int): Min days for the last period.

#     Returns:
#         list: A list of tuples, where each tuple is
#               (start_date (date), end_date (date), leaves_to_allocate (int)).
#               Returns an empty list if input is invalid or calculation fails.
#     """
#     if not isinstance(input_date, date):
#         # If input_date might be datetime, convert it
#         if isinstance(input_date, datetime):
#             input_date = input_date.date()
#         else:
#             logger.error(f"get_week_ranges received invalid input type: {type(input_date)}")
#             return [] # Return empty list on invalid input

#     year = input_date.year
#     month = input_date.month

#     try:
#         # Find the first and last day of the month as date objects
#         first_day_of_month = date(year, month, 1)
#         if month == 12:
#             last_day_of_month = date(year, 12, 31)
#         else:
#             # Find first day of next month, then subtract one day
#             first_day_next_month = date(year, month + 1, 1)
#             last_day_of_month = first_day_next_month - timedelta(days=1)

#         raw_weeks = []
#         current_start = first_day_of_month

#         while current_start <= last_day_of_month:
#             # Week traditionally ends on Sunday (weekday == 6)
#             days_until_sunday = 6 - current_start.weekday()
#             current_end = current_start + timedelta(days=days_until_sunday)

#             # Ensure the end date doesn't exceed the last day of the month
#             if current_end > last_day_of_month:
#                 current_end = last_day_of_month

#             # Add the calculated week (start_date, end_date)
#             if current_start <= current_end: # Basic sanity check
#                  raw_weeks.append((current_start, current_end))

#             # Move to the start of the next week (Monday)
#             current_start = current_end + timedelta(days=1)

#         # --- Process raw weeks for merging and adding leaf count ---
#         final_weeks_data = []
#         num_raw_weeks = len(raw_weeks)

#         if num_raw_weeks == 0:
#             return [] # No weeks found

#         # Check if merging is needed (Rule 5)
#         if num_raw_weeks > 1: # Need at least two weeks to merge
#             last_week_start, last_week_end = raw_weeks[-1]
#             days_in_last_week = (last_week_end - last_week_start).days + 1

#             if days_in_last_week < min_days_for_separate_last_week:
#                 # Merge is needed
#                 logger.info(f"Last week ({last_week_start} to {last_week_end}, {days_in_last_week} days) is shorter than {min_days_for_separate_last_week} days. Merging.")

#                 # Add all weeks except the last two, with 1 leaf each
#                 for i in range(num_raw_weeks - 2):
#                     start, end = raw_weeks[i]
#                     final_weeks_data.append((start, end, 1)) # 1 leaf

#                 # Create the merged period from the start of the penultimate week to the end of the last week
#                 penultimate_start, penultimate_end = raw_weeks[-2]
#                 merged_start = penultimate_start
#                 merged_end = last_week_end # Use the actual end date of the original short week
#                 # Add the merged week with 2 leaves
#                 final_weeks_data.append((merged_start, merged_end, 2)) # 2 leaves
#                 logger.info(f"Merged period: {merged_start} to {merged_end}, allocating 2 leaves.")

#             else:
#                 # No merge needed, just add leaf count=1 to all raw weeks
#                 logger.info(f"Last week ({days_in_last_week} days) is long enough. No merge needed.")
#                 for start, end in raw_weeks:
#                     final_weeks_data.append((start, end, 1)) # 1 leaf each

#         elif num_raw_weeks == 1:
#              # Only one week in the month (or calculation resulted in one period)
#              start, end = raw_weeks[0]
#              final_weeks_data.append((start, end, 1)) # 1 leaf

#         return final_weeks_data

#     except Exception as e:
#         logger.error(f"Error calculating week ranges for {year}-{month}: {e}\n{traceback.format_exc()}", exc_info=True)
#         return [] # Return empty list on error

# import frappe,traceback
# from frappe.utils import get_first_day, get_last_day, getdate
# from datetime import timedelta, date, datetime
# import logging


# # Initialize logger
# logger = logging.getLogger(__name__)

# @frappe.whitelist()
# def allocate_weekly_leaves(custom_date=None):
#     try:
#         # Set the current date
#         if custom_date:
#             pass
#             # try:
#             #     current_date = date(2024, 12, 1)
#             #     current_date = getdate(custom_date)
#             # except:
#             #     frappe.throw(("Invalid date format for custom_date. Please use YYYY-MM-DD."))
#         else:
#             current_date = getdate()


#         if current_date.day != 1:
#             return
#         # current_date = date(2024, 3, 1)


#         weeks = get_week_ranges(current_date)

#         logger.info(f"Generated weeks: {weeks}")

#         # Fetch all active employees
#         employees = frappe.get_all("Employee", filters={
#                                                         "status": "Active",
#                                                         # "name":"HR-EMP-00002"
#                                                         }, fields=["name"])
        
#         for employee in employees:
#             # if employee.name != "HR-EMP-00002":
#             #     continue
#             sunady_month_start_leaves = 0
            
#             for week in weeks:
#                 try:
#                     if week[0] == week[1]:
#                         sunady_month_start_leaves = 1
#                         continue
#                     # Prevent duplicate allocations
#                     existing_allocation = frappe.get_all("Leave Allocation",
#                                                         filters={
#                                                             "employee": employee.name,
#                                                             "from_date": week[0],
#                                                             "to_date": week[1]
#                                                         },
#                                                         fields=["name"])
#                     if existing_allocation:
#                         logger.info(f"Leave Allocation already exists for {employee.name} from {week[0]} to {week[1]}")
#                         continue  # Skip to prevent duplicate allocations

#                     # Fetch the Leave Type configuration
#                     # leave_type = frappe.get_value("Leave Allocation", {"employee": employee.name, "from_date": week['from_date'], "to_date": week['to_date']}, "leave_type")
#                     # if not leave_type:
#                     leave_type = "Privilege Leave"  # Default or fetch based on your logic

#                     # Check if the Leave Type allows carry forward
#                     leave_type_doc = frappe.get_doc("Leave Type", leave_type)
                    
                    
#                     new_leaves_allocated = 1
#                     if sunady_month_start_leaves: 
#                         new_leaves_allocated = new_leaves_allocated + sunady_month_start_leaves
#                         sunady_month_start_leaves = 0
                    
#                     carry_forward = 1
#                     if week[0].day == 1 and not sunady_month_start_leaves:
#                         carry_forward = 0

#                     # Create a new Leave Allocation
#                     print(new_leaves_allocated)
#                     allocation = frappe.get_doc({
#                         "doctype": "Leave Allocation",
#                         "employee": employee.name,
#                         "leave_type": leave_type,  # Ensure this leave type exists
#                         "from_date": week[0],
#                         "to_date": week[1],
#                         "carry_forward": carry_forward,
#                         "new_leaves_allocated": new_leaves_allocated,
#                         # Do not modify 'new_leaves_allocated' based on unused leaves
#                         # Frappe HRMS will handle carry forward automatically
#                         # "status": "Approved"  # Uncomment if your workflow requires it
#                     })
#                     # print(week)

#                     allocation.insert(ignore_permissions=True)
#                     # Optionally submit the allocation if required
#                     allocation.submit()
#                     frappe.db.commit()

#                     logger.info(f"Allocated 1 leave to {employee.name} from {week[0]} to {week[1]} with carry_forward={allocation.carry_forward}")
#                 except Exception as e:
#                     frappe.log_error(message = f"Error in allocating weekly leaves: {e},{traceback.format_exc()}", title = f"Leave Allocation Error for {employee.name} date:  {getdate()}")
#         frappe.db.commit()
#         frappe.msgprint(("Weekly leave allocations have been successfully processed."))

#     except Exception as e:
#         # logger.error(f"Error in allocating weekly leaves: {e}")
#         frappe.log_error(message = f"Error in allocating weekly leaves: {e},{traceback.format_exc()}", title = f"Leave Allocation Error for date:  {getdate()}")
#         frappe.throw(("An error occurred while allocating weekly leaves: {0}").format(str(e)))





# def get_week_ranges(input_date):
#     """
#     Given a datetime object, return a list of tuples representing
#     the week ranges for that month.

#     Each tuple contains ('from_date', 'to_date') as datetime objects.
#     """
#     year = input_date.year
#     month = input_date.month

#     # Find the first and last day of the month
#     first_day = datetime(year, month, 1)
#     # To get the last day, add one month then subtract one day
#     if month == 12:
#         last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
#     else:
#         last_day = datetime(year, month + 1, 1) - timedelta(days=1)

#     week_ranges = []
#     current_start = first_day

#     while current_start <= last_day:
#         if current_start == first_day:
#             # Calculate the first Sunday of the month
#             days_until_sunday = (6 - current_start.weekday())  # Monday=0, Sunday=6
#             current_end = current_start + timedelta(days=days_until_sunday)
#             if current_end > last_day:
#                 current_end = last_day
#         else:
#             # Subsequent weeks start on Monday
#             # current_start is already set to Monday from the previous iteration
#             current_end = current_start + timedelta(days=6)  # Sunday
#             if current_end > last_day:
#                 current_end = last_day

#         week_ranges.append((current_start, current_end))

#         # Move to the next week (Monday)
#         current_start = current_end + timedelta(days=1)
#     print(week_ranges)
#     return week_ranges




