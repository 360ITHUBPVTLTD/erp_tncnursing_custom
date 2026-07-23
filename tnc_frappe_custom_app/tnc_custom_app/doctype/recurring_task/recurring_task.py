# -*- coding: utf-8 -*-
# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from tnc_frappe_custom_app.tnc_custom_app.recurring_task.date_calculator import (
	get_next_run_date,
	get_recurrence_summary,
)


class RecurringTask(Document):
	def before_save(self):
		# Automatically generate recurrence summary
		self.recurrence_summary = get_recurrence_summary(self)

		# Check if any recurrence configuration fields changed
		config_fields = [
			"frequency", "day_of_week", "repeat_by", "day_of_month", 
			"repeat_every", "unit", "start_date", "ends", "end_date", 
			"number_of_occurrences", "enabled"
		]
		is_config_changed = False
		before_save_doc = self.get_doc_before_save()
		if before_save_doc:
			for field in config_fields:
				if self.get(field) != before_save_doc.get(field):
					is_config_changed = True
					break
		else:
			is_config_changed = True

		# State Transitions based on checkbox
		if self.enabled:
			if self.status in ["Draft", "Paused", "Completed"]:
				self.status = "Active"
		else:
			if self.status == "Active":
				self.status = "Paused"
			elif self.status not in ["Draft", "Completed", "Stopped"]:
				self.status = "Paused"

		# Recalculate next_run_date if config changed or if next_run_date is missing
		if is_config_changed or not self.next_run_date:
			if self.status == "Active":
				from frappe.utils import getdate
				# Determine reference date: Use last_run_date if start_date is not ahead of it
				ref_date = self.start_date
				if self.last_run_date and getdate(self.start_date) <= getdate(self.last_run_date):
					ref_date = self.last_run_date
				self.next_run_date = get_next_run_date(self, reference_date=ref_date)

		# Validate and check if limits are exceeded
		is_completed = False
		if self.status == "Active" and self.next_run_date:
			from frappe.utils import getdate
			if self.ends == "On Date" and self.end_date:
				if getdate(self.next_run_date) > getdate(self.end_date):
					is_completed = True
			elif self.ends == "After Occurrences" and self.number_of_occurrences:
				if (self.generated_occurrence_count or 0) >= int(self.number_of_occurrences):
					is_completed = True

		if is_completed:
			self.status = "Completed"
			self.enabled = 0
			self.next_run_date = None

		# If Completed or Stopped, force enabled to 0
		if self.status in ["Completed", "Stopped"]:
			self.enabled = 0
			self.next_run_date = None

	@frappe.whitelist()
	def pause_recurrence(self):
		self.enabled = 0
		self.status = "Paused"
		self.save()
		return self.status

	@frappe.whitelist()
	def resume_recurrence(self):
		self.enabled = 1
		self.status = "Active"
		# Force re-calculation of Next Run Date relative to current state
		self.next_run_date = get_next_run_date(self)
		self.save()
		return self.status

	@frappe.whitelist()
	def stop_recurrence(self):
		self.enabled = 0
		self.status = "Stopped"
		self.save()
		return self.status
