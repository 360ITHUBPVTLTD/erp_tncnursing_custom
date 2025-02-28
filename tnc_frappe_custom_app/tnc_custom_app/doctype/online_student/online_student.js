// Copyright (c) 2024, Administrator and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Online Student", {
// 	refresh(frm) {

// 	},
// });


////////////////// Payment Link Generating in CLient script //////////////////

// frappe.ui.form.on('Online Student', {
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

//                                             // Set the payment link value in the Online Student doctype
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

//////////////////////////// Below is the whatsapp button Functionality( WITH PDF ) //////////////////////////////////////////////////////////////



// frappe.ui.form.on('Online Student', {
//     refresh: function(frm) {
//         // Add a custom button
//         // frappe.call({
//         //     method: 'tnc_frappe_custom_app.custom_whatsapp.valiadting_user_for_bulk_wa_msg',  // Your server script method path
//         //     args: {
//         //     },
//         //     callback: function(respWAValid) {
//         //         if(respWAValid.message && respWAValid.message.status){
//                     frm.add_custom_button(__('Send WhatsApp Message'), function() {
//                         // Get student details
//                         let name = frm.doc.name;
//                         let mobile_number = frm.doc.mobile;
//                         let student_name = frm.doc.student_name;

//                         // Prompt the user for the mobile number and custom message
//                         frappe.prompt([
//                             {
//                                 label: 'Mobile Number',
//                                 fieldname: 'mobile_number',
//                                 fieldtype: 'Data',
//                                 default: mobile_number,  // Pre-fill the mobile number
//                                 reqd: 1  // Make the field mandatory
//                             },
//                             {
//                                 label: 'Message',
//                                 fieldname: 'message',
//                                 fieldtype: 'Small Text',
//                                 reqd: 1,
//                                 default: `Assessment Report by TNC Experts
                        
// You are doing very good 👍    

// Your score is very fantastic. According to TNC experts, you will achieve a good rank in NORCET Exam.

// Video link :
// https://drive.google.com/file/d/1ewpJJMgrZOa6n0eOipKK9RyZftGzPW4t/view?usp=sharing

// 🎯📚 Just continue your hard work and study, maximum question practice, 
// and try to control minus marking.

// 🎖️ We hope strongly that you are our next interviewer on our TNC YouTube channel.

// 👍 Be confident and be consistent.

// 💐 All the Best and Best wishes.

// आपकी सफलता वाली कॉल का इंतजार रहेगा।
                        
// Thanks

// AIIMS 20+ Expert TNC TEAM
                        
// If you need any help and assistance, please message us on the official number:

// 7484999051
// TNC Nursing`,
//                                 reqd: 1  // Make the field mandatory
//                             }
//                         ],
//                         function(values){
//                             // Confirm the action before sending
//                             frappe.confirm(
//                                 __('Are you sure you want to send this message?'),
//                                 function() {
//                                     // If confirmed, proceed with WhatsApp message sending
//                                     frappe.call({
//                                         method: 'tnc_frappe_custom_app.custom_whatsapp.send_whatsapp_pdf_message',  // Your server script method path
//                                         args: {
//                                             name: name,
//                                             mobile_number: values.mobile_number,  // Use the value from the prompt
//                                             student_name: student_name,
//                                             message: values.message  // Custom message entered by the user
//                                         },
//                                         callback: function(response) {
//                                             // console.log(response.message);
//                                             // console.log(response.message.status);
//                                             if (response.message.status === 'Success') {
//                                                 frappe.msgprint(__('WhatsApp message sent successfully!'));
//                                             } else {
//                                                 frappe.msgprint(__('Failed to send WhatsApp message.'));
//                                             }
//                                         },
//                                         error: function(err) {
//                                             frappe.msgprint(__('Error occurred while sending the WhatsApp message.'));
//                                         }
//                                     });
//                                 }
//                             );
//                         },
//                         __('Enter Mobile Number and Message'),  // Dialog title
//                         __('Send WhatsApp')  // Button text  
//                         );
//                     });
//         //         }
//         //     },
//         //     error: function(err) {
//         //         // frappe.msgprint(__('Not Authenticated user to send WA'));
//         //     }
//         // });
//     }
// });




//////////////////////////////////// Print Button in the Form View //////////////////////////////////

frappe.ui.form.on('Online Student', {
    refresh: function(frm) {
        frm.add_custom_button(__('Print'), function() {
            // Call the custom function to handle the prompt and printing
            show_print_prompt(frm);
        });
    }
});

