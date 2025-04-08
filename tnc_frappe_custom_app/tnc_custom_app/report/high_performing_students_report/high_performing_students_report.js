// Copyright (c) 2025, Administrator and contributors
// For license information, please see license.txt

frappe.query_reports["High performing Students Report"] = {
	"filters": [
		{
			fieldname: "exam_date",
			label: "Exam Date Range",
			fieldtype: "Date Range",
			reqd: 0
		},
		{
			fieldname: "exam_name",
			label: "Test Series",
			fieldtype: "Link",
			options: "Test Series Type"
		},
		{
			fieldname: "student_id",
			label: "Student",
			fieldtype: "Link",
			options: "Online Student"
		},
		// {
		// 	fieldname: "exam_id",
		// 	label: "Exam Title",
		// 	fieldtype: "Link",
		// 	options: "Student Exam"
		// },
		{
			fieldname: "min_total_exams",
			label: "Total Exams Attempted",
			fieldtype: "Int",
			default: 0
		},		
		{
			fieldname: "count",
			label: "Top Students",
			fieldtype: "Int",
			// default: 50
		}
		
	],
	"onload": function (report) {
		// Adding a custom inner button to the report page
		report.page.add_inner_button("Send WhatsApp", () => {
			let filters = report.get_filter_values(true);
			if (!filters) return;
			
			// First, create a Bulk WhatsApp Entry from the report filters.
			frappe.call({
				method: "tnc_frappe_custom_app.tnc_custom_app.report.high_performing_students_report.high_performing_students_report.create_bulk_whatsapp_entry_from_report",
				args: { filters: JSON.stringify(filters) },
				callback: function(r) {
					if (r.message && r.message.count !== undefined && r.message.bulk_docname) {
						const count = r.message.count;
						const bulk_docname = r.message.bulk_docname;
						frappe.confirm(
							`There will be ${count} WhatsApp messages triggered. Do you want to proceed?`,
							() => {
								// User confirmed: trigger the background job to send the messages
								frappe.call({
									method: "tnc_frappe_custom_app.tnc_custom_app.report.high_performing_students_report.high_performing_students_report.send_whatsapp_from_reports_using_rq",
									args: { filters: JSON.stringify(filters), bulk_docname: bulk_docname },
									callback: function(r) {
										if (r.message) {
											if (r.message.status === "Queued") {
												frappe.msgprint({
													title: __("✅ Success"),
													message: "🎉 WhatsApp messages scheduled successfully!",
													indicator: "green"
												});
											} else {
												frappe.msgprint({
													title: __("⚠️ Partial Success"),
													message: "Some issues occurred scheduling WhatsApp messages. Check logs for details.",
													indicator: "orange"
												});
											}
										} else {
											frappe.msgprint({
												title: __("❌ Failed"),
												message: "WhatsApp messages could not be scheduled.",
												indicator: "red"
											});
										}
									}
								});
							},
							() => {
								// User cancelled – now cancel the Bulk WhatsApp Entry
								frappe.call({
									method: "tnc_frappe_custom_app.tnc_custom_app.report.high_performing_students_report.high_performing_students_report.cancel_bulk_result",
									args: { bulk_docname: bulk_docname },
									callback: function() {
										frappe.msgprint(__('Sending cancelled and bulk entry deleted.'));
									}
								});
							}
						);
					} else {
						frappe.msgprint(__('Failed to create bulk entry for WhatsApp sharing.'));
					}
				}
			});
		});

		
		// report.page.add_inner_button("Send WhatsApp", () => {
		// 	let filters = report.get_filter_values(true);
		// 	if (!filters) return;
	
		// 	frappe.confirm(
		// 		"Are you sure you want to send WhatsApp messages to these students?",
		// 		() => {
		// 			// Yes - proceed to send
		// 			frappe.call({
		// 				method: "tnc_frappe_custom_app.tnc_custom_app.report.high_performing_students_report.high_performing_students_report.send_whatsapp_from_reports_using_rq", 
		// 				args: {
		// 					filters: filters
		// 				},
		// 				callback: function (r) {
		// 					if (r.message) {
		// 						if (r.message.success) {
		// 							frappe.msgprint({
		// 								title: __("✅ Success"),
		// 								message: `🎉 WhatsApp messages sent successfully! <br> ✅ Sent: ${r.message.sent_count} <br> ❌ Failed: ${r.message.failed_count}`,
		// 								indicator: "green"
		// 							});
		// 						} else {
		// 							frappe.msgprint({
		// 								title: __("⚠️ Partial Success"),
		// 								message: `✅ Sent: ${r.message.sent_count} <br> ❌ Failed: ${r.message.failed_count} <br> 🔍 Check logs for details.`,
		// 								indicator: "orange"
		// 							});
		// 						}
		// 					} else {
		// 						frappe.msgprint({
		// 							title: __("❌ Failed"),
		// 							message: "WhatsApp messages could not be sent.",
		// 							indicator: "red"
		// 						});
		// 					}
		// 				}
		// 			});
		// 		},
		// 		() => {
		// 			// No - cancelled
		// 			frappe.msgprint(__('Sending cancelled.'));
		// 		}
		// 	);
		// });
	}
	
	
};



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
