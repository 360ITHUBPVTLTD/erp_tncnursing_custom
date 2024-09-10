// // // // // Copyright (c) 2024, Administrator and contributors
// // // // // For license information, please see license.txt

// frappe.query_reports["Custom Student Result report"] = {
//     "filters": [
//         {
//             "fieldname": "exam_name",
//             "label": __("Exam Name"),
//             "fieldtype": "Link",
//             "options": "Test Series Type",
//             "reqd": 1,
//             "default": 0,
//             "on_change": function() {
//                 updateExamTitleNameFilter();
//             }
//         },
//         {
//             "fieldname": "exam_title_name",
//             "label": __("Exam Title Name"),
//             "fieldtype": "Select",
//             "options": [],
//             "read_only": 0
//         }
//     ],
//     onload: function(report) {
//         // Add the Process Data button
//         // report.page.add_inner_button(__('Process Data'), function() {
//         //     frappe.call({
//         //         method: "tnc_frappe_custom_app.report_sync_button.sync_data",
//         //         args: {
//         //             report_name: frappe.query_report.get_filter_value("exam_title_name")
//         //         },
//         //         callback: function(r) {
//         //             if (r.message) {
//         //                 if (r.message.status === "success") {
//         //                     frappe.msgprint(__('Data synchronized successfully'));
//         //                     report.refresh();
//         //                 } else if (r.message.status === "no_data") {
//         //                     frappe.msgprint(__('No data to synchronize'));
//         //                 }
//         //             }
//         //         }
//         //     });
//         // });

//         // Add the Generate Rank button
//         report.page.add_inner_button(__('Generate Rank'), function() {
//             var actualCandidates = report.data.length > 1 ? report.data.length - 1 : 0;
//             frappe.prompt([
//                 {'fieldname': 'start_rank', 'fieldtype': 'Int', 'label': 'Start Rank', 'default': 1, 'reqd': 1},
//                 {'fieldname': 'last_rank', 'fieldtype': 'Int', 'label': 'Last Rank', 'reqd': 1},
//                 {'fieldname': 'initial_regularised_ranks', 'fieldtype': 'Int', 'label': 'Initial Regularised Ranks', 'reqd': 1},
//                 {'fieldname': 'actual_candidates', 'fieldtype': 'Int', 'label': 'Actual Candidates', 'read_only': 1, 'default': actualCandidates},
//             ], function(values) {
//                 frappe.call({
//                     method: "tnc_frappe_custom_app.report_rank_generation.generate_ranks",
//                     args: {
//                         docname: frappe.query_report.get_filter_value("exam_title_name"),
//                         start_rank: values.start_rank,
//                         initial_regularised_ranks: values.initial_regularised_ranks,
//                         last_regularised_ranks: 0,
//                         last_rank: values.last_rank,
//                         actual_candidates: values.actual_candidates
//                     },
//                     callback: function(r) {
//                         if (r.message) {
//                             frappe.msgprint(r.message);
//                             report.refresh();  // Refresh the report data if ranks were generated successfully
//                         }
//                     }
//                 });
//             }, __('Generate Ranks'), __('Generate'));
//         });

//         // Add the Reset Rank button
//         report.page.add_inner_button(__('Reset Rank'), function() {
//             frappe.confirm(__('Are you sure you want to reset the ranks?'), function() {
//                 frappe.call({
//                     method: "tnc_frappe_custom_app.report_rank_generation.reset_ranks",
//                     args: {
//                         exam_title_name: frappe.query_report.get_filter_value("exam_title_name")
//                     },
//                     callback: function(r) {
//                         if (r.message) {
//                             frappe.msgprint(__('Ranks have been reset successfully'));
//                             report.refresh();  // Refresh the report data if ranks were reset successfully
//                         }
//                     }
//                 });
//             });
//         });

//         // Add the Readjust Rank button directly
//         report.page.add_inner_button(__('Readjust Rank'), function() {
//             frappe.call({
//                 method: "tnc_frappe_custom_app.report_rank_generation.get_rank_details",
//                 args: {
//                     exam_title_name: frappe.query_report.get_filter_value("exam_title_name")
//                 },
//                 callback: function(response) {
//                     var data = response.message;
//                     if (data) {
//                         frappe.prompt([
//                             {'fieldname': 'start_rank', 'fieldtype': 'Int', 'label': 'Start Rank', 'default': data.start_rank, 'read_only': 1},
//                             {'fieldname': 'last_rank', 'fieldtype': 'Int', 'label': 'Last Rank', 'default': data.last_rank, 'read_only': 1},
//                             {'fieldname': 'initial_regularised_ranks', 'fieldtype': 'Int', 'label': 'Initial Regularised Ranks', 'default': data.initial_regularised_ranks, 'read_only': 1},
//                             {'fieldname': 'actual_candidates', 'fieldtype': 'Int', 'label': 'Actual Candidates', 'default': data.actual_candidates, 'read_only': 1},
//                             {'fieldname': 'last_regularised_ranks', 'fieldtype': 'Int', 'label': 'Last Regularised Ranks', 'reqd': 1} // This field is editable
//                         ], function(values) {
//                             frappe.call({
//                                 method: "tnc_frappe_custom_app.report_rank_generation.readjust_ranks",
//                                 args: {
//                                     docname: frappe.query_report.get_filter_value("exam_title_name"),
//                                     start_rank: values.start_rank,
//                                     initial_regularised_ranks: values.initial_regularised_ranks,
//                                     last_regularised_ranks: values.last_regularised_ranks,
//                                     last_rank: values.last_rank,
//                                     actual_candidates: values.actual_candidates
//                                 },
//                                 callback: function(r) {
//                                     if (r.message) {
//                                         frappe.msgprint(r.message);
//                                         report.refresh();  // Refresh the report data if ranks were readjusted successfully
//                                     }
//                                 }
//                             });
//                         }, __('Readjust Ranks'), __('Readjust'));
//                     }
//                 }
//             });
//         });
//     }
// };

