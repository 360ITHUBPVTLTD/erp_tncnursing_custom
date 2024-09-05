// Copyright (c) 2024, Administrator and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Student", {
// 	refresh(frm) {

// 	},
// });


////////////////// Payment Link Generating in CLient script //////////////////

// frappe.ui.form.on('Student', {
//     refresh: function(frm) {
//         frappe.call({
//             method: 'frappe.client.get_list',
//             args: {
//                 doctype: 'Razorpay Payment Links',
//                 filters: {
//                     'student_id': frm.doc.name,
//                     'status': ['in', ['Created', 'Paid']]
//                 },
//                 fields: ['name']
//             },
//             callback: function(response) {
//                 if (response.message && response.message.length > 0) {
//                     frm.clear_custom_buttons();
//                 } else {
//                     frm.add_custom_button(__('Generate Payment Link'), function() {
//                         frappe.confirm(
//                             'Are you sure you want to generate the payment link?',
//                             function() {
//                                 frm.call({
//                                     method: 'tnc_frappe_custom_app.razorpay_payment_link.generate_payment_link',
//                                     args: {
//                                         student_id: frm.doc.name,
//                                         amount: frm.doc.amount,
//                                         description: 'Payment for student fees'
//                                     },
//                                     callback: function(response) {
//                                         if (response.message && response.message.short_url) {
//                                             frappe.msgprint(__('Payment Link Generated Successfully'));

//                                             // Set the payment link value in the Student doctype
//                                             frm.set_value('payment_link', response.message.short_url);
                                            
//                                             // Automatically save the form after setting the payment link
//                                             frm.save();
//                                         } else {
//                                             frappe.msgprint(__('Failed to generate payment link.'));
//                                         }
//                                     }
//                                 });
//                             }
//                         );
//                     });
//                 }
//             }
//         });
//     }
// });


frappe.ui.form.on('Student', {
    refresh: function(frm) {
        // Add a custom button
        frm.add_custom_button(__('Send WhatsApp Message'), function() {
            // Get student details
            let name = frm.doc.name;
            let mobile_number = frm.doc.mobile;
            let student_name = frm.doc.student_name;

            // Make an AJAX call to the server script
            frappe.call({
                method: 'tnc_frappe_custom_app.custom_whatsapp.send_whatsapp_message',  // Change to your Python file path
                args: {
                    name: name,
                    mobile_number: mobile_number,
                    student_name: student_name
                },
                callback: function(response) {
                    if (response.message === 'Success') {
                        frappe.msgprint(__('WhatsApp message sent successfully!'));
                    } else {
                        frappe.msgprint(__('Failed to send WhatsApp message.'));
                    }
                },
                error: function(err) {
                    frappe.msgprint(__('Error occurred while sending the WhatsApp message.'));
                }
            });
        });
    }
});


////////////////// Print format  Button on Student Form for their desired subject//////////////////

frappe.ui.form.on('Student', {
    refresh: function(frm) {
        frm.add_custom_button(__('Print'), function() {
            // Call the custom function to handle the prompt and printing
            show_print_prompt(frm);
        });
    }
});

function show_print_prompt(frm) {
    // Fetch exam_name from Student Results where student_id = frm.doc.name
    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'Student Results',
            filters: {
                student_id: frm.doc.name
            },
            fields: ['exam_title_name']
        },
        callback: function(r) {
            if (r.message) {
                // Extract exam_name values
                let exam_names = r.message.map(result => result.exam_title_name);

                // Show the prompt
                frappe.prompt([
                    {
                        label: 'Student Name',
                        fieldname: 'student_name',
                        fieldtype: 'Data',
                        default: frm.doc.student_name,
                        read_only: 1
                    },
                    {
                        label: 'Mobile',
                        fieldname: 'mobile',
                        fieldtype: 'Data',
                        default: frm.doc.mobile,
                        read_only: 1
                    },
                    {
                        label: 'Subject',
                        fieldname: 'subject',
                        fieldtype: 'MultiSelect',
                        options: exam_names.join('\n'),
                        reqd: 1
                    }
                ],
                function(values){
                    // Update the subject field in the Student doctype
                    frm.set_value('subjects', values.subject);

                    // Save the form
                    frm.save().then(function() {
                        // Redirect to the print page after saving
                        // window.location.href = `http://192.168.1.128:8010/app/print/Student/${frm.doc.name}`;
                        window.location.href = `http://3.111.226.95/api/method/frappe.utils.print_format.download_pdf?doctype=Student&name=${frm.doc.name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang=en`;
                    });
                },
                __('Print Student Information'),
                __('Print'));
            }
        }
    });
}


///////////////////////////// Below code is to redirect the Student results doctype for the particular filters(student_id) /////////
frappe.ui.form.on('Student', {
    refresh: function(frm) {
        // Add the "Go to Result" button
        frm.add_custom_button(__('Go to Result'), function() {
            // Get the student's name from the form
            var student_id = frm.doc.name;
            
            // Construct the URL with the filter
            var url = `/app/student-results?student_id=${encodeURIComponent(student_id)}`;
            
            // Redirect to the Student Results doctype with the filter
            window.open(url, '_blank');  // Open in a new tab
        });
    }
});