function show_print_prompt(frm) {
    // Fetch exam_name from Online Student Results where student_id = frm.doc.name
    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'Test Series Type',
            filters: {
                // student_id: frm.doc.name
            },
            fields: ['name1']
        },
        callback: function(r) {
            if (r.message) {
                // Extract exam_name values
                let exam_names = r.message.map(result => result.name1);

                // Show the prompt
                frappe.prompt([
                    {
                        label: 'Online Student Name',
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
                    // Update the subject field in the Online Student doctype
                    frm.set_value('subjects', values.subject);

                    // Save the form
                    frm.save().then(function() {
                        // Redirect to the print page after saving
                        const baseUrl = window.location.origin;
                        window.open(`${baseUrl}/api/method/frappe.utils.print_format.download_pdf?doctype=Online Student&name=${frm.doc.name}&format=Student%20Results%20PF&no_letterhead=0&letterhead=TNC%20Logo&settings=%7B%7D&_lang= en`);

                        // Clear the subject field after successful save
                        frm.set_value('subjects', '');
                        frm.refresh_field('subjects');
                        frm.save();
                    });
                },
                __('Print Online Student Information'),
                __('Print'));
            }
        }
    });
}


///////////////////////////// Below code is to redirect the Online Student results doctype for the particular filters(student_id) /////////
frappe.ui.form.on('Online Student', {
    refresh: function(frm) {
        // Add the "Go to Result" button
        frm.add_custom_button(__('Go to Result'), function() {
            // Get the student's name from the form
            var student_id = frm.doc.name;
            
            // Construct the URL with the filter
            var url = `/app/student-results?student_id=${encodeURIComponent(student_id)}`;
            
            // Redirect to the Online Student Results doctype with the filter
            window.open(url, '_blank');  // Open in a new tab
        });
    }
});

/////////////////////////////////////////

// frappe.ui.form.on('Online Student', {
//     refresh: function(frm) {
//         // Add a custom button
//         // frappe.call({
//         //     method: 'tnc_frappe_custom_app.custom_whatsapp.valiadting_user_for_bulk_wa_msg',  // Your server script method path
//         //     args: {
//         //     },
//         //     callback: function(respWAValid) {
//         //         if(respWAValid.message && respWAValid.message.status){
//                     frm.add_custom_button(__('Send WhatsApp'), function() {
//                         // Get student details
//                         let name = frm.doc.name;
//                         let mobile_number = frm.doc.mobile;
//                         let student_name = frm.doc.student_name;

//                         // Prompt the user for the mobile number and custom message
//                         frappe.prompt([
//                             {
//                                 label: 'Mobile Number',
//                                 fieldname: 'mobile_number',
//                                 fieldtype: 'Data',
//                                 default: mobile_number,  // Pre-fill the mobile number
//                                 reqd: 1  // Make the field mandatory
//                             },
//                             {
//                                 label: 'Message',
//                                 fieldname: 'message',
//                                 fieldtype: 'Small Text',
//                                 reqd: 1,
//                                 default: `Dear Online Students ,
 
// Many Many Congratulations
                                 
// I hope this message finds you well!
                                 
// The results for NORCET 7.0 prelims have been announced .
                                 
// Kindly check your result and inform us whether you have qualified or not.
                                 
// If you have qualified, please fill out the Google Form linked below to submit your details:
                                 
// https://docs.google.com/forms/d/e/1FAIpQLSelyNyqBGaU0AKkZrfrQaIjAEdlxHsX5Y1GYR0ALtUfjMkuRQ/viewform
                                 
// Congratulations to all the qualifiers! Your hard work and dedication have paid off, and we are truly proud of you.
                                 
// For those who didn’t qualify this time, remember this is just a step in the journey. Keep putting in the effort, and success will surely come your way!
                                 
// Warm regards,
// TNC Nursing classes`,
//                                 reqd: 1  // Make the field mandatory
//                             }
//                         ],
//                         function(values){
//                             // Confirm the action before sending
//                             frappe.confirm(
//                                 __('Are you sure you want to send this message?'),
//                                 function() {
//                                     // If confirmed, proceed with WhatsApp message sending
//                                     frappe.call({
//                                         method: 'tnc_frappe_custom_app.custom_whatsapp.send_whatsapp_custom_message',  // Your server script method path
//                                         args: {
//                                             name: name,
//                                             mobile_number: values.mobile_number,  // Use the value from the prompt
//                                             student_name: student_name,
//                                             message: values.message  // Custom message entered by the user
//                                         },
//                                         callback: function(response) {
//                                             // console.log(response.message);
//                                             // console.log(response.message.status);
//                                             if (response.message.status === 'Success') {
//                                                 frappe.msgprint(__('WhatsApp message sent successfully!'));
//                                             } else {
//                                                 frappe.msgprint(__('Failed to send WhatsApp message.'));
//                                             }
//                                         },
//                                         error: function(err) {
//                                             frappe.msgprint(__('Error occurred while sending the WhatsApp message.'));
//                                         }
//                                     });
//                                 }
//                             );
//                         },
//                         __('Enter Mobile Number and Message'),  // Dialog title
//                         __('Send WhatsApp')  // Button text
//                         );
//                     });
//         //         }
//         //     },
//         //     error: function(err) {
//         //         // frappe.msgprint(__('Not Authenticated user to send WA'));
//         //     }
//         // });
//     }
// });








