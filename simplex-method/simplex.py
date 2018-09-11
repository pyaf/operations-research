import numpy as np
import pdb
from data import data
from utils import print_table, print_vars, canonicalize, \
    update_basis, update_vars, final_print

a = np.asarray(data["a"], dtype="float")  # contraint coefficients
b = np.asarray(data["b"], dtype="float")  # value of constraints
c = np.asarray(data["c"], dtype="float")  # objective function coefficients
n = data["num_of_variables"]
n_slack_vars = data["num_of_slack_variables"]
m = data["num_of_constraints"]

# define variables
vars = {}
for i in range(1, n + 1):
    vars["x" + str(i)] = None

# basis = collection of basic variables (non-zero)
basis = []
for i in range(n - n_slack_vars + 1, n + 1):
    basis.append("x" + str(i))

# initial feasible basic solution
# slack variables are basic variables
# decision variables are non-basic varialbles
for i in range(1, n - n_slack_vars + 1):
    vars["x" + str(i)] = 0.0

for i, j in enumerate(range(n - n_slack_vars + 1, n + 1)):
    vars["x" + str(j)] = b[i, 0]

# check if initial solution is feasible or not!
for key in vars:
    if vars[key] < 0:
        print("Non feasible initial solution found")
        exit()

print("\nInitial feasible basic solution: ")
print_vars(vars)
s = np.argmin(c)  # idx of min cost coefficient
r = print_table(a, b, c, s, basis, vars)  # the idx min b/a value

i = 1

while True:
    input()
    print("\nIteration number : %d" % i)
    # we have pivot element at coordinates = [r, s], we need to modify `basis`
    # a basis variable will be converted into non-basis variable.
    basis = update_basis(a, basis, r, s)
    # get the table in canonical form
    a, b, c = canonicalize(a, b, c, r, s)
    # evaluate variables
    vars = update_vars(a, b, vars, basis)
    s = np.argmin(c)  # idx of min cost coefficient
    r = print_table(a, b, c, s, basis, vars)  # the idx min b/a value

    # check if any non basic variable's cost coeff has become zero
    # if yes, then infinite solutions are possible
    for var in vars:
        if var not in basis:  # non basic variable
            if c[int(var[-1]) - 1] == 0:
                print("Cost coeff corresponding to " + var + " is zero, \
                     which is a non basic variable.")
                final_print("Infinite Solutions possible")
                exit()

    if np.min(c) >= 0:  # all cost coefficients are positive
        final_print("Optimal solution reached.")
        print_vars(vars)
        exit()

    if np.min(np.amax(a, axis=0)) <= 0:  # if any column is all negative
        final_print("Solution out of bounds.")
        exit()

    print("Solution for this iteration:")
    print_vars(vars)
    i += 1
