from abc import ABC, abstractmethod
import numpy as np

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