// Copyright (c) 2024, Administrator and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Students Master Data", {
// 	refresh(frm) {

// 	},
// });





frappe.listview_settings['Students Master Data'] = {
    onload: function(listview) {

        // Add a custom menu item to trigger duplicate removal.
        listview.page.add_inner_button(__('Remove Duplicates'), function() {
            // Create a dialog to accept the doctype and exam_id
            let d = new frappe.ui.Dialog({
                title: 'Remove Duplicate Records',
                fields: [
                    {
                        "fieldname": "doctype",
                        "fieldtype": "Select",
                        "label": "Select Doctype",
                        "options": "\nStudents Master Data\nStudent Results",
                        "reqd": 1
                    },
                    {
                        "fieldname": "exam_id",
                        "fieldtype": "Link",
                        "label": "Exam ID",
                        "options": "Student Exam",
                        "reqd": 1
                    }
                ]
            });
            
            // Primary action - trigger backend function based on input
            d.set_primary_action(__('Submit'), function() {
                let values = d.get_values();
                if(values) {
                    let backend_method = "";
                    
                    // Determine which backend method to call based on the selected doctype.
                    if(values.doctype === 'Students Master Data'){
                        backend_method = "tnc_frappe_custom_app.tnc_custom_app.doctype.students_master_data.students_master_data.remove_duplicate_students_master_data";
                    } else if(values.doctype === 'Student Results'){
                        backend_method = "tnc_frappe_custom_app.tnc_custom_app.doctype.students_master_data.students_master_data.remove_duplicate_student_results";
                    } else {
                        frappe.msgprint(__("Invalid doctype selected."));
                        return;
                    }
                    
                    // Call the corresponding backend function with the provided exam_id.
                    frappe.call({
                        method: backend_method,
                        args: {
                            exam_id: values.exam_id
                        },
                        callback: function(r) {
                            if(r.message) {
                                frappe.msgprint(__("Result: " + r.message));
                            }
                        }
                    });
                    d.hide();
                }
            });
            
            d.show();
        });

        // listview.page.add_inner_button(__('Delete Data'), function() {
        //     // Show a confirmation dialog
        //     frappe.confirm(
        //         'Are you sure you want to delete all records?',
        //         function() {
        //             // If confirmed, make a Frappe call to the server
        //             frappe.call({
        //                 method: 'tnc_frappe_custom_app.delete_import_data_master_students.delete_all_records',
        //                 callback: function(response) {
        //                     if (response.message === 'success') {
        //                         frappe.show_alert({
        //                             message: __('All records have been deleted successfully.'),
        //                             indicator: 'green'
        //                         });
        //                         listview.refresh(); // Refresh the list view to reflect the changes
        //                     } else {
        //                         frappe.show_alert({
        //                             message: __('There was an issue deleting the records.'),
        //                             indicator: 'red'
        //                         });
        //                     }
        //                 }
        //             });
        //         }
        //     );
        // });

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
        // listview.page.add_inner_button('Process Data', () => {
        //             frappe.prompt(
        //                 {
        //                     label: 'File ID',
        //                     fieldname: 'file_id',
        //                     fieldtype: 'Data',
        //                     reqd: 1
        //                 },
        //                 (values) => {
        //                     frappe.call({
        //                         method: 'tnc_frappe_custom_app.script_to_import_data.import_student_results_sql_student_master_data',
        //                         args: { file_id: values.file_id },
        //                         callback: function(r) {
        //                             if (!r.exc) {
        //                                 frappe.msgprint('Data processing started. Check logs for updates.');
        //                             }
        //                         }
        //                     });
        //                 },
        //                 'Enter File ID',
        //                 'Start Processing'
        //             );
        //  });

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
                        method: 'tnc_frappe_custom_app.script_to_import_data.process_excel_to_create_a_student_exam_from_client_script',
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

///////////////////////// Below is the button for Sync unimported records //////////////////////////

// // File: student_masters_data_list.js
// frappe.listview_settings['Students Master Data'] = {
//     onload: function(listview) {
//         listview.page.add_inner_button(__('Sync Unimported Data'), function() {
//             frappe.confirm(
//                 'Are you sure you want to fetch the unimported Records?',
//             function() {
//             frappe.call({
//                 method: "tnc_frappe_custom_app.tnc_custom_app.doctype.students_master_data.students_master_data.sync_uninported_data",
//                 callback: function(r) {
//                     // console.log(r.message.status)
//                     if (r.message.status === 'success') {
//                         frappe.msgprint(__('Data synced successfully!'));
//                     } else {
//                         frappe.msgprint(__('Failed to sync data.'));
//                     }
//                 }
//             });
//           });
//         });
//     }
// };


















