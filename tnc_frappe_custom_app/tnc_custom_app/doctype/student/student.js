// Copyright (c) 2024, Administrator and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Student", {
// 	refresh(frm) {

// 	},
// });


////////////////// Payment Link Generating in CLient script //////////////////

frappe.ui.form.on('Student', {
    refresh: function(frm) {
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Razorpay Payment Links',
                filters: {
                    'student_id': frm.doc.name,
                    'status': ['in', ['Created', 'Paid']]
                },
                fields: ['name']
            },
            callback: function(response) {
                if (response.message && response.message.length > 0) {
                    frm.clear_custom_buttons();
                } else {
                    frm.add_custom_button(__('Generate Payment Link'), function() {
                        frappe.confirm(
                            'Are you sure you want to generate the payment link?',
                            function() {
                                frm.call({
                                    method: 'tnc_frappe_custom_app.razorpay_payment_link.generate_payment_link',
                                    args: {
                                        student_id: frm.doc.name,
                                        amount: frm.doc.amount,
                                        description: 'Payment for student fees'
                                    },
                                    callback: function(response) {
                                        if (response.message && response.message.short_url) {
                                            frappe.msgprint(__('Payment Link Generated Successfully'));

                                            // Set the payment link value in the Student doctype
                                            frm.set_value('payment_link', response.message.short_url);
                                            
                                            // Automatically save the form after setting the payment link
                                            frm.save();
                                        } else {
                                            frappe.msgprint(__('Failed to generate payment link.'));
                                        }
                                    }
                                });
                            }
                        );
                    });
                }
            }
        });
    }
});
