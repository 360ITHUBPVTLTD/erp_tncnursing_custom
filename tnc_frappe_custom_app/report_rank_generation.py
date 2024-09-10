

########################################### Below is including the Last Rank  #################################


import frappe

@frappe.whitelist()
def generate_ranks(docname, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank, actual_candidates):
    print(docname)  # Pediatric Prelims Exam

    exam_title_name = frappe.get_value('Student Exam', {'exam_title_name': docname}, 'name')

    if not exam_title_name:
        # If no exam_title_name found, return an error message
        return {"status": "no_exam_title_name"}

    try:
        start_rank = int(start_rank)
        initial_regularised_ranks = int(initial_regularised_ranks)
        last_regularised_ranks = int(last_regularised_ranks)
        last_rank = int(last_rank)
        actual_candidates = int(actual_candidates)
    except ValueError:
        return {"message": "Invalid input values"}

    def get_step_size(actual_candidates, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank):
        if (last_rank - start_rank + 1) < actual_candidates:
            return "Actual number of candidates should be equal or more than the Rank Range"
        if (initial_regularised_ranks + last_regularised_ranks) > (last_rank - start_rank + 1):
            return "Sum of Regularised Ranks should be less than Rank Range"

        ranks = []
        for i in range(initial_regularised_ranks):
            ranks.append(start_rank + i)

        starting_rank_after_regularised_ranks = start_rank + initial_regularised_ranks
        last_rank_after_regularised_ranks = last_rank - last_regularised_ranks + 1
        balance_candidates_to_be_set_in_unregularised_rank_range = actual_candidates - (initial_regularised_ranks + last_regularised_ranks)
        gap = (last_rank_after_regularised_ranks - starting_rank_after_regularised_ranks) / balance_candidates_to_be_set_in_unregularised_rank_range

        step1 = int(gap)
        if step1 != gap:
            step2 = step1 + 1
            extra_ranks = (last_rank_after_regularised_ranks - starting_rank_after_regularised_ranks) - (balance_candidates_to_be_set_in_unregularised_rank_range * step1)
            for i in range(balance_candidates_to_be_set_in_unregularised_rank_range - extra_ranks):
                ranks.append(ranks[-1] + step1)
            for i in range(extra_ranks):
                ranks.append(ranks[-1] + step2)
        else:
            for i in range(balance_candidates_to_be_set_in_unregularised_rank_range):
                ranks.append(ranks[-1] + step1)

        for i in range(last_regularised_ranks):
            ranks.append(last_rank - i)

        # Ensure the last rank is included
        if ranks[-1] != last_rank:
            ranks.append(last_rank)

        return ranks

    ranks = get_step_size(actual_candidates, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank)
    print(f"Calculated Ranks: {ranks}")

    if isinstance(ranks, str):
        return {"message": ranks}

    students = frappe.get_all('Student Results', 
                              filters={'exam_title_name': docname}, 
                              fields=['name', 'percentage'], 
                              order_by='percentage desc')

    if not students:
        return {"message": "No Students are there to Generate the Ranks"}

    if len(students) != len(ranks):

        return {"message": "Mismatch between number of students and calculated ranks"}

    for i in range(len(students)):
        frappe.db.set_value('Student Results', students[i]['name'], 'rank', ranks[i])

    # frappe.db.set_value('Student Exam', exam_title_name, 'status', 'Rank Generated(step1)')
    frappe.db.set_value('Student Exam', exam_title_name, {
    'status': 'Rank Generated(step1)',
    'start_rank': start_rank,  # Add other fields as needed
    'last_rank': last_rank,
    'initial_regularised_ranks': initial_regularised_ranks,
    'actual_candidates': actual_candidates
})
    print(len(students)) ## 19
    print(len(ranks)) ## 19

    frappe.db.commit()

    return {"message": "Ranks Generated successfully"}



################### Below code is having all the validations while generating Ranks and including Last Rank also ###########


# import frappe

# @frappe.whitelist()
# def generate_ranks(docname, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank, actual_candidates):
#     print(docname)  # Pediatric Prelims Exam

#     exam_title_name = frappe.get_value('Student Exam', {'exam_title_name': docname}, 'name')

#     if not exam_title_name:
#         # If no exam_title_name found, return an error message
#         return {"status": "no_exam_title_name"}

