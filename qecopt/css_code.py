import numpy as np
from qecopt.gf2 import GF2Matrix

class CSSCode:
    def __init__(self,Hx,Hz):

        if not isinstance(Hx,GF2Matrix):
            Hx=GF2Matrix(Hx)
        if not isinstance(Hz,GF2Matrix):
            Hz=GF2Matrix(Hz)


        if Hx.n_cols != Hz.n_cols:
            raise ValueError("Hx and Hz must have the same number of columns")
        
        self.Hx=Hx
        self.Hz=Hz
        if not self.is_commuting():
            raise ValueError("Invalid CSSCode: Hx and Hz do not commute")
        

    @property
    def n(self):
        return self.Hx.n_cols

    @property
    def rank_x(self):
        return self.Hx.rank()

    @property
    def rank_z(self):
        return self.Hz.rank()

    @property
    def k(self):
        return self.n-self.rank_x-self.rank_z

    def is_commuting(self):
        Hx=self.Hx.to_numpy()
        Hz=self.Hz.to_numpy()
        product= (Hx @ Hz.T) %2
        return np.all(product==0)

    def total_weight(self):
        return(self.Hx.total_weight()+self.Hz.total_weight())

    def max_weight(self):
        x_max=int(np.max(self.Hx.row_weights()))
        z_max=int(np.max(self.Hz.row_weights()))
        return max(x_max,z_max)

    def add_x_row(self,target,source):
        new_Hx=self.Hx.add_row(target,source)
        return CSSCode(new_Hx,self.Hz) 
      
    def add_z_row(self,target,source):
        new_Hz=self.Hz.add_row(target,source)
        return CSSCode(self.Hx,new_Hz)

    def same_code_space(self,other):
        if not isinstance(other,CSSCode):
            raise TypeError("other must be a CSSCode")
        return (self.Hx.same_row_space(other.Hx) and self.Hz.same_row_space(other.Hz))

    def __repr__(self):
        return (
            f"CSSCode(n={self.n}, k={self.k}, "
            f"rank_x={self.rank_x}, rank_z={self.rank_z})")