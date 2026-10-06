import numpy as np


class GF2Matrix:

    def __init__(self,data):
        array=np.asarray(data,dtype=np.uint8)

        if array.ndim != 2:
            raise ValueError("GF2Matrix must be two-dimensional.")
        self._data = (array % 2)

    @property 
    def shape(self):
        return self._data.shape
    
    @property
    def n_rows(self):
        return self._data.shape[0]

    @property
    def n_cols(self):
        return self._data.shape[1]

    def to_numpy(self):
        return self._data.copy()

    def rank(self):
        A = self._data.copy()
        rows, cols = A.shape
        rank = 0
        for col in range(cols):
            pivot = None
            for row in range(rank, rows):
                if A[row, col] == 1:
                    pivot = row
                    break
            if pivot is None:
                continue
            if pivot != rank:
                A[[rank, pivot]] = A[[pivot, rank]]
            for row in range(rows):
                if row != rank and A[row, col] == 1:
                    A[row] ^= A[rank]
            rank += 1
            if rank == rows:
                break
        return rank
    
    def row_weights(self):
        return np.sum(self._data,axis=1)

    def column_weights(self):
        return np.sum(self._data,axis=0)

    def total_weight(self):
        return int(np.sum(self._data))

    def add_row(self,target,source):
        if target==source:
            raise ValueError("Target and Source rows must be different.")
        
        if not (0<= target <self.n_rows):
            raise IndexError("Target is out of range")

        if not (0<= source <self.n_rows):
                raise IndexError("Source is out of range")

        new_data=self._data.copy()
        new_data[target] ^= new_data[source]
        return GF2Matrix(new_data)
    
    def swap_rows(self,row1,row2):
        new_data=self._data.copy()
        new_data[[row1,row2]]=new_data[[row2,row1]]
        return GF2Matrix(new_data)

    def same_row_space(self,other):
        if not isinstance(other,GF2Matrix):
            raise TypeError("other must be a GF2Matrix")

        if self.n_cols != other.n_cols or self.rank() != other.rank():
            return False

        stacked=GF2Matrix(np.vstack([self._data,other._data,]))

        return stacked.rank()==self.rank()

    def overlap_matrix(self):
        data=self._data.astype(int)
        return data@ data.T

    def row_add_weight_delta(self,target,source):
        if target==source:
            raise ValueError("Target and Source must be different rows")
        if not (0 <= target < self.n_rows):
            raise IndexError("Target is out of range")
        if not (0 <= source < self.n_rows):
            raise IndexError("Source is out of range")
        overlap=self.overlap_matrix()
        source_weight=overlap[source,source]
        shared=overlap[target,source]
        return int(source_weight - 2*shared)
    
    def __repr__(self):
        return f"GF2Matrix({self._data!r})"

    def __str__(self):
        return str(self._data)