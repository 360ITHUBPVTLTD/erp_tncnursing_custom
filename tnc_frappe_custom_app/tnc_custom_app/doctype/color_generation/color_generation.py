# Copyright (c) 2024, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ColorGeneration(Document):
	pass


@frappe.whitelist()
def assign_colors(exam_name):
    # Fetch the Student Exam document
    exam_doc = frappe.get_doc('Student Exam', exam_name)
    
    # Fetch the color generation ranges from the child table
    color_ranges = {}
    total_students = len(frappe.get_all('Student Results', filters={'batch_id': exam_name}, fields=['name']))
    
    # Extract color ranges from the color_generation child table
    for color_row in exam_doc.color_generation:
        color_ranges[color_row.color] = int(total_students * (color_row.end_to) / 100)
    print(color_ranges)
        
    
    # Calculate percentage thresholds and student counts
    # thresholds = {}
    # for color, range_values in color_ranges.items():
    #     # start_percentage = range_values['start']
    #     end_percentage = range_values['end']
    #     thresholds[color] = {
    #         # 'start_count': int(total_students * (start_percentage - 1) / 100),
    #         'end_count': int(total_students * end_percentage / 100)
    #     }
    
    # Fetch the Student Results for the current exam
    student_results = frappe.get_all('Student Results', filters={'batch_id': exam_name}, fields=['name'],order_by='rank desc')
    counter=1
    for student_results in student_results:
        if counter<color_ranges["Green"]:
            frappe.db.set_value('Student Results', student_results.name, 'rank_color', 'G')
        elif counter<color_ranges["Yellow"]:
            frappe.db.set_value('Student Results', student_results.name, 'rank_color', 'Y')
        else:
            frappe.db.set_value('Student Results', student_results.name, 'rank_color', 'R')
        counter+=1

    
    # # Initialize variables for color assignment
    # color_counts = {color: 0 for color in color_ranges}
    # current_index = 0
    
    # # Assign colors based on percentage ranges
    # for color, range_values in color_ranges.items():
    #     start_count = thresholds[color]['start_count']
    #     end_count = thresholds[color]['end_count']
        
    #     # Assign color within the calculated range
    #     while current_index < len(sorted_results) and current_index < end_count:
    #         if current_index >= start_count:
    #             result_name = sorted_results[current_index]['name']
    #             rank_color = 'G' if color == 'Green' else 'Y' if color == 'Yellow' else 'R'
    #             frappe.db.set_value('Student Results', result_name, 'rank_color', rank_color)
    #         current_index += 1
    
    return {'message': 'Colors assigned successfully'}


