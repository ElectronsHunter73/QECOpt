from qecopt.gf2 import GF2Matrix
from qecopt.tanner import tanner_metrics


def test_tanner_metrics():

    H = GF2Matrix([
        [1, 1, 0],
        [1, 1, 1],
    ])

    metrics = tanner_metrics(H)

    assert metrics.edges == 5
    assert metrics.max_check_degree == 3
    assert metrics.max_qubit_degree == 2
    assert metrics.four_cycles == 1
    assert metrics.interaction_depth == 3