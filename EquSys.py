import sympy


def _forward_eliminate(system: sympy.Matrix, i, j):
    n = system.shape[1]
    c = system[j, i] / system[i, i]
    for k in range(0, n):
        system[j, k] -= c * system[i, k]
    return system


def gauss(system: sympy.Matrix, max_err=1e-5, max_iter=50):
    system = system.as_mutable()
    n = system.shape[0]
    # iterate over columns
    for i in range(0, n):
        # find maximum magnitude and index in this column
        max_mag, max_ind = abs(system[i, i]), i
        for j in range(i + 1, n):
            if abs(system[j, i]) > max_mag:
                max_mag, max_ind = abs(system[j, i]), j
        # swap current row with the row found to have the maximum element
        system.row_swap(max_ind, i)
        # forward elimination, iterate over remaining rows and eliminate
        for j in range(i + 1, n):
            _forward_eliminate(system, i, j)
    # TODO: back substitution
    return system
