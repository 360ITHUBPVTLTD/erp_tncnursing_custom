
frappe.listview_settings['Student Results'] = {
    onload: function(listview) {

        // Select Exam button (already working)
        listview.page.add_inner_button(__('Select Exam'), function () {
            let dialog = new frappe.ui.Dialog({
                title: __('Select Exam'),
                fields: [
                    {
                        label: 'Exam',
                        fieldname: 'exam_id',
                        fieldtype: 'Link',
                        options: 'Student Exam',
                        reqd: true
                    }
                ],
                primary_action_label: __('Send'),
                primary_action(values) {
                    if (!values.exam_id) {
                        frappe.msgprint(__('Please select an exam.'));
                        return;
                    }
        
                    frappe.call({
                        method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.student_results.student_results.create_bulk_whatsapp_entry_for_single_exam',
                        args: {
                            exam_ids: [values.exam_id]
                        },
                        callback: function (r) {
                            if (!r.exc && r.message && r.message.success) {
                                const bulk_docname = r.message.docname;
                                const student_count = r.message.unique_student_count;
        
                                frappe.confirm(
                                    `Are you sure you want to share the results for ${student_count} students?`,
                                    function () {
                                        // YES: Proceed to send WhatsApp results
                                        frappe.call({
                                            method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.student_results.student_results.send_results_for_single_exam',
                                            args: {
                                                exam_ids: values.exam_id,
                                                bulk_docname: bulk_docname
                                            },
                                            callback: function (res) {
                                                if (!res.exc) {
                                                    frappe.msgprint(__('WhatsApp results sent successfully.'));
                                                    dialog.hide();
                                                } else {
                                                    frappe.msgprint(__('Failed to send WhatsApp messages.'));
                                                }
                                            }
                                        });
                                    },
                                    function () {
                                        // NO: Cancel the bulk record
                                        frappe.call({
                                            method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.student_results.student_results.cancel_bulk_result',
                                            args: {
                                                bulk_docname: bulk_docname
                                            },
                                            callback: function () {
                                                frappe.msgprint(__('WhatsApp result sharing was cancelled.'));
                                                dialog.hide();
                                            }
                                        });
                                    }
                                );
                            } else {
                                frappe.msgprint(__('Failed to create bulk entry. Please check the logs.'));
                            }
                        }
                    });
                }
            });
        
            dialog.show();
        }, __("Actions"));
        

        // ✅ NEW BUTTON: Select Date Range
        listview.page.add_inner_button(__('Select Date Range'), function () {
            let bulk_docname = null;
            let cancel_on_hide = false;
        
            const dialog = new frappe.ui.Dialog({
                title: __('Select Date Range & Test Series'),
                fields: [
                    {
                        label: 'Date Range',
                        fieldname: 'date_range',
                        fieldtype: 'Date Range',
                        // reqd: true
                    },
                    {
                        fieldtype: 'HTML',
                        fieldname: 'test_series_checkboxes',
                        label: 'Choose Test Series'
                    }
                ],
                primary_action_label: __('Send'),
                primary_action(values) {
                    const [from_date, to_date] = values.date_range || [];
                    // if (!from_date || !to_date) {
                    //     frappe.msgprint(__('Please select a valid date range.'));
                    //     return;
                    // }
        
                    const selected = Array.from(
                        dialog.fields_dict.test_series_checkboxes.$wrapper[0]
                            .querySelectorAll('input[type=checkbox]:checked')
                    ).map(cb => cb.value);
        
                    if (selected.length === 0) {
                        frappe.msgprint(__('Please select at least one test series.'));
                        return;
                    }
        
                    // Save the bulk entry
                    frappe.call({
                        method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.student_results.student_results.create_bulk_whatsapp_entry',
                        args: {
                            from_date,
                            to_date,
                            test_series: selected
                        },
                        callback: function (r) {
                            console.log(r); 
                                if (!r.exc && r.message && r.message.success) {
                                    const bulk_docname = r.message.docname;
                                    const student_count = r.message.unique_student_count;
                                    cancel_on_hide = true; // Allow cancel logic if dialog is closed
                                
                                // Show confirmation
                                frappe.confirm(
                                    `Are you sure you want to share the results for ${student_count} students?`,
                                    function () {
                                        // YES
                                        cancel_on_hide = false; // prevent cancelling on hide
                                        frappe.call({
                                            method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.student_results.student_results.send_results_by_date_range',
                                            args: {
                                                test_series: selected,
                                                bulk_docname: bulk_docname,
                                                from_date,
                                                to_date,
                                            },
                                            callback: function (res) {
                                                if (!res.exc) {
                                                    frappe.msgprint(__('WhatsApp results sent successfully.'));
                                                    dialog.hide();
                                                } else {
                                                    frappe.msgprint(__('Failed to send WhatsApp messages.'));
                                                }
                                            }
                                        });
                                    },
                                    function () {
                                        // NO clicked — cancel via server-side
                                        cancel_on_hide = false; // prevent double cancel
                                        frappe.call({
                                            method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.student_results.student_results.cancel_bulk_result',
                                            args: {
                                                bulk_docname
                                            },
                                            callback: function () {
                                                frappe.msgprint(__('WhatsApp result sharing was cancelled.'));
                                                dialog.hide();
                                            }
                                        });
                                    }
                                );
                            } else {
                                frappe.msgprint(__('Failed to save bulk entry.'));
                            }
                        }
                    });
                }
            });
        
            dialog.show();
        
            // ✅ Hook for detecting closing without action
            $(dialog.$wrapper).on('hide.bs.modal', () => {
                if (cancel_on_hide && bulk_docname) {
                    // Only cancel if not already handled
                    frappe.call({
                        method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.student_results.student_results.cancel_bulk_result',
                        args: {
                            bulk_docname
                        },
                        callback: function () {
                            frappe.msgprint(__('Dialog closed. WhatsApp result sharing was cancelled.'));
                        }
                    });
                }
            });
        
            // Load Test Series Checkboxes
            frappe.db.get_list('Test Series Type', {
                fields: ['name'],
                limit: 1000
            }).then(test_series => {
                const wrapper = dialog.fields_dict.test_series_checkboxes.$wrapper;
                let html = `
                    <div style="margin-bottom: 10px;">
                        <button class="btn btn-xs btn-primary" type="button" id="select-all">Select All</button>
                        <button class="btn btn-xs btn-default" type="button" id="unselect-all">Unselect All</button>
                    </div>
                    <div style="max-height: 200px; overflow-y: auto; border: 1px solid #d1d8dd; padding: 10px;">
                `;
        
                for (let series of test_series) {
                    html += `
                        <div>
                            <label>
                                <input type="checkbox" value="${series.name}"> ${series.name}
                            </label>
                        </div>
                    `;
                }
        
                html += `</div>`;
                wrapper.html(html);
        
                wrapper.find('#select-all').on('click', () => {
                    wrapper.find('input[type=checkbox]').prop('checked', true);
                });
                wrapper.find('#unselect-all').on('click', () => {
                    wrapper.find('input[type=checkbox]').prop('checked', false);
                });
            });
        }, __("Actions"));
        
        
        
    }
};



