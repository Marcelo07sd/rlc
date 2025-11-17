"""
Módulo para graficar los resultados de la simulación
Utiliza Matplotlib integrado con Qt6
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class Plotter:
    """
    Clase para crear gráficos de las señales del circuito RLC
    """
    
    def __init__(self):
        self.colors = {
            'current': '#2196F3',
            'voltage_R': '#FF5722',
            'voltage_L': '#4CAF50',
            'voltage_C': '#9C27B0',
            'input': '#FF9800'
        }
        
    def plot_results(self, figure, time, current, v_R, v_L, v_C, input_signal, signal_type):
        """
        Crea una figura con múltiples subgráficos mostrando todos los resultados
        
        Args:
            figure: Figura de matplotlib
            time: Vector de tiempo
            current: Corriente del circuito
            v_R, v_L, v_C: Voltajes en R, L y C
            input_signal: Señal de entrada
            signal_type: Tipo de señal de entrada
        """
        # Limpiar figura
        figure.clear()
        
        # Crear subgráficos
        gs = figure.add_gridspec(3, 2, hspace=0.5, wspace=0.3)
        
        # 1. Señal de entrada
        ax1 = figure.add_subplot(gs[0, :])
        self._plot_signal(ax1, time, input_signal, 
                         'Señal de Entrada V(t)', 
                         'Voltaje (V)', 
                         self.colors['input'])
        
        # 2. Corriente del circuito
        ax2 = figure.add_subplot(gs[1, :])
        self._plot_signal(ax2, time, current, 
                         'Corriente del Circuito i(t)', 
                         'Corriente (A)', 
                         self.colors['current'])
        
        # 3. Voltaje en R
        ax3 = figure.add_subplot(gs[2, 0])
        self._plot_signal(ax3, time, v_R, 
                         'Voltaje en Resistencia V_R(t)', 
                         'Voltaje (V)', 
                         self.colors['voltage_R'],
                         small=True)
        
        # 4. Voltajes en L y C superpuestos
        ax4 = figure.add_subplot(gs[2, 1])
        ax4.plot(time * 1000, v_L, label='V_L(t)', 
                color=self.colors['voltage_L'], linewidth=1.5)
        ax4.plot(time * 1000, v_C, label='V_C(t)', 
                color=self.colors['voltage_C'], linewidth=1.5, linestyle='--')
        ax4.set_xlabel('Tiempo (ms)', fontsize=9)
        ax4.set_ylabel('Voltaje (V)', fontsize=9)
        ax4.set_title('Voltajes en L y C', fontsize=10, fontweight='bold')
        ax4.legend(fontsize=8)
        ax4.grid(True, alpha=0.3)
        ax4.tick_params(labelsize=8)
        
        # Ajustar diseño
        figure.tight_layout()
        
    def _plot_signal(self, ax, time, signal, title, ylabel, color, small=False):
        """
        Grafica una señal individual
        
        Args:
            ax: Axes de matplotlib
            time: Vector de tiempo
            signal: Señal a graficar
            title: Título del gráfico
            ylabel: Etiqueta del eje Y
            color: Color de la línea
            small: Si True, usa fuentes más pequeñas
        """
        fontsize_title = 10 if small else 11
        fontsize_label = 9 if small else 10
        fontsize_tick = 8 if small else 9
        
        ax.plot(time * 1000, signal, color=color, linewidth=2)
        ax.set_xlabel('Tiempo (ms)', fontsize=fontsize_label)
        ax.set_ylabel(ylabel, fontsize=fontsize_label)
        ax.set_title(title, fontsize=fontsize_title, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=fontsize_tick)
        
        # Línea en cero para referencia
        ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
        
    def plot_phase_diagram(self, figure, current, voltage):
        """
        Crea un diagrama de fase corriente vs voltaje
        
        Args:
            figure: Figura de matplotlib
            current: Vector de corriente
            voltage: Vector de voltaje
        """
        figure.clear()
        ax = figure.add_subplot(111)
        
        ax.plot(voltage, current, color=self.colors['current'], linewidth=2)
        ax.set_xlabel('Voltaje (V)', fontsize=11)
        ax.set_ylabel('Corriente (A)', fontsize=11)
        ax.set_title('Diagrama de Fase: Corriente vs Voltaje', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Marcar punto inicial y final
        ax.plot(voltage[0], current[0], 'go', markersize=8, label='Inicio')
        ax.plot(voltage[-1], current[-1], 'ro', markersize=8, label='Final')
        ax.legend()
        
        figure.tight_layout()
        
    def plot_frequency_response(self, figure, frequencies, impedances):
        """
        Grafica la respuesta en frecuencia del circuito
        
        Args:
            figure: Figura de matplotlib
            frequencies: Vector de frecuencias
            impedances: Vector de impedancias complejas
        """
        figure.clear()
        
        # Magnitud
        ax1 = figure.add_subplot(211)
        magnitude = np.abs(impedances)
        ax1.semilogx(frequencies, magnitude, color=self.colors['current'], linewidth=2)
        ax1.set_ylabel('|Z| (Ω)', fontsize=10)
        ax1.set_title('Respuesta en Frecuencia', fontsize=11, fontweight='bold')
        ax1.grid(True, which='both', alpha=0.3)
        
        # Fase
        ax2 = figure.add_subplot(212)
        phase = np.angle(impedances, deg=True)
        ax2.semilogx(frequencies, phase, color=self.colors['voltage_L'], linewidth=2)
        ax2.set_xlabel('Frecuencia (Hz)', fontsize=10)
        ax2.set_ylabel('Fase (°)', fontsize=10)
        ax2.grid(True, which='both', alpha=0.3)
        
        figure.tight_layout()