////////// Below is the Template selector sending message to the Online Students( WITHOUT PDF )//////////////////////////

// frappe.ui.form.on('Online Student', {
//     refresh: function(frm) {
//         frm.add_custom_button(__('WhatsApp Template Message'), function() {
//             // Create the prompt dialog
//             let mobile_number = frm.doc.mobile;
//             let dialog = new frappe.ui.Dialog({
//                 title: 'Send WhatsApp Message',
//                 fields: [
//                     {
//                         'fieldname': 'mobile_number', 
//                         'fieldtype': 'Data', 
//                         'label': 'Mobile Number', 
//                         'default': mobile_number,
//                         'reqd': 1
//                     },
//                     {
//                         'fieldname': 'template', 
//                         'fieldtype': 'Link', 
//                         'label': 'Choose Template', 
//                         'options': 'WhatsApp Templates', 
//                         'reqd': 1
//                     },
//                     {
//                         'fieldname': 'message', 
//                         'fieldtype': 'Small Text', 
//                         'label': 'Message', 
//                         'read_only': 0,
//                     }
//                 ],
//                 primary_action: function(values) {
//                     // Hide the current dialog
//                     dialog.hide();

//                     // Show confirmation dialog
//                     frappe.confirm(
//                         __('Are you sure you want to send this message?'),
//                         () => {
//                             // Send the WhatsApp message
//                             frappe.call({
//                                 method: 'tnc_frappe_custom_app.custom_whatsapp.send_whatsapp_Template_message',
//                                 args: {
//                                     name: frm.doc.name,
//                                     mobile_number: values.mobile_number,
//                                     student_name: frm.doc.student_name,
//                                     template: values.template,
//                                     message: values.message
//                                 },
//                                 callback: function(response) {
//                                     if (response.message) {
//                                         frappe.show_alert({
//                                             message: __('Message sent successfully!'),
//                                             indicator: 'green'
//                                         });
//                                     } else {
//                                         frappe.show_alert({
//                                             message: __('Failed to send message.'),
//                                             indicator: 'red'
//                                         });
//                                     }
//                                 }
//                             });
//                         },
//                         () => {
//                             // User clicked "No"
//                             console.log('Message sending canceled.');
//                         }
//                     );
//                 },
//                 primary_action_label: 'Send'
//             });

//             // Show the dialog
//             dialog.show();

//             // Function to fetch and set message based on template selection
//             function fetchAndSetMessage(templateId) {
//                 if (templateId) {
//                     console.log(templateId)
//                     frappe.call({
//                         method: 'tnc_frappe_custom_app.custom_whatsapp.get_template_message',
//                         args: {
//                             template_id: templateId
//                         },
//                         callback: function(r) {
//                             if (r.message) {
//                                 dialog.set_value('message', r.message);
//                             } else {
//                                 console.error('No message returned from server.');
//                             }
//                         }
//                     });
//                 }
//             }

//             // Listen for the value being set in the template field
//             dialog.fields_dict.template.get_query = function() {
//                 return {
//                     query: 'tnc_frappe_custom_app.custom_whatsapp.get_template_options', // Custom query to get template options
//                 };
//             };

//             // Listen to template selection and fetch the corresponding message
//             dialog.fields_dict.template.$input.on('awesomplete-selectcomplete', function(e) {
//                 let selectedTemplateValue = dialog.get_value('template'); // Get the selected value
//                 if (selectedTemplateValue) {
//                     fetchAndSetMessage(selectedTemplateValue); // Fetch and set message
//                 }
//             });
//         });
//     }
// });