/////////////////////////////////////////// Below is the Multiselect Exam /////////////////////////////////////////////

// frappe.listview_settings['Student Results'] = {
//     onload: function(listview) {
//         listview.page.add_inner_button(__('Select Exam'), function () {

//             // Fetch exam data
//             frappe.db.get_list('Student Exam', {
//                 fields: ['name', 'exam_title_name', 'exam_date'],
//                 limit: 1000
//             }).then(records => {
//                 if (!records.length) {
//                     frappe.msgprint(__('No exams found.'));
//                     return;
//                 }

//                 const options = records.map(r => {
//                     const label = `${r.name} - ${r.exam_title_name || ''} (${frappe.datetime.str_to_user(r.exam_date)})`;
//                     return { label: label, value: r.name };
//                 });

//                 let dialog = new frappe.ui.Dialog({
//                     title: __('Select Exams'),
//                     fields: [
//                         {
//                             label: 'Exams',
//                             fieldname: 'exam_ids',
//                             fieldtype: 'MultiCheck',
//                             options: options,
//                             columns: 2
//                         }
//                     ],
//                     primary_action_label: __('Send'),
//                     primary_action(values) {
//                         if (!values.exam_ids || values.exam_ids.length === 0) {
//                             frappe.msgprint(__('Please select at least one exam.'));
//                             return;
//                         }

//                         frappe.call({
//                             method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.student_results.student_results.send_results_for_selected_exams',
//                             args: {
//                                 exam_ids: values.exam_ids
//                             },
//                             callback: function (r) {
//                                 if (!r.exc) {
//                                     frappe.msgprint(__('Results sent successfully.'));
//                                     dialog.hide();
//                                 } else {
//                                     frappe.msgprint(__('Failed to send results. Check logs for details.'));
//                                 }
//                             }
//                         });
//                     }
//                 });

//                 dialog.show();
//             });
//         }, __("Actions"));
//     }
// };


/////////////////////////////////////////// Above is the Multiselect Exam /////////////////////////////////////////////


/////////////////////////////////////////// Below is the Bulk sharing resultss (Previous one) /////////////////////////////////////////////

// frappe.listview_settings['Student Results'] = {
//     onload: function(listview) {
//         // Add "Bulk Send Results" button
//         listview.page.add_inner_button(__('Bulk Send Results'), function() {
//             frappe.confirm(
//                 __('Are you sure you want to send results to all students?'),
//                 function() {
//                     frappe.call({
//                         method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.online_student.online_student.send_bulk_student_results_to_students',
//                         callback: function(r) {
//                             if (!r.exc) {
//                                 frappe.msgprint(__('Results sent successfully'));
//                             } else {
//                                 frappe.msgprint(__('Failed to send results. Check logs for details.'));
//                             }
//                         }
//                     });
//                 }
//             );
//         }, __("Actions"));