#     try:
#         start_rank = int(start_rank)
#         initial_regularised_ranks = int(initial_regularised_ranks)
#         last_regularised_ranks = int(last_regularised_ranks)
#         last_rank = int(last_rank)
#         actual_candidates = int(actual_candidates)
#     except ValueError:
#         return {"message": "Invalid input values"}

#     # Validation logic
#     if not (start_rank < last_rank):
#         return {"message": "Start Rank must be less than Last Rank"}
    
#     # if not (initial_regularised_ranks < last_regularised_ranks < last_rank):
#     #     return {"message": "Initial Regularised Ranks must be less than Last Regularised Ranks and Last Rank"}
    
#     if not ((initial_regularised_ranks + last_regularised_ranks) < (last_rank - start_rank)):
#         return {"message": "Sum of Initial and Last Regularised Ranks must be less than the difference between Last Rank and Start Rank"}

#     def get_step_size(actual_candidates, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank):
#         if (last_rank - start_rank + 1) < actual_candidates:
#             return "Actual number of candidates should be equal or more than the Rank Range"
#         if (initial_regularised_ranks + last_regularised_ranks) > (last_rank - start_rank + 1):
#             return "Sum of Regularised Ranks should be less than Rank Range"

#         ranks = []
#         for i in range(initial_regularised_ranks):
#             ranks.append(start_rank + i)

#         starting_rank_after_regularised_ranks = start_rank + initial_regularised_ranks
#         last_rank_after_regularised_ranks = last_rank - last_regularised_ranks + 1
#         balance_candidates_to_be_set_in_unregularised_rank_range = actual_candidates - (initial_regularised_ranks + last_regularised_ranks)
#         gap = (last_rank_after_regularised_ranks - starting_rank_after_regularised_ranks) / balance_candidates_to_be_set_in_unregularised_rank_range

#         step1 = int(gap)
#         if step1 != gap:
#             step2 = step1 + 1
#             extra_ranks = (last_rank_after_regularised_ranks - starting_rank_after_regularised_ranks) - (balance_candidates_to_be_set_in_unregularised_rank_range * step1)
#             for i in range(balance_candidates_to_be_set_in_unregularised_rank_range - extra_ranks):
#                 ranks.append(ranks[-1] + step1)
#             for i in range(extra_ranks):
#                 ranks.append(ranks[-1] + step2)
#         else:
#             for i in range(balance_candidates_to_be_set_in_unregularised_rank_range):
#                 ranks.append(ranks[-1] + step1)

#         for i in range(last_regularised_ranks):
#             ranks.append(last_rank - i)

#         # Ensure the last rank is included
#         if ranks[-1] != last_rank:
#             ranks.append(last_rank)

#         return ranks

#     ranks = get_step_size(actual_candidates, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank)

#     if isinstance(ranks, str):
#         return {"message": ranks}

#     students = frappe.get_all('Student Results', 
#                               filters={'exam_title_name': docname}, 
#                               fields=['name', 'percentage'], 
#                               order_by='percentage desc')

#     if not students:
#         return {"message": "No Students are there to Generate the Ranks"}

#     if len(students) != len(ranks):
#         return {"message": "Mismatch between number of students and calculated ranks"}

#     for i in range(len(students)):
#         frappe.db.set_value('Student Results', students[i]['name'], 'rank', ranks[i])

#     frappe.db.set_value('Student Exam', exam_title_name, {
#         'status': 'Rank Generated(step1)',
#         'start_rank': start_rank,  # Add other fields as needed
#         'last_rank': last_rank,
#         'initial_regularised_ranks': initial_regularised_ranks,
#         'actual_candidates': actual_candidates
#     })

#     frappe.db.commit()

#     return {"message": "Ranks Generated successfully"}


################################################ Rank reseting to 0 ######################################################

@frappe.whitelist()
def reset_ranks(exam_title_name):
    # Fetch all records where exam_title_name matches
    student_results = frappe.get_all(
        "Student Results",
        filters={"exam_title_name": exam_title_name},
        fields=["name"]
    )
    
    # Loop through each record and set the rank to a default value, e.g., 0
    for result in student_results:
        frappe.db.set_value("Student Results", result.name, "rank", 0)

    # Update the status in the Student Exam doctype
    frappe.db.set_value("Student Exam", {"exam_title_name": exam_title_name}, "status", "Rank Reset")
    
    # Commit the changes to the database
    frappe.db.commit()
    
    return {"status": "success"}



