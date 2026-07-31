__version__ = "0.0.1"


def _patch_toggle_notifications():
	"""Frappe core's User.check_enable_disable() calls toggle_notifications(),
	which saves the target user's Notification Settings without ignore_permissions.
	Notification Settings restricts write access to the doc's own owner (or System
	Manager), so any non-System-Manager role that is otherwise allowed to edit/
	disable Users fails with a permission error on this unrelated side effect.
	Whether the caller may disable/enable a user is already enforced separately by
	the User doctype's own permissions before this code runs, so bypassing this
	incidental check does not widen who can disable/enable users.
	"""
	import frappe.core.doctype.user.user as user_module

	def patched_toggle_notifications(user, enable=False):
		import frappe

		try:
			settings = frappe.get_doc("Notification Settings", user)
		except frappe.DoesNotExistError:
			frappe.clear_last_message()
			return

		if settings.enabled != enable:
			settings.enabled = enable
			settings.save(ignore_permissions=True)

	user_module.toggle_notifications = patched_toggle_notifications


_patch_toggle_notifications()
