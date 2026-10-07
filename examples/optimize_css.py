from qecopt.css_code import CSSCode
from qecopt.optimizer import optimize_css_code


Hx = [
    [1, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
]

Hz = [
    [1, 1, 1, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1],
]


code = CSSCode(Hx, Hz)
optimized = optimize_css_code(code)


print("ORIGINAL CODE")
print()

print("Hx:")
print(code.Hx)

print("Hz:")
print(code.Hz)

print("Total weight:", code.total_weight())
print("Max weight:", code.max_weight())
print("n:", code.n)
print("k:", code.k)


print()
print("OPTIMIZED CODE")
print()

print("Hx:")
print(optimized.Hx)

print("Hz:")
print(optimized.Hz)

print("Total weight:", optimized.total_weight())
print("Max weight:", optimized.max_weight())
print("n:", optimized.n)
print("k:", optimized.k)


print()
print("CERTIFICATION")

print(
    "Same X row space:",
    code.Hx.same_row_space(optimized.Hx)
)

print(
    "Same Z row space:",
    code.Hz.same_row_space(optimized.Hz)
)

print(
    "Commuting:",
    optimized.is_commuting()
)

print(
    "Same n:",
    code.n == optimized.n
)

print(
    "Same k:",
    code.k == optimized.k
)