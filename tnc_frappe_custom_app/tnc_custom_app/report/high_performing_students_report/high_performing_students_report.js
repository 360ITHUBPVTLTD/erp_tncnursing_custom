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
			default: 50
		}
		
	],
	"onload": function (report) {
		report.page.add_inner_button("Send WhatsApp", () => {
			let filters = report.get_filter_values(true);
			if (!filters) return;
	
			frappe.confirm(
				"Are you sure you want to send WhatsApp messages to these students?",
				() => {
					// Yes - proceed to send
					frappe.call({
						method: "tnc_frappe_custom_app.tnc_custom_app.report.high_performing_students_report.high_performing_students_report.send_whatsapp_from_reports_using_rq", 
						args: {
							filters: filters
						},
						callback: function (r) {
							console.log("Response", r);
							
							if (r.message) {  // Ensure message exists
								console.log("SENT", r.message.success);
						
								if (r.message.status === 'Queued') {
									frappe.msgprint({
										title: __("✅ Success"),
										message: `🎉 WhatsApp messages sent successfully to students!`,
										indicator: "green"
									});
								} else {
									frappe.msgprint({
										title: __("⚠️ Partial Success"),
										message: `✅ Sent: ${r.message.sent_count} <br> ❌ Failed: ${r.message.failed_count} <br> 🔍 Check logs for details.`,
										indicator: "orange"
									});
								}
							} else {
								frappe.msgprint({
									title: __("❌ Failed"),
									message: "WhatsApp messages could not be sent.",
									indicator: "red"
								});
							}
						}
						
					});
				},
				() => {
					// No - cancelled
					frappe.msgprint(__('Sending cancelled.'));
				}
			);
		});
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
