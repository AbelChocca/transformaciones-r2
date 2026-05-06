from abc import ABC, abstractmethod
import numpy as np
from numpy.typing import NDArray

class Transformation(ABC):
    """
    Clase base abstracta para todas las transformaciones en R².
    
    Todas las transformaciones deben recibir un array de puntos (Nx2)
    y devolver otro array de puntos transformados (Nx2).
    """

    @abstractmethod
    def apply(self, points: np.ndarray) -> np.ndarray:
        """
        Aplica la transformación a un conjunto de puntos.

        Parameters:
        -----------
        points : np.ndarray
            Array de forma (N, 2) representando puntos en ℝ².

        Returns:
        --------
        np.ndarray
            Nuevos puntos transformados (N, 2).
        """
        pass

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

class Rotation(Transformation):
    def __init__(self, theta_degrees: float):
        self.theta = np.radians(theta_degrees)
        
    def apply(self, points: NDArray[np.float64]) -> NDArray[np.float64]:  #Se debe usar np.array, no np.ndarray. np.ndarray es la clase interna de numpy,
        R = np.array([                  #mientras que np.array es la función para crear las matrices. Además da error al ejecutar
            [np.cos(self.theta), -np.sin(self.theta)],
            [np.sin(self.theta), np.cos(self.theta)]
        ])

        return points @ R.T
    
class Scale(Transformation):
    def __init__(self, kx: float, ky: float | None = None):
        self.kx = kx
        self.ky = ky if ky is not None else kx  # uniforme si no se pasa ky
        
    def apply(self, points: NDArray[np.float64]) -> NDArray[np.float64]:
        scale_matrix = np.array([
            [self.kx, 0],
            [0, self.ky]
        ])

        return points @ scale_matrix.T