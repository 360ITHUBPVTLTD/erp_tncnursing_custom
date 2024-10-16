


############ AUg31 code If there is no data in the Stude Results it will throw No data is there ###########
                  
import frappe

@frappe.whitelist()
def generate_ranks(docname, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank, actual_candidates):
    # Validate input
    try:
        start_rank = int(start_rank)
        initial_regularised_ranks = int(initial_regularised_ranks)
        last_regularised_ranks = int(last_regularised_ranks)
        last_rank = int(last_rank)
        actual_candidates = int(actual_candidates)
    except ValueError:
        return {"message": "Invalid input values"}

    # Function to calculate ranks
    def get_step_size(actual_candidates, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank):
        if (last_rank - start_rank) < actual_candidates:
            return "Actual number of candidates should be equal or more than the Rank Range"
        if (initial_regularised_ranks + last_regularised_ranks) > (last_rank - start_rank):
            return "Sum of Regularised Ranks should be less than Rank Range"
        
        ranks = []
        for i in range(initial_regularised_ranks):
            ranks.append(start_rank + i)
        
        starting_rank_after_regularised_ranks = start_rank + initial_regularised_ranks
        last_rank_after_regularised_ranks = last_rank - last_regularised_ranks
        balance_candidates_to_be_set_in_unregularised_rank_range = actual_candidates - (initial_regularised_ranks + last_regularised_ranks)
        gap = (last_rank_after_regularised_ranks - starting_rank_after_regularised_ranks) / balance_candidates_to_be_set_in_unregularised_rank_range
        
        step1 = int(gap)
        if step1 != gap:
            step2 = step1 + 1
            extra_ranks = (last_rank_after_regularised_ranks - starting_rank_after_regularised_ranks) - (balance_candidates_to_be_set_in_unregularised_rank_range * int(step1))
            for i in range(balance_candidates_to_be_set_in_unregularised_rank_range - extra_ranks):
                ranks.append(ranks[-1] + step1)
            for i in range(extra_ranks):
                ranks.append(ranks[-1] + step2)
        else:
            for i in range(balance_candidates_to_be_set_in_unregularised_rank_range):
                ranks.append(ranks[-1] + step1)

        for i in range(last_regularised_ranks - 1, -1, -1):
            ranks.append(last_rank - i)
        
        return ranks

    ranks = get_step_size(actual_candidates, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank)
    
    if isinstance(ranks, str):
        return {"message": ranks}
    
    # Fetch all students filtered by exam_id, sorted by percentage in descending order
    students = frappe.get_all('Student Results', 
                              filters={'exam_id': docname}, 
                              fields=['name', 'percentage'], 
                              order_by='percentage desc')

    if not students:
        return {"message": "No Students are there to Generate the Ranks"}  # Return if no students are found
    
    # Ensure that the number of students matches the number of calculated ranks
    if len(students) != len(ranks):
        return {"message": "Mismatch between number of students and calculated ranks"}
    
    # Assign ranks
    for i in range(len(students)):
        frappe.db.set_value('Student Results', students[i]['name'], 'rank', ranks[i])

    frappe.db.commit()
    
    return {"message": "Ranks Generated successfully"}




