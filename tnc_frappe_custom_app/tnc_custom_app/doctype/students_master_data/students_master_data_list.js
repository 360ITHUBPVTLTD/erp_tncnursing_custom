// Copyright (c) 2024, Administrator and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Students Master Data", {
// 	refresh(frm) {

// 	},
// });

////////////////////// Below code is without having the DELETE Button in the List view //////////////////

// frappe.listview_settings['Students Master Data'] = {
//     onload: function(listview) {
//         listview.page.add_inner_button(__('Sync Data'), function() {
//             console.log('Sync Data button clicked');
//             frappe.call({
//                 method: 'tnc_frappe_custom_app.sync.sync_data',
//                 callback: function(response) {
//                     if(response.message === "success") {
//                         frappe.msgprint(__('Data synced successfully!'));
//                     } else {
//                         frappe.msgprint(__('There was an issue with syncing the data.'));
//                     }
//                 },
//                 error: function(err) {
//                     frappe.msgprint(__('Syncing the data is not possible.'));
//                 }
//             });
//         });
//     }
// };


///////////////////////// Below code is adding the delete button in the ListView to delete the imported data deleted /////////


// frappe.listview_settings['Students Master Data'] = {
//     onload: function(listview) {
//         // Add the "Sync Data" button
//         listview.page.add_inner_button(__('Sync Data'), function() {
//             console.log('Sync Data button clicked');
//             frappe.call({
//                 method: 'tnc_frappe_custom_app.sync.sync_data',
//                 callback: function(response) {
//                     if(response.message === "success") {
//                         frappe.msgprint(__('Data synced successfully!'));
//                         // Hide the "Sync Data" button
//                         listview.page.inner_toolbar.find('.btn').hide();
//                         // Add the "Delete Data" button
//                         listview.page.add_inner_button(__('Delete Data'), function() {
//                             frappe.confirm(
//                                 __('Are you sure you want to delete all records?'),
//                                 function() {
//                                     // User confirmed deletion
//                                     frappe.call({
//                                         method: 'tnc_frappe_custom_app.sync.delete_data',
//                                         callback: function(response) {
//                                             if (response.message === "success") {
//                                                 frappe.msgprint(__('All data deleted successfully!'));
//                                                 listview.refresh();  // Refresh the list view
//                                             } else {
//                                                 frappe.msgprint(__('There was an issue deleting the data.'));
//                                             }
//                                         },
//                                         error: function(err) {
//                                             frappe.msgprint(__('Error while deleting the data.'));
//                                         }
//                                     });
//                                 },
//                                 function() {
//                                     // User canceled deletion
//                                     frappe.msgprint(__('Deletion canceled.'));
//                                 }
//                             );
//                         });
//                     } else {
//                         frappe.msgprint(__('There was an issue with syncing the data.'));
//                     }
//                 },
//                 error: function(err) {
//                     frappe.msgprint(__('Syncing the data is not possible.'));
//                 }
//             });
//         });
//     }
// };


frappe.listview_settings['Students Master Data'] = {
    onload: function(listview) {
        // Initially, don't show any button
        frappe.call({
            method: 'tnc_frappe_custom_app.sync.check_all_imported',
            callback: function(response) {
                if (response.message === "no_data") {
                    // No button should be shown if there's no data
                    return;
                } else if (response.message === "all_imported") {
                    // Show "Delete Data" button if all records are imported
                    listview.page.add_inner_button(__('Delete Data'), function() {
                        frappe.confirm(
                            __('Are you sure you want to delete all records?'),
                            function() {
                                frappe.call({
                                    method: 'tnc_frappe_custom_app.sync.delete_data',
                                    callback: function(response) {
                                        if (response.message === "success") {
                                            frappe.msgprint(__('All data deleted successfully!'));
                                            listview.refresh();  // Refresh the list view
                                        } else {
                                            frappe.msgprint(__('There was an issue deleting the data.'));
                                        }
                                    },
                                    error: function(err) {
                                        frappe.msgprint(__('Error while deleting the data.'));
                                    }
                                });
                            }
                        );
                    });
                } else if (response.message === "not_imported") {
                    // Show "Sync Data" button if there are records that need to be imported
                    listview.page.add_inner_button(__('Sync Data'), function() {
                        frappe.call({
                            method: 'tnc_frappe_custom_app.sync.sync_data',
                            callback: function(response) {
                                if (response.message === "success") {
                                    frappe.msgprint(__('Data synced successfully!'));
                                    listview.refresh();  // Refresh the list view to check the status again
                                } else {
                                    frappe.msgprint(__('There was an issue with syncing the data.'));
                                }
                            },
                            error: function(err) {
                                frappe.msgprint(__('Syncing the data is not possible.'));
                            }
                        });
                    });
                }
            }
        });
    }
};


























