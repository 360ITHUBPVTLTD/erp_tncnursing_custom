// Copyright (c) 2024, Administrator and contributors
// For license information, please see license.txt

// frappe.ui.form.on("WhatsApp Instance", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('WhatsApp Instance', {
    // onload: function (frm) {
    //     sync_inst(frm)
    //     frm.refresh()
    // },
    refresh: function (frm) {
        if(!frm.doc.__islocal){
            if(frm.doc.connection_status==0 ){
                // Add a custom button to connect now
                // frm.fields_dict.connected_number.$wrapper.hide();
                frm.page.add_button(__('Connect Now'), function() {
                    frappe.call({
                        method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.whatsapp_instance.whatsapp_instance.storing_the_qrcode', 
                        args: {
                            'name': frm.doc.name
                        },
                        callback: function(response) {
                            if (response.message) {
                                // Create a custom modal dialog
                                var dialog = new frappe.ui.Dialog({
                                    title: __("QR Code"),
                                    fields: [
                                        {
                                            fieldtype: 'HTML',
                                            fieldname: 'qr_code_html',
                                            label: __("QR Code"),
                                            options: `<div style="text-align:center;">
<img src="${response.message}" alt="You Already Connected to Instance">
</div>`
                                        }
                                    ],
                                    primary_action_label: __("OK"),
                                    primary_action: function () {
                                        dialog.hide();
                                        // frm.reload_doc();
                                        sync_inst(frm,function() {
                                        frm.reload_doc();
                                        });
                                    }
                                });
                                // Show the dialog
                                dialog.show();
                            } else {
                                frappe.msgprint('Failed to retrieve QR code link.');
                            }
                        }
                    });
                });
            }else{
                frm.fields_dict.connected_number.$wrapper.show();
                frm.page.add_button(__('Sync Instance'), function() {
                    var res_msg = sync_inst(frm);
                    frappe.msgprint(res_msg);
                    frappe.msgprint("Instance is succesfully synced")
                    setTimeout(function() {
                        window.location.reload(); // Reload the page
                        }, 1000);
                    // console.log(res_msg)
                    console.log("Hello")
                });
                 frm.page.add_button(__('Disconnect'), function() {
                    frappe.confirm(
                            'Are you sure you want to disconnect Instance?',
                            function(){
                                frappe.call({
                                    method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.whatsapp_instance.whatsapp_instance.logout_instance',
                                    args: {
                                        "name":frm.doc.name
                                    },
                                    callback: function(response) {
                                        frappe.msgprint(response.message);
                                        frm.reload_doc();
                                    }
                                });
                            }
                        );
                });
            }
        }
    }
});
 
function sync_inst(frm, callback) {
    frappe.call({
        method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.whatsapp_instance.whatsapp_instance.storing_the_instance_data',
        args: {
            'name': frm.doc.name
        },
        callback: function(response) {
            if (callback) {
                callback(response.message);
            }
        }
    });
}

