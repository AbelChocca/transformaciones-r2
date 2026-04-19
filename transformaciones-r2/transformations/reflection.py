import numpy as np
from numpy.typing import NDArray
from transformations.base import Transformation

class Reflection(Transformation):
    def __init__(self, theta):
        self.theta = theta  # ángulo en radianes

    def apply(self, points: NDArray[np.float64]):
        # Matriz de reflexión
        cos_2t = np.cos(2 * self.theta)
        sin_2t = np.sin(2 * self.theta)

        reflection_matrix = np.array([
            [cos_2t, sin_2t],
            [sin_2t, -cos_2t]
        ])

        # Aplicar transformación
        return np.dot(points, reflection_matrix.T)