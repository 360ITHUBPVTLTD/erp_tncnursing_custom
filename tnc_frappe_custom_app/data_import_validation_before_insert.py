
import frappe

@frappe.whitelist()
def validate_imported_batch_id():
    # Check if all records in 'Student Master Data' have an 'exam_id'
    records_without_imported_batch_id = frappe.get_all(
        'Students Master Data',
        filters=[['exam_id', 'is', 'not set']],
        fields=['name']
    )
    
    if records_without_imported_batch_id:
        return {
            'status': 'error',
            'message': 'Before inserting, please sync the bundle. Some records are missing an exam_id.'
        }
    
    return {'status': 'success'}