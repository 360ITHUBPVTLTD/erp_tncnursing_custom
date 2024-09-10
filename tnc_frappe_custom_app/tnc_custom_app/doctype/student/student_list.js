
// frappe.listview_settings['Student'] = {
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

///////////////////Below is the BUlk message button whatsapp ///////////////////////////////////////////////
// frappe.listview_settings['Student'] = {
//     onload: function (listview) {
//         listview.page.add_inner_button(__('Bulk WA'), function () {
//             frappe.prompt({
//                 fieldtype: 'Small Text',
//                 fieldname: 'message_text',
//                 label: __('Enter message text'),
//                 reqd: false,
//             }, function (values) {
//                 frappe.confirm(
//                     __('Are you sure you want to send bulk WhatsApp messages to all students?'),
//                     function () {
//                         frappe.call({
//                             method: 'tnc_frappe_custom_app.custom_whatsapp.send_bulk_whatsapp_messages',
//                             args: {
//                                 // message: values.
//                             },
//                             callback: function (response) {
//                                 if (response.message) {
//                                     frappe.msgprint(__('Bulk WhatsApp messages sent successfully!'));
//                                 }
//                             }
//                         });
//                     }
//                 );
//             });
//         });
//     }
// };

