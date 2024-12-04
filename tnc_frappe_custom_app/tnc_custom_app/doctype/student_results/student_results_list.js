frappe.listview_settings['Student Results'] = {
    onload: function(listview) {
        listview.page.add_inner_button(__('Delete Data'), function() {
            // Show a confirmation dialog
            frappe.confirm(
                'Are you sure you want to delete all records?',
                function() {
                    // If confirmed, make a Frappe call to the server
                    frappe.call({
                        method: 'tnc_frappe_custom_app.delete_import_data_master_students.delete_all_records_in_student_results',
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
        listview.page.add_inner_button('Process Data', () => {
            frappe.prompt(
                {
                    label: 'File ID',
                    fieldname: 'file_id',
                    fieldtype: 'Data',
                    reqd: 1
                },
                (values) => {
                    frappe.call({
                        method: 'tnc_frappe_custom_app.script_to_import_data.import_student_results_sql_student_results',
                        args: { file_id: values.file_id },
                        callback: function(r) {
                            if (!r.exc) {
                                frappe.msgprint('Data processing started. Check logs for updates.');
                            }
                        }
                    });
                },
                'Enter File ID',
                'Start Processing'
            );
        });
    }
};
