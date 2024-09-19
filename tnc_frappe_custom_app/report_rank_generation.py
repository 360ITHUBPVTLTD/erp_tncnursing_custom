

########################################### Below is to Generate the Ranks and assign the colors #################################

import frappe

@frappe.whitelist()
def generate_ranks(docname, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank, actual_candidates, green_end, yellow_end):
    try:
        print(docname)  # Pediatric Prelims Exam   ## TNC-EXM-00045 

        exam_title_name = frappe.get_value('Student Exam', {'name': docname}, 'name')

        if not exam_title_name:
            return {"status": "error", "message": "Exam not found with the given document name"}

        student_exam_doc = frappe.get_doc('Student Exam', exam_title_name)
        if student_exam_doc.lock_ranks:
            return {"status": "error", "message": "The ranks for the Exam are locked. Please contact admin to unlock them"}

        try:
            # Convert string inputs to integers
            start_rank = int(start_rank)
            initial_regularised_ranks = int(initial_regularised_ranks)
            last_regularised_ranks = int(last_regularised_ranks)
            last_rank = int(last_rank)
            actual_candidates = int(actual_candidates)
        except ValueError:
            return {"status": "error", "message": "Invalid input values. Please enter valid integers"}

        # Rank calculation logic
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

            if ranks[-1] != last_rank:
                ranks.append(last_rank)

            return ranks

        ranks = get_step_size(actual_candidates, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank)

        if isinstance(ranks, str):
            return {"status": "error", "message": ranks}

        students = frappe.get_all('Student Results', filters={'batch_id': docname}, fields=['name', 'percentage'], order_by='percentage desc')

        if not students:
            return {"status": "error", "message": "No students found to generate ranks"}

        if len(students) != len(ranks):
            return {"status": "error", "message": "Mismatch between the number of students and calculated ranks"}

        # Assign ranks to students
        for i in range(len(students)):
            frappe.db.set_value('Student Results', students[i]['name'], 'rank', ranks[i])

        frappe.db.set_value('Student Exam', exam_title_name, {
            'status': 'Rank Generated(step1)',
            'start_rank': start_rank,
            'last_rank': last_rank,
            'initial_regularised_ranks': initial_regularised_ranks,
            'actual_candidates': actual_candidates,
        })
        frappe.db.commit()

        # Call to assign colors
        color_assign_status = assign_colors(docname, green_end, yellow_end)
        if color_assign_status.get("status") == "error":
            return {"status": "error", "message": color_assign_status.get("message")}

        return {"status": "success", "message": "Ranks and colors assigned successfully"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in Rank Generation")
        return {"status": "error", "message": "An error occurred during rank generation. Please contact support", "error_details": str(e)}


@frappe.whitelist()
def assign_colors(docname, green_end, yellow_end):
    try:
        exam_doc = frappe.get_doc('Student Exam', docname)

        # Assign color ranges
        exam_doc.green_starts_from = 0
        exam_doc.yellow_starts_from = int(green_end) + 1
        exam_doc.red_starts_from = int(yellow_end) + 1
        exam_doc.green_ends_to = int(green_end)
        exam_doc.yellow_ends_to = int(yellow_end)
        exam_doc.red_ends_to = 100

        exam_doc.save()

        total_students = float(exam_doc.last_rank)
        green_end = int(total_students * (exam_doc.green_ends_to / 100))
        yellow_end = int(total_students * (exam_doc.yellow_ends_to / 100))

        student_results = frappe.get_all('Student Results', filters={'batch_id': docname}, fields=['name', 'rank'], order_by='rank asc')

        for student_result in student_results:
            if student_result.rank <= green_end:
                frappe.db.set_value('Student Results', student_result.name, 'rank_color', 'G')
            elif student_result.rank <= yellow_end:
                frappe.db.set_value('Student Results', student_result.name, 'rank_color', 'Y')
            else:
                frappe.db.set_value('Student Results', student_result.name, 'rank_color', 'R')

        exam_doc.colors_assigned = 1  # Set colors assigned flag
        exam_doc.save()
        frappe.db.commit()

        return {"status": "success", "message": "Colors assigned successfully"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"Error in Color assignment for Exam: {docname}")
        return {"status": "error", "message": "An error occurred during color assignment. Please contact support", "error_details": str(e)}



################################################ Rank reseting to 0 ######################################################

@frappe.whitelist()
def reset_ranks(exam_title_name):

    # print(exam_title_name)  ##TNC-EXM-00047

    # Fetch all records where exam_title_name matches
    student_results = frappe.get_all(
        "Student Results",
        filters={"batch_id": exam_title_name},
        fields=["name"]
    )
    exam_title_name = frappe.get_value('Student Exam', {'name': exam_title_name}, 'name')

    student_exam_doc = frappe.get_doc('Student Exam', exam_title_name)
    if student_exam_doc.lock_ranks:
        return{"status": "The ranks for the Exam are locked, please contact admin to unlock them"}

    
    # Loop through each record and set the rank to a default value, e.g., 0
    for result in student_results:
        frappe.db.set_value("Student Results", result.name, "rank", 0)

    # Update the status in the Student Exam doctype
    frappe.db.set_value("Student Exam", {"name": exam_title_name}, "status", "Rank Reset")
    
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
    print(exam_title_name)  ## TNC-EXM-00045

    # Fetch the Student Exam document using get_doc
    student_exam = frappe.get_all('Student Exam',
                                  filters={'name': exam_title_name},
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







################### It is new readjust ranks from the in the reports based on the columns in reports #########################################################


import frappe

@frappe.whitelist()
def readjust_ranks(docname, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank, actual_candidates, green_end, yellow_end):
    try:
        # Fetch the exam title name
        exam_title_name = frappe.get_value('Student Exam', {'name': docname}, 'name')
        if not exam_title_name:
            return {"status": "No exam title found"}

        student_exam_doc = frappe.get_doc('Student Exam', exam_title_name)
        if student_exam_doc.lock_ranks:
            return {"status": "The ranks for the Exam are locked, please contact admin to unlock them"}

        # Validate and convert input values
        try:
            start_rank = int(start_rank)
            initial_regularised_ranks = int(initial_regularised_ranks)
            last_regularised_ranks = int(last_regularised_ranks)
            last_rank = int(last_rank)
            actual_candidates = int(actual_candidates)
            from_regularization = int(actual_candidates) - int(last_regularised_ranks) + 1
        except ValueError:
            return {"message": "Invalid input values, please provide proper numerical values"}

        # Function to generate the ranks
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

            for i in range(last_regularised_ranks-1, 0, -1):
                ranks.append(last_rank - i)

            if ranks[-1] != last_rank:
                ranks.append(last_rank)

            return ranks

        # Generate ranks
        ranks = get_step_size(actual_candidates, start_rank, initial_regularised_ranks, last_regularised_ranks, last_rank)
        if isinstance(ranks, str):
            return {"message": ranks}  # Handle validation errors from get_step_size

        # Fetch students and validate
        students = frappe.get_all('Student Results', filters={'batch_id': docname}, fields=['name', 'percentage'], order_by='percentage desc')
        if not students:
            return {"message": "No Students are available to generate the ranks"}

        if len(students) != len(ranks):
            return {"message": "Mismatch between the number of students and calculated ranks"}

        # Update student ranks
        for i in range(len(students)):
            frappe.db.set_value('Student Results', students[i]['name'], 'rank', ranks[i])

        # Update exam status and last regularised ranks
        frappe.db.set_value('Student Exam', exam_title_name, {
            'status': 'Rank Generated(step2)',
            'last_regularised_ranks': from_regularization
        })
        frappe.db.commit()

        # Call the assign_colors function
        try:
            assign_colors(docname, green_end, yellow_end)
        except Exception as e:
            frappe.log_error(f"Error during color assignment: {str(e)}", "Rank Readjustment")
            return {"message": "Rank readjustment completed, but color assignment failed. Please contact support."}

        return {"message": "Readjusted ranks and colors successfully"}

    except Exception as e:
        frappe.log_error(f"Error during rank readjustment: {str(e)}", "Rank Readjustment")
        return {"message": "Failed to readjust ranks. Please try again or contact support."}

