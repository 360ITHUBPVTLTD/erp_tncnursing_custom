// Copyright (c) 2024, Administrator and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Students Master Data", {
// 	refresh(frm) {

// 	},
// });





frappe.listview_settings['Students Master Data'] = {
    onload: function(listview) {
        listview.page.add_inner_button(__('Delete Data'), function() {
            // Show a confirmation dialog
            frappe.confirm(
                'Are you sure you want to delete all records?',
                function() {
                    // If confirmed, make a Frappe call to the server
                    frappe.call({
                        method: 'tnc_frappe_custom_app.delete_import_data_master_students.delete_all_records',
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

        // listview.page.add_inner_button(__('Uncheck Imported'), function() {
        //     // Show a confirmation dialog
        //     frappe.confirm(
        //         'Are you sure you want to uncheck the imported field for all records?',
        //         function() {
        //             // If confirmed, make a Frappe call to the server
        //             frappe.call({
        //                 method: 'tnc_frappe_custom_app.delete_import_data_master_students.uncheck_imported',
        //                 callback: function(response) {
        //                     if (response.message === 'success') {
        //                         frappe.show_alert({
        //                             message: __('All records have been updated successfully.'),
        //                             indicator: 'green'
        //                         });
        //                         listview.refresh(); // Refresh the list view to reflect the changes
        //                     } else {
        //                         frappe.show_alert({
        //                             message: __('There was an issue updating the records.'),
        //                             indicator: 'red'
        //                         });
        //                     }
        //                 }
        //             });
        //         }
        //     );
        // });
    }
};




















