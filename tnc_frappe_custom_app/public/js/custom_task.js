frappe.ui.form.on('Task', {
    onload: function(frm) {
        // 1. Capture the initial status from the database
        frm.last_known_status = frm.doc.status;
    },

    status: function(frm) {
        // 2. Define the Restricted Rule
        const target_status = "Completed";
        
        // If they are NOT selecting 'Completed', it's a valid move.
        // Update our tracker and exit.
        if (frm.doc.status !== target_status) {
            frm.last_known_status = frm.doc.status;
            return;
        }

        // 3. Permission Check (Only running if status IS 'Completed')
        const allowed_roles = ["Administrator", "System Manager", "TNC Super Admin"];
        let is_admin = allowed_roles.some(role => frappe.user.has_role(role));
        
        // If new doc, session user is creator. If saved doc, check owner field.
        let is_creator = frm.is_new() ? true : (frm.doc.owner === frappe.session.user);

        // 4. Enforce Revert
        if (!is_admin && !is_creator) {
            
            // UX: Tell them what happened
            frappe.show_alert({
                message: __('Permission Denied: Only the Creator can mark task as Completed.'),
                indicator: 'red'
            }, 5);

            // MAGIC: Revert to the specific status it held 1 second ago
            // We verify last_known_status exists (fallback to 'Open' just in case)
            let revert_to = frm.last_known_status || "Open";
            
            frm.set_value('status', revert_to);
            
            // Note: We do NOT update frm.last_known_status here, 
            // because the current attempt was invalid.
        }
    }
});