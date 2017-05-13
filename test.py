from Equations import *
import sympy
from EquSys import *

methods = {'Newton-Raphson': newton, 'Secant': secant, 'Bisection': bisection,
           'Regula-Falsi': regula_falsi, 'Modified Newton 1': newton_mod1,
           'Modified Newton 2': newton_mod2}
m = sympy.Matrix([[25, 5, 1, 106.8], [64, 8, 1, 177.2], [144, 12, 1, 279.2]])
print(gauss(m))
