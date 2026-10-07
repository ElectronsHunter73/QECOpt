from qecopt.gf2 import GF2Matrix
from qecopt.css_code import CSSCode
from qecopt.optimizer import best_row_move,optimize_matrix,optimize_css_code


def test_best_row_move():
    H = GF2Matrix([
        [1, 1, 1, 0],
        [1, 1, 0, 1],
        [0, 1, 1, 1],
    ])

    move, delta = best_row_move(H)

    assert move is not None
    assert delta == -1

    target, source = move

    H_new = H.add_row(target, source)

    assert H_new.total_weight() - H.total_weight() == delta

def test_best_row_move_none():
    H = GF2Matrix([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ])

    move, delta = best_row_move(H)

    assert move is None
    assert delta == 0
def test_optimize_matrix():
    H = GF2Matrix([
        [1, 1, 1, 0],
        [1, 1, 0, 1],
        [0, 1, 1, 1],
    ])

    optimized = optimize_matrix(H)

    assert optimized.total_weight() <= H.total_weight()
    assert optimized.same_row_space(H)

    move, delta = best_row_move(optimized)

    assert move is None
    assert delta == 0
def test_optimize_css_code():
    Hx = [
        [1, 1, 1, 0],
        [1, 1, 0, 1],
    ]

    Hz = [
        [1, 0, 1, 1],
    ]

    code = CSSCode(Hx, Hz)

    optimized = optimize_css_code(code)

    assert optimized.total_weight() <= code.total_weight()

    assert optimized.Hx.same_row_space(code.Hx)
    assert optimized.Hz.same_row_space(code.Hz)

    assert optimized.is_commuting()

    assert optimized.n == code.n
    assert optimized.k == code.k