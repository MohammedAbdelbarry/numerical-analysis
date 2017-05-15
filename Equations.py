"""Root Finding Methods:
A collection of methods to find roots of equations.
"""
import numpy
from part1_output import Output
import matplotlib.pyplot

from equations_util import *


def regula_falsi(f, xl, xu, max_err=1e-5, max_iter=50):
    if f(xl) * f(xu) > 0:
        raise ValueError("Error! There are no roots in the range [%d, %d]" % (xl, xu))
    prev_xr = 0
    output = sympy.Matrix([[0, 0]])
    output.row_del(0)
    for _ in range(0, max_iter):
        yl = f(xl)
        yu = f(xu)
        xr = (xl * yu - xu * yl) / (yu - yl)
        yr = f(xr)
        err = abs(xr - prev_xr)
        if yr * yu < 0:
            xl = xr
        elif yr * yl < 0:
            xu = xr
        else:
            err = 0
        prev_xr = xr
        output = output.col_join(sympy.Matrix([[xr, err]]))
        if err <= max_err:
            return numpy.array(output).astype(numpy.float64)
    return numpy.array(output).astype(numpy.float64)


def bisection(expr, arguments, max_err=1e-5, max_iter=50):
    assert len(arguments) == 2
    xl, xu = min(arguments[0], arguments[1]), max(arguments[0], arguments[1])
    if f(xl) * f(xu) > 0:
        raise ValueError("Error! There are no roots in the range [%d, %d]" % (xl, xu))
    prev_xr = 0
    f = expr_to_lambda(expr)
    symbol = get_symbol(expr)
    output = Output()
    _init_output(output, "Secant", f, expr_to_lambda(diff(expr)))
    cur_xi = []
    cur_err_i = []
    for _ in range(0, max_iter):
        yl = f(xl)
        yu = f(xu)
        xr = (xl + xu) / 2
        yr = f(xr)
        err = abs(xr - prev_xr)
        if yr * yu < 0:
            xl = xr
        elif yr * yl < 0:
            xu = xr
        else:
            err = 0
        prev_xr = xr
        output = output.col_join(sympy.Matrix([[xr, err]]))
        if err <= max_err:
            return numpy.array(output).astype(numpy.float64)
    return numpy.array(output).astype(numpy.float64)


def newton(expr, arguments, max_err=1e-5, max_iter=50):
    assert len(arguments) == 1
    xi = arguments[0]
    f = expr_to_lambda(expr)
    expr_diff = diff(expr)
    f_diff = expr_to_lambda(expr_diff)
    symbol = get_symbol(expr)
    output = Output()
    _init_output(output, "Newton-Raphson Mod#2", f, f_diff)
    cur_xi = []
    cur_err_i = []
    for _ in range(0, max_iter):
        fxi = f(xi)
        fxi_diff = f_diff(xi)
        root = xi - fxi / fxi_diff
        err = abs((root - xi))
        xi = root
        cur_xi.append(root)
        cur_err_i.append(err)
        if err <= max_err:
            break
    output.roots.append(root)
    output.roots.append(xi)
    output.dataframes.append(create_dataframe(cur_xi, output.function, cur_err_i, symbol))
    output.roots = numpy.array(output.roots).astype(numpy.float64)
    output.errors = numpy.array(output.errors).astype(numpy.float64)
    return output


def newton_mod1(expr, arguments, max_err=1e-5, max_iter=50):
    assert len(arguments) == 2
    xi, m = arguments[0], arguments[1]
    f = expr_to_lambda(expr)
    expr_diff = diff(expr)
    f_diff = expr_to_lambda(expr_diff)
    symbol = get_symbol(expr)
    output = Output()
    _init_output(output, "Newton-Raphson Mod#2", f, f_diff)
    cur_xi = []
    cur_err_i = []
    for _ in range(0, max_iter):
        fxi = f(xi)
        fxi_diff = f_diff(xi)
        root = xi - m * fxi / fxi_diff
        err = abs((root - xi))
        xi = root
        cur_xi.append(root)
        cur_err_i.append(err)
        if err <= max_err:
            break
    output.roots.append(root)
    output.roots.append(xi)
    output.dataframes.append(create_dataframe(cur_xi, output.function, cur_err_i, symbol))
    output.roots = numpy.array(output.roots).astype(numpy.float64)
    output.errors = numpy.array(output.errors).astype(numpy.float64)
    return output


