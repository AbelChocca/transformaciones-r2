# animations/animate.py
import numpy as np
from matplotlib.ticker import MaxNLocator, FormatStrFormatter

def animate(ax, points: np.ndarray, transformed_points: np.ndarray, steps=40, canvas=None):
    ax.clear()

    ax.set_title("Animación de Transformaciones en ℝ²")
    ax.set_aspect('equal')

    # 🔥 calcular límites dinámicos (esto era CLAVE)
    todos = np.vstack((points, transformed_points))
    x_min, x_max = todos[:, 0].min(), todos[:, 0].max()
    y_min, y_max = todos[:, 1].min(), todos[:, 1].max()
    margen = 1.0

    ax.set_xlim(x_min - margen, x_max + margen)
    ax.set_ylim(y_min - margen, y_max + margen)

    ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    ax.axhline(0, color='black', linewidth=1.2)
    ax.axvline(0, color='black', linewidth=1.2)
    ax.grid(True, linestyle='--', alpha=0.7)

    # figura original
    orig = np.vstack([points, points[0]])
    ax.plot(orig[:, 0], orig[:, 1], 'b--', label="Original", alpha=0.6)

    line, = ax.plot([], [], 'r-o', label="Transformada", linewidth=2)
    ax.legend()

    # 🎬 animación
    for i in range(steps + 1):
        t = i / steps
        current = points * (1 - t) + transformed_points * t
        curr = np.vstack([current, current[0]])

        line.set_data(curr[:, 0], curr[:, 1])

        if canvas:
            canvas.draw()
            from PyQt6.QtWidgets import QApplication
            QApplication.processEvents()
        else:
            import matplotlib.pyplot as plt
            plt.pause(0.03)