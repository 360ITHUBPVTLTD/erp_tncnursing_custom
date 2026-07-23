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

		# State Transitions based on checkbox
		if self.enabled:
			if self.status in ["Draft", "Paused"]:
				self.status = "Active"
			
			# If Active, ensure Next Run Date is populated
			if self.status == "Active" and not self.next_run_date:
				self.next_run_date = get_next_run_date(self)
		else:
			if self.status == "Active":
				self.status = "Paused"
			elif self.status not in ["Draft", "Completed", "Stopped"]:
				self.status = "Paused"

		# If Completed or Stopped, force enabled to 0
		if self.status in ["Completed", "Stopped"]:
			self.enabled = 0

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
