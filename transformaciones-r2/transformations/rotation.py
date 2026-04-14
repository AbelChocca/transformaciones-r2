from transformations.base import Transformation

class Rotation(Transformation):
    def __init__(self, theta: float):
        self.theta = theta
        
    def apply(self, points):
        ...