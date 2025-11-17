"""
Modelo matemático del circuito RLC en serie
"""

import numpy as np


class RLCModel:
    """
    Representa un circuito RLC en serie
    
    Ecuación diferencial del circuito:
    L·di/dt + R·i + (1/C)·∫i·dt = V(t)
    
    Aplicando la transformada de Laplace:
    L·s·I(s) + R·I(s) + I(s)/(s·C) = V(s)
    I(s) = V(s) / [R + s·L + 1/(s·C)]
    """
    
    def __init__(self, R, L, C):
        """
        Inicializa el circuito RLC
        
        Args:
            R (float): Resistencia en Ohmios (Ω)
            L (float): Inductancia en Henrios (H)
            C (float): Capacitancia en Faradios (F)
        """
        self.R = R
        self.L = L
        self.C = C
        
        # Calcular parámetros característicos
        self._calculate_characteristic_params()
        
    def _calculate_characteristic_params(self):
        """
        Calcula los parámetros característicos del circuito
        """
        # Frecuencia natural de oscilación
        self.omega_0 = 1 / np.sqrt(self.L * self.C)
        
        # Factor de amortiguamiento
        self.zeta = (self.R / 2) * np.sqrt(self.C / self.L)
        
        # Frecuencia de resonancia
        self.f_0 = self.omega_0 / (2 * np.pi)
        
        # Determinar tipo de amortiguamiento
        if self.zeta < 1:
            self.damping_type = "subamortiguado"
            self.omega_d = self.omega_0 * np.sqrt(1 - self.zeta**2)
        elif self.zeta == 1:
            self.damping_type = "críticamente amortiguado"
            self.omega_d = 0
        else:
            self.damping_type = "sobreamortiguado"
            self.omega_d = 0
            
    def get_impedance(self, frequency):
        """
        Calcula la impedancia del circuito a una frecuencia dada
        
        Args:
            frequency (float): Frecuencia en Hz
            
        Returns:
            complex: Impedancia compleja Z = R + j(ωL - 1/ωC)
        """
        omega = 2 * np.pi * frequency
        X_L = omega * self.L  # Reactancia inductiva
        X_C = 1 / (omega * self.C)  # Reactancia capacitiva
        
        return self.R + 1j * (X_L - X_C)
        
    def get_info(self):
        """
        Retorna información del circuito
        
        Returns:
            dict: Diccionario con información del circuito
        """
        return {
            'R': self.R,
            'L': self.L,
            'C': self.C,
            'omega_0': self.omega_0,
            'f_0': self.f_0,
            'zeta': self.zeta,
            'damping_type': self.damping_type,
            'omega_d': self.omega_d
        }
        
    def __str__(self):
        """
        Representación en string del circuito
        """
        return (f"Circuito RLC:\n"
                f"  R = {self.R} Ω\n"
                f"  L = {self.L} H\n"
                f"  C = {self.C} F\n"
                f"  Frecuencia natural: {self.f_0:.2f} Hz\n"
                f"  Factor de amortiguamiento: {self.zeta:.4f}\n"
                f"  Tipo: {self.damping_type}")