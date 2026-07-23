# -*- coding: utf-8 -*-
# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import add_days, getdate


def generate_task_from_recurring_task(doc):
	"""
	Generates a normal Task document from the Recurring Task template.
	Returns the generated Task document or the existing one if it was already generated.
	"""
	next_occurrence = (doc.generated_occurrence_count or 0) + 1
	scheduled_date = getdate(doc.next_run_date)

	# 1. Duplicate prevention check
	existing_task = frappe.db.exists("Task", {
		"recurring_task": doc.name,
		"occurrence_number": next_occurrence
	})
	if existing_task:
		frappe.logger().warning(
			f"Task for Recurring Task {doc.name} occurrence #{next_occurrence} already exists: {existing_task}. Skipping generation."
		)
		return frappe.get_doc("Task", existing_task)

	# 2. Compute expected start and end dates
	exp_start_date = scheduled_date
	if doc.allocated_days and int(doc.allocated_days) > 0:
		exp_end_date = add_days(exp_start_date, int(doc.allocated_days))
	else:
		exp_end_date = exp_start_date

	# 3. Create the Task doc
	task_data = {
		"doctype": "Task",
		"subject": doc.subject,
		"description": doc.description,
		"task_owner": doc.task_owner,
		"priority": doc.priority or "Medium",
		"project": doc.project,
		"exp_start_date": exp_start_date,
		"exp_end_date": exp_end_date,
		# Custom tracking fields
		"recurring_task": doc.name,
		"generated_automatically": 1,
		"occurrence_number": next_occurrence,
	}

	# Check for other assignees in custom task field mapping if needed.
	# Standard assignment rules and triggers will automatically fire on insert.
	new_task = frappe.get_doc(task_data)
	new_task.insert(ignore_permissions=True)

	# 4. Copy attachments from the Recurring Task to the generated Task
	copy_attachments(doc.doctype, doc.name, new_task.doctype, new_task.name)

	return new_task


def copy_attachments(from_doctype, from_name, to_doctype, to_name):
	"""Copies attachments from one document to another in Frappe."""
	files = frappe.get_all("File", filters={
		"attached_to_doctype": from_doctype,
		"attached_to_name": from_name
	})

	for f in files:
		file_doc = frappe.get_doc("File", f.name)
		# Clone the file document
		new_file = frappe.copy_doc(file_doc)
		new_file.attached_to_doctype = to_doctype
		new_file.attached_to_name = to_name
		# If the file path is a private or public path, keeping file_url is sufficient
		new_file.insert(ignore_permissions=True)