// function updateExamTitleNameFilter() {
//     var examName = frappe.query_report.get_filter_value("exam_name");

//     if (examName) {
//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Student Exam",
//                 filters: { "exam_name": examName },
//                 fields: ["exam_title_name"],
//                 distinct: 1
//             },
//             callback: function(response) {
//                 var selectField = frappe.query_report.get_filter("exam_title_name");
//                 var options = [];

//                 if (response.message && response.message.length > 0) {
//                     options = response.message.map(function(item) {
//                         return item.exam_title_name;
//                     });

//                     selectField.df.options = "\n" + options.join("\n");
//                     selectField.refresh();
//                 } else {
//                     selectField.df.options = [];
//                     selectField.refresh();
//                 }
//             }
//         });
//     } else {
//         var selectField = frappe.query_report.get_filter("exam_title_name");
//         selectField.df.options = [];
//         selectField.refresh();
//     }
// }


// /////////////////////// Below code is Row Selection //////////////////////

var previousSelectedRow = null;
 
document.addEventListener('click', function(event) {
    // Check if the clicked element is within a .dt-cell__content element
    var cellContent = event.target.closest('.dt-cell__content');
 
    if (cellContent) {
        // Get the parent row of the clicked cell
        var row = cellContent.closest('.dt-row');
 
        // If there's a previously selected row, deselect it
        if (previousSelectedRow) {
            var cellsInPreviousRow = previousSelectedRow.querySelectorAll('.dt-cell__content');
            cellsInPreviousRow.forEach(function(cellInRow) {
                cellInRow.style.backgroundColor = '';
            });
        }
 
        // Reset the background color of all cells in the new row
        var cellsInRow = row.querySelectorAll('.dt-cell__content');
        cellsInRow.forEach(function(cellInRow) {
            cellInRow.style.backgroundColor = 'skyblue';
        });
 
        // Update the previously selected row
        previousSelectedRow = row;
    }
});



