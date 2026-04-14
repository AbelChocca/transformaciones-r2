from transformations.base import Transformation

class Scale(Transformation):
    def __init__(self, factor: float):
        self.factor = factor
        
    def apply(self, points):
        ...