//         // Add "Send Selected Students" button
//         listview.page.add_inner_button(__('Send Selected Students'), function() {
//             frappe.call({
//                 method: "tnc_frappe_custom_app.tnc_custom_app.doctype.online_student.online_student.get_online_students",
//                 callback: function(response) {
//                     if (response.message) {
//                         let student_options = response.message.map(student => ({
//                             label: `${student.student_name} (${student.name}) - ${student.mobile || 'No Mobile'}`,
//                             value: student.name,
//                             mobile: student.mobile || 'No Mobile'
//                         }));

//                         // Preserve the selected values and keep them at the top
//                         let selected_values = [];

//                         let dialog = new frappe.ui.form.MultiSelectDialog({
//                             doctype: "Online Student",
//                             target: listview,
//                             setters: {
//                                 student_name: null,
//                                 mobile: null
//                             },
//                             data: student_options,
//                             primary_action_label: __('Send'),
//                             action(selected_values_list) {
//                                 if (!selected_values_list || selected_values_list.length === 0) {
//                                     frappe.msgprint(__('Please select at least one student.'));
//                                     return;
//                                 }

//                                 let selected_students = student_options.filter(opt => selected_values_list.includes(opt.value));

//                                 let student_ids = selected_students.map(s => s.value);
//                                 let student_names = selected_students.map(s => s.label.split(" - ")[0]);
//                                 let student_mobiles = selected_students.map(s => s.mobile);

//                                 frappe.call({
//                                     method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.online_student.online_student.send_results_to_selected_students',
//                                     args: {
//                                         student_ids: student_ids,
//                                         student_names: student_names,
//                                         student_mobiles: student_mobiles
//                                     },
//                                     callback: function(r) {
//                                         if (!r.exc) {
//                                             frappe.msgprint(__('Results sent successfully to selected students.'));
//                                             selected_values = [...selected_values_list]; // Store selected values
//                                             dialog.dialog.hide();
//                                         } else {
//                                             frappe.msgprint(__('Failed to send results. Check logs for details.'));
//                                         }
//                                     }
//                                 });
//                             }
//                         });

//                         // Show selected values at the top
//                         dialog.dialog.fields_dict['selected'].$wrapper.find('.form-control').on('input', function() {
//                             let input = $(this).val().toLowerCase();
//                             let filtered = student_options.filter(s => s.label.toLowerCase().includes(input));
                            
//                             let selected_options = filtered.filter(s => selected_values.includes(s.value));
//                             let unselected_options = filtered.filter(s => !selected_values.includes(s.value));

//                             let sorted_options = [...selected_options, ...unselected_options];

//                             dialog.dialog.fields_dict['selected'].$wrapper.find('.awesomplete ul').empty();

//                             sorted_options.forEach(s => {
//                                 dialog.dialog.fields_dict['selected'].$wrapper.find('.awesomplete ul').append(`
//                                     <li data-value="${s.value}">${s.label}</li>
//                                 `);
//                             });
//                         });

//                     } else {
//                         frappe.msgprint(__('No students found.'));
//                     }
//                 }
//             });
//         }, __("Actions"));
//     }
// };

/////////////////////////////////////////// Above is the Bulk sharing resultss (Previous one) /////////////////////////////////////////////



/////////////////////////////////////////// Below is Delete and Process the Data /////////////////////////////////////////////

// frappe.listview_settings['Student Results'] = {
//     onload: function(listview) {
//         listview.page.add_inner_button(__('Delete Data'), function() {
//             // Show a confirmation dialog
//             frappe.confirm(
//                 'Are you sure you want to delete all records?',
//                 function() {
//                     // If confirmed, make a Frappe call to the server
//                     frappe.call({
//                         method: 'tnc_frappe_custom_app.delete_import_data_master_students.delete_all_records_in_student_results',
//                         callback: function(response) {
//                             if (response.message === 'success') {
//                                 frappe.show_alert({
//                                     message: __('All records have been deleted successfully.'),
//                                     indicator: 'green'
//                                 });
//                                 listview.refresh(); // Refresh the list view to reflect the changes
//                             } else {
//                                 frappe.show_alert({
//                                     message: __('There was an issue deleting the records.'),
//                                     indicator: 'red'
//                                 });
//                             }
//                         }
//                     });
//                 }
//             );
//         });
//         listview.page.add_inner_button('Process Data', () => {
//             frappe.prompt(
//                 {
//                     label: 'File ID',
//                     fieldname: 'file_id',
//                     fieldtype: 'Data',
//                     reqd: 1
//                 },
//                 (values) => {
//                     frappe.call({
//                         method: 'tnc_frappe_custom_app.script_to_import_data.import_student_results_sql_student_results',
//                         args: { file_id: values.file_id },
//                         callback: function(r) {
//                             if (!r.exc) {
//                                 frappe.msgprint('Data processing started. Check logs for updates.');
//                             }
//                         }
//                     });
//                 },
//                 'Enter File ID',
//                 'Start Processing'
//             );
//         });
//     }
// };


/////////////////////////////////////////// Above is Delete and Process the Data /////////////////////////////////////////////