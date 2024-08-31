// Copyright (c) 2024, Administrator and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Student Exam", {
// 	refresh(frm) {

// 	},
// });

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// frappe.ui.form.on('Student Exam', {
//     refresh: function(frm) {
//         // Check if the 'exam_id_linked' field is already checked
//         if (!frm.doc.exam_id_linked) {
//             // If not, add the custom button
//             frm.add_custom_button(__('Sync Exam ID'), function() {
//                 frappe.call({
//                     method: 'tnc_frappe_custom_app.data_import_id.update_imported_batch_id',
//                     args: {
//                         exam_id: frm.doc.name  // Send the current document name (Student Exam ID)
//                     },
//                     callback: function(r) {
//                         if (r.message.status === 'success') {
//                             frappe.msgprint(__('Student Master Data updated successfully!'));

//                             // Check the 'exam_id_linked' field
//                             frm.set_value('exam_id_linked', 1);

//                             // Save the form to update the 'exam_id_linked' field in the backend
//                             frm.save().then(() => {
//                                 // Hide the button after saving
//                                 frm.reload_doc();
//                             });
//                         } else {
//                             frappe.msgprint(__('Error: ' + r.message.message));
//                         }
//                     }
//                 });
//             });
//         }
//     }
// });

/////////////////////// Below is the Sync and Generate the rank button ///////////////////////////
// frappe.ui.form.on('Student Exam', {
//     refresh: function(frm) {
//         // Add "Sync Data" button to the form view
//         frm.add_custom_button(__('Sync Data'), function() {
//             frappe.call({
//                 method: 'tnc_frappe_custom_app.sync.sync_data',
//                 args: {
//                     name: frm.doc.name  // Add the form name to the arguments
//                     },
//                 callback: function(response) {
//                     if (response.message === "success") {
//                         frappe.msgprint(__('Data synced successfully!'));
//                         frm.set_value('data_synced', 1);
//                         frm.save()
//                         frm.refresh();  // Refresh the form view to check the status again
//                     } else {
//                         frappe.msgprint(__('There was an issue with syncing the data.'));
//                     }
//                 },
//                 error: function(err) {
//                     frappe.msgprint(__('Syncing the data is not possible.'));
//                 }
//             });
//         });

//         // Add "Generate Ranks" button to the form view
//         frm.add_custom_button(__('Generate Ranks'), function() {
//             frappe.prompt([
//                 {fieldname: 'start_rank', label: 'Start Rank', fieldtype: 'Int', reqd: 1},
//                 {fieldname: 'initial_regularised_ranks', label: 'Initial Regularised Ranks', fieldtype: 'Int', reqd: 1},
//                 {fieldname: 'last_regularised_ranks', label: 'Last Regularised Ranks', fieldtype: 'Int', reqd: 1},
//                 {fieldname: 'last_rank', label: 'Last Rank', fieldtype: 'Int', reqd: 1},
//                 {fieldname: 'actual_candidates', label: 'Actual Candidates', fieldtype: 'Int', reqd: 1}
//             ], function(values) {
//                 frappe.call({
//                     method: 'tnc_frappe_custom_app.rank_generation.generate_ranks',
//                     args: {
//                         ...values,  // Spread the values from the prompt
//                         docname: frm.doc.name  // Add the form name to the arguments
//                     },
//                     freeze: true,
//                     callback: function(response) {
//                         frappe.msgprint(__('Ranks have been generated and assigned.'));
//                         frm.refresh();
//                     }
//                 });
//             }, 'Generate Ranks', 'OK');
//         });
//     }
// });

/////////////// Aug 31 Modification Below code if there is no data in the SMD doctype it will throw error //////////////////////
frappe.ui.form.on('Student Exam', {
    refresh: function(frm) {
        // Add "Sync Data" button to the form view
        frm.add_custom_button(__('Sync Data'), function() {
            frappe.call({
                method: 'tnc_frappe_custom_app.sync.sync_data',
                args: {
                    name: frm.doc.name  // Add the form name to the arguments
                },
                callback: function(response) {
                    if (response.message === "success") {
                        frappe.msgprint(__('Data synced successfully!'));
                        frm.set_value('data_synced', 1);  // Only set to 1 if data was synced
                        frm.save();
                        frm.refresh();  // Refresh the form view to check the status again
                    } else if (response.message === "no_data") {
                        frappe.msgprint(__('No data available to sync.'));
                    } else {
                        frappe.msgprint(__('There was an issue with syncing the data.'));
                    }
                },
                error: function(err) {
                    frappe.msgprint(__('Syncing the data is not possible.'));
                }
            });
        });

        // Add "Generate Ranks" button to the form view
        frm.add_custom_button(__('Generate Ranks'), function() {
            frappe.prompt([
                {fieldname: 'start_rank', label: 'Start Rank', fieldtype: 'Int', reqd: 1},
                {fieldname: 'initial_regularised_ranks', label: 'Initial Regularised Ranks', fieldtype: 'Int', reqd: 1},
                {fieldname: 'last_regularised_ranks', label: 'Last Regularised Ranks', fieldtype: 'Int', reqd: 1},
                {fieldname: 'last_rank', label: 'Last Rank', fieldtype: 'Int', reqd: 1},
                {fieldname: 'actual_candidates', label: 'Actual Candidates', fieldtype: 'Int', reqd: 1}
            ], function(values) {
                frappe.call({
                    method: 'tnc_frappe_custom_app.rank_generation.generate_ranks',
                    args: {
                        ...values,  // Spread the values from the prompt
                        docname: frm.doc.name  // Add the form name to the arguments
                    },
                    freeze: true,
                    callback: function(response) {
                        if (response.message === "no_data") {
                            frappe.msgprint(__('No data available to generate ranks.'));
                        } else if (response.message === "ranks_assigned") {
                            frappe.msgprint(__('Ranks have been generated and assigned.'));
                            frm.refresh();
                        } else {
                            frappe.msgprint(response.message);  // Show specific error message from server
                        }
                    }
                });
            }, 'Generate Ranks', 'OK');
        });
    }
});



