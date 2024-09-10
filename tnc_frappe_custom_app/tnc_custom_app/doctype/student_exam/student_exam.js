// Copyright (c) 2024, Administrator and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Student Exam", {
// 	refresh(frm) {

// 	},
// });



/////////////////////////////// Below is the FInal code #################################################################

frappe.ui.form.on('Student Exam', {
    refresh: function(frm) {

        frm.add_custom_button(__('Process Data'), function() {
            frappe.call({
                method: "frappe.client.get_count",
                args: {
                    doctype: "Students Master Data",
                    filters: {
                        // Add your filters here
                        'imported': 0,
                        'imported_batch_id': frm.doc.name,
                    }
                },
                callback: function(r) {
                    if (r.message) {
                        let record_count = r.message; // This directly gives you the count of records
                        console.log("Number of records: " + record_count);
            
                        if(record_count<=1500){
                            frappe.realtime.on('sync_progress', function(data) {
                                // console.log("Progress:",data.completed_records, data.total_records);
                                frm.dashboard.show_progress('Creating Results', data.progress, data.total_records, 'progress-bar-primary');
                
                                if (data.completed_records == data.total_records) {
                                    frappe.show_alert({message: __('Results created successfully'), indicator: 'green'});
                                    setTimeout(function() {
                                        frm.dashboard.hide_progress('Creating Results');
                                    }, 1000);
                                }
                            });
                        }
                    }
                }
            });
            
            
            frappe.call({
                method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.student_exam.student_exam.student_process_data',
                args: {
                    name: frm.doc.name  // Pass the current form's name as argument
                },
                callback: function(response) {
                    if (response.message && response.message.status) {
                        // if (response.message.enqueued){
                        //     frappe.msgprint(__(response.message.msg));
                        //     // frappe.show_alert({message: __('Data syncing is Enqueued Successfully!'), indicator: 'green'});
                        //     frm.refresh();  // Refresh the form view to check the status again
                        // }else{
                        //     frappe.realtime.on('sync_progress', function(data) {
                        //         // console.log("Progress:",data.completed_records, data.total_records);
                        //         frm.dashboard.show_progress('Creating Results', data.progress, data.total_records, 'progress-bar-primary');
                
                        //         if (data.completed_records == data.total_records) {
                        //             frappe.show_alert({message: __('Results created successfully'), indicator: 'green'});
                        //             setTimeout(function() {
                        //                 frm.dashboard.hide_progress('Creating Results');
                        //             }, 1000);
                        //         }
                        //     });
 
                        // }
                        frappe.msgprint(__(response.message.msg));
                        // frappe.show_alert({message: __('Data syncing is Enqueued Successfully!'), indicator: 'green'});
                        frm.refresh();
 
                    } else {
                        frappe.msgprint(__(response.message.msg));
                    }
                },
                error: function(err) {
                    frappe.msgprint(__('Error in Syncing data.'));
                    console.error(err)
                }
            });
        });
        
// frm.add_custom_button(__('Process Data'), function() {
//     frappe.realtime.on('sync_progress', function(data) {
//         // console.log("Progress:",data.completed_records, data.total_records);
//         frm.dashboard.show_progress('Creating Results', data.progress, data.total_records, 'progress-bar-primary');

//         if (data.completed_records == data.total_records) {
//             frappe.show_alert({message: __('Results created successfully'), indicator: 'green'});
//             setTimeout(function() {
//                 frm.dashboard.hide_progress('Creating Results');
//             }, 1000);
//         }
//     });
//     frappe.call({
//         method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.student_exam.student_exam.student_process_data',
//         args: {
//             name: frm.doc.name  // Add the form name to the arguments
//         },
//         callback: function(response) {
//             if (response.message === "success") {
//                 frappe.msgprint(__('Data synced successfully!'));
//                 // frm.set_value('data_synced', 1);  // Only set to 1 if data was synced
//                 // frm.set_value('status', 'Data Synced');
//                 // frm.save();
//                 frm.refresh();  // Refresh the form view to check the status again
//             } else if (response.message === "no_data") {
//                 frappe.msgprint(__('No Data available to sync.'));
//             } else {
//                 frappe.msgprint(__('There was an issue with syncing the data.'));
//             }
//         },
//         error: function(err) {
//             frappe.msgprint(__('Syncing data is not possible.'));
//             console.log(err)
//         }
//     });
// });

// Conditionally add "Redirect to Reports" button based on status
if (frm.doc.status === 'Data Synced' || frm.doc.status === 'Rank Generated(step1)' || frm.doc.status === 'Rank Generated(step2)' || frm.doc.status === 'Rank Reset') {
    frm.add_custom_button(__('Redirect to Reports'), function() {
        const examName = frm.doc.exam_name;
        const examTitleName = frm.doc.exam_title_name;
        const baseUrl = window.location.origin

        // const reportUrl = `frappe.utils.get_url('app/query-report/Custom%20Student%20Result%20report?exam_name=${encodeURIComponent(examName)}&exam_title_name=${encodeURIComponent(examTitleName)}')`;
        // window.open(reportUrl, '_blank');  // Open the URL in a new tab
        window.open(`${baseUrl}/app/query-report/Custom%20Student%20Result%20report?exam_name=${encodeURIComponent(examName)}&exam_title_name=${encodeURIComponent(examTitleName)}`); 
    });
}

// Conditionally add "Go to Data Import" button based on field values and status
if (frm.doc.exam_name &&  frm.doc.exam_title_name && frm.doc.status !== 'Data Synced'  ) {
    frm.add_custom_button(__('Go to Data Import'), function() {
        const baseUrl = window.location.origin
 
        window.open(`${baseUrl}/app/data-import`);  // Open the URL in a new tab
        //http://3.111.226.95/app/data-import
    });
}

    }
});









