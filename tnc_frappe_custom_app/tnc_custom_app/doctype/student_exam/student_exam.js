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
    frappe.call({
        method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.student_exam.student_exam.student_process_data',
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
        window.open('http://3.111.226.95//app/data-import', '_blank');  // Open the URL in a new tab
    });
}

    }
});









