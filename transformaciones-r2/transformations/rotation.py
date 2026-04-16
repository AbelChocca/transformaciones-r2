from transformations.base import Transformation
import numpy as np

class Rotation(Transformation):
    def __init__(self, theta: float):
        self.theta = theta
        
    def apply(self, points: np.array) -> np.array:  #Se debe usar np.array, no np.ndarray. np.ndarray es la clase interna de numpy,
        R = np.array([                  #mientras que np.array es la función para crear las matrices. Además da error al ejecutar
            [np.cos(self.theta), -np.sin(self.theta)],
            [np.sin(self.theta), np.cos(self.theta)]
        ])

        return points @ R.T
