// Copyright (c) 2024, Administrator and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Employee Attendance", {
// 	refresh(frm) {

// 	},
// });
// Employee Attendance Client Script
// Employee Attendance Client Script
frappe.ui.form.on('Employee Attendance', {
    refresh(frm) {
        // Ensure attendance_date is set
        if (!frm.doc.attendance_date) {
            frm.get_field("attendance_html").$wrapper.html("<p>Please set the Attendance Date to mark attendance.</p>");
            return;
        }

        // Always clear the attendance_html field before populating
        frm.get_field("attendance_html").$wrapper.empty();

        if (!frm.doc.attendance_marked) {
            // Attendance not marked yet; show attendance marking interface
            frm.get_field("attendance_html").$wrapper.html('<p>Loading attendance interface...</p>');

            // Fetch active employees and render the attendance interface
            frappe.call({
                method: "tnc_frappe_custom_app.tnc_custom_app.doctype.employee_attendance.employee_attendance.get_active_employees",
                args: {
                    "attendance_date": frm.doc.attendance_date
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        let employees = r.message;

                        // Construct HTML for attendance marking with checkboxes
                        let html = `
                            <div style="margin-bottom:10px;">
                                <button class="btn btn-default btn-select-all">Select All</button>
                                <button class="btn btn-default btn-unselect-all">Unselect All</button>
                                <button class="btn btn-primary btn-submit-attendance">Submit Attendance</button>
                            </div>
                            <table class="table table-bordered table-hover">
                                <thead>
                                    <tr>
                                        <th>Mark Present</th>
                                        <th>Employee ID</th>
                                        <th>Employee Name</th>
                                    </tr>
                                </thead>
                                <tbody>`;

                        employees.forEach(function(emp) {
                            html += `
                                <tr>
                                    <td style="text-align: center;">
                                        <input type="checkbox" class="attendance-checkbox" data-employee-id="${emp.name}">
                                    </td>
                                    <td>${emp.name}</td>
                                    <td>${emp.employee_name}</td>
                                </tr>`;
                        });

                        html += `</tbody></table>`;
                        frm.get_field("attendance_html").$wrapper.html(html);
                    } else {
                        frm.get_field("attendance_html").$wrapper.html("<p>No active employees found.</p>");
                    }
                },
                error: function(err) {
                    frm.get_field("attendance_html").$wrapper.html("<p>Error fetching active employees.</p>");
                    console.error("Error fetching active employees:", err);
                }
            });

            // Unbind any existing click handlers to prevent duplicates
            frm.get_field("attendance_html").$wrapper.off('click', '.btn-submit-attendance');

            // Event delegation for Select All button
            frm.get_field("attendance_html").$wrapper.on('click', '.btn-select-all', function() {
                frm.get_field("attendance_html").$wrapper.find('.attendance-checkbox').prop('checked', true);
            });

            // Event delegation for Unselect All button
            frm.get_field("attendance_html").$wrapper.on('click', '.btn-unselect-all', function() {
                frm.get_field("attendance_html").$wrapper.find('.attendance-checkbox').prop('checked', false);
            });

            // Event delegation for Submit Attendance button with Confirmation
            frm.get_field("attendance_html").$wrapper.on('click', '.btn-submit-attendance', function() {
                let attendance_list = [];
                frm.get_field("attendance_html").$wrapper.find('.attendance-checkbox').each(function() {
                    attendance_list.push({
                        employee_id: $(this).data('employee-id'),
                        status: $(this).is(':checked') ? 'Present' : 'Absent'
                    });
                });

                console.log("Attendance List:", attendance_list);

                // Validation: Ensure attendance_list is not empty
                if (attendance_list.length === 0) {
                    frappe.msgprint("No attendance data to submit.");
                    return;
                }

                // Confirmation Dialog
                frappe.confirm(
                    'Are you sure you want to submit attendance for the selected employees?',
                    function() {
                        // Show a loading indicator
                        frappe.show_alert({message: 'Submitting attendance...', indicator: 'blue'}, 5);

                        // Disable the Submit button to prevent multiple submissions
                        $('.btn-submit-attendance').prop('disabled', true);

                        // Proceed with API call
                        frappe.call({
                            method: "tnc_frappe_custom_app.tnc_custom_app.doctype.employee_attendance.employee_attendance.submit_employee_attendance",
                            args: {
                                "attendance_date": frm.doc.attendance_date,
                                "attendance_list": attendance_list
                            },
                            callback: function(response) {
                                if (response.message === "OK") {
                                    frappe.msgprint("Attendance submitted successfully!");
                                    // Set attendance_marked to true and save the document
                                    frm.set_value("attendance_marked", 1);
                                    frm.save();
                                } else {
                                    frappe.msgprint({
                                        title: __('Error'),
                                        indicator: 'red',
                                        message: response.message || "There was an error submitting attendance."
                                    });
                                }
                                // Re-enable the Submit button
                                $('.btn-submit-attendance').prop('disabled', false);
                            },
                            error: function(err) {
                                frappe.msgprint({
                                    title: __('Error'),
                                    indicator: 'red',
                                    message: err.message || "There was an error submitting attendance."
                                });
                                console.error("Error submitting attendance:", err);
                                // Re-enable the Submit button
                                $('.btn-submit-attendance').prop('disabled', false);
                            }
                        });
                    },
                    function() {
                        // User cancelled, do nothing
                        frappe.msgprint("Attendance submission cancelled.");
                    }
                );
            });
        } else {
            // Attendance already marked; fetch and display existing attendance records
            frm.get_field("attendance_html").$wrapper.html('<p>Loading existing attendance records...</p>');

            frappe.call({
                method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.employee_attendance.employee_attendance.get_existing_attendance',
                args: {
                    "attendance_date": frm.doc.attendance_date
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        const records = r.message;

                        // Construct HTML for displaying session attendance
                        let html = `<table class="table table-bordered" style="border-collapse: collapse; width: 100%;">
                            <thead style="background-color: lightSkyBlue; border: 1px solid black;">
                                <tr>
                                    <th style="border: 1px solid black;">Employee ID</th>
                                    <th style="border: 1px solid black;">Employee Name</th>
                                    <th style="border: 1px solid black;">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${records.map(row => `
                                    <tr>
                                        <td style="border: 1px solid black;">${row.employee_id}</td>
                                        <td style="border: 1px solid black;">${row.employee_name}</td>
                                        <td style="border: 1px solid black;">${row.status || ''}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>`;

                        // Set the constructed HTML to the attendance_html field
                        frm.get_field("attendance_html").$wrapper.html(html);
                    } else {
                        // Display message when no attendance records are found
                        let html = '<p style="color: gray; text-align: center;">No Attendance records found for this date.</p>';
                        frm.get_field("attendance_html").$wrapper.html(html);
                    }
                },
                error: function(err) {
                    frm.get_field("attendance_html").$wrapper.html("<p>Error fetching attendance records.</p>");
                    console.error("Error fetching attendance records:", err);
                }
            });
        }
    },
});

