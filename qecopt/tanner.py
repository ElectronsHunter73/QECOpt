import numpy as np
from .gf2 import GF2Matrix
from dataclasses import dataclass
@dataclass(frozen=True)
class TannerMetrics:
    edges:int
    max_check_degree:int
    max_qubit_degree:int
    four_cycles:int
    interaction_depth:int

def tanner_metrics(h:GF2Matrix):
    A=h.to_numpy().astype(int)
    check_degrees=np.sum(A,axis=1)
    qubit_degrees=np.sum(A,axis=0)
    edges=int(np.sum(A))
    max_check_degree= (int(np.max(check_degrees)) if check_degrees.size >0 else 0)
    max_qubit_degree=(int(np.max(qubit_degrees) if qubit_degrees.size>0 else 0))
    overlap= A @ A.T
    four_cycles=0
    for i in range(overlap.shape[0]):
        for j in range(i+1,overlap.shape[0]):
            shared = int(overlap[i,j])
            four_cycles += shared* (shared-1) // 2
    interaction_depth=max(max_check_degree, max_qubit_degree)

    return TannerMetrics(edges=edges,max_check_degree=max_check_degree,
        max_qubit_degree=max_qubit_degree,
        four_cycles=four_cycles,
        interaction_depth=interaction_depth,
    )
