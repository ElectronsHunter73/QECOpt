from qecopt.gf2 import GF2Matrix
from qecopt.css_code import CSSCode
from qecopt.tanner import tanner_metrics
from qecopt.optimizer import (
    graph_score,
    optimize_tanner_graph,
    optimize_css_graph,
)


def test_graph_optimizer():
    H = GF2Matrix([
        [1, 1, 1],
        [1, 1, 0],
    ])

    optimized = optimize_tanner_graph(H)

    assert H.same_row_space(optimized)
    assert tanner_metrics(H).four_cycles == 1
    assert tanner_metrics(optimized).four_cycles == 0
    assert graph_score(optimized) < graph_score(H)


def test_css_graph_optimizer():
    code = CSSCode(
        Hx=[
            [1, 1, 1],
            [1, 1, 0],
        ],
        Hz=[
            [1, 1, 0],
        ],
    )

    optimized = optimize_css_graph(code)

    assert code.same_code_space(optimized)
    assert optimized.is_commuting()
    assert optimized.n == code.n
    assert optimized.k == code.k
    assert tanner_metrics(optimized.Hx).four_cycles == 0
    