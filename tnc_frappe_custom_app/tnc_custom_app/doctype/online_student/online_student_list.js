
// frappe.listview_settings['Online Student'] = {
//     onload: function(listview) {
//         listview.page.add_inner_button(__('Delete Data'), function() {
//             // Show a confirmation dialog
//             frappe.confirm(
//                 'Are you sure you want to delete all records?',
//                 function() {
//                     // If confirmed, make a Frappe call to the server
//                     frappe.call({
//                         method: 'tnc_frappe_custom_app.delete_import_data_master_students.delete_all_records_in_student',
//                         callback: function(response) {
//                             if (response.message === 'success') {
//                                 frappe.show_alert({
//                                     message: __('All records have been deleted successfully.'),
//                                     indicator: 'green'
//                                 });
//                                 listview.refresh(); // Refresh the list view to reflect the changes
//                             } else {
//                                 frappe.show_alert({
//                                     message: __('There was an issue deleting the records.'),
//                                     indicator: 'red'
//                                 });
//                             }
//                         }
//                     });
//                 }
//             );
//         });
//     }
// };

////////////////////////////////  Official whatsapp button  /////////////////////////////////////////////
// frappe.listview_settings['Online Student'] = {
//     onload: function(listview) {
//         listview.page.add_inner_button(__('Bulk Send Results'), function() {
//             frappe.confirm(
//                 __('Are you sure you want to send results to all students?'),
//                 function() {
//                     frappe.call({
//                         method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.online_student.online_student.send_bulk_student_results_to_students',
                        
//                         callback: function(r) {
//                             if (!r.exc) {
//                                 frappe.msgprint(__('Results sent successfully'));
//                             } else {
//                                 frappe.msgprint(__('Failed to send results. Check logs for details.'));
//                             }
//                         }
//                     });
//                 }
//             );
//         },("Actions"));
//     }
// };



// frappe.listview_settings['Online Student'] = {
//     onload: function(listview) {
//         // Add "Bulk Send Results" button
//         listview.page.add_inner_button(__('Bulk Send Results'), function() {
//             frappe.confirm(
//                 __('Are you sure you want to send results to all students?'),
//                 function() {
//                     frappe.call({
//                         method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.online_student.online_student.send_bulk_student_results_to_students',
//                         callback: function(r) {
//                             if (!r.exc) {
//                                 frappe.msgprint(__('Results sent successfully'));
//                             } else {
//                                 frappe.msgprint(__('Failed to send results. Check logs for details.'));
//                             }
//                         }
//                     });
//                 }
//             );
//         }, __("Actions"));

//         // Add "Send Selected Students" button
//         listview.page.add_inner_button(__('Send Selected Students'), function() {
//             frappe.call({
//                 method: "tnc_frappe_custom_app.tnc_custom_app.doctype.online_student.online_student.get_online_students",
//                 callback: function(response) {
//                     if (response.message) {
//                         let student_options = response.message.map(student => ({
//                             label: `${student.student_name} (${student.name}) - ${student.mobile || 'No Mobile'}`,
//                             value: student.name,
//                             mobile: student.mobile || 'No Mobile'
//                         }));

//                         // Preserve the selected values and keep them at the top
//                         let selected_values = [];

//                         let dialog = new frappe.ui.form.MultiSelectDialog({
//                             doctype: "Online Student",
//                             target: listview,
//                             setters: {
//                                 student_name: null,
//                                 mobile: null
//                             },
//                             data: student_options,
//                             primary_action_label: __('Send'),
//                             action(selected_values_list) {
//                                 if (!selected_values_list || selected_values_list.length === 0) {
//                                     frappe.msgprint(__('Please select at least one student.'));
//                                     return;
//                                 }

//                                 let selected_students = student_options.filter(opt => selected_values_list.includes(opt.value));

//                                 let student_ids = selected_students.map(s => s.value);
//                                 let student_names = selected_students.map(s => s.label.split(" - ")[0]);
//                                 let student_mobiles = selected_students.map(s => s.mobile);

//                                 frappe.call({
//                                     method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.online_student.online_student.send_results_to_selected_students',
//                                     args: {
//                                         student_ids: student_ids,
//                                         student_names: student_names,
//                                         student_mobiles: student_mobiles
//                                     },
//                                     callback: function(r) {
//                                         if (!r.exc) {
//                                             frappe.msgprint(__('Results sent successfully to selected students.'));
//                                             selected_values = [...selected_values_list]; // Store selected values
//                                             dialog.dialog.hide();
//                                         } else {
//                                             frappe.msgprint(__('Failed to send results. Check logs for details.'));
//                                         }
//                                     }
//                                 });
//                             }
//                         });

//                         // Show selected values at the top
//                         dialog.dialog.fields_dict['selected'].$wrapper.find('.form-control').on('input', function() {
//                             let input = $(this).val().toLowerCase();
//                             let filtered = student_options.filter(s => s.label.toLowerCase().includes(input));
                            
//                             let selected_options = filtered.filter(s => selected_values.includes(s.value));
//                             let unselected_options = filtered.filter(s => !selected_values.includes(s.value));

//                             let sorted_options = [...selected_options, ...unselected_options];

//                             dialog.dialog.fields_dict['selected'].$wrapper.find('.awesomplete ul').empty();

//                             sorted_options.forEach(s => {
//                                 dialog.dialog.fields_dict['selected'].$wrapper.find('.awesomplete ul').append(`
//                                     <li data-value="${s.value}">${s.label}</li>
//                                 `);
//                             });
//                         });

//                     } else {
//                         frappe.msgprint(__('No students found.'));
//                     }
//                 }
//             });
//         }, __("Actions"));
//     }
// };



