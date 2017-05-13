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

def jacobi(A: sympy.Matrix, b=None, max_iter=100, max_err=1e-5, x=None):
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
