import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QPushButton
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from transformations.rotation import Rotation
from transformations.scale import Scale
from transformations.reflection import Reflection
from animations.animation import animate

def get_figure(name: str):
    if name == "Cuadrado":
        return np.array([
            [0, 0],
            [1, 0],
            [1, 1],
            [0, 1]
        ])

    elif name == "Triángulo":
        return np.array([
            [0, 0],
            [1, 0],
            [0.5, 1]
        ])

    elif name == "Rectángulo":
        return np.array([
            [0, 0],
            [2, 0],
            [2, 1],
            [0, 1]
        ])

    elif name == "L":
        return np.array([
            [0,0],[2,0],[2,1],[1,1],[1,2],[0,2]
        ])

    return np.array([[0,0]])


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Transformaciones en ℝ²")
        self.setGeometry(100, 100, 900, 700)

        # figura base
        self.points = np.array([
            [0, 0],
            [1, 0],
            [1, 1],
            [0, 1]
        ])

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 🔽 Selector de transformación
        self.combo = QComboBox()
        self.combo.addItems(["Rotación", "Escala", "Reflexión"])
        self.combo.currentTextChanged.connect(self.update_inputs)

        layout.addWidget(QLabel("Tipo de Transformación"))
        layout.addWidget(self.combo)

        self.figure_combo = QComboBox()
        self.figure_combo.addItems(["Cuadrado", "Triángulo", "Rectángulo", "L"])
        self.figure_combo.currentTextChanged.connect(self.change_figure)

        layout.addWidget(QLabel("Figura"))
        layout.addWidget(self.figure_combo)

        # 🔧 Inputs dinámicos
        self.input_layout = QHBoxLayout()
        layout.addLayout(self.input_layout)

        # botón
        self.btn = QPushButton("Transformar")
        self.btn.clicked.connect(self.apply_transformation)
        layout.addWidget(self.btn)

        # Matplotlib embebido
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        self.update_inputs()

    # Cambia inputs según transformación
    def update_inputs(self):
        # limpiar layout
        for i in reversed(range(self.input_layout.count())):
            self.input_layout.itemAt(i).widget().setParent(None)

        self.inputs = {}

        t = self.combo.currentText()

        if t == "Rotación":
            self.add_input("theta", "Ángulo (°)")

        elif t == "Escala":
            self.add_input("kx", "kx")
            self.add_input("ky", "ky (opcional)")

        elif t == "Reflexión":
            self.add_input("axis", "Eje (x / y)")

    def add_input(self, key, label):
        lbl = QLabel(label)
        inp = QLineEdit()
        self.input_layout.addWidget(lbl)
        self.input_layout.addWidget(inp)
        self.inputs[key] = inp

    def change_figure(self):
        name = self.figure_combo.currentText()
        self.points = get_figure(name)

        # opcional: dibujar inmediatamente
        self.ax.clear()
        pts = np.vstack([self.points, self.points[0]])
        self.ax.plot(pts[:, 0], pts[:, 1], 'b-o')
        self.canvas.draw()

    # 🔥 Aplicar transformación
    def apply_transformation(self):
        t = self.combo.currentText()
        transformation = None

        try:
            if t == "Rotación":
                theta = float(self.inputs["theta"].text())
                transformation = Rotation(theta)

            elif t == "Escala":
                kx = float(self.inputs["kx"].text())
                ky_text = self.inputs["ky"].text()

                if ky_text == "":
                    transformation = Scale(kx)
                else:
                    transformation = Scale(kx, float(ky_text))

            elif t == "Reflexión":
                axis = self.inputs["axis"].text().lower()
                transformation = Reflection(axis)

        except:
            print("Error en inputs ❌")
            return

        transformed = transformation.apply(self.points)

        animate(self.ax, self.points, transformed, canvas=self.canvas)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())