frappe.ui.form.on('Online Student', {
    refresh: function(frm) {
        // Add the main dropdown button
        // frm.add_custom_button(__('Send WhatsApp'), function() {
        //     // This is where the dropdown functionality will go
        // }, __('Actions')); // This label will be for the dropdown button

        // Sub-button 1: Send WhatsApp Message
        frm.add_custom_button(__('Send Result '), function() {
            // Existing functionality for sending WhatsApp message
            let name = frm.doc.name;
            let mobile_number = frm.doc.mobile;
            let student_name = frm.doc.student_name;

            frappe.prompt([
                {
                    label: 'Mobile Number',
                    fieldname: 'mobile_number',
                    fieldtype: 'Data',
                    default: mobile_number,
                    reqd: 1
                },
                {
                    label: 'Message',
                    fieldname: 'message',
                    fieldtype: 'Small Text',
                    reqd: 1,
                    default: `Assessment Report by TNC Experts
                        
You are doing very good 👍    

Your score is very fantastic. According to TNC experts, you will achieve a good rank in NORCET Exam.

Video link:
https://drive.google.com/file/d/1ewpJJMgrZOa6n0eOipKK9RyZftGzPW4t/view?usp=sharing

🎯📚 Just continue your hard work and study, maximum question practice, 
and try to control minus marking.

🎖️ We hope strongly that you are our next interviewer on our TNC YouTube channel.

👍 Be confident and be consistent.

💐 All the Best and Best wishes.

आपकी सफलता वाली कॉल का इंतजार रहेगा।
                        
Thanks

AIIMS 20+ Expert TNC TEAM
                        
If you need any help and assistance, please message us on the official number:
7484999051
TNC Nursing`
                }
            ],
            function(values) {
                frappe.confirm(
                    __('Are you sure you want to send this message?'),
                    function() {
                        frappe.call({
                            method: 'tnc_frappe_custom_app.custom_whatsapp.send_whatsapp_pdf_message',
                            args: {
                                name: name,
                                mobile_number: values.mobile_number,
                                student_name: student_name,
                                message: values.message
                            },
                            callback: function(response) {
                                if (response.message.status === 'Success') {
                                    frappe.msgprint(__('WhatsApp message sent successfully!'));
                                } else {
                                    frappe.msgprint(__('Failed to send WhatsApp message.'));
                                }
                            },
                            // error: function(err) {
                            //     frappe.msgprint(__('Error occurred while sending the WhatsApp message.'));
                            // }
                        });
                    }
                );
            });
        }, __('Send WhatsApp')); // End of sub-button 1

        // Sub-button 2: WA
        frm.add_custom_button(__('Broadcast Template Message'), function() {
            let mobile_number = frm.doc.mobile;
            let dialog = new frappe.ui.Dialog({
                title: 'Send WhatsApp Message',
                fields: [
                    {
                        'fieldname': 'mobile_number',
                        'fieldtype': 'Data',
                        'label': 'Mobile Number',
                        'default': mobile_number,
                        'reqd': 1
                    },
                    {
                        'fieldname': 'template',
                        'fieldtype': 'Link',
                        'label': 'Choose Template',
                        'options': 'WhatsApp Templates',
                        'reqd': 1
                    },
                    {
                        'fieldname': 'message',
                        'fieldtype': 'Small Text',
                        'label': 'Message',
                        'read_only': 0,
                    },
                    {
                        'fieldname': 'image',
                        'fieldtype': 'Attach',
                        'label': 'Image',
                        'read_only': 0,
                    }
                ],
                primary_action: function(values) {
                    dialog.hide();
                    frappe.confirm(
                        __('Are you sure you want to send this message?'),
                        () => {
                            frappe.call({
                                method: 'tnc_frappe_custom_app.custom_whatsapp.send_whatsapp_Image_message',
                                args: {
                                    name: frm.doc.name,
                                    mobile_number: values.mobile_number,
                                    student_name: frm.doc.student_name,
                                    template: values.template,
                                    message: values.message,
                                    image: values.image,
                                },
                                callback: function(response) {
                                    if (response.message) {
                                        frappe.show_alert({
                                            message: __('Message sent successfully!'),
                                            indicator: 'green'
                                        });
                                    } else {
                                        frappe.show_alert({
                                            message: __('Failed to send message.'),
                                            indicator: 'red'
                                        });
                                    }
                                }
                            });
                        },
                        () => {
                            console.log('Message sending canceled.');
                        }
                    );
                },
                primary_action_label: 'Send'
            });

            dialog.show();

            function fetchAndSetMessage(templateId) {
                if (templateId) {
                    frappe.call({
                        method: 'tnc_frappe_custom_app.custom_whatsapp.get_template_message',
                        args: {
                            template_id: templateId
                        },
                        callback: function(r) {
                            if (r.message) {
                                dialog.set_value('message', r.message[0]);
                                dialog.set_value('image', r.message[1]);
                            } else {
                                console.error('No message returned from server.');
                            }
                        }
                    });
                }
            }

            dialog.fields_dict.template.get_query = function() {
                return {
                    query: 'tnc_frappe_custom_app.custom_whatsapp.get_template_options',
                };
            };

            dialog.fields_dict.template.$input.on('awesomplete-selectcomplete', function(e) {
                let selectedTemplateValue = dialog.get_value('template');
                if (selectedTemplateValue) {
                    fetchAndSetMessage(selectedTemplateValue);
                }
            });
        }, __('Send WhatsApp')); // End of sub-button 2
    }
});
