from transformations.base import Transformation
import numpy as np
from numpy.typing import NDArray

class Rotation(Transformation):
    def __init__(self, theta_degrees: float):
        self.theta = np.radians(theta_degrees)
        
    def apply(self, points: NDArray[np.float64]) -> NDArray[np.float64]:  #Se debe usar np.array, no np.ndarray. np.ndarray es la clase interna de numpy,
        R = np.array([                  #mientras que np.array es la función para crear las matrices. Además da error al ejecutar
            [np.cos(self.theta), -np.sin(self.theta)],
            [np.sin(self.theta), np.cos(self.theta)]
        ])

        return points @ R.T
