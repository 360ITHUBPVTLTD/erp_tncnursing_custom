// Copyright (c) 2024, Administrator and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Students Master Data", {
// 	refresh(frm) {

// 	},
// });

frappe.listview_settings['Students Master Data'] = {
    onload: function(listview) {
        listview.page.add_inner_button(__('Sync Data'), function() {
            console.log('Sync Data button clicked');
            frappe.call({
                method: 'tnc_frappe_custom_app.sync.sync_data',
                callback: function(response) {
                    if(response.message === "success") {
                        frappe.msgprint(__('Data synced successfully!'));
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
};

// frappe.listview_settings['Students Master Data'] = {
//     onload: function(listview) {
//         console.log('ListView onload event triggered');

//         // Function to add the 'Sync Data' button if there are records
//         function add_sync_button() {
//             if (listview.get_total_count() > 0) {  // Check if there are records
//                 listview.page.add_inner_button(__('Sync Data'), function() {
//                     console.log('Sync Data button clicked');
//                     frappe.call({
//                         method: 'tnc_frappe_custom_app.sync.sync_data',
//                         callback: function(response) {
//                             console.log('Sync Data response:', response);
//                             if(response.message === "success") {
//                                 frappe.msgprint(__('Data synced successfully!'));
//                             } else {
//                                 frappe.msgprint(__('There was an issue with syncing the data.'));
//                             }
//                         },
//                         error: function(err) {
//                             console.error(err);
//                             frappe.msgprint(__('An error occurred while syncing the data.'));
//                         }
//                     });
//                 });
//             }
//         }

//         // Add button initially if there are records
//         add_sync_button();

//         // Also, handle case when data is dynamically loaded
//         listview.on('refresh', function() {
//             console.log('ListView refreshed');
//             add_sync_button();
//         });
//     }
// };
