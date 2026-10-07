from qecopt.css_code import CSSCode
from qecopt.optimizer import optimize_css_code
from qecopt.optimizer import optimize_css_graph
from qecopt.tanner import tanner_metrics
from random import Random

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
graph_optimized = optimize_css_graph(code)


def report(name, c):
    x = tanner_metrics(c.Hx)
    z = tanner_metrics(c.Hz)

    print(f"\n{name}")
    print("Total weight:", c.total_weight())
    print("Max stabilizer weight:", c.max_weight())

    print("X 4-cycles:", x.four_cycles)
    print("Z 4-cycles:", z.four_cycles)

    print("X interaction depth:", x.interaction_depth)
    print("Z interaction depth:", z.interaction_depth)

    print("X max qubit degree:", x.max_qubit_degree)
    print("Z max qubit degree:", z.max_qubit_degree)


report("ORIGINAL", code)
report("WEIGHT OPTIMIZED", optimized)
report("GRAPH OPTIMIZED", graph_optimized)


for candidate in (optimized, graph_optimized):
    assert code.same_code_space(candidate)
    assert candidate.is_commuting()
    assert candidate.n == code.n
    assert candidate.k == code.k

print("\nAll equivalence checks passed.")
rng = Random(42)


def random_basis(H, steps=15):
    current = H

    for _ in range(steps):
        target, source = rng.sample(range(H.n_rows), 2)
        current = current.add_row(target, source)

    return current


def count_cycles(c):
    return (
        tanner_metrics(c.Hx).four_cycles
        + tanner_metrics(c.Hz).four_cycles
    )


graph_wins = 0
weight_wins = 0
ties = 0

for _ in range(50):
    start = CSSCode(
        random_basis(code.Hx),
        random_basis(code.Hz),
    )

    weight_result = optimize_css_code(start)
    graph_result = optimize_css_graph(start)

    assert code.same_code_space(weight_result)
    assert code.same_code_space(graph_result)

    w_cycles = count_cycles(weight_result)
    g_cycles = count_cycles(graph_result)

    if g_cycles < w_cycles:
        graph_wins += 1
    elif w_cycles < g_cycles:
        weight_wins += 1
    else:
        ties += 1

print("\n50 RANDOM EQUIVALENT BASES")
print("Graph optimizer fewer 4-cycles:", graph_wins)
print("Weight optimizer fewer 4-cycles:", weight_wins)
print("Equal 4-cycle counts:", ties)