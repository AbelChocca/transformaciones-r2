import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

def animate(points: np.ndarray, transformed_points: np.ndarray, steps = 40):

    fig, ax = plt.subplots(figsize = (7.3, 7.3))
    plt.title("Animación de Transformaciones en ℝ²")

    ax.set_aspect('equal')

    todos_los_puntos = np.vstack((points, transformed_points))
    x_min, x_max = todos_los_puntos[:, 0].min(), todos_los_puntos[:, 0].max()
    y_min, y_max = todos_los_puntos[:, 1].min(), todos_los_puntos[:, 1].max()
    margen = 1.0

    ax.set_xlim(x_min - margen, x_max + margen)
    ax.set_ylim(y_min - margen, y_max + margen)

    ancho_total = (x_max + margen) -(x_min - margen)

    if ancho_total > 10:
        paso = 1.0    
        paso = 0.5    
    else:
        paso = 0.25
    
    ax.xaxis.set_major_locator(MultipleLocator(paso))
    ax.yaxis.set_major_locator(MultipleLocator(paso))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    plt.axhline(0, color='black', linewidth=1.3)
    plt.axvline(0, color='black', linewidth=1.3)
    plt.grid(True, linestyle='--', which='major', alpha=0.7)

    orig = np.vstack([points, points[0]])
    ax.plot(orig[:, 0], orig[:, 1], 'b--', label="Original", alpha=0.6)
    line, = ax.plot([], [], 'r-o', label='Transformada', linewidth=2)
    plt.legend()

    plt.ion()
    plt.show()
    plt.pause(1.0)

    for i in range(steps + 1):
        t = i / steps
        
        current_pts = points * (1 - t) + transformed_points * t
        curr = np.vstack([current_pts, current_pts[0]])
        line.set_data(curr[:, 0], curr[:, 1])
        plt.pause(0.03)

    plt.ioff()
    plt.show()

