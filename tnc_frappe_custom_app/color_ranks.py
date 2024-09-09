import frappe
import frappe

@frappe.whitelist()
def sync_ranks():
    # Fetch all Student Exam records
    exam_docs = frappe.get_all('Student Exam', fields=['name'])

    for exam in exam_docs:
        # Get the name of the current exam record
        exam_name = exam['name']
        print(exam_name)
        
        # Fetch results for the current exam's batch_id
        results = frappe.get_all('Student Results', filters={'batch_id': exam_name}, fields=['rank'], order_by='rank asc')

        if results:
            # Get the last rank (the highest rank number)
            last_rank = results[-1]['rank']
            # Get the total number of actual candidates
            actual_candidates = len(results)
            
            print(f"Batch ID: {exam_name}, Last Rank: {last_rank}, Actual Candidates: {actual_candidates}")
            
            # Fetch the Student Exam document
            exam_doc = frappe.get_doc('Student Exam', exam_name)
            
            # Set the last_rank and actual_candidates in the main Student Exam document
            exam_doc.last_rank = last_rank
            exam_doc.actual_candidates = actual_candidates

            # Initialize flags to track updates for Green and Red
            red_updated = False
            green_updated = False
            
            # Loop through the color_generation child table
            for color_row in exam_doc.color_generation:
                # Update the row where color is "Red" to set the last rank
                if color_row.color == "Red":
                    color_row.end_to = last_rank
                    red_updated = True
                
                # Update the row where color is "Green" to set starts_from as 1
                if color_row.color == "Green":
                    color_row.starts_from = 1
                    green_updated = True
                
                # Break the loop if both "Red" and "Green" have been updated
                if red_updated and green_updated:
                    break

            # Save the updated document
            exam_doc.save()

    return {'message': 'Ranks synchronized successfully'}



################################ Assign color_generation to Ranks #################################

import frappe

@frappe.whitelist()
def assign_colors(exam_name):
    # Fetch the Student Exam document
    exam_doc = frappe.get_doc('Student Exam', exam_name)
    
    # Fetch the rank ranges from the color_generation child table
    color_ranges = {}
    for color_row in exam_doc.color_generation:
        color_ranges[color_row.color] = {
            'start': color_row.starts_from,
            'end': color_row.end_to
        }
    
    # Fetch the Student Results for the current exam
    student_results = frappe.get_all('Student Results', filters={'batch_id': exam_name}, fields=['name', 'rank'])

    # Loop through the results and assign colors based on the rank ranges
    for result in student_results:
        rank = result['rank']
        result_name = result['name']

        # Initialize rank_color
        rank_color = None

        # Check rank against the color ranges and assign the color
        for color, range_values in color_ranges.items():
            if range_values['start'] <= rank <= range_values['end']:
                if color == "Green":
                    rank_color = "G"
                elif color == "Yellow":
                    rank_color = "Y"
                elif color == "Red":
                    rank_color = "R"
                break  # Stop once the rank fits into a range
        
        if rank_color:
            # Update the rank_color field in the Student Results doctype
            frappe.db.set_value('Student Results', result_name, 'rank_color', rank_color)

    return {'message': 'Colors assigned successfully'}
