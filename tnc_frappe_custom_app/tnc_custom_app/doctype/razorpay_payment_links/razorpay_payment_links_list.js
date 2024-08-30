
frappe.listview_settings['Razorpay Payment Links'] = {
    onload: function (listview) {
        listview.page.add_inner_button(__('Sync'), function() {
            frappe.call({
                method: 'tnc_frappe_custom_app.razorpay_payment_link.sync_payment_links', // Replace with your server script path
                freeze: true,
                freeze_message: __('Syncing payment links...'),
                callback: function (r) {
                    if (r.exc) {
                        frappe.msgprint(__('Error occurred while syncing payment links.'));
                    } else {
                        frappe.msgprint(__('Payment links synced successfully.'));
                        listview.refresh();
                    }
                }
            });
        });
    }
};
