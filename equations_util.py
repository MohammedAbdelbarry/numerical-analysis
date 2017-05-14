"""Equation Utilities:
A module containing some equation parsing methods.
"""
from EquSys import *
import pandas


def equations_to_matrices(equations: list):
    """Equations to Matrix:
    Transform a list of equations into two matrices A(the coefficients matrix)
    and b(the r.h.s matrix).

    Keyword arguments:
    equations: list -- A list of containing the string representation of the equations.

    return:
    1) The matrix A containing the coefficients of the equation
       sorted according to the alphabetical order of their symbols.
    2) The vector b containing the r.h.s of the equations
    3) The symbols sorted in alphabetical order.
    """
    print(equations)
    parsed_equations = []
    symbols = set()
    for eq in equations:
        parts = eq.replace('==', '=').split('=')
        assert len(parts) == 2
        lhs, rhs = parts
        parsed_eqn = sympy.Eq(sympy.sympify(lhs), sympy.sympify(rhs))
        symbols |= parsed_eqn.free_symbols
        parsed_equations.append(parsed_eqn)
    symbol_list = sorted(list(symbols), key=str)
    A, b = sympy.linear_eq_to_matrix(parsed_equations, symbol_list)

    # asserts that both matrices do not contain any symbols
    # since bool(empty_set) returns False and bool(non_empty_set) returns true
    assert not bool(A.free_symbols) and not bool(b.free_symbols)
    return A, b, symbol_list


def equations_to_aug_matrix(equations: list):
    """Equations to Augmented Matrix:
    Transform a list of equations into an augmented matrix.

    Keyword arguments:
    equations: list -- A list of containing the string representation of the equations.

    return:
    1) The augmented matrix with coefficients sorted according to the alphabetical
       order of their symbols.
    2) The symbols sorted in alphabetical order.
    """
    A, b, symbol_list = equations_to_matrices(equations)
    return A.row_join(b), symbol_list


def print_table(method_name: str, x: list, f,
                err: list, symbol: sympy.Symbol):
    print(method_name + ":")
    df = pandas.DataFrame({str(symbol): x,
                           "f(" + str(symbol) + ")": list(map(f, x)),
                           "error": err})
    df = df[[str(symbol), "f(" + str(symbol) + ")", "error"]]
    print(df)
    ### WE COULD ADD AN OPTION TO CHOOSE THE FILE NAME AND EXTENSION
    ### available formats: HTML, CSV, PICKLE (Pickle Serializer)
    ### LATEX, EXCEL, SQL, JSON, HDF,FEATHER and GBQ (Google BigQuery)
    df.to_csv(path_or_buf=method_name + '.csv')
    with open(method_name + '.html', 'w') as html_file:
        html_file.write(df.to_html())


def string_to_lambda(expr_str: str):
    expr = sympy.sympify(expr_str)
    free_symbols = expr.free_symbols
    if len(free_symbols) != 1:
        raise ValueError("The Expression Contains More Than One Variable")
    symbol = free_symbols.pop()
    f = sympy.utilities.lambdify(symbol, expr)
    return f


def diff(expr: sympy.Expr):
    free_symbols = expr.free_symbols
    symbol = free_symbols.pop()
    return sympy.diff(expr, symbol)

if __name__ == '__main__':
    aug, sym = equations_to_aug_matrix(["12*x + 3*y - 5*z - 1 == 0", "x+5*y+3*z=28", "3*x+7*y+13*z=76"])
    sympy.pprint(sympy.N(aug))
    # x, x_hist, err_hist = jacobi(aug, x=sympy.Matrix([[1], [0], [1]]))
    # sympy.pprint(x)
    # print(len(err_hist))
