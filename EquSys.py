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


def _get_max_elem(system, i):
    n = system.shape[0]
    max_mag, max_ind = abs(system[i, i]), i
    for j in range(i + 1, n):
        if abs(system[j, i]) > max_mag:
            max_mag, max_ind = abs(system[j, i]), j
    return max_mag, max_ind


def gauss_jordan(system: sympy.Matrix):
    """
    Performs gauss jordan elimination with partial pivoting on a system of
    linear equations.
    :param system: system of linear equations.
    :return: a [n, 1] matrix (vector) containing result.
    """
    system = system.as_mutable()
    n = system.shape[0]
    # iterate over rows
    for i in range(0, n):
        # find maximum magnitude and index in this column
        max_mag, max_ind = _get_max_elem(system, i)
        # swap current row with the row found to have the maximum element
        system.row_swap(max_ind, i)
        # normalize current row
        system.row_op(i, lambda u,v: u / system[i,i])
        # forward elimination, iterate over remaining rows and eliminate
        for j in range(i + 1, n):
            _forward_eliminate(system, i, j)
        # forward elimination, iterate over previous rows and eliminate
        for j in range(i - 1, -1, -1):
            _forward_eliminate(system, i, j)
    # return last column reversed
    return sympy.Matrix(system.col(system.shape[0]))

def jacobi(A: sympy.Matrix, b=None, max_iter=100, max_err=1e-5, x=None):
    """Jacobi Iterative Method for Solving A System of Linear Equations:
    takes a system of linear equations and returns an approximate solution
    for the system using Jacobi's approximation.

    Keyword arguments:
    A: sympy.Matrix -- The augmented matrix representing the system if b = None
    else the coefficients matrix.
    b: sympy.Matrix -- The r.h.s matrix of the system.
    max_iter: int -- The maximum number of iterations to perform.
    max_err: float -- The maximum allowed error.
    x: sympy.Matrix -- The initial value for the variables.

    return:
    1) The vector x containing the final approximate solution.
    2) The matrix x_hist containing the values of x during each iteration.
    3) The list err_hist containing the values of the error during each iteration.
    """

    n = A.shape[0]
    if b == None:
        A, b = [A[:, :-1], A[:, -1]]
    if x == None:
        x = sympy.Matrix.zeros(n, 1)
    D = A.multiply_elementwise(sympy.Matrix.eye(n))
    x_prev = x[:, :]
    err_hist = []
    x_hist = sympy.Matrix(x)
    for _ in range(0, max_iter):
        x = D.inv() * (b - (A - D) * x)
        x_hist = x_hist.row_join(x)
        diff = (x - x_prev).applyfunc(abs)
        err = max(max(diff.tolist()))
        err_hist.append(err.evalf())
        x_prev = x[:, :]
        if err < max_err:
            return sympy.N(x), sympy.N(x_hist), err_hist
    return sympy.N(x), sympy.N(x_hist), err_hist

def gauss_seidel(A: sympy.Matrix, b=None, max_iter=100, max_err=1e-5, x=None):
    """Gauss-Seidel Iterative Method for Solving A System of Linear Equations:
    takes a system of linear equations and returns an approximate solution
    for the system using Gauss-Seidel approximation.

    Keyword arguments:
    A: sympy.Matrix -- The augmented matrix representing the system if b = None
    else the coefficients matrix.
    b: sympy.Matrix -- The r.h.s matrix of the system.
    max_iter: int -- The maximum number of iterations to perform.
    max_err: float -- The maximum allowed error.
    x: sympy.Matrix -- The initial value for the variables.

    return:
    1) The vector x containing the final approximate solution.
    2) The matrix x_hist containing the values of x during each iteration.
    3) The list err_hist containing the values of the error during each iteration.
    """
    n = A.shape[0]
    if b == None:
        A, b = [A[:, :-1], A[:, -1]]
    if x == None:
        x = sympy.Matrix.zeros(n, 1)
    print(A)
    print(b)
    x_prev = x[:, :]
    err_hist = []
    x_hist = sympy.Matrix(x)
    for _ in range(0, max_iter):
        for i in range(0, n):
            xi_new = b[i]
            for j in range(0, n):
                if i != j:
                    xi_new -= A[i, j] * x[j]
                x[i] = xi_new / A[i, i]
        x_hist = x_hist.row_join(x)
        diff = (x - x_prev).applyfunc(abs)
        err = max(max(diff.tolist()))
    #    print(x_prev)
        err_hist.append(err.evalf())
        x_prev = x[:, :]
        if err < max_err:
            return sympy.N(x), sympy.N(x_hist), err_hist
    return sympy.N(x), sympy.N(x_hist), err_hist