# import frappe

# @frappe.whitelist()
# def check_ranks_generated(exam_title_name):
#     # Fetch the status from Student Exam doctype where the exam_title_name matches
    
    
#     # Get the status from the Student Exam doctype
#     exam_status = frappe.get_value('Student Exam', 
#                                    filters={'exam_title_name': exam_title_name}, 
#                                    fieldname='status')
#     print(exam_status)
#     # Return status based on the value of the status field
#     if exam_status == 'Rank Generated(step1)':
#         # print(exam_title_name)
#         return {"status": "generated"}
    
#     return {"status": "not_generated"}






################## Below code is by clicking on the Readjust Ranks button the prompt take all the values when we generate the Generate Rank Buttons #################

import frappe

@frappe.whitelist()
def get_rank_details(exam_title_name):
    # Fetch the Student Exam document using get_doc
    student_exam = frappe.get_all('Student Exam',
                                  filters={'exam_title_name': exam_title_name},
                                  fields=['start_rank', 'last_rank', 'initial_regularised_ranks', 'actual_candidates', 'last_regularised_ranks'],
                                  limit=1)

    if not student_exam:
        return {"message": "No rank details found for the given exam title"}

    # Since get_all returns a list, get the first element
    student_exam = student_exam[0]

    # Return the values needed for the prompt
    return {
        "start_rank": student_exam.get('start_rank'),
        "last_rank": student_exam.get('last_rank'),
        "initial_regularised_ranks": student_exam.get('initial_regularised_ranks'),
        "actual_candidates": student_exam.get('actual_candidates'),
        "last_regularised_ranks": student_exam.get('last_regularised_ranks')
    }






############################################### BElow is the Readjust Ranks Final CODE #####################################

# import frappe

# @frappe.whitelist()
# def readjust_ranks(docname, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank, actual_candidates):
#     print(f"Docname: {docname}")
#     print(f"Start Rank: {start_rank}")
#     print(f"Initial Regularised Ranks: {initial_regularised_ranks}")
#     print(f"Last Regularised Ranks: {last_regularised_ranks}")
#     print(f"Last Rank: {last_rank}")
#     print(f"Actual Candidates: {actual_candidates}")

#     from_regularization = int(actual_candidates) - int(last_regularised_ranks) + 1 


    


#     # Validate and convert input values
#     try:
#         start_rank = int(start_rank)
#         initial_regularised_ranks = int(initial_regularised_ranks)
#         last_regularised_ranks = int(last_regularised_ranks)
#         last_rank = int(last_rank)
#         actual_candidates = int(actual_candidates)
#     except ValueError:
#         return {"message": "Invalid input values"}

#     # Fetch the exam title name
#     exam_title_name = frappe.get_value('Student Exam', {'exam_title_name': docname}, 'name')
#     if not exam_title_name:
#         return {"status": "no_exam_title_name"}

#     # Define the function to calculate ranks (Your original code)
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
#             extra_ranks = (last_rank_after_regularised_ranks - starting_rank_after_regularised_ranks) - (
#                     balance_candidates_to_be_set_in_unregularised_rank_range * int(step1))
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

#     # Generate ranks
#     ranks = get_step_size(actual_candidates, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank)
#     print(f"Calculated Ranks: {ranks}")

#     if isinstance(ranks, str):
#         # Handle error messages returned by get_step_size
#         return {"message": ranks}

#     # Fetch students and validate
#     students = frappe.get_all('Student Results', filters={'exam_title_name': docname}, fields=['name', 'percentage'], order_by='percentage desc')
#     print(f"Number of Students: {len(students)}")

#     if not students:
#         return {"message": "No Students are there to Generate the Ranks"}

#     if len(students) != len(ranks):
#         print(len(students))
#         print(len(ranks))
#         return {"message": "Mismatch between number of students and calculated ranks"}

#     # Update student ranks
#     for i in range(len(students)):
#         frappe.db.set_value('Student Results', students[i]['name'], 'rank', ranks[i])

#     # Update exam status
#     # Update exam status and last regularised ranks
#     frappe.db.set_value('Student Exam', exam_title_name, {
#     'status': 'Rank Generated(step2)',
#     'last_regularised_ranks': last_regularised_ranks
# })
#     frappe.db.commit()

