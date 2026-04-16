from transformations.base import Transformation
import numpy as np
from numpy.typing import NDArray

class Scale(Transformation):
    def __init__(self, factor: float):
        self.factor = factor
        
    def apply(self, points: NDArray[np.float64]) -> NDArray[np.float64]:
        scale_matrix = np.array([
            [self.factor, 0],
            [0, self.factor]
        ])

        return points @ scale_matrix.T