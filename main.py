"""Punto de entrada del prototipo académico. Ejecutar: python main.py"""
from residencias.frameworks.consola import ejecutar_consola


if __name__ == "__main__":
    try:
        ejecutar_consola()
    except (KeyboardInterrupt, EOFError):
        print("\nSimulación finalizada.")