#     return {"message": "Readjust Ranks are Generated successfully"}












################### It is new readjust ranks from the in the reports based on the columns in reports #########################################################


import frappe

@frappe.whitelist()
def readjust_ranks(docname, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank, actual_candidates):
    print(f"Docname: {docname}")
    print(f"Start Rank: {start_rank}")
    print(f"Initial Regularised Ranks: {initial_regularised_ranks}")
    print(f"Last Regularised Ranks: {last_regularised_ranks}")
    print(f"Last Rank: {last_rank}")
    print(f"Actual Candidates: {actual_candidates}")

    from_regularization = int(actual_candidates) - int(last_regularised_ranks) + 1 


    


    # Validate and convert input values
    try:
        start_rank = int(start_rank)
        initial_regularised_ranks = int(initial_regularised_ranks)
        # last_regularised_ranks = int(last_regularised_ranks)
        last_rank = int(last_rank)
        actual_candidates = int(actual_candidates)
        from_regularization = int(actual_candidates) - int(last_regularised_ranks) + 1 
    except ValueError:
        return {"message": "Invalid input values"}

    # Fetch the exam title name
    exam_title_name = frappe.get_value('Student Exam', {'exam_title_name': docname}, 'name')
    if not exam_title_name:
        return {"status": "no_exam_title_name"}

    # Define the function to calculate ranks (Your original code)
    def get_step_size(actual_candidates, start_rank, initial_regularised_ranks, from_regularization, last_rank):
        if (last_rank - start_rank) < actual_candidates:
            return "Actual number of candidates should be equal or more than the Rank Range"
        if (initial_regularised_ranks + from_regularization) > (last_rank - start_rank):
            return "Sum of Regularised Ranks should be less than Rank Range"

        ranks = []
        for i in range(initial_regularised_ranks):
            ranks.append(start_rank + i)

        starting_rank_after_regularised_ranks = start_rank + initial_regularised_ranks
        last_rank_after_regularised_ranks = last_rank - from_regularization
        balance_candidates_to_be_set_in_unregularised_rank_range = actual_candidates - (initial_regularised_ranks + from_regularization)
        gap = (last_rank_after_regularised_ranks - starting_rank_after_regularised_ranks) / balance_candidates_to_be_set_in_unregularised_rank_range
        step1 = int(gap)

        if step1 != gap:
            step2 = step1 + 1
            extra_ranks = (last_rank_after_regularised_ranks - starting_rank_after_regularised_ranks) - (
                    balance_candidates_to_be_set_in_unregularised_rank_range * int(step1))
            for i in range(balance_candidates_to_be_set_in_unregularised_rank_range - extra_ranks):
                ranks.append(ranks[-1] + step1)
            for i in range(extra_ranks):
                ranks.append(ranks[-1] + step2)
        else:
            for i in range(balance_candidates_to_be_set_in_unregularised_rank_range):
                ranks.append(ranks[-1] + step1)

        for i in range(from_regularization - 1, -1, -1):
            ranks.append(last_rank - i)

        return ranks

    # Generate ranks
    ranks = get_step_size(actual_candidates, start_rank, initial_regularised_ranks, from_regularization, last_rank)
    print(f"Calculated Ranks: {ranks}")

    if isinstance(ranks, str):
        # Handle error messages returned by get_step_size
        return {"message": ranks}

    # Fetch students and validate
    students = frappe.get_all('Student Results', filters={'exam_title_name': docname}, fields=['name', 'percentage'], order_by='percentage desc')
    print(f"Number of Students: {len(students)}")

    if not students:
        return {"message": "No Students are there to Generate the Ranks"}

    if len(students) != len(ranks):
        print(len(students))
        print(len(ranks))
        return {"message": "Mismatch between number of students and calculated ranks"}

    # Update student ranks
    for i in range(len(students)):
        frappe.db.set_value('Student Results', students[i]['name'], 'rank', ranks[i])

    # Update exam status
    # Update exam status and last regularised ranks
    frappe.db.set_value('Student Exam', exam_title_name, {
    'status': 'Rank Generated(step2)',
    'last_regularised_ranks': from_regularization
})
    frappe.db.commit()

    return {"message": "Readjust Ranks are Generated successfully"}