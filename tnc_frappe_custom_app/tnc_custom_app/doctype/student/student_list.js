
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

///////////////////Below is the BUlk message button whatsapp ///////////////////////////////////////////////

// frappe.listview_settings['Student'] = {
//     onload: function (listview) {
//         listview.page.add_inner_button(__('Bulk WhatsApp'), function () {
//             // Prompt user to enter a custom message
//             frappe.prompt({
//                 fieldtype: 'Small Text',
//                 fieldname: 'message_text',
//                 label: __('Enter the message text to send to all students'),
//                 reqd: true  // Make the field mandatory
//             }, function (values) {
//                 // Confirm sending messages
//                 frappe.confirm(
//                     __('Are you sure you want to send bulk WhatsApp messages to all students?'),
//                     function () {
//                         // Show a notification that the messages are being sent
//                         frappe.show_alert({
//                             message: __('Sending WhatsApp messages...'),
//                             indicator: 'blue'
//                         });

//                         // Call the server-side method to send bulk messages
//                         frappe.call({
//                             method: 'tnc_frappe_custom_app.custom_whatsapp.send_bulk_whatsapp_messages',
//                             args: {
//                                 message_text: values.message_text  // Pass the message entered in the prompt
//                                 // name: frm.doc.name,

//                             },
//                             callback: function (response) {
//                                 if (response.message) {
//                                     frappe.msgprint(__('Bulk WhatsApp messages sent successfully!'));
//                                 } else {
//                                     frappe.msgprint(__('Failed to send bulk WhatsApp messages.'));
//                                 }
//                             },
//                             error: function (err) {
//                                 frappe.msgprint(__('There was an error sending the messages. Please try again.'));
//                                 console.error(err);  // Log error for debugging
//                             }
//                         });
//                     }
//                 );
//             });
//         });
//     }
// };



