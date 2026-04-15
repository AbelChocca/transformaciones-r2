import matplotlib.pyplot as plt
import numpy as np

class Renderer:
    def draw(self, points):
        closed_points = np.vstack([points, points[0]])

        plt.figure(figsize = (6, 6))
        plt.title("Vizualización de Transformaciones")

        plt.plot(closed_points[:, 0], closed_points[:, 1], 'b-o', label = 'Figura Original')

        plt.axhline(0, color = 'black', linewidth = 1)
        plt.axvline(0, color = 'black', linewidth = 1)
        plt.grid('equal')
        plt.legend()

        plt.show()
