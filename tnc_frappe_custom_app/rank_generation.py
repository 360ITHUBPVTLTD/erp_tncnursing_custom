


################################# Below code is working good and it can able to reassign the ranks(Final code ) #################################
# import frappe

# @frappe.whitelist()
# def generate_ranks(docname, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank, actual_candidates):
#     # Validate input
#     try:
#         start_rank = int(start_rank)
#         initial_regularised_ranks = int(initial_regularised_ranks)
#         last_regularised_ranks = int(last_regularised_ranks)
#         last_rank = int(last_rank)
#         actual_candidates = int(actual_candidates)
#     except ValueError:
#         return {"message": "Invalid input values"}

#     # Function to calculate ranks
#     def get_step_size(actual_candidates, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank):
#         if (last_rank - start_rank) < actual_candidates:
#             return "Actual number of candidates should be equal or more than the Rank Range"
#         if (initial_regularised_ranks + last_regularised_ranks) > (last_rank - start_rank):
#             return "Sum of Regularised Ranks should be less than Rank Range"
        
#         ranks = []
#         for i in range(initial_regularised_ranks):
#             ranks.append(start_rank + i)
        
#         starting_rank_after_regularised_ranks = start_rank + initial_regularised_ranks
#         last_rank_after_regularised_ranks = last_rank - last_regularised_ranks
#         balance_candidates_to_be_set_in_unregularised_rank_range = actual_candidates - (initial_regularised_ranks + last_regularised_ranks)
#         gap = (last_rank_after_regularised_ranks - starting_rank_after_regularised_ranks) / balance_candidates_to_be_set_in_unregularised_rank_range
        
#         step1 = int(gap)
#         if step1 != gap:
#             step2 = step1 + 1
#             extra_ranks = (last_rank_after_regularised_ranks - starting_rank_after_regularised_ranks) - (balance_candidates_to_be_set_in_unregularised_rank_range * int(step1))
#             for i in range(balance_candidates_to_be_set_in_unregularised_rank_range - extra_ranks):
#                 ranks.append(ranks[-1] + step1)
#             for i in range(extra_ranks):
#                 ranks.append(ranks[-1] + step2)
#         else:
#             for i in range(balance_candidates_to_be_set_in_unregularised_rank_range):
#                 ranks.append(ranks[-1] + step1)

#         for i in range(last_regularised_ranks - 1, -1, -1):
#             ranks.append(last_rank - i)
        
#         return ranks

#     ranks = get_step_size(actual_candidates, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank)
    
#     if isinstance(ranks, str):
#         return {"message": ranks}
    
#     # Fetch all students filtered by batch_id, sorted by percentage in descending order
#     students = frappe.get_all('Student Results', 
#                               filters={'batch_id': docname}, 
#                               fields=['name', 'percentage'], 
#                               order_by='percentage desc')

#     # Ensure that the number of students matches the number of calculated ranks
#     if len(students) != len(ranks):
#         return {"message": "Mismatch between number of students and calculated ranks"}
    
#     # Clear existing ranks
#     frappe.db.sql('UPDATE `tabStudent Results` SET rank = NULL WHERE rank IS NOT NULL')
    
#     # Assign ranks
#     for student in range(len(list(students))):
#         print(students[student], ranks[student])
#         # frappe.db.set_value('Student Results', student['name'], 'rank',)
    
#     return {"message": "Ranks successfully assigned to students."}




################################ Below is the FInal code for Rank Generation #################################

# import frappe

# @frappe.whitelist()
# def generate_ranks(docname, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank, actual_candidates):
#     # Validate input
#     try:
#         start_rank = int(start_rank)
#         initial_regularised_ranks = int(initial_regularised_ranks)
#         last_regularised_ranks = int(last_regularised_ranks)
#         last_rank = int(last_rank)
#         actual_candidates = int(actual_candidates)
#     except ValueError:
#         return {"message": "Invalid input values"}

#     # Function to calculate ranks
#     def get_step_size(actual_candidates, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank):
#         if (last_rank - start_rank) < actual_candidates:
#             return "Actual number of candidates should be equal or more than the Rank Range"
#         if (initial_regularised_ranks + last_regularised_ranks) > (last_rank - start_rank):
#             return "Sum of Regularised Ranks should be less than Rank Range"
        
#         ranks = []
#         for i in range(initial_regularised_ranks):
#             ranks.append(start_rank + i)
        
#         starting_rank_after_regularised_ranks = start_rank + initial_regularised_ranks
#         last_rank_after_regularised_ranks = last_rank - last_regularised_ranks
#         balance_candidates_to_be_set_in_unregularised_rank_range = actual_candidates - (initial_regularised_ranks + last_regularised_ranks)
#         gap = (last_rank_after_regularised_ranks - starting_rank_after_regularised_ranks) / balance_candidates_to_be_set_in_unregularised_rank_range
        
