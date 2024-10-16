// Copyright (c) 2024, Administrator and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Student Exam", {
// 	refresh(frm) {

// 	},
// });



/////////////////////////////// Below is the FInal code #################################################################

frappe.ui.form.on('Student Exam', {
    refresh: function(frm) {
    if (!frm.doc.lock_ranks && (frm.doc.status === 'Pending to Process Data' || frm.doc.status === 'Failed Queue' || frm.doc.status === '')) {
        frm.add_custom_button(__('Process Data'), function() {
            frappe.call({
                method: "frappe.client.get_count",
                args: {
                    doctype: "Students Master Data",
                    filters: {
                        // Add your filters here
                        'imported': 0, 
                        'exam_id': frm.doc.name,
                    }
                },
                callback: function(r) {
                    if (r.message) {
                        let record_count = r.message; // This directly gives you the count of records
                        // console.log("Number of records: " + record_count);
            
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
                // error: function(err) {
                //     frappe.msgprint(__('Error in Syncing data.'));
                //     console.error(err)
                // }
            });
        });
    }
        
        ///////////////////////// Previous working Data Processing with progress bar and real time processing /////////////////////
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
        //                 frm.refresh();  // Refresh the form view to check the status again
        //             } else if (response.message === "no_data") {
        //                 // frappe.msgprint(__('No Data available to sync.'));
        //             } else {
        //                 console.log(response.message);
        //                 // frappe.msgprint(__('There was an issue with syncing the data.'));
        //             }
        //         },
        //         error: function(err) {
        //             frappe.msgprint(__('Syncing data is not possible.'));
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
                window.open(`${baseUrl}/app/query-report/Custom%20Student%20Result%20report?exam_name=${encodeURIComponent(examName)}&exam_title_name=${encodeURIComponent(frm.doc.name)}`); 
            });
        }

        // Conditionally add "Go to Data Import" button based on field values and status
        if (frm.doc.exam_name &&  !['Data Synced', 'Rank Generated(step1)','Rank Generated(step2)','Rank Reset'].includes(frm.doc.status)) {
            frm.add_custom_button(__('Go to Data Import'), function() {
                const baseUrl = window.location.origin
        
                window.open(`${baseUrl}/app/data-import`);  // Open the URL in a new tab
                
            });
        }
        
        // Add the "Assign Colors" button to the form
        // frm.add_custom_button(__('Assign Colors'), function() {
        //     // Call the server-side method and pass the current document name
        //     frappe.call({
        //         method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.student_exam.student_exam.assign_colors',
        //         args: {
        //             exam_name: frm.doc.name
        //         },
        //         callback: function(response) {
        //             if (response.message) {
        //                 frappe.msgprint(__('Colors assigned successfully!'));
        //             }
        //         }
        //     });
        // });


        
        // Hide the "Add Row" and "Add Multiple Rows" buttons
        // frm.fields_dict['color_generation'].grid.wrapper.find('.grid-add-row').hide();
        // frm.fields_dict['color_generation'].grid.wrapper.find('.grid-add-multiple-rows').hide();
        // // Hide the "Delete Rows" and "Delete All Rows" buttons
        // frm.fields_dict['color_generation'].grid.wrapper.find('.grid-remove-rows').hide();
        // frm.fields_dict['color_generation'].grid.wrapper.find('.grid-remove-all-rows').hide();
        // // Hide the "Edit" button
        // frm.fields_dict['color_generation'].grid.wrapper.find('.btn-open-row').hide();

    }
});


///////////////////////////////  Assign color Button ///////////////////////////


frappe.ui.form.on('Student Exam', {
    refresh: function(frm) {
        // Add the "Assign Colors" button to the form
        if(frm.doc.status == 'Data Synced' || 'Rank Generated(step1)' || 'Rank Generated(step2)') {
        frm.add_custom_button(__('Assign Colors'), function() {
            // Show a confirmation prompt before proceeding
            frappe.confirm(
                __('Are you sure you want to assign colors to the students for this exam?'),
                function() {
                    // If confirmed, call the server-side method
                    frappe.call({
                        method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.student_exam.student_exam.assign_colors',
                        args: {
                            exam_name: frm.doc.name
                        },
                        callback: function(response) {
                            if (response.message) {
                                frappe.msgprint(__('Colors assigned successfully!'));
                            }
                        }
                    });
                },
            );
        });
     }
         else {
        frm.clear_custom_buttons();
    }
    }

});



