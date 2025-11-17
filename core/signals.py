"""
Módulo para generar diferentes tipos de señales de entrada
Incluye implementaciones simbólicas y numéricas
"""

import numpy as np
import sympy as sp


class SignalGenerator:
    """
    Generador de señales para el circuito RLC
    Implementa señales por tramos: escalón, pulso, rampa, retardos, impulso
    """
    
    def __init__(self):
        self.t = sp.Symbol('t', real=True, positive=True)
        
    def generate_signal(self, signal_type, params, time_array):
        """
        Genera una señal numérica para un vector de tiempo dado
        
        Args:
            signal_type (str): Tipo de señal
            params (dict): Parámetros de la señal
            time_array (np.array): Vector de tiempo
            
        Returns:
            np.array: Señal evaluada en los puntos de tiempo
        """
        if signal_type == 'step':
            return self._step_signal(params, time_array)
        elif signal_type == 'pulse':
            return self._pulse_signal(params, time_array)
        elif signal_type == 'ramp':
            return self._ramp_signal(params, time_array)
        elif signal_type == 'delayed':
            return self._delayed_signal(params, time_array)
        elif signal_type == 'impulse':
            return self._impulse_signal(params, time_array)
        else:
            raise ValueError(f"Tipo de señal no reconocido: {signal_type}")
            
    def _step_signal(self, params, t):
        """
        Señal escalón: A·U(t)
        
        U(t) = 0 para t < 0
        U(t) = 1 para t >= 0
        """
        A = params.get('amplitude', 1)
        return A * np.ones_like(t)
        
    def _pulse_signal(self, params, t):
        """
        Señal pulso: A·[U(t) - U(t-a)]
        
        Pulso rectangular de amplitud A y duración a
        """
        A = params.get('amplitude', 1)
        a = params.get('a', 0.001)
        
        signal = np.zeros_like(t)
        signal[t >= 0] = A
        signal[t >= a] = 0
        
        return signal
        
    def _ramp_signal(self, params, t):
        """
        Señal rampa: A·t·U(t)
        
        Señal que crece linealmente con el tiempo
        """
        A = params.get('amplitude', 1)
        
        signal = np.zeros_like(t)
        signal[t >= 0] = A * t[t >= 0]
        
        return signal
        
    def _delayed_signal(self, params, t):
        """
        Señal retardada: A·U(t-t0)
        
        Escalón que comienza en t = t0
        """
        A = params.get('amplitude', 1)
        t0 = params.get('t0', 0.001)
        
        signal = np.zeros_like(t)
        signal[t >= t0] = A
        
        return signal
        
    def _impulse_signal(self, params, t):
        """
        Impulso de Dirac: A·δ(t)
        
        Simulado numéricamente como un pulso muy estrecho de área A
        """
        A = params.get('amplitude', 1)
        dt = t[1] - t[0] if len(t) > 1 else 0.0001
        
        # Crear un pulso muy estrecho centrado en t=0
        width = dt * 2  # Ancho del pulso
        height = A / width  # Altura para mantener área = A
        
        signal = np.zeros_like(t)
        signal[np.abs(t) < width/2] = height
        
        return signal
        
    # Métodos simbólicos para referencia
    def heaviside(self, t_expr):
        """
        Función escalón de Heaviside simbólica
        """
        return sp.Heaviside(t_expr)
        
    def step_symbolic(self, amplitude=1):
        """
        Escalón simbólico: A·U(t)
        """
        return amplitude * self.heaviside(self.t)
        
    def pulse_symbolic(self, amplitude=1, a=1):
        """
        Pulso simbólico: A·[U(t) - U(t-a)]
        """
        return amplitude * (self.heaviside(self.t) - self.heaviside(self.t - a))
        
    def ramp_symbolic(self, amplitude=1):
        """
        Rampa simbólica: A·t·U(t)
        """
        return amplitude * self.t * self.heaviside(self.t)
        
    def delayed_symbolic(self, amplitude=1, t0=0):
        """
        Señal retardada simbólica: A·U(t-t0)
        """
        return amplitude * self.heaviside(self.t - t0)
        
    def impulse_symbolic(self, amplitude=1):
        """
        Impulso de Dirac simbólico: A·δ(t)
        """
        return amplitude * sp.DiracDelta(self.t)