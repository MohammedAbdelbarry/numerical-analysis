import sympy

def equations_to_aug_matrix(equations: list):
    """Equations to Augmented Matrix:
    Transform a list of equations into an augmented matrix.

    Keyword arguments:
    equations -- A list of containing the string representation of the equations.

    return:
    1) The augmented matrix with coefficients sorted according to the alphabetical
       order of their symbols.
    2) The symbols sorted in alphabetical order.
    """
    print(equations)
    parsed_equations = []
    symbols = set()
    for eq in equations:
        parts = eq.replace('==', '=').split('=')
        assert(len(parts) == 2)
        lhs, rhs = parts
        parsed_eqn = sympy.Eq(sympy.sympify(lhs), sympy.sympify(rhs))
        symbols |= parsed_eqn.free_symbols
        parsed_equations.append(parsed_eqn)
    symbol_list = sorted(list(symbols), key = str)
    A, b = sympy.linear_eq_to_matrix(parsed_equations, symbol_list)

    #asserts that both matrices do not contain any symbols
    #since bool(empty_set) returns False and bool(non_empty_set) returns true
    assert(not bool(A.free_symbols) and not bool(b.free_symbols))
    return A.row_join(b), symbol_list

sympy.init_printing()
aug, sym = equations_to_aug_matrix(["2*x - 3*y + 4 == 0", "x+y+z=-3", "x-z-2*y=-15"])
print(aug)
print(equations_to_aug_matrix.__doc__)
print(sym)