////////////////////////// Delete the Particular Exam Student results doctype based on the ID ///////////////////////////


frappe.ui.form.on('Student Exam', {
    refresh: function(frm) {
        // Add the custom button
        frm.add_custom_button(__('Delete the Exam'), function() {
            // Show confirmation prompt
            frappe.confirm(
                __('Are you sure you want to delete all student results for this exam?'),
                function() {
                    // If confirmed, call the server-side function
                    frappe.call({
                        method: "tnc_frappe_custom_app.tnc_custom_app.doctype.student_exam.student_exam.delete_student_results",
                        args: {
                            exam_id: frm.doc.name
                        },
                        callback: function(r) {
                            if (r.message) {
                                frappe.msgprint(r.message);
                            }
                        }
                    });
                },
                function() {
                    // If cancelled, do nothing
                    // frappe.msgprint(__('Operation cancelled.'));
                }
            );
        });
    }
});




//////////////////////// Below code is to show the HTML table in the Student Exam (Not Imported Logs) ////////

frappe.ui.form.on('Student Exam', {
    refresh: function(frm) {
        if (frm.doc.name) {
            frappe.call({
                method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.student_exam.student_exam.fetch_unimported_logs',
                args: {
                    imported_batch_id: frm.doc.name
                },
                callback: function(r) {
                    if (r.message) {
                        let base_url = window.location.origin;
                        let html_table = '';
                        
                        if (r.message.length > 0) {
                            html_table = `
                                <table class="table table-bordered">
                                    <thead>
                                        <tr style="background-color:#3498DB;color:white;text-align: left;">
                                            <th style="vertical-align: middle;border: solid 2px #bcb9b4;">Not Imported Log ID</th>
                                            <th style="vertical-align: middle;border: solid 2px #bcb9b4;">Student Name</th>
                                            <th style="vertical-align: middle;border: solid 2px #bcb9b4;">Mobile</th>
                                            <th style="vertical-align: middle;border: solid 2px #bcb9b4;">District</th>
                                            <th style="vertical-align: middle;border: solid 2px #bcb9b4;">State</th>
                                            <th style="vertical-align: middle;border: solid 2px #bcb9b4;">Rank</th>
                                            <th style="vertical-align: middle;border: solid 2px #bcb9b4;">Total Marks</th>
                                            <th style="vertical-align: middle;border: solid 2px #bcb9b4;">Total Right</th>
                                            <th style="vertical-align: middle;border: solid 2px #bcb9b4;">Total Wrong</th>
                                            <th style="vertical-align: middle;border: solid 2px #bcb9b4;">Total Skip</th>
                                            <th style="vertical-align: middle;border: solid 2px #bcb9b4;">Percentage</th>
                                            <th style="vertical-align: middle;border: solid 2px #bcb9b4;">Status</th>
                                        </tr>
                                    </thead>
                                    <tbody>`;

                            r.message.forEach(function(log) {
                                let student_link = `${base_url}/app/not-imported-logs/${log.name}`;
                                html_table += `
                                    <tr>
                                        <td style="border: solid 2px #bcb9b4;"><a href="${student_link}" target="_blank">${log.name}</a></td>
                                        <td style="border: solid 1px #bcb9b4;">${log.student_name}</td>
                                        <td style="border: solid 1px #bcb9b4;">${log.mobile}</td>
                                        <td style="border: solid 1px #bcb9b4;">${log.district}</td>
                                        <td style="border: solid 1px #bcb9b4;">${log.state}</td>
                                        <td style="border: solid 1px #bcb9b4;">${log.rank}</td>
                                        <td style="border: solid 1px #bcb9b4;">${log.total_marks}</td>
                                        <td style="border: solid 1px #bcb9b4;">${log.total_right}</td>
                                        <td style="border: solid 1px #bcb9b4;">${log.total_wrong}</td>
                                        <td style="border: solid 1px #bcb9b4;">${log.total_skip}</td>
                                        <td style="border: solid 1px #bcb9b4;">${log.percentage}</td>
                                        <td style="border: solid 1px #bcb9b4;">${log.status}</td>
                                    </tr>`;
                            });

                            html_table += `
                                    </tbody>
                                </table>`;
                        } else {
                            html_table = `<h3>All Students are imported for this exam</h3>`;
                        }

                        // Set HTML content in the 'unimported_logs' field
                        frm.set_df_property('unimported_logs', 'options', html_table);
                    }
                }
            });
        }
    }
});

