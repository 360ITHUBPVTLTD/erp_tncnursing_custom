

frappe.listview_settings['Student Exam'] = {
    onload: function(listview) {
        listview.page.add_inner_button(__('Sync Ranks'), function() {
            frappe.call({
                method: 'tnc_frappe_custom_app.color_ranks.sync_ranks',
                args: {},
                callback: function(response) {
                    if (response.message) {
                        frappe.msgprint(__('Ranks synchronized successfully'));
                        listview.refresh(); // Optionally refresh the listview after syncing
                    }
                }
            });
        });
    }
};


