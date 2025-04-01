// // // // // Copyright (c) 2024, Administrator and contributors
// // // // // For license information, please see license.txt

////////////////////////// Below is the Custom Report //////////////////////////

frappe.query_reports["Custom Student Result report"] = {
    "filters": [
        {
            "fieldname": "exam_name",
            "label": __("Exam Name"),
            "fieldtype": "Link",
            "options": "Test Series Type",  // Link to the "Test Series" doctype
            "reqd": 1,
            "on_change": function() {
                // Additional logic if needed when "Exam Name" changes
                checkRankLockStatus();
            }
        },
        {
            "fieldname": "exam_title_name",
            "label": __("Exam Title Name"),
            "fieldtype": "Link",
            "options": "Student Exam",  // Link to the "Student Exam" doctype
            "read_only": 0
        }
    ],
    onload: function(report) {
        // Add the Generate Rank button
        // report.page.add_inner_button(__('Generate Rank and Assign Colors'), function() {
        //     checkRankLockStatus(function(lockRanks) {
        //         if (lockRanks) {
        //             // $("button:contains('Generate Rank and Assign Colors')").hide();
        //             frappe.msgprint(__('Ranks are locked for this exam'));
        //         } else {
        //             var actualCandidates = report.data.length > 1 ? report.data.length - 1 : 0;
        //             frappe.prompt([
        //                 {'fieldname': 'start_rank', 'fieldtype': 'Int', 'label': 'Start Rank', 'default': 1, 'reqd': 1},
        //                 {'fieldname': 'last_rank', 'fieldtype': 'Int', 'label': 'Last Rank', 'reqd': 1},
        //                 {'fieldname': 'initial_regularised_ranks', 'fieldtype': 'Int', 'label': 'Initial Regularised Ranks', 'reqd': 1},
        //                 {'fieldname': 'actual_candidates', 'fieldtype': 'Int', 'label': 'Actual Candidates', 'read_only': 1, 'default': actualCandidates},
        //                 {'fieldname': 'green_end', 'fieldtype': 'Int', 'label': 'Green End', 'reqd': 1,'default':10},
        //                 {'fieldname': 'yellow_end', 'fieldtype': 'Int', 'label': 'Yellow End', 'reqd': 1,'default':30}
        //             ], function(values) {
        
        //                 // Validation for Green and Yellow ends
        //                 if (values.green_end >= 100 || values.yellow_end >= 100) {
        //                     frappe.msgprint(__('Both Green End and Yellow End values must be less than 100.'));
        //                     return;
        //                 }
        
        //                 if (values.green_end >= values.yellow_end) {
        //                     frappe.msgprint(__('Green End value must be less than Yellow End value.'));
        //                     return;
        //                 }
        
        //                 // First call: Generate Ranks
        //                 frappe.call({
        //                     method: "tnc_frappe_custom_app.report_rank_generation.generate_ranks",
        //                     args: {
        //                         docname: frappe.query_report.get_filter_value("exam_title_name"),
        //                         start_rank: values.start_rank,
        //                         initial_regularised_ranks: values.initial_regularised_ranks,
        //                         last_regularised_ranks: 0,
        //                         last_rank: values.last_rank,
        //                         actual_candidates: values.actual_candidates,
        //                         green_end: values.green_end,
        //                         yellow_end: values.yellow_end
        //                     },
        //                     callback: function(r) {
        //                         if (r.message) {
        //                             frappe.msgprint(r.message);
        
                                    
        //                         }
        //                     }
        //                 });
        //             }, __('Generate Ranks and Assign Colors'), __('Generate'));
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
        //                             {'fieldname': 'last_regularised_ranks', 'fieldtype': 'Int', 'label': 'Last Regularised Ranks', 'reqd': 1}, // Editable field
        //                             {'fieldname': 'green_end', 'fieldtype': 'Int', 'label': 'Green End', 'reqd': 1,'default':10}, // New field
        //                             {'fieldname': 'yellow_end', 'fieldtype': 'Int', 'label': 'Yellow End', 'reqd': 1,'default':30}  // New field
        //                         ], function(values) {
        
        //                             // Validate Green and Yellow End values
        //                             if (values.green_end >= 100 || values.yellow_end >= 100) {
        //                                 frappe.msgprint(__('Both Green End and Yellow End values must be less than 100.'));
        //                                 return;
        //                             }
        
        //                             if (values.green_end >= values.yellow_end) {
        //                                 frappe.msgprint(__('Green End value must be less than Yellow End value.'));
        //                                 return;
        //                             }
        
        //                             // First Call: Readjust Ranks
        //                             frappe.call({
        //                                 method: "tnc_frappe_custom_app.report_rank_generation.readjust_ranks",
        //                                 args: {
        //                                     docname: frappe.query_report.get_filter_value("exam_title_name"),
        //                                     start_rank: values.start_rank,
        //                                     initial_regularised_ranks: values.initial_regularised_ranks,
        //                                     last_regularised_ranks: values.last_regularised_ranks,
        //                                     last_rank: values.last_rank,
        //                                     actual_candidates: values.actual_candidates,
        //                                     green_end: values.green_end,
        //                                     yellow_end: values.yellow_end
        //                                 },
        //                                 callback: function(r) {
        //                                     if (r.message) {
        //                                         frappe.msgprint(r.message);
        
                                                
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

function checkRankLockStatus(callback) {
    var examTitleName = frappe.query_report.get_filter_value("exam_title_name");

    if (examTitleName) {
        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Student Exam",
                filters: { "name": examTitleName },
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



///////////////////////////////// Below code is Row Selection ///////////////////////////////////////////


document.addEventListener('click', function(event) {
    // Check if the clicked element is a cell
    var clickedCell = event.target.closest('.dt-cell__content');
    if (clickedCell) {
        // Remove highlight from previously highlighted cells
        var previouslyHighlightedCells = document.querySelectorAll('.highlighted-cell');
        previouslyHighlightedCells.forEach(function(cell) {
            cell.classList.remove('highlighted-cell');
            cell.style.backgroundColor = ''; // Remove background color
            cell.style.border = ''; // Remove border
            cell.style.fontWeight = '';
        });

        // Highlight the clicked row's cells
        var clickedRow = event.target.closest('.dt-row');
        var cellsInClickedRow = clickedRow.querySelectorAll('.dt-cell__content');

        cellsInClickedRow.forEach(function(cell) {
            cell.classList.add('highlighted-cell');
            cell.style.backgroundColor = '#d7eaf9'; // Light blue background color
            cell.style.border = '2px solid #90c9e3'; // Border color
            cell.style.fontWeight = 'bold';
        });
    }
});
