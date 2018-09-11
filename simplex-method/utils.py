import pdb
import traceback
import numpy as np
from beautifultable import BeautifulTable


def evaluate_obj_fn(c, vars):
    """Evaluates objective function, takes in `c` and `var`"""
    f = sum([c[i, 0] * vars["x" + str(i + 1)] for i in range(c.shape[0])])
    return f


def calculate_b_a_ratios(a, b, c, s):
    b_a_ratios = []
    for i in range(a.shape[0]):
        ratio = b[i, 0] / a[i, s] if a[i, s] > 0 else 0
        b_a_ratios.append(ratio)
    ratio = b[i + 1, 0] / c[s, 0] if c[s, 0] > 0 else 0
    b_a_ratios.append(ratio)
    return np.array(b_a_ratios, dtype='float')


def print_table(a, b, c, s, basis, vars):
    """Beautifully prints table"""
    try:
        # pdb.set_trace()
        b_a_ratios = calculate_b_a_ratios(a, b, c, s)
        table = BeautifulTable()
        header = ["x" + str(i) for i in range(1, a.shape[1] + 1)]
        header.extend(["-f", "b", "b/a"])
        table.column_headers = ["Basic Variables"] + header
        for i in range(a.shape[0]):  # #equations
            row = [basis[i]]
            for j in range(a.shape[1]):
                row.append(a[i, j])
            _f = evaluate_obj_fn(c, vars)
            ratio = '' if b_a_ratios[i] <= 0 else b_a_ratios[i]
            row.extend([_f, b[i, 0], ratio])
            table.append_row(row)
        row = ["-f"]
        for j in range(c.shape[0]):
            row.append(c[j, 0])
        ratio = '' if b_a_ratios[-1] <= 0 else b_a_ratios[-1]
        row.extend([1, b[i + 1, 0], ratio])
        table.append_row(row)
        print(table)
        b_a_ratios[b_a_ratios <= 0] = 'inf'
        r = np.argmin(b_a_ratios)
        return r
    except:
        traceback.print_exc()
        pdb.set_trace()


def print_vars(vars):
    table = BeautifulTable()
    headers = list(sorted(vars.keys()))
    table.column_headers = headers
    table.append_row([vars[key] for key in headers])
    print(table)


def canonicalize(a, b, c, x, y):
    # x, y = pivot coordinates
    # modifying b before a is v. imp.
    b[x, 0] /= a[x, y]  # divide by coeff of pivot element
    a[x, :] /= a[x, y]  # divide by coeff of pivot element
    c = c.T  # 6, 1 => 1, 6; required
    for i in range(a.shape[0]):
        if i == x:
            continue
        b[i, 0] -= b[x, 0] * a[i, y]
        a[i, :] -= a[x, :] * a[i, y]
    b[i + 1, 0] -= b[x, 0] * c[0, y]
    c -= a[x, :] * c[0, y]
    return a, b, c.T


def update_vars(a, b, vars, basis):
    # set non basic vars to zero
    for var in vars:
        if var not in basis:
            vars[var] = 0.0
    # evaluate basic vars
    for var in basis:
        column_idx = int(var[1:]) - 1
        vars[var] = b[a[:, column_idx].tolist().index(1), 0]
    return vars


def update_basis(a, basis, pivot_idx, s):
    for i, var in enumerate(basis):
        idx = int(var[1:])
        if a[pivot_idx][idx - 1] == 1:
            basis[i] = "x" + str(s + 1)
            break
    return basis


def final_print(text):
    print("\n" + "*" * 10 + " " + text + " " + "*" * 10)
