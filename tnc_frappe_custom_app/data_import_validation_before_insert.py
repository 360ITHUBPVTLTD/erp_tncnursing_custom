
import frappe

@frappe.whitelist()
def validate_imported_batch_id():
    # Check if all records in 'Student Master Data' have an 'imported_batch_id'
    records_without_imported_batch_id = frappe.get_all(
        'Students Master Data',
        filters=[['imported_batch_id', 'is', 'not set']],
        fields=['name']
    )
    
    if records_without_imported_batch_id:
        return {
            'status': 'error',
            'message': 'Before inserting, please sync the bundle. Some records are missing an imported_batch_id.'
        }
    
    return {'status': 'success'}