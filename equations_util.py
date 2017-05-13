import sympy

def equations_to_aug_matrix(equations: list):
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
    print(parsed_equations, symbols)
    symbol_list = list(symbols)
    A, b = sympy.linear_eq_to_matrix(parsed_equations, symbol_list)
    print(A.shape, b.shape)
    return A.row_join(b), symbol_list

sympy.init_printing()
aug, sym = equations_to_aug_matrix(["2*x - 3*y + 4 == 0", "x+y+z=-3", "x-z-2*y=-15"])
print(aug)
print(sym)
