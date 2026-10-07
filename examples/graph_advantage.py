from qecopt.css_code import CSSCode
from qecopt.optimizer import (
    optimize_css_code,
    optimize_css_graph,
)
from qecopt.tanner import tanner_metrics


code = CSSCode(
    Hx=[
        [0, 1, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 0, 0],
        [1, 1, 0, 1, 1, 0, 0, 1],
    ],
    Hz=[
        [0, 0, 1, 0, 0, 0, 1, 0],
    ],
)

weight = optimize_css_code(code)
graph = optimize_css_graph(code)


for name, c in [
    ("Original", code),
    ("Weight optimized", weight),
    ("Graph optimized", graph),
]:
    m = tanner_metrics(c.Hx)

    print(f"\n{name}")
    print("Total weight:", c.total_weight())
    print("X 4-cycles:", m.four_cycles)
    print("X interaction depth:", m.interaction_depth)

    assert code.same_code_space(c)
    assert c.is_commuting()