#         step1 = int(gap)
#         if step1 != gap:
#             step2 = step1 + 1
#             extra_ranks = (last_rank_after_regularised_ranks - starting_rank_after_regularised_ranks) - (balance_candidates_to_be_set_in_unregularised_rank_range * int(step1))
#             for i in range(balance_candidates_to_be_set_in_unregularised_rank_range - extra_ranks):
#                 ranks.append(ranks[-1] + step1)
#             for i in range(extra_ranks):
#                 ranks.append(ranks[-1] + step2)
#         else:
#             for i in range(balance_candidates_to_be_set_in_unregularised_rank_range):
#                 ranks.append(ranks[-1] + step1)

#         for i in range(last_regularised_ranks - 1, -1, -1):
#             ranks.append(last_rank - i)
        
#         return ranks

#     ranks = get_step_size(actual_candidates, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank)
    
#     if isinstance(ranks, str):
#         return {"message": ranks}
    
#     # Fetch all students filtered by batch_id, sorted by percentage in descending order
#     students = frappe.get_all('Student Results', 
#                               filters={'batch_id': docname}, 
#                               fields=['name', 'percentage'], 
#                               order_by='percentage desc')

#     # Ensure that the number of students matches the number of calculated ranks
#     if len(students) != len(ranks):
#         return {"message": "Mismatch between number of students and calculated ranks"}
    
#     # Clear existing ranks
#     # frappe.db.sql('UPDATE `tabStudent Results` SET rank = NULL WHERE rank IS NOT NULL')
    
#     # Assign ranks
#     for i in range(len(students)):
#         student_name = students[i]['name']
#         rank = ranks[i]
#         # print(f"Assigning rank {rank} to student {student_name} with percentage {students[i]['percentage']}")
#         frappe.db.set_value('Student Results', student_name, 'rank', rank)
    
#     return {"message": "Ranks successfully assigned to students."}


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
    
    # Fetch all students filtered by batch_id, sorted by percentage in descending order
    students = frappe.get_all('Student Results', 
                              filters={'batch_id': docname}, 
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


################# Below code is for generating the ranks it is making unchek the imported field in Student Master Data doctype #################################################################

# import frappe

# @frappe.whitelist()
# def generate_ranks(start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank, actual_candidates):
#     # Validate input
#     try:
#         start_rank = int(start_rank)
#         initial_regularised_ranks = int(initial_regularised_ranks)
#         last_regularised_ranks = int(last_regularised_ranks)
#         last_rank = int(last_rank)
#         actual_candidates = int(actual_candidates)
#     except ValueError:
#         return {"message": "Invalid input values"}

#     # Function to calculate ranks
#     def get_step_size(actual_candidates, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank):
#         if (last_rank - start_rank) < actual_candidates:
#             return "Actual number of candidates should be equal or more than the Rank Range"
#         if (initial_regularised_ranks + last_regularised_ranks) > (last_rank - start_rank):
#             return "Sum of Regularised Ranks should be less than Rank Range"
        
#         ranks = []
#         for i in range(initial_regularised_ranks):
#             ranks.append(start_rank + i)
        
#         starting_rank_after_regularised_ranks = start_rank + initial_regularised_ranks
#         last_rank_after_regularised_ranks = last_rank - last_regularised_ranks
#         balance_candidates_to_be_set_in_unregularised_rank_range = actual_candidates - (initial_regularised_ranks + last_regularised_ranks)
#         gap = (last_rank_after_regularised_ranks - starting_rank_after_regularised_ranks) / balance_candidates_to_be_set_in_unregularised_rank_range
        
#         step1 = int(gap)
#         if step1 != gap:
#             step2 = step1 + 1
#             extra_ranks = (last_rank_after_regularised_ranks - starting_rank_after_regularised_ranks) - (balance_candidates_to_be_set_in_unregularised_rank_range * int(step1))
#             for i in range(balance_candidates_to_be_set_in_unregularised_rank_range - extra_ranks):
#                 ranks.append(ranks[-1] + step1)
#             for i in range(extra_ranks):
#                 ranks.append(ranks[-1] + step2)
#         else:
#             for i in range(balance_candidates_to_be_set_in_unregularised_rank_range):
#                 ranks.append(ranks[-1] + step1)

#         for i in range(last_regularised_ranks - 1, -1, -1):
#             ranks.append(last_rank - i)
        
#         return ranks

#     ranks = get_step_size(actual_candidates, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank)
    
#     if isinstance(ranks, str):
#         return {"message": ranks}
    
#     # Fetch all students, regardless of their current rank
#     students = frappe.get_all('Students Master Data', fields=['name', 'percentage'])

#     # Ensure that the number of students matches the number of calculated ranks
#     if len(students) != len(ranks):
#         return {"message": "Mismatch between number of students and calculated ranks"}
    
#     # Sort students by percentage
#     students = sorted(students, key=lambda x: x['percentage'], reverse=True)
    
#     # Clear existing ranks
#     frappe.db.sql('UPDATE `tabStudents Master Data` SET rank = NULL WHERE rank IS NOT NULL')

#     # Assign ranks and reset the 'imported' field to 0
#     for student, rank in zip(students, ranks):
#         frappe.db.set_value('Students Master Data', student['name'], 'rank', rank)
#         frappe.db.set_value('Students Master Data', student['name'], 'imported', 0)  # Reset 'imported' to 0
    
#     return {"message": "Ranks successfully assigned to students and 'imported' field reset to 0."}