frappe.query_reports["Custom Student Result report"] = {
    "filters": [
        {
            "fieldname": "exam_name",
            "label": __("Exam Name"),
            "fieldtype": "Link",
            "options": "Test Series Type",
            "reqd": 1,
            "default": 0,
            "on_change": function() {
                updateExamTitleNameFilter();
                checkRankLockStatus();
            }
        },
        {
            "fieldname": "exam_title_name",
            "label": __("Exam Title Name"),
            "fieldtype": "Select",
            "options": [],
            "read_only": 0
        }
    ],
    onload: function(report) {
        // Add the Generate Rank button
        // report.page.add_inner_button(__('Generate Rank'), function() {
        //     checkRankLockStatus(function(lockRanks) {
        //         if (lockRanks) {
        //             frappe.msgprint(__('Ranks are locked for this exam'));
        //         } else {
        //             var actualCandidates = report.data.length > 1 ? report.data.length - 1 : 0;
        //             frappe.prompt([
        //                 {'fieldname': 'start_rank', 'fieldtype': 'Int', 'label': 'Start Rank', 'default': 1, 'reqd': 1},
        //                 {'fieldname': 'last_rank', 'fieldtype': 'Int', 'label': 'Last Rank', 'reqd': 1},
        //                 {'fieldname': 'initial_regularised_ranks', 'fieldtype': 'Int', 'label': 'Initial Regularised Ranks', 'reqd': 1},
        //                 {'fieldname': 'actual_candidates', 'fieldtype': 'Int', 'label': 'Actual Candidates', 'read_only': 1, 'default': actualCandidates}
        //             ], function(values) {
        //                 frappe.call({
        //                     method: "tnc_frappe_custom_app.report_rank_generation.generate_ranks",
        //                     args: {
        //                         docname: frappe.query_report.get_filter_value("exam_title_name"),
        //                         start_rank: values.start_rank,
        //                         initial_regularised_ranks: values.initial_regularised_ranks,
        //                         last_regularised_ranks: 0,
        //                         last_rank: values.last_rank,
        //                         actual_candidates: values.actual_candidates
        //                     },
        //                     callback: function(r) {
        //                         if (r.message) {
        //                             frappe.msgprint(r.message);
        //                             report.refresh();  // Refresh the report data if ranks were generated successfully
        //                         }
        //                     }
        //                 });
        //             }, __('Generate Ranks'), __('Generate'));
        //         }
        //     });
        // });

        // Add the Readjust Rank button
        // report.page.add_inner_button(__('Readjust Rank'), function() {
        //     checkRankLockStatus(function(lockRanks) {
        //         if (lockRanks) {
        //             frappe.msgprint(__('Ranks are locked for this exam'));
        //         } else {
        //             frappe.call({
        //                 method: "tnc_frappe_custom_app.report_rank_generation.get_rank_details",
        //                 args: {
        //                     exam_title_name: frappe.query_report.get_filter_value("exam_title_name")
        //                 },
        //                 callback: function(response) {
        //                     var data = response.message;
        //                     if (data) {
        //                         frappe.prompt([
        //                             {'fieldname': 'start_rank', 'fieldtype': 'Int', 'label': 'Start Rank', 'default': data.start_rank, 'read_only': 1},
        //                             {'fieldname': 'last_rank', 'fieldtype': 'Int', 'label': 'Last Rank', 'default': data.last_rank, 'read_only': 1},
        //                             {'fieldname': 'initial_regularised_ranks', 'fieldtype': 'Int', 'label': 'Initial Regularised Ranks', 'default': data.initial_regularised_ranks, 'read_only': 1},
        //                             {'fieldname': 'actual_candidates', 'fieldtype': 'Int', 'label': 'Actual Candidates', 'default': data.actual_candidates, 'read_only': 1},
        //                             {'fieldname': 'last_regularised_ranks', 'fieldtype': 'Int', 'label': 'Last Regularised Ranks', 'reqd': 1} // This field is editable
        //                         ], function(values) {
        //                             frappe.call({
        //                                 method: "tnc_frappe_custom_app.report_rank_generation.readjust_ranks",
        //                                 args: {
        //                                     docname: frappe.query_report.get_filter_value("exam_title_name"),
        //                                     start_rank: values.start_rank,
        //                                     initial_regularised_ranks: values.initial_regularised_ranks,
        //                                     last_regularised_ranks: values.last_regularised_ranks,
        //                                     last_rank: values.last_rank,
        //                                     actual_candidates: values.actual_candidates
        //                                 },
        //                                 callback: function(r) {
        //                                     if (r.message) {
        //                                         frappe.msgprint(r.message);
        //                                         report.refresh();  // Refresh the report data if ranks were readjusted successfully
        //                                     }
        //                                 }
        //                             });
        //                         }, __('Readjust Ranks'), __('Readjust'));
        //                     }
        //                 }
        //             });
        //         }
        //     });
        // });

        // Add the Reset Rank button
        // report.page.add_inner_button(__('Reset Rank'), function() {
        //     checkRankLockStatus(function(lockRanks) {
        //         if (lockRanks) {
        //             frappe.msgprint(__('Ranks are locked for this exam'));
        //         } else {
        //             frappe.confirm(__('Are you sure you want to reset the ranks?'), function() {
        //                 frappe.call({
        //                     method: "tnc_frappe_custom_app.report_rank_generation.reset_ranks",
        //                     args: {
        //                         exam_title_name: frappe.query_report.get_filter_value("exam_title_name")
        //                     },
        //                     callback: function(r) {
        //                         if (r.message) {
        //                             frappe.msgprint(__('Ranks have been reset successfully'));
        //                             report.refresh();  // Refresh the report data if ranks were reset successfully
        //                         }
        //                     }
        //                 });
        //             });
        //         }
        //     });
        // });
    }
};

function updateExamTitleNameFilter() {
    var examName = frappe.query_report.get_filter_value("exam_name");

    if (examName) {
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Student Exam",
                filters: { "exam_name": examName },
                fields: ["exam_title_name"],
                distinct: 1
            },
            callback: function(response) {
                var selectField = frappe.query_report.get_filter("exam_title_name");
                var options = [];

                if (response.message && response.message.length > 0) {
                    options = response.message.map(function(item) {
                        return item.exam_title_name;
                    });

                    selectField.df.options = "\n" + options.join("\n");
                    selectField.refresh();
                } else {
                    selectField.df.options = [];
                    selectField.refresh();
                }
            }
        });
    } else {
        var selectField = frappe.query_report.get_filter("exam_title_name");
        selectField.df.options = [];
        selectField.refresh();
    }
}

function checkRankLockStatus(callback) {
    var examTitleName = frappe.query_report.get_filter_value("exam_title_name");

    if (examTitleName) {
        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Student Exam",
                filters: { "exam_title_name": examTitleName },
                fieldname: "lock_ranks"
            },
            callback: function(response) {
                var lockRanks = response.message ? response.message.lock_ranks : 0;
                if (callback) callback(lockRanks);
            }
        });
    } else {
        if (callback) callback(0); // Assume not locked if no exam title name
    }
}

