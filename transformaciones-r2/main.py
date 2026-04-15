import numpy as np

from transformations.rotation import Rotation
from transformations.scale import Scale
from transformations.reflection import Reflection
from render.renderer import Renderer

#from animation.animator import animate


def menu():
    print("\n=== TRANSFORMACIONES EN ℝ² ===")
    print("1. Rotación")
    print("2. Escalado (Homotecia)")
    print("3. Reflexión")
    return input("Elige opción: ")


def main():
    # figura base en ℝ²
    points = np.array([
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1]
    ])

    option = menu()

    transformation = None

    if option == "1":
        theta = float(input("Ángulo (rad): "))
        transformation = Rotation(theta)

    elif option == "2":
        factor = float(input("Factor de escala: "))
        transformation = Scale(factor)

    elif option == "3":
        transformation = Reflection()

    else:
        print("Opción inválida ❌")
        return

    renderer = Renderer()

    print("\nMostrando figura original...")
    print("(Nota: Las transformaciones se verán cuando las fórmulas estén listas)")

    renderer.draw(points)
    # conexión total del sistema
    # animate(transformation, renderer, points)


if __name__ == "__main__":
    main()
