import pytest

from qecopt.css_code import CSSCode


def make_example_code():
    Hx = [
        [1, 1, 1, 0],
        [1, 1, 0, 1]
    ]

    Hz = [
        [1, 0, 1, 1]
    ]

    return CSSCode(Hx, Hz)


def test_code_parameters():
    code = make_example_code()

    assert code.n == 4
    assert code.k == 1
    assert code.rank_x == 2
    assert code.rank_z == 1


def test_commutation():
    code = make_example_code()

    assert code.is_commuting()


def test_weight_reduction_preserves_code():
    code = make_example_code()

    optimized = code.add_x_row(1, 0)

    assert code.total_weight() == 9
    assert optimized.total_weight() == 8

    assert code.same_code_space(optimized)

    assert code.n == optimized.n
    assert code.k == optimized.k


def test_invalid_css_code():
    Hx = [
        [1, 0]
    ]

    Hz = [
        [1, 0]
    ]

    with pytest.raises(ValueError):
        CSSCode(Hx, Hz)