from qecopt.gf2 import GF2Matrix


def test_rank():
    H = GF2Matrix([
        [1, 1, 0],
        [0, 1, 1],
        [1, 0, 1]
    ])

    assert H.rank() == 2


def test_add_row():
    H = GF2Matrix([
        [1, 1, 1, 0],
        [1, 1, 0, 1]
    ])

    new_H = H.add_row(1, 0)

    expected = GF2Matrix([
        [1, 1, 1, 0],
        [0, 0, 1, 1]
    ])

    assert new_H.same_row_space(H)
    assert new_H.total_weight() == 5
    assert new_H.same_row_space(expected)


def test_swap_rows_preserves_row_space():
    H = GF2Matrix([
        [1, 1, 1, 0],
        [1, 1, 0, 1]
    ])

    swapped = H.swap_rows(0, 1)

    assert H.same_row_space(swapped)