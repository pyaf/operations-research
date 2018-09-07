'''All notations are according to S. S. Rao's Engineering Optimization book'''
'''Please, convert all inequality constraints to equalities, add slack variables, then 
fill the value in the matrices'''

'''for a given problem:

    Minimize f = -x1 -2x2 -x3

    Subjected to:
        2x1 + x2 -x3 <= 2
        2x1 -x2 +5x3 <= 6
        4x1 + x2 + x3 <= 6

        x1,x2,x3 >= 0

    the `data` variable can be set as following: '''

data = {
    "num_of_decision_variables": 3,
    "num_of_slack_variables": 3,
    "num_of_variables": 6,
    "num_of_constraints": 3,
    "a": [
        [2, 1, -1, 1, 0, 0],
        [2, -1, 5, 0, 1, 0],
        [4, 1, 1, 0, 0, 1]
    ],
    "b": [
        [2],
        [6],
        [6],
        [0]  # for -f
    ],
    "c": [
        [-1],
        [-2],
        [-1],
        [0],
        [0],
        [0]
    ],
}

