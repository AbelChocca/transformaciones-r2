import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QComboBox, QPushButton
)

from core.geometry import get_figure
from ui.canvas import Canvas

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editor 2D - Transformaciones")
        self.setGeometry(100, 100, 1000, 700)

        # ======================
        # 🧠 STATE
        # ======================
        self.current_figure = "Cuadrado"

        # ======================
        # 🎨 CANVAS
        # ======================
        base = get_figure(self.current_figure)
        self.canvas = Canvas(base)

        self.init_ui()

    # ======================
    # UI
    # ======================
    def init_ui(self):
        layout = QVBoxLayout()

        # ======================
        # TOOLBAR
        # ======================
        toolbar = QHBoxLayout()

        # FIGURAS
        self.figure_combo = QComboBox()
        self.figure_combo.addItems(["Cuadrado", "Triángulo", "Rectángulo", "L"])
        self.figure_combo.currentTextChanged.connect(self.change_figure)

        toolbar.addWidget(QLabel("Figura:"))
        toolbar.addWidget(self.figure_combo)

        # REFLEXIÓN
        self.reflection_btn = QPushButton("Reflexión")
        self.reflection_btn.clicked.connect(self.apply_reflection)

        toolbar.addWidget(self.reflection_btn)

        layout.addLayout(toolbar)

        # ======================
        # CANVAS
        # ======================
        layout.addWidget(self.canvas.canvas)

        self.setLayout(layout)

    # ======================
    # LOGIC
    # ======================
    def change_figure(self, name):
        self.current_figure = name

        new_points = get_figure(name)

        self.canvas.base_points = new_points.copy()
        self.canvas.active_points = new_points.copy()

        self.canvas.draw()

    def apply_reflection(self):
        theta = 0.5  # ejemplo fijo o luego input
        self.canvas.apply_reflection(theta)