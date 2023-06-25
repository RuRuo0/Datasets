from sympy import *

a = symbols("a")
b = symbols("b")
c = symbols("c")
d = symbols("d")
e = symbols("e")
f = symbols("f")
g = symbols("g")
h = symbols("h")
t = symbols("t")

# eq1 = a / b * c / d * e / f - 1
# eq2 = g / c - a / b
# eq3 = d / h - e / f
# t_eq = t - g + h
# solution = solve([eq1, eq2, eq3, t_eq], t, dict=True)
# print(eq1)
# print(eq2)
# print(eq3)
# print(t_eq)
# print()
# print(solution)
# print()

# ab_solved = solve(eq2, a / b, dict=True)[0]
# ef_solved = solve(eq3, e / f, dict=True)[0]
# eq1 = eq1.subs(a / b, ab_solved[a / b])
# eq1 = eq1.subs(e / f, ef_solved[e / f])
# g_solved = solve(eq1, g, dict=True)[0]
# t_eq = t_eq.subs(g, g_solved[g])
# solution = solve(t_eq, t, dict=True)
# print(solution)

# eq1 = h / g - 1
# t_eq = t + g - h
# solution = solve([eq1, t_eq], t, dict=True)
# print(eq1)
# print(t_eq)
# print()
# print(solution)

l = [1, 2, 3, 4, 5, 6, 7]
print(l[0:2])
