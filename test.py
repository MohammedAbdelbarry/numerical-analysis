from Equations import *
from EquSys import *
from sympy.abc import x, y, z

methods = {'Newton-Raphson': newton, 'Secant': secant, 'Bisection': bisection,
           'Regula-Falsi': regula_falsi, 'Modified Newton 1': newton_mod1,
           'Modified Newton 2': newton_mod2}

# testing gauss elimination with partial pivoting.
# m = sympy.Matrix([[25, 5, 1, 106.8], [64, 8, 1, 177.2], [144, 12, 1, 279.2]])
# m = sympy.Matrix([[1, 2, 2, 106.8], [2, 4, 1, 177.2], [4, 2, 1, 279.2]])
m = sympy.Matrix([[8, 4, -1, 11], [-2, 3, 1, 4], [2, -1, 6, 7]])
# sympy.pprint(sympy.N(gauss_jordan(m), 4))
print(sympy.solve_linear_system(m, x, y, z))
# print(sympy.Matrix(reversed(m.col(m.shape[0]))))
# print(m.col(m.shape[0]).tolist()[0][0])
sympy.pprint(sympy.N(lu_decomp(m), 4))
