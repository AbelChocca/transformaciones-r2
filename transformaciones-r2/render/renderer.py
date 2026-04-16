from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

class Renderer:
    # class Renderer: Esto daba error
    def draw(self, original_pts, transformed_pts = None):

        fig, ax = plt.figure(figsize = (7, 7))
        plt.title("Vizualización de Transformaciones")

        orig = np.vstack([original_pts, original_pts[0]])
        plt.plot(orig[:, 0], orig[:, 1], 'b--', label = "Original", alpha = 0.6)

        if transformed_pts is not None:
            trans = np.vstack([transformed_pts, transformed_pts[0]])
            plt.plot(trans[:, 0], trans[:, 1], "r-o", label = 'Transformada', linewidth = 2)
    
        ax.xaxis.set_major_locator(MultipleLocator(0.25))
        ax.yaxis.set_major_locator(MultipleLocator(0.25))
        plt.axhline(0, color = 'black', linewidth = 1.3)
        plt.axvline(0, color = 'black', linewidth = 1.3)
        plt.grid(True, linestyle = '--', which='major', alpha=0.7)
        plt.axis('equal')
        plt.legend()

        plt.show()
