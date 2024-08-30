// Copyright (c) 2024, Administrator and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Students Master Data", {
// 	refresh(frm) {

// 	},
// });



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

//////////////////////////  Existing code for all functionalities of sync and delete //////////////////////////

// frappe.listview_settings['Students Master Data'] = {
//     onload: function(listview) {
//         // Initially, don't show any button
//         frappe.call({
//             method: 'tnc_frappe_custom_app.sync.check_all_imported',
//             callback: function(response) {
//                 if (response.message === "no_data") {
//                     // No button should be shown if there's no data
//                     return;
//                 } else if (response.message === "all_imported") {
//                     // Show "Delete Data" button if all records are imported
//                     listview.page.add_inner_button(__('Delete Data'), function() {
//                         frappe.confirm(
//                             __('Are you sure you want to delete all records?'),
//                             function() {
//                                 frappe.call({
//                                     method: 'tnc_frappe_custom_app.sync.delete_data',
//                                     callback: function(response) {
//                                         if (response.message === "success") {
//                                             frappe.msgprint(__('All data deleted successfully!'));
//                                             listview.refresh();  // Refresh the list view
//                                         } else {
//                                             frappe.msgprint(__('There was an issue deleting the data.'));
//                                         }
//                                     },
//                                     error: function(err) {
//                                         frappe.msgprint(__('Error while deleting the data.'));
//                                     }
//                                 });
//                             }
//                         );
//                     });
//                 } else if (response.message === "not_imported") {
//                     // Show "Sync Data" button if there are records that need to be imported
//                     listview.page.add_inner_button(__('Sync Data'), function() {
//                         frappe.call({
//                             method: 'tnc_frappe_custom_app.sync.sync_data',
//                             callback: function(response) {
//                                 if (response.message === "success") {
//                                     frappe.msgprint(__('Data synced successfully!'));
//                                     listview.refresh();  // Refresh the list view to check the status again
//                                 } else {
//                                     frappe.msgprint(__('There was an issue with syncing the data.'));
//                                 }
//                             },
//                             error: function(err) {
//                                 frappe.msgprint(__('Syncing the data is not possible.'));
//                             }
//                         });
//                     });
//                 }
//             }
//         });
//     }
// };


///////////////////////////// Below code is only for the Sync Data if the check box is Not checked //////////////////////////////


// frappe.listview_settings['Students Master Data'] = {
//     onload: function(listview) {
//         // Call server to check the data import status
//         frappe.call({
//             method: 'tnc_frappe_custom_app.sync.check_all_imported',
//             callback: function(response) {
//                 if (response.message === "no_data") {
//                     // No button should be shown if there's no data
//                     return;
//                 } else if (response.message === "not_imported") {
//                     // Show "Sync Data" button if there are records that need to be imported
//                     listview.page.add_inner_button(__('Sync Data'), function() {
//                         frappe.call({
//                             method: 'tnc_frappe_custom_app.sync.sync_data',
//                             callback: function(response) {
//                                 if (response.message === "success") {
//                                     frappe.msgprint(__('Data synced successfully!'));
//                                     listview.refresh();  // Refresh the list view to check the status again
//                                 } else {
//                                     frappe.msgprint(__('There was an issue with syncing the data.'));
//                                 }
//                             },
//                             error: function(err) {
//                                 frappe.msgprint(__('Syncing the data is not possible.'));
//                             }
//                         });
//                     });
//                 }
//                 // No code for "Delete Data" button
//             }
//         });
//     }
// };

////////////////////// Belwo code is to add the buttons in the Students Master Doctype List view //////////////////

// frappe.listview_settings['Students Master Data'] = {
//     onload: function(listview) {
//         // Add "Sync Data" button to the inner toolbar
//         listview.page.add_inner_button(__('Sync Data'), function() {
//             frappe.call({
//                 method: 'tnc_frappe_custom_app.sync.sync_data',
//                 callback: function(response) {
//                     if (response.message === "success") {
//                         frappe.msgprint(__('Data synced successfully!'));
//                         listview.refresh();  // Refresh the list view to check the status again
//                     } else {
//                         frappe.msgprint(__('There was an issue with syncing the data.'));
//                     }
//                 },
//                 error: function(err) {
//                     frappe.msgprint(__('Syncing the data is not possible.'));
//                 }
//             });
//         });

//         // Add "Generate Ranks" button to the inner toolbar
//         listview.page.add_inner_button(__('Generate Ranks'), function() {
//             frappe.prompt([
//                 {fieldname: 'start_rank', label: 'Start Rank', fieldtype: 'Int', reqd: 1},
//                 {fieldname: 'initial_regularised_ranks', label: 'Initial Regularised Ranks', fieldtype: 'Int', reqd: 1},
//                 {fieldname: 'last_regularised_ranks', label: 'Last Regularised Ranks', fieldtype: 'Int', reqd: 1},
//                 {fieldname: 'last_rank', label: 'Last Rank', fieldtype: 'Int', reqd: 1},
//                 {fieldname: 'actual_candidates', label: 'Actual Candidates', fieldtype: 'Int', reqd: 1}
//             ], function(values) {
//                 frappe.call({
//                     method: 'tnc_frappe_custom_app.rank_generation.generate_ranks',
//                     args: values,
//                     freeze: true,
//                     callback: function(response) {
//                         frappe.msgprint(__('Ranks have been generated and assigned.'));
//                         listview.refresh();
//                     }
//                 });
//             }, 'Generate Ranks', 'OK');
//         });
//     }
// };





















