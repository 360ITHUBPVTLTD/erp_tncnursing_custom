// // Copyright (c) 2024, Administrator and contributors
// // For license information, please see license.txt

// // frappe.ui.form.on("Not Imported Logs", {
// // 	refresh(frm) {

// // 	},
// // });

frappe.ui.form.on('Not Imported Logs', {
    refresh: function(frm) {
        // Show "Create Student" button only when student_id is empty
        if (!frm.doc.student_id) {
            frm.add_custom_button(__('Create Student'), function() {
                // Prompt for Student Name and Mobile
                frappe.prompt([
                    {
                        label: 'Student Name',
                        fieldname: 'student_name',
                        fieldtype: 'Data',
                        reqd: 1
                    },
                    {
                        label: 'Mobile',
                        fieldname: 'mobile',
                        fieldtype: 'Data',
                        default: frm.doc.mobile,
                        reqd: 1
                    }
                ], (values) => {
                    // Check if mobile number exists in the Student doctype
                    frappe.call({
                        method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.not_imported_logs.not_imported_logs.check_mobile_exists',
                        args: {
                            mobile: values.mobile
                        },
                        callback: function(response) {
                            if (response.message) {
                                // Mobile already exists, show error
                                frappe.msgprint(__('Student with this mobile number already exists.'));
                            } else {
                                // Mobile does not exist, proceed to create student
                                frappe.call({
                                    method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.not_imported_logs.not_imported_logs.create_student',
                                    args: {
                                        student_name: values.student_name,
                                        mobile: values.mobile,
                                        imported_batch_id :frm.doc.exam_id,
                                    },
                                    callback: function(create_response) {
                                        const student_id = create_response.message;
                                        if (student_id) {
                                            // Set the student_id in the current form
                                            frm.set_value('student_id', student_id);

                                            // Create Student Result with the newly created student_id
                                            frappe.call({
                                                method: 'tnc_frappe_custom_app.tnc_custom_app.doctype.not_imported_logs.not_imported_logs.create_student_result',
                                                args: {
                                                    student_id: student_id,
                                                    exam_id: frm.doc.exam_id,
                                                    student_name: values.student_name,
                                                    mobile: values.mobile,
                                                    rank: frm.doc.rank,
                                                    total_right: frm.doc.total_right,
                                                    total_wrong: frm.doc.total_wrong,
                                                    total_marks: frm.doc.total_marks,
                                                    total_skip: frm.doc.total_skip,
                                                    percentage: frm.doc.percentage
                                                },
                                                callback: function(result_response) {
                                                    const result_id = result_response.message;
                                                    if (result_id) {
                                                        // After creating result, update the status to 'Resolved'
                                                        frm.set_value('status', 'Resolved');
                                                        frm.set_value('student_result_id', result_id);

                                                        // Save the form to persist the changes
                                                        frm.save();
                                                    }
                                                }
                                            });
                                        }
                                    }
                                });
                            }
                        }
                    });
                }, 'Enter Student Details', 'Create Student');
            });
        }
    }
});
