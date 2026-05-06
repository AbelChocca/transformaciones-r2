# geometry.py
import numpy as np

# =========================
# 🧱 FIGURAS BASE
# =========================

def square():
    return np.array([
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1]
    ], dtype=float)


def triangle():
    return np.array([
        [0, 0],
        [1, 0],
        [0.5, 1]
    ], dtype=float)


def rectangle():
    return np.array([
        [0, 0],
        [2, 0],
        [2, 1],
        [0, 1]
    ], dtype=float)


def letter_l():
    return np.array([
        [0, 0],
        [2, 0],
        [2, 1],
        [1, 1],
        [1, 2],
        [0, 2]
    ], dtype=float)


# =========================
# 🎯 FACTORY DE FIGURAS
# =========================

FIGURES = {
    "Cuadrado": square,
    "Triángulo": triangle,
    "Rectángulo": rectangle,
    "L": letter_l
}


def get_figure(name: str) -> np.ndarray:
    """
    Devuelve la figura solicitada.
    Siempre retorna una copia independiente.
    """
    if name not in FIGURES:
        return np.array([[0, 0]], dtype=float)

    return FIGURES[name]().copy()


# =========================
# 🧠 HELPERS GEOMÉTRICOS
# =========================

def centroid(points: np.ndarray) -> np.ndarray:
    """
    Centro geométrico (para rotaciones futuras).
    """
    return np.mean(points, axis=0)


def translate_to_origin(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Mueve figura al origen y devuelve (transformed, centroid).
    """
    c = centroid(points)
    return points - c, c


def restore_from_origin(points: np.ndarray, centroid: np.ndarray) -> np.ndarray:
    """
    Devuelve figura a su posición original.
    """
    return points + centroid