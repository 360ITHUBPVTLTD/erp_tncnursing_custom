import frappe
from frappe.utils.background_jobs import get_queue

@frappe.whitelist()
def clear_queue(queue_type):
    """
    Clears the jobs from the specified queue that have not been started yet.
    
    Args:
        queue_type (str): The type of queue to clear. Allowed values: 'default', 'short', 'long'.
    
    Returns:
        str: A success or error message.
    """
    valid_queues = ['default', 'short', 'long']
    if queue_type not in valid_queues:
        return "Invalid queue type. Please choose from: " + ", ".join(valid_queues)
    
    try:
        q = get_queue(queue_type)
        jobs = q.jobs
        removed_count = 0

        # Iterate over the jobs and remove only those that haven't started
        for job in jobs:
            if not job.started_at:
                q.remove(job.id)
                removed_count += 1

        return f"Cleared {removed_count} jobs from the {queue_type} queue that were not started."
    except Exception as e:
        return f"Error clearing queue: {str(e)}"
