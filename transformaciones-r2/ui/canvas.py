import numpy as np
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from core.transformations import Rotation
from core.transformations import Scale
from core.transformations import Reflection
from core.geometry import centroid

def bounding_box(points: np.ndarray):
    min_x, min_y = np.min(points, axis=0)
    max_x, max_y = np.max(points, axis=0)

    return np.array([
        [min_x, min_y],
        [max_x, min_y],
        [max_x, max_y],
        [min_x, max_y]
    ])

class Canvas(QWidget):
    def __init__(self, base_points):
        super().__init__()

        # ======================
        # 🧠 STATE
        # ======================
        self.base_points = base_points.copy()
        self.active_points = base_points.copy()

        # ======================
        # 🎨 MATPLOTLIB
        # ======================
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("motion_notify_event", self.on_move)
        self.canvas.mpl_connect("button_release_event", self.on_release)

        self.selected_vertex = None
        self.handle_radius = 0.15

        self.rotating = False
        self.rotation_handle_radius = 0.2

        self.selected_corner = None
        self.scale_start_points = None

        self.init_plot()
    # ======================
    # SETUP
    # ======================
    def init_plot(self):
        self.ax.set_title("Transformaciones ℝ²")
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        self.draw()

    # ======================
    # RENDER
    # ======================
    def draw(self):
        self.ax.clear()

        # BASE 
        base = np.vstack([self.base_points, self.base_points[0]])
        self.ax.plot(base[:, 0], base[:, 1], 'gray', linestyle="--", alpha=0.5)

        # ACTIVA
        active = np.vstack([self.active_points, self.active_points[0]])
        self.ax.plot(active[:, 0], active[:, 1], 'r-o', linewidth=2)

        # =========================
        # BOUNDING BOX (PASO 1)
        # =========================
        box = bounding_box(self.active_points)
        box = np.vstack([box, box[0]])

        self.ax.plot(
            box[:, 0],
            box[:, 1],
            color='white',
            linestyle='--',
            linewidth=1.5,
            alpha=0.9
        )

        # VÉRTICES
        for i, p in enumerate(self.active_points):
            self.ax.scatter(
                p[0],
                p[1],
                s=60,              # tamaño del punto
                color='white',
                edgecolors='black',
                zorder=5,
                marker='o'
            )

        # =========================
        # ROTATION HANDLE
        # =========================
        handle = self.get_rotation_handle()
        self.ax.scatter(
            handle[0],
            handle[1],
            s=80,
            color='yellow',
            edgecolors='black',
            zorder=6
        )

        self.ax.plot(
            [centroid(self.active_points)[0], handle[0]],
            [centroid(self.active_points)[1], handle[1]],
            'yellow',
            linestyle='dotted'
        )

        self.ax.set_aspect('equal')
        self.ax.grid(True)

        self.canvas.draw()

    # ======================
    # INPUT
    # ======================
    def on_press(self, event):
        if event.xdata is None:
            return

        mouse = np.array([event.xdata, event.ydata])

        # 🔁 ROTATION
        if self.is_near(mouse, self.get_rotation_handle()):
            self.rotating = True
            self.last_mouse = mouse
            return

        # 📐 SCALE
        self.selected_corner = self.get_corner_index(mouse)
        if self.selected_corner is not None:
            self.scale_start_points = self.active_points.copy()
            return

        # ⚪ VERTEX EDIT
        self.selected_vertex = self.get_handle_index(mouse)
        return

    def on_move(self, event):
        if event.xdata is None:
            return

        mouse = np.array([event.xdata, event.ydata])

        # SCALE
        if self.selected_corner is not None:
            box = bounding_box(self.scale_start_points)
            center = centroid(self.scale_start_points)

            corner = box[self.selected_corner]

            sx = (mouse[0] - center[0]) / (corner[0] - center[0] + 1e-6)
            sy = (mouse[1] - center[1]) / (corner[1] - center[1] + 1e-6)

            S = np.array([[sx, 0], [0, sy]])

            pts = self.scale_start_points - center
            self.active_points = (pts @ S.T) + center

            self.draw()
            return

        # ROTATION
        if self.rotating:
            c = centroid(self.active_points)

            v1 = self.last_mouse - c
            v2 = mouse - c

            angle = np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0])

            R = Rotation(np.degrees(angle))

            pts = self.active_points - c
            self.active_points = R.apply(pts) + c

            self.last_mouse = mouse
            self.draw()
            return

        # VERTEX
        if self.selected_vertex is not None:
            self.active_points[self.selected_vertex] = mouse
            self.draw()

    def on_release(self, event):
        self.is_dragging = False
        self.selected_vertex = None
        self.rotating = False
        self.selected_corner = None
        self.scale_start_points = None

    # ======================
    # 🧠 TRANSFORMACIONES
    # ======================
    def translate(self, dx, dy):
        self.active_points += np.array([dx, dy])

    def rotate(self, dx):
        angle = dx * 5  # sensibilidad

        R = Rotation(angle)

        c = centroid(self.active_points)
        pts = self.active_points - c
        pts = R.apply(pts)

        self.active_points = pts + c

    def scale(self, dx):
        factor = 1 + dx

        S = Scale(factor)

        c = centroid(self.active_points)
        pts = self.active_points - c
        pts = S.apply(pts)

        self.active_points = pts + c

    # ======================
    # REFLEXIÓN
    # ======================
    def apply_reflection(self, theta=0.0):
        R = Reflection(theta)

        c = centroid(self.active_points)
        pts = self.active_points - c
        self.active_points = R.apply(pts) + c

        self.draw()

    def get_handle_index(self, mouse_pos):
        mouse = mouse_pos

        for i, p in enumerate(self.active_points):
            if np.linalg.norm(p - mouse) < self.handle_radius:
                return i

        return None
    
    def get_rotation_handle(self):
        c = centroid(self.active_points)
        return np.array([c[0], c[1] + 1.0])  # offset vertical
    
    def is_near(self, a, b, threshold=0.2):
        return np.linalg.norm(a - b) < threshold


    def check_rotation_handle(self, mouse):
        handle = self.get_rotation_handle()
        return self.is_near(mouse, handle)
    
    def get_corner_index(self, mouse):
        box = bounding_box(self.active_points)

        for i, corner in enumerate(box):
            if np.linalg.norm(corner - mouse) < 0.2:
                return i

        return None