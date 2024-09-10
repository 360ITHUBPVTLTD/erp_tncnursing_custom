// Copyright (c) 2024, Administrator and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Razorpay Payment Links", {
// 	refresh(frm) {

// 	},
// });

/////////////////////////////////// Below code is to cancel the payment //////////////////////////////////

frappe.ui.form.on('Razorpay Payment Links', {
    refresh: function(frm) {
        // Show the "Cancel Payment Link" button only if the status is "Created"
        if (frm.doc.status === "Created") {
            frm.add_custom_button(__('Cancel Payment Link'), function() {
                frappe.confirm(
                    'Are you sure you want to cancel this payment link?',
                    function() {
                        frappe.call({
                            method: 'tnc_frappe_custom_app.razorpay_payment_link.cancel_payment_link',
                            args: {
                                link_id: frm.doc.link_id
                            },
                            callback: function(response) {
                                if (response.message === 'success') {
                                    frappe.msgprint(__('Payment link cancelled successfully.'));
                                    frm.set_value('status', 'Cancelled');
                                    frm.refresh_field('status');
                                    frm.reload_doc();  // Reload the doc to refresh the form
                                } else {
                                    frappe.msgprint(__('Failed to cancel payment link.'));
                                }
                            }
                        });
                    }
                );
            });
        }
    }
});
