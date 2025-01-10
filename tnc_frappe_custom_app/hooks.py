app_name = "tnc_frappe_custom_app"
app_title = "TNC Custom App"
app_publisher = "Administrator"
app_description = "About the TNC"
app_email = "admin@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "tnc_frappe_custom_app",
# 		"logo": "/assets/tnc_frappe_custom_app/logo.png",
# 		"title": "TNC Custom App",
# 		"route": "/tnc_frappe_custom_app",
# 		"has_permission": "tnc_frappe_custom_app.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------





# include js, css files in header of desk.html
# app_include_css = "/assets/tnc_frappe_custom_app/css/tnc_frappe_custom_app.css"
# app_include_js = "/assets/tnc_frappe_custom_app/js/tnc_frappe_custom_app.js"

# include js, css files in header of web template
# web_include_css = "/assets/tnc_frappe_custom_app/css/tnc_frappe_custom_app.css"
# web_include_js = "/assets/tnc_frappe_custom_app/js/tnc_frappe_custom_app.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "tnc_frappe_custom_app/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "tnc_frappe_custom_app/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------


scheduler_events = {

    "cron":{
    	"0 3 1 * *": [
            "tnc_frappe_custom_app.custom_employee.allocate_weekly_leaves"
        ],
    },
    
    # "all": [
    #   "lsa.tasks.all"
    # ],
    # "daily": [
    #   "lsa.tasks.daily"
    # ],
    # "hourly": [
    #   "lsa.tasks.hourly"
    # ],
    # "weekly": [
    #   "lsa.tasks.weekly"
    # ],
    # "monthly": [
    #   "tnc_frappe_custom_app.custom_employee.allocate_weekly_leaves"
    # ],
}

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "tnc_frappe_custom_app.utils.jinja_methods",
# 	"filters": "tnc_frappe_custom_app.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "tnc_frappe_custom_app.install.before_install"
# after_install = "tnc_frappe_custom_app.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "tnc_frappe_custom_app.uninstall.before_uninstall"
# after_uninstall = "tnc_frappe_custom_app.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "tnc_frappe_custom_app.utils.before_app_install"
# after_app_install = "tnc_frappe_custom_app.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "tnc_frappe_custom_app.utils.before_app_uninstall"
# after_app_uninstall = "tnc_frappe_custom_app.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "tnc_frappe_custom_app.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"tnc_frappe_custom_app.tasks.all"
# 	],
# 	"daily": [
# 		"tnc_frappe_custom_app.tasks.daily"
# 	],
# 	"hourly": [
# 		"tnc_frappe_custom_app.tasks.hourly"
# 	],
# 	"weekly": [
# 		"tnc_frappe_custom_app.tasks.weekly"
# 	],
# 	"monthly": [
# 		"tnc_frappe_custom_app.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "tnc_frappe_custom_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "tnc_frappe_custom_app.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "tnc_frappe_custom_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["tnc_frappe_custom_app.utils.before_request"]
# after_request = ["tnc_frappe_custom_app.utils.after_request"]

# Job Events
# ----------
# before_job = ["tnc_frappe_custom_app.utils.before_job"]
# after_job = ["tnc_frappe_custom_app.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"tnc_frappe_custom_app.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# your_app/hooks.py
doc_events = {
    "Data Import": {
        # "on_update": "tnc_frappe_custom_app.data_import_id.handle_data_import_after_save"
    },
    # "Data Import Log": {
    #     # "after_insert": "tnc_frappe_custom_app.data_import_id.handle_data_import_after_save"
    # }
}

