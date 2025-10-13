def find_best_score(scores, pars):
    best_score = 100
    holes = len(scores)

    if len(scores) == 0 or len(pars) == 0 or len(scores) != len(pars):
        return "Invalid data."
    for score in scores:
        if type(score) != int or score <= 0:
            return "Invalid data."
    for par in pars:
        if type(par) != int or par <= 0:
            return "Invalid data."


    for hole in range(holes):
        over_under = scores[hole] - pars[hole]
        if over_under <= best_score:
            best_score = over_under

    return best_score       


def find_best_holes(scores, pars, best_score):
    holes = len(scores)
    best_score = find_best_score(scores, pars)
    if type(best_score) == str:
        return "Invalid data."
    best_holes = []
    
    for hole in range(holes):
        score = scores[hole] - pars[hole]
        if score == best_score:
            hole_num = hole + 1
            best_holes.append(hole_num)
    return best_holes

def display_best_score_and_holes(scores, pars):
    best_score = find_best_score(scores, pars)
    if type(best_score) == str:
        print("Invalid data.")
        return
    best_holes = find_best_holes(scores, pars, best_score)

    if best_score < 0:
        scr = best_score * -1
        print(f"Best score: {scr} under par")
    elif best_score == 0:
        print("Best score: par")
    else:
        print(f"Best score: {best_score} over par")

    print(f"Scored on the following holes: {best_holes}")
'''
Begin Test Cases
'''

"""
# Test case <<N>>: 
# Expected output: <<TBD>>
print("Test case <<N>>")
print(<< call the funciton! >>)
"""
# Test case 1: Empty lists
# Expected output: "Invalid data."
print("\nTest case 1")
player_scores = []
course_pars = []
display_best_score_and_holes(player_scores, course_pars)

# Test case 2: Unequal length lists
# Expected output: "Invalid data."
print("\nTest case 2")
player_scores = [4, 5, 6]
course_pars = [3, 4]
display_best_score_and_holes(player_scores, course_pars)

# Test case 3: Non-integer values
# Expected output: "Invalid data."
print("\nTest case 3")
player_scores = [4, '5', 6, 7]
course_pars = [3, 4, 5, 4]
display_best_score_and_holes(player_scores, course_pars)

# Test case 4: Negative/0 integer score
# Expected output: "Invalid data."
print("\nTest case 4")
player_scores = [-2, 0, 1, 4, 5]
course_pars = [3, 3, 3, 3, 3]
display_best_score_and_holes(player_scores, course_pars)

# Test case 5: Perfect par round
# Expected output: "Best score: par" and holes listed
print("\nTest case 5")
player_scores = [3, 4, 5, 3, 4, 5]
course_pars = [3, 4, 5, 3, 4, 5]
display_best_score_and_holes(player_scores, course_pars)
