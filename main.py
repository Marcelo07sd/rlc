"""
Simulador de Circuito RLC en Serie
Punto de entrada de la aplicación
"""

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """
    Función principal que inicializa la aplicación Qt
    """
    app = QApplication(sys.argv)
    app.setApplicationName("Simulador RLC")
    app.setOrganizationName("RLC Simulator")
    
    # Crear y mostrar la ventana principal
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()