import numpy as np
import pdb
from data import data
from utils import print_table, print_vars, canonicalize, update_basis, update_vars

a = np.asarray(data['a'], dtype='float')
b = np.asarray(data['b'], dtype='float')
c = np.asarray(data['c'], dtype='float')
n = data['num_of_variables']
n_slack_vars = data['num_of_slack_variables']
m = data['num_of_constraints']

# define variables
vars = {}
for i in range(1, n+1):
    vars["x" + str(i)] = None

# basis = collection of basic variables (non-zero)
basis = []
for i in range(n-n_slack_vars+1, n+1):
    basis.append("x" + str(i))


# initial feasible basic solution
# slack variables are basic variables, decision variables are non-basic varialbles
for i in range(1, n-n_slack_vars+1):
    vars["x" + str(i)] = 0.0

for i, j in enumerate(range(n-n_slack_vars+1, n+1)):
    vars["x" + str(j)] = b[i-1, 0]


# check if initial solution is feasible or not!
for key in vars:
    if vars[key] < 0:
        print('Non feasible initial solution found')
        exit()

print('\nInitial feasible basic solution: ')
print_vars(vars)

# find `s` such that c[s, 0] is min(c)
while True:
    cs = np.min(c)
    if cs >= 0:
        print('Optimal solution reached.')
        print_vars(vars)
        exit()

    s = np.argmin(c)
    pivot_idx = print_table(a, b, c, s, basis, vars)
    print(pivot_idx)  # remember matrix is zero indexed
    # now we have pivot element, we need to modify `basis`
    # a basis variable will be converted into non-basis variable.
    basis = update_basis(a, basis, pivot_idx, s)
    # get the table in canonical form
    a, b, c = canonicalize(a, b, c, pivot_idx, s)
    # evaluate variables
    vars = update_vars(a, b, vars, basis)
    print('Solution obtained:')
    print_vars(vars)
    # print the updated table
    print_table(a, b, c, s, basis, vars)


