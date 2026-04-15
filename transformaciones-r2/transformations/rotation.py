from transformations.base import Transformation
import numpy as np

class Rotation(Transformation):
    def __init__(self, theta: float):
        self.theta = theta
        
    def apply(self, points: np.ndarray):
        R = np.ndarray([
            [np.cos(self.theta), -np.sin(self.theta)],
            [np.sin(self.theta), np.cos(self.theta)]
        ])

        return points @ R.T