
frappe.listview_settings['Student'] = {
    onload: function(listview) {
        listview.page.add_inner_button(__('Delete Data'), function() {
            // Show a confirmation dialog
            frappe.confirm(
                'Are you sure you want to delete all records?',
                function() {
                    // If confirmed, make a Frappe call to the server
                    frappe.call({
                        method: 'tnc_frappe_custom_app.delete_import_data_master_students.delete_all_records_in_student',
                        callback: function(response) {
                            if (response.message === 'success') {
                                frappe.show_alert({
                                    message: __('All records have been deleted successfully.'),
                                    indicator: 'green'
                                });
                                listview.refresh(); // Refresh the list view to reflect the changes
                            } else {
                                frappe.show_alert({
                                    message: __('There was an issue deleting the records.'),
                                    indicator: 'red'
                                });
                            }
                        }
                    });
                }
            );
        });
    }
};
