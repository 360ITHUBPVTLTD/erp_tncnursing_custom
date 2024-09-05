// Copyright (c) 2024, Administrator and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Student Exam", {
// 	refresh(frm) {

// 	},
// });


// frappe.ui.form.on('Student Exam', {
//     refresh: function(frm) {
//         // Add "Redirect to Reports" button to the form view
//         frm.add_custom_button(__('Redirect to Reports'), function() {
//             const examName = frm.doc.exam_name;
//             const examTitleName = frm.doc.exam_title_name;

//             if (examName && examTitleName) {
//                 const reportUrl = `/app/query-report/Custom%20Student%20Result%20report?exam_name=${encodeURIComponent(examName)}&exam_title_name=${encodeURIComponent(examTitleName)}`;
//                 window.open(reportUrl, '_blank');  // Open the URL in a new tab
//             } else {
//                 frappe.msgprint(__('Please ensure both Exam Name and Exam Title Name are set before redirecting.'));
//             }
//         });
//     }
// });




/////////////////////////////// Below is the FInal code #################################################################

frappe.ui.form.on('Student Exam', {
    refresh: function(frm) {
        // Add "Process Data" button to the form view
        frm.add_custom_button(__('Process Data'), function() {
            frappe.call({
                method: 'tnc_frappe_custom_app.sync.sync_data',
                args: {
                    name: frm.doc.name  // Add the form name to the arguments
                },
                callback: function(response) {
                    if (response.message === "success") {
                        frappe.msgprint(__('Data synced successfully!'));
                        // frm.set_value('data_synced', 1);  // Only set to 1 if data was synced
                        // frm.set_value('status', 'Data Synced');
                        // frm.save();
                        frm.refresh();  // Refresh the form view to check the status again
                    } else if (response.message === "no_data") {
                        frappe.msgprint(__('No Data available to sync.'));
                    } else {
                        frappe.msgprint(__('There was an issue with syncing the data.'));
                    }
                },
                error: function(err) {
                    frappe.msgprint(__('Syncing the data is not possible.'));
                }
            });
        });

        // Conditionally add "Redirect to Reports" button based on status
        if (frm.doc.status === 'Data Synced' || frm.doc.status === 'Rank Generated(step1)' || frm.doc.status === 'Rank Generated(step2)' || frm.doc.status === 'Rank Reset') {
            frm.add_custom_button(__('Redirect to Reports'), function() {
                const examName = frm.doc.exam_name;
                const examTitleName = frm.doc.exam_title_name;

                const reportUrl = `/app/query-report/Custom%20Student%20Result%20report?exam_name=${encodeURIComponent(examName)}&exam_title_name=${encodeURIComponent(examTitleName)}`;
                window.open(reportUrl, '_blank');  // Open the URL in a new tab
            });
        }

        // Conditionally add "Go to Data Import" button based on field values and status
            if (frm.doc.exam_name &&  frm.doc.exam_title_name && frm.doc.status !== 'Data Synced'  ) {
                frm.add_custom_button(__('Go to Data Import'), function() {
                    window.open('http://192.168.1.128:8010/app/data-import', '_blank');  // Open the URL in a new tab
                });
            }
    }
});











// frappe.ui.form.on('Student Exam', {
//     refresh: function(frm) {
//         frm.add_custom_button(__('Sync Data'), function() {
//             // Show the progress bar dialog
//             var dialog = new frappe.ui.Dialog({
//                 title: __('Synchronization Progress'),
//                 fields: [
//                     {
//                         fieldtype: 'HTML',
//                         fieldname: 'progress_html',
//                         label: 'Progress',
//                         options: '<div class="progress"><div class="progress-bar" role="progressbar" style="width: 0%;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div></div><div id="progress-info"></div>'
//                     }
//                 ]
//             });
//             dialog.show();

//             // Add debugging output
//             console.log('Dialog shown. Listening for real-time updates...');

//             // Listen for real-time updates
//             frappe.realtime.on("sync_progress", function(data) {
//                 console.log('Received progress update:', data); // Debugging output

//                 if (data && data.total && data.completed) {
//                     var progress = (data.completed / data.total) * 100;

//                     dialog.fields_dict.progress_html.$wrapper.find('.progress-bar')
//                         .css('width', progress + '%')
//                         .attr('aria-valuenow', progress);

//                     // Update progress text
//                     dialog.fields_dict.progress_html.$wrapper.find('#progress-info')
//                         .html(`${data.completed} out of ${data.total} records processed`);

//                     console.log(`Progress updated: ${progress}% (${data.completed} out of ${data.total})`); // Debugging output

//                     if (progress >= 100) {
//                         dialog.hide();
//                         frappe.msgprint(__('Synchronization completed successfully!'));
//                         console.log('Synchronization completed successfully.'); // Debugging output
//                     }
//                 } else {
//                     console.error('Invalid progress data received:', data); // Debugging output
//                 }
//             });

//             // Start the synchronization process
//             frappe.call({
//                 method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.student_exam.student_exam.sync_data',
//                 args: {
//                     name: frm.doc.name  // Pass the form name to the server script
//                 },
//                 callback: function(response) {
//                     if (response.message === "success") {
//                         frm.set_value('data_synced', 1);
//                         frm.set_value('status', 'Data Synced');
//                         frm.save();
//                         frm.refresh();
//                         console.log('Data synced and form updated.'); // Debugging output
//                     } else if (response.message === "no_data") {
//                         frappe.msgprint(__('No Data available to sync.'));
//                         console.log('No data available to sync.'); // Debugging output
//                     } else {
//                         frappe.msgprint(__('There was an issue with syncing the data.'));
//                         console.error('Error syncing data:', response.message); // Debugging output
//                     }
//                 }
//             });
//         });
//     }
// });