def newton_mod2(expr, arguments, max_err=1e-5, max_iter=50):
    assert len(arguments) == 1
    xi = arguments[0]
    f = expr_to_lambda(expr)
    expr_diff = diff(expr)
    f_diff = expr_to_lambda(expr_diff)
    f_diff2 = expr_to_lambda(diff(expr_diff))
    symbol = get_symbol(expr)
    output = Output()
    _init_output(output, "Newton-Raphson Mod#2", f, f_diff)
    cur_xi = []
    cur_err_i = []
    for _ in range(0, max_iter):
        fxi = f(xi)
        f_diff_xi = f_diff(xi)
        f_diff_xi2 = f_diff2(xi)
        root = xi - f_diff_xi * fxi / (f_diff_xi ** 2 - fxi * f_diff_xi2)
        err = abs((root - xi))
        xi = root
        cur_xi.append(root)
        cur_err_i.append(err)
        if err <= max_err:
            break
    output.roots.append(root)
    output.roots.append(xi)
    output.dataframes.append(create_dataframe(cur_xi, output.function, cur_err_i, symbol))
    output.roots = numpy.array(output.roots).astype(numpy.float64)
    output.errors = numpy.array(output.errors).astype(numpy.float64)
    return output


def secant(expr, arguments, max_err=1e-5, max_iter=50):
    assert len(arguments) == 2
    xi, xi_prev = arguments[0], arguments[1]
    f = expr_to_lambda(expr)
    symbol = get_symbol(expr)
    output = Output()
    _init_output(output, "Secant", f, expr_to_lambda(diff(expr)))
    cur_xi = []
    cur_err_i = []
    for _ in range(0, max_iter):
        fxi = f(xi)
        fxi_prev = f(xi_prev)
        root = xi - fxi * (xi_prev - xi) / (fxi_prev - fxi)
        err = abs((root - xi))
        xi_prev = xi
        xi = root
        cur_xi.append(root)
        cur_err_i.append(err)
        if err <= max_err:
            break
    output.roots.append(root)
    output.roots.append(xi)
    output.dataframes.append(create_dataframe(cur_xi, output.function, cur_err_i, symbol))
    output.roots = numpy.array(output.roots).astype(numpy.float64)
    output.errors = numpy.array(output.errors).astype(numpy.float64)
    return output

def fixed_point(expr, arguments, max_err=1e-5, max_iter=50):
    assert len(arguments) == 1
    xi = arguments[0]
    f = expr_to_lambda(expr)
    symbol = get_symbol(expr)
    output = Output()
    _init_output(output, "Fixed-Point", f, lambda x: x)
    cur_xi = []
    cur_err_i = []
    for _ in range(0, max_iter):
        root = xi - f(xi)
        err = abs((root - xi))
        xi = root
        cur_xi.append(root)
        cur_err_i.append(err)
        if err <= max_err:
            break
    output.roots.append(root)
    output.roots.append(xi)
    output.dataframes.append(create_dataframe(cur_xi, output.function, cur_err_i, symbol))
    output.roots = numpy.array(output.roots).astype(numpy.float64)
    output.errors = numpy.array(output.errors).astype(numpy.float64)
    return output

