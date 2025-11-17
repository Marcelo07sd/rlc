"""
Formulario para ingresar parámetros del circuito RLC y seleccionar señales
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QComboBox, QGroupBox, QFormLayout)
from PySide6.QtCore import Qt


class ParameterForm(QWidget):
    """
    Widget que contiene el formulario de parámetros del circuito y señales
    """
    
    def __init__(self):
        super().__init__()
        self._init_ui()
        
    def _init_ui(self):
        """
        Inicializa la interfaz del formulario
        """
        layout = QVBoxLayout(self)
        
        # Grupo de parámetros del circuito
        circuit_group = QGroupBox("⚡ Parámetros del Circuito")
        circuit_layout = QFormLayout()
        
        self.r_input = QLineEdit("100")
        self.r_input.setPlaceholderText("Resistencia en Ω")
        circuit_layout.addRow("Resistencia R (Ω):", self.r_input)
        
        self.l_input = QLineEdit("0.1")
        self.l_input.setPlaceholderText("Inductancia en H")
        circuit_layout.addRow("Inductancia L (H):", self.l_input)
        
        self.c_input = QLineEdit("0.00001")
        self.c_input.setPlaceholderText("Capacitancia en F")
        circuit_layout.addRow("Capacitancia C (F):", self.c_input)
        
        circuit_group.setLayout(circuit_layout)
        layout.addWidget(circuit_group)
        
        # Grupo de señales de entrada
        signal_group = QGroupBox("📡 Señal de Entrada")
        signal_layout = QVBoxLayout()
        
        # Selector de tipo de señal
        signal_type_layout = QFormLayout()
        self.signal_combo = QComboBox()
        self.signal_combo.addItems([
            "Escalón U(t)",
            "Pulso U(t) - U(t-a)",
            "Rampa t·U(t)",
            "Señal Retardada U(t-t0)",
            "Impulso δ(t)"
        ])
        self.signal_combo.currentIndexChanged.connect(self._on_signal_changed)
        signal_type_layout.addRow("Tipo de señal:", self.signal_combo)
        signal_layout.addLayout(signal_type_layout)
        
        # Parámetros específicos de la señal
        self.signal_params_layout = QFormLayout()
        
        # Amplitud (común para todas)
        self.amplitude_input = QLineEdit("10")
        self.amplitude_input.setPlaceholderText("Amplitud en V")
        self.signal_params_layout.addRow("Amplitud (V):", self.amplitude_input)
        
        # Parámetro 'a' para pulso
        self.param_a_label = QLabel("Duración a (s):")
        self.param_a_input = QLineEdit("0.001")
        self.param_a_input.setPlaceholderText("Duración del pulso")
        self.signal_params_layout.addRow(self.param_a_label, self.param_a_input)
        
        # Parámetro 't0' para retardo
        self.param_t0_label = QLabel("Retardo t0 (s):")
        self.param_t0_input = QLineEdit("0.001")
        self.param_t0_input.setPlaceholderText("Tiempo de retardo")
        self.signal_params_layout.addRow(self.param_t0_label, self.param_t0_input)
        
        signal_layout.addLayout(self.signal_params_layout)
        signal_group.setLayout(signal_layout)
        layout.addWidget(signal_group)
        
        # Inicializar visibilidad de parámetros
        self._on_signal_changed(0)
        
    def _on_signal_changed(self, index):
        """
        Actualiza la visibilidad de los parámetros según la señal seleccionada
        """
        # Ocultar todos los parámetros específicos
        self.param_a_label.hide()
        self.param_a_input.hide()
        self.param_t0_label.hide()
        self.param_t0_input.hide()
        
        # Mostrar según el tipo de señal
        if index == 1:  # Pulso
            self.param_a_label.show()
            self.param_a_input.show()
        elif index == 3:  # Señal Retardada
            self.param_t0_label.show()
            self.param_t0_input.show()
            
    def get_parameters(self):
        """
        Obtiene todos los parámetros del formulario
        
        Returns:
            dict: Diccionario con todos los parámetros
        """
        signal_types = ['step', 'pulse', 'ramp', 'delayed', 'impulse']
        signal_index = self.signal_combo.currentIndex()
        
        params = {
            'R': float(self.r_input.text()),
            'L': float(self.l_input.text()),
            'C': float(self.c_input.text()),
            'signal_type': signal_types[signal_index],
            'signal_params': {
                'amplitude': float(self.amplitude_input.text())
            }
        }
        
        # Agregar parámetros específicos según el tipo de señal
        if signal_index == 1:  # Pulso
            params['signal_params']['a'] = float(self.param_a_input.text())
        elif signal_index == 3:  # Retardada
            params['signal_params']['t0'] = float(self.param_t0_input.text())
            
        return params
        
    def set_parameters(self, params):
        """
        Establece los parámetros en el formulario
        
        Args:
            params (dict): Diccionario con los parámetros a establecer
        """
        self.r_input.setText(str(params['R']))
        self.l_input.setText(str(params['L']))
        self.c_input.setText(str(params['C']))
        
        # Establecer tipo de señal
        signal_types = ['step', 'pulse', 'ramp', 'delayed', 'impulse']
        if params['signal_type'] in signal_types:
            index = signal_types.index(params['signal_type'])
            self.signal_combo.setCurrentIndex(index)
            
        # Establecer parámetros de la señal
        if 'signal_params' in params:
            sp = params['signal_params']
            if 'amplitude' in sp:
                self.amplitude_input.setText(str(sp['amplitude']))
            if 'a' in sp:
                self.param_a_input.setText(str(sp['a']))
            if 't0' in sp:
                self.param_t0_input.setText(str(sp['t0']))