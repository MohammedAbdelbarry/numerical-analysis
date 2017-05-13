import sympy


def _forward_eliminate(system: sympy.Matrix, i, j):
    """
    Performs forward eliminates on a row inside a system of linear equations.
    :param system: linear equations system.
    :param i: index of the base row.
    :param j: index of the row to be eliminated.
    :var system: a mutable matrix can be passed (reference passing)
    :return: an augmented square matrix after eliminating the row.
    """
    n = system.shape[1]
    c = system[j, i] / system[i, i]
    for k in range(0, n):
        system[j, k] -= c * system[i, k]
    return system


def _back_sub(tri_mat: sympy.Matrix):
    """
    Performs back substitution on an augmented upper triangular matrix.
    :param tri_mat: augmented triangular matrix.
    :return: a [n, 1] matrix containing result.
    """
    # TODO: Check if scaling is necessary
    n = tri_mat.shape[0]
    x = sympy.zeros(n, 1)
    x[n - 1] = tri_mat[n - 1, n] / tri_mat[n - 1, n - 1]
    for i in range(n - 2, -1, -1):
        s = 0
        for j in range(i + 1, n):
            s += tri_mat[i, j] * x[j, 0]
        x[i] = (tri_mat[i, n] - s) / tri_mat[i, i]
    return x


def gauss(system: sympy.Matrix):
    """
    Performs gauss elimination with partial pivoting on a system of
    linear equations.
    :param system: system of linear equations.
    :return: a [n, 1] matrix containing result.
    """
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
    # perform back substitution.
    return _back_sub(system)
