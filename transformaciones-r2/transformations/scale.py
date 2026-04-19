from transformations.base import Transformation
import numpy as np
from numpy.typing import NDArray
from typing import Optional

class Scale(Transformation):
    def __init__(self, kx: float, ky: Optional[float] = None):
        self.kx = kx
        self.ky = ky if ky is not None else kx  # uniforme si no se pasa ky
        
    def apply(self, points: NDArray[np.float64]) -> NDArray[np.float64]:
        scale_matrix = np.array([
            [self.kx, 0],
            [0, self.ky]
        ])

        return points @ scale_matrix.T