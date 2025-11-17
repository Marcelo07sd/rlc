"""
Ventana principal de la aplicación
Contiene la interfaz gráfica y coordina los componentes
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QTextEdit, QSplitter, QMessageBox,
                               QFileDialog, QLabel)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import json

from ui.parameter_form import ParameterForm
from core.rlc_model import RLCModel
from core.laplace_solver import LaplaceSolver
from plots.plotter import Plotter


class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación del simulador RLC
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Circuito RLC en Serie")
        self.setMinimumSize(1200, 800)
        
        # Componentes del modelo
        self.rlc_model = None
        self.laplace_solver = LaplaceSolver()
        self.plotter = Plotter()
        
        self._init_ui()
        
    def _init_ui(self):
        """
        Inicializa la interfaz de usuario
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Título
        title_label = QLabel("🔌 Simulador de Circuito RLC en Serie")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Splitter principal (izquierda: controles, derecha: gráficos)
        splitter = QSplitter(Qt.Horizontal)
        
        # Panel izquierdo: controles
        left_panel = self._create_control_panel()
        splitter.addWidget(left_panel)
        
        # Panel derecho: gráficos
        right_panel = self._create_plot_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([400, 800])
        main_layout.addWidget(splitter)
        
    def _create_control_panel(self):
        """
        Crea el panel de controles (formulario y botones)
        """
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Formulario de parámetros
        self.param_form = ParameterForm()
        layout.addWidget(self.param_form)
        
        # Botones de acción
        btn_layout = QVBoxLayout()
        
        self.btn_simulate = QPushButton("🚀 Simular")
        self.btn_simulate.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.btn_simulate.clicked.connect(self.simulate)
        btn_layout.addWidget(self.btn_simulate)
        
        self.btn_export_plot = QPushButton("💾 Exportar Gráfica")
        self.btn_export_plot.clicked.connect(self.export_plot)
        btn_layout.addWidget(self.btn_export_plot)
        
        self.btn_save_params = QPushButton("📝 Guardar Parámetros")
        self.btn_save_params.clicked.connect(self.save_parameters)
        btn_layout.addWidget(self.btn_save_params)
        
        self.btn_load_params = QPushButton("📂 Cargar Parámetros")
        self.btn_load_params.clicked.connect(self.load_parameters)
        btn_layout.addWidget(self.btn_load_params)
        
        layout.addLayout(btn_layout)
        
        # Área de solución simbólica
        solution_label = QLabel("📊 Solución Simbólica i(t):")
        solution_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(solution_label)
        
        self.solution_text = QTextEdit()
        self.solution_text.setReadOnly(True)
        self.solution_text.setMaximumHeight(150)
        self.solution_text.setPlaceholderText("La solución aparecerá aquí después de la simulación...")
        layout.addWidget(self.solution_text)
        
        layout.addStretch()
        return panel
        
    def _create_plot_panel(self):
        """
        Crea el panel de gráficos
        """
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Figura de matplotlib
        self.figure = Figure(figsize=(10, 8))
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout.addWidget(self.canvas)
        
        return panel
        
    def simulate(self):
        """
        Ejecuta la simulación del circuito RLC
        """
        try:
            # Obtener parámetros del formulario
            params = self.param_form.get_parameters()
            
            # Validar parámetros
            if params['R'] <= 0 or params['L'] <= 0 or params['C'] <= 0:
                QMessageBox.warning(self, "Error", "Los valores de R, L y C deben ser positivos")
                return
            
            # Crear modelo RLC
            self.rlc_model = RLCModel(params['R'], params['L'], params['C'])
            
            # Resolver usando Laplace
            solution = self.laplace_solver.solve(
                self.rlc_model,
                params['signal_type'],
                params['signal_params']
            )
            
            # Mostrar solución simbólica
            self.solution_text.setText(f"i(t) = {solution['symbolic']}")
            
            # Graficar resultados
            self.figure.clear()
            self.plotter.plot_results(
                self.figure,
                solution['time'],
                solution['current'],
                solution['voltage_R'],
                solution['voltage_L'],
                solution['voltage_C'],
                solution['input_signal'],
                params['signal_type']
            )
            self.canvas.draw()
            
            QMessageBox.information(self, "Éxito", "Simulación completada correctamente")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error durante la simulación:\n{str(e)}")
            
    def export_plot(self):
        """
        Exporta la gráfica actual como imagen
        """
        if self.figure.get_axes():
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Exportar Gráfica",
                "",
                "PNG (*.png);;PDF (*.pdf);;SVG (*.svg)"
            )
            
            if filename:
                self.figure.savefig(filename, dpi=300, bbox_inches='tight')
                QMessageBox.information(self, "Éxito", f"Gráfica exportada a:\n{filename}")
        else:
            QMessageBox.warning(self, "Advertencia", "No hay gráfica para exportar. Ejecuta primero una simulación.")
            
    def save_parameters(self):
        """
        Guarda los parámetros actuales en un archivo JSON
        """
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Parámetros",
            "",
            "JSON (*.json)"
        )
        
        if filename:
            params = self.param_form.get_parameters()
            with open(filename, 'w') as f:
                json.dump(params, f, indent=4)
            QMessageBox.information(self, "Éxito", f"Parámetros guardados en:\n{filename}")
            
    def load_parameters(self):
        """
        Carga parámetros desde un archivo JSON
        """
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Cargar Parámetros",
            "",
            "JSON (*.json)"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    params = json.load(f)
                self.param_form.set_parameters(params)
                QMessageBox.information(self, "Éxito", "Parámetros cargados correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar parámetros:\n{str(e)}")