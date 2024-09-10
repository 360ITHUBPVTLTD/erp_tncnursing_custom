

frappe.listview_settings['Student Exam'] = {
    // onload: function(listview) {
    //     listview.page.add_inner_button(__('Sync Ranks'), function() {
    //         frappe.call({
    //             method: 'tnc_frappe_custom_app.color_ranks.sync_ranks',
    //             args: {},
    //             callback: function(response) {
    //                 if (response.message) {
    //                     frappe.msgprint(__('Ranks synchronized successfully'));
    //                     listview.refresh(); // Optionally refresh the listview after syncing
    //                 }
    //             }
    //         });
    //     });
    // }
    refresh: function(listview) {
        listview.page.add_inner_button(__('Assign Colours'), function() {
            // Create a new dialog
            let dialog = new frappe.ui.Dialog({
                title: __('Assign Colours'),
                fields: [
                    {
                        fieldtype: 'Int',
                        label: __('Green End'),
                        fieldname: 'green_end',
                        reqd: 1
                    },
                    {
                        fieldtype: 'Int',
                        label: __('Yellow End'),
                        fieldname: 'yellow_end',
                        reqd: 1
                    }
                ],
                primary_action: function() {
                    // Retrieve the values from the dialog
                    let values = dialog.get_values();
                    
                    // Validation
                    if (values.green_end >= 100 || values.yellow_end >= 100) {
                        frappe.msgprint(__('Both values must be less than 100.'));
                        return;
                    }
                    
                    if (values.green_end >= values.yellow_end) {
                        frappe.msgprint(__('Green End value must be less than Yellow End value.'));
                        return;
                    }
                    
                    dialog.hide();
    
                    // Make the AJAX call with the validated arguments
                    frappe.call({
                        method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.student_exam.student_exam.bulk_assign_colors',
                        args: {
                            green_end: values.green_end,
                            yellow_end: values.yellow_end
                        },
                        callback: function(response) {
                            if (response.message && response.message.status) {
                                frappe.msgprint(__(response.message.msg));
                                listview.refresh(); // Optionally refresh the listview after syncing
                            } else {
                                frappe.msgprint(__('An error occurred.'));
                            }
                        }
                    });
                },
                primary_action_label: __('Submit')
            });
    
            // Show the dialog
            dialog.show();
        });
    }
    
    
};