def birge_vieta(expr, arguments, max_err=1e-5, max_iter=50):
    assert len(arguments) == 1
    xi = arguments[0]
    output = Output()
    symbol = get_symbol(expr)
    _init_output(output, "Birge-Vieta", expr_to_lambda(expr),
     expr_to_lambda(diff(expr)))
    poly = sympy.Poly(expr, expr.free_symbols)
    a = poly.all_coeffs()
    m = len(a) - 1
    n = m + 1
    i = 1
    while m > 0:
        cur_xi = []
        cur_err_i = []
        b = numpy.zeros(m + 1, dtype=numpy.float64)
        c = numpy.zeros(m + 1, dtype=numpy.float64)
        err = 0
        for _ in range(0, max_iter):
            find_coeffs(a, b, c, xi)
            root = xi - b[m] / c[m - 1]
            err = abs((root - xi))
            xi = root
            cur_xi.append(xi)
            cur_err_i.append(err)
            if err <= max_err:
                break
        a = b[0: -1]
        m = len(a) - 1
        output.dataframes.append(create_dataframe(cur_xi, output.function, cur_err_i, symbol, i))
        i += 1
        output.roots.append(sympy.N(xi, 6))
        output.errors.append(sympy.N(err, 6))
    output.roots = numpy.array(output.roots).astype(numpy.float64)
    output.errors = numpy.array(output.errors).astype(numpy.float64)
    return output

def _init_output(output: Output, method_name: str, f, f_bound):
    output.roots = []
    output.errors = []
    output.title = method_name
    output.function = f
    output.boundary_function = f_bound


def find_coeffs(a, b, c, xi):
    m = len(a) - 1
    c[0] = b[0] = a[0]
    for i in range(1, m + 1):
        b[i] = a[i] + xi * b[i-1]
        c[i] = b[i] + xi * c[i-1]

if __name__ == '__main__':
    # print("""Please Select A Method:
    # 1) Newton-Raphson Method
    # 2) Secant Method
    # 3) Bisection Method
    # 4) Regula-Falsi Method
    # 5) Modified Newton(With Known Multiplicity)
    # 6) Modified Newton(With Unknown Multiplicity)""")
    out = birge_vieta(sympy.sympify("x**4 - 9*x**3 - 2*x**2 + 120 * x -130"), -3)
    for df in out.dataframes:
        print(df)
    #print(birge_vieta(sympy.sympify("x ** 4 - 9 * x ** 3 - 2 * x ** 2 + 120 * x - 130"), -3))
    eqn = input("Please Enter The Equation: ")  # Test Code (Just Enter x^2 - 4)
    # var = input("Please Enter The Name of The Variable: ")#Test Code (Use x as a symbol)
    # symbol = sympy.symbols(var)
    expr = sympy.sympify(eqn)
    free_symbols = expr.free_symbols
    if len(free_symbols) != 1:
        raise ValueError("The Expression Contains More Than One Variable")
    symbol = free_symbols.pop()
    expr_diff = sympy.diff(expr, symbol)
    expr_diff2 = sympy.diff(expr_diff, symbol)
    f = sympy.utilities.lambdify(symbol, expr)
    g = sympy.utilities.lambdify(symbol, expr_diff)
    h = sympy.utilities.lambdify(symbol, expr_diff2)
    # f = lambda x: x ** 3 - 2 * x ** 2 - 4 * x + 8
    # g = lambda x: 3 * x ** 2 - 4 * x - 4
    # h = lambda x: 6 * x - 4
    #output = regula_falsi(f, 1.5, 2.2, 1e-5, 100)
    #print_table("Regula-Falsi", output[:, 0], f, output[:, 1], symbol)
    output = bisection(f, 1, 2.2, 1e-5, 100)
    print_table("Bisection", output[:, 0], f, output[:, 1], symbol)
    output = newton(f, g, 2.2)
    print_table("Newton-Raphson", output[:, 0], f, output[:, 1], symbol)
    # output = fixed_point(f, 0.1)
    # print_table("Fixed Point", output[:, 0], f, output[:, 1], symbol)
    output = secant(f, 1.5, 2.2)
    print_table("Secant", output[:, 0], f, output[:, 1], symbol)
    output = newton_mod1(f, g, 2.2, 2)
    print_table("Newton-Raphson Mod#1", output[:, 0], f, output[:, 1], symbol)
    output = newton_mod2(f, g, h, 2.2)
    print_table("Newton-Raphson Mod#2", output[:, 0], f, output[:, 1], symbol)
