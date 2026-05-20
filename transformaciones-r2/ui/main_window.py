import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QMessageBox
)

from core.geometry import get_figure
from ui.canvas import Canvas
import numpy as np

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

        #Homotecia
        self.k_input = QLineEdit()
        self.k_input.setPlaceholderText("Factor k (ej: 2.0)")
        self.k_btn = QPushButton("Aplicar Homotecia")
        self.k_btn.clicked.connect(self.apply_homothety)

        toolbar.addWidget(QLabel("Homotecia (k):"))
        toolbar.addWidget(self.k_input)
        toolbar.addWidget(self.k_btn)
        
        # REFLEXIÓN
        toolbar.addWidget(QLabel("Eje de Reflexión:"))
        
        self.refl_combo = QComboBox()
        self.refl_combo.addItems(["Eje X", "Eje Y", "Recta y=x", "Recta y=-x"])
        toolbar.addWidget(self.refl_combo)

        self.reflection_btn = QPushButton("Reflejar")
        self.reflection_btn.clicked.connect(self.apply_reflection)
        toolbar.addWidget(self.reflection_btn)

        self.reset_btn =QPushButton("Restablecer")
        self.reset_btn.clicked.connect(self.reset_canvas)
        toolbar.addWidget(self.reset_btn)
        
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
        tipo = self.refl_combo.currentText()
        
        if tipo == "Eje X":
            theta = 0.0        #0 grados
        elif tipo == "Eje Y":
            theta = np.pi / 2  #90 grados
        elif tipo == "Recta y=x":
            theta = np.pi / 4  #45 grados
        elif tipo == "Recta y=-x":
            theta = -np.pi / 4 #-45 grados
        else:
            theta = 0.0

        self.canvas.apply_reflection(theta)
        
    def apply_homothety(self):
        try:
            k = float(self.k_input.text())
            if abs(k) < 0.0001:
                QMessageBox.warning(self, "Error", "El factor k no puede ser cero porque la figura desaparecería")
                return
            self.canvas.homothety(k)
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingresa un número válido para el factor k")
            
    def reset_canvas(self):
        self.canvas.reset_transformations()
        
