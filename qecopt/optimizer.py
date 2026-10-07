from qecopt.gf2 import GF2Matrix
from qecopt.css_code import CSSCode

def best_row_move(matrix):
    if not isinstance(matrix,GF2Matrix):
        raise TypeError("matrix must be GF2Matrix")

    best_move=None
    best_delta=0
    overlap=matrix.overlap_matrix()
    for target in range(matrix.n_rows):
        for source in range(matrix.n_rows):
            if target==source:
                continue
            source_weight=overlap[source,source]
            shared=overlap[target,source]
            delta=int(source_weight - 2*shared)
            if delta<best_delta:
                best_delta=delta
                best_move=(target,source)

    return best_move,best_delta
def optimize_matrix(matrix):
    if not isinstance(matrix,GF2Matrix):
        raise TypeError("Matrix must be GF2Matrix")
    current=matrix
    while True:
        move, delta=best_row_move(current)
        if move is None:
            break
        target, source= move
        current=current.add_row(target,source)
    return current
def optimize_css_code(code):
    if not isinstance(code, CSSCode):
        raise TypeError("code must be CSSCode")

    optimized_Hx = optimize_matrix(code.Hx)
    optimized_Hz = optimize_matrix(code.Hz)

    return CSSCode(optimized_Hx, optimized_Hz)