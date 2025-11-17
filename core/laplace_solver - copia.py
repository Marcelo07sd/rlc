"""
Módulo para resolver ecuaciones diferenciales del circuito RLC
usando Transformada de Laplace con SymPy
"""

import sympy as sp
import numpy as np
from core.signals import SignalGenerator


class LaplaceSolver:
    """
    Clase para resolver ecuaciones del circuito RLC usando Transformada de Laplace
    """
    
    def __init__(self):
        # Símbolos de SymPy
        self.t = sp.Symbol('t', real=True, positive=True)
        self.s = sp.Symbol('s')
        self.signal_gen = SignalGenerator()
        
    def solve(self, rlc_model, signal_type, signal_params):
        """
        Resuelve el circuito RLC para una señal de entrada dada
        
        Args:
            rlc_model: Modelo del circuito RLC
            signal_type: Tipo de señal ('step', 'pulse', 'ramp', 'delayed', 'impulse')
            signal_params: Parámetros de la señal
            
        Returns:
            dict: Diccionario con solución simbólica, numérica y vectores de tiempo
        """
        R, L, C = rlc_model.R, rlc_model.L, rlc_model.C
        
        # Obtener la transformada de Laplace de la señal de entrada
        V_s = self._get_signal_laplace(signal_type, signal_params)
        
        # Impedancia del circuito en el dominio de Laplace
        # Z(s) = R + sL + 1/(sC)
        Z_s = R + self.s * L + 1 / (self.s * C)
        
        # Corriente en el dominio de Laplace: I(s) = V(s) / Z(s)
        I_s = V_s / Z_s
        
        # Simplificar
        I_s = sp.simplify(I_s)
        
        # Transformada inversa de Laplace para obtener i(t)
        try:
            i_t = sp.inverse_laplace_transform(I_s, self.s, self.t)
            i_t = sp.simplify(i_t)
        except Exception as e:
            print(f"Error en transformada inversa: {e}")
            # Solución numérica alternativa
            i_t = self._numerical_inverse_laplace(I_s, R, L, C)
        
        # Generar solución numérica
        time_array, current_array, input_signal_array = self._generate_numerical_solution(
            i_t, signal_type, signal_params, R, L, C
        )
        
        # Calcular voltajes en cada componente
        voltage_R = current_array * R
        voltage_L = self._calculate_voltage_L(time_array, current_array, L)
        voltage_C = self._calculate_voltage_C(time_array, current_array, C)
        
        return {
            'symbolic': i_t,
            'time': time_array,
            'current': current_array,
            'voltage_R': voltage_R,
            'voltage_L': voltage_L,
            'voltage_C': voltage_C,
            'input_signal': input_signal_array
        }
        
    def _get_signal_laplace(self, signal_type, params):
        """
        Obtiene la transformada de Laplace de la señal de entrada
        
        Args:
            signal_type: Tipo de señal
            params: Parámetros de la señal
            
        Returns:
            Expresión de SymPy con la transformada de Laplace
        """
        A = params.get('amplitude', 1)
        
        if signal_type == 'step':
            # L{A·U(t)} = A/s
            return A / self.s
            
        elif signal_type == 'pulse':
            # L{A·[U(t) - U(t-a)]} = A/s - (A/s)·exp(-as) = (A/s)·[1 - exp(-as)]
            a = params.get('a', 0.001)
            return (A / self.s) * (1 - sp.exp(-a * self.s))
            
        elif signal_type == 'ramp':
            # L{A·t·U(t)} = A/s²
            return A / (self.s ** 2)
            
        elif signal_type == 'delayed':
            # L{A·U(t-t0)} = (A/s)·exp(-t0·s)
            t0 = params.get('t0', 0.001)
            return (A / self.s) * sp.exp(-t0 * self.s)
            
        elif signal_type == 'impulse':
            # L{A·δ(t)} = A
            return A
            
        else:
            raise ValueError(f"Tipo de señal no reconocido: {signal_type}")
            
    def _numerical_inverse_laplace(self, I_s, R, L, C):
        """
        Método alternativo numérico para la transformada inversa de Laplace
        cuando SymPy falla
        """
        # Retornar una expresión simplificada
        return I_s  # Se evaluará numéricamente más adelante
        
    def _generate_numerical_solution(self, i_t, signal_type, signal_params, R, L, C):
        """
        Genera la solución numérica evaluando la expresión simbólica
        
        Returns:
            tuple: (time_array, current_array, input_signal_array)
        """
        # Vector de tiempo
        duration = self._get_duration(signal_type, signal_params)
        time_array = np.linspace(0, duration, 2000)
        
        # Evaluar la señal de entrada
        input_signal_array = self.signal_gen.generate_signal(
            signal_type, signal_params, time_array
        )
        
        # Convertir la expresión simbólica a función numérica
        try:
            # Lambdify: convertir expresión de SymPy a función NumPy
            i_func = sp.lambdify(self.t, i_t, modules=['numpy'])
            current_array = np.array([i_func(t_val) for t_val in time_array])
            
            # Manejar valores complejos (tomar solo la parte real)
            if np.iscomplexobj(current_array):
                current_array = np.real(current_array)
                
        except Exception as e:
            print(f"Error en evaluación numérica: {e}")
            # Simulación numérica alternativa usando diferencias finitas
            current_array = self._numerical_simulation(
                time_array, input_signal_array, R, L, C
            )
            
        return time_array, current_array, input_signal_array
        
    def _numerical_simulation(self, time_array, input_signal, R, L, C):
        """
        Simulación numérica del circuito usando método de Euler
        Resuelve: L·di/dt + R·i + (1/C)·∫i·dt = V(t)
        """
        dt = time_array[1] - time_array[0]
        n = len(time_array)
        
        i = np.zeros(n)
        v_c = np.zeros(n)  # Voltaje en el capacitor
        
        for k in range(1, n):
            # di/dt = (V - R·i - v_c) / L
            di_dt = (input_signal[k-1] - R * i[k-1] - v_c[k-1]) / L
            i[k] = i[k-1] + di_dt * dt
            
            # dv_c/dt = i / C
            dv_c_dt = i[k-1] / C
            v_c[k] = v_c[k-1] + dv_c_dt * dt
            
        return i
        
    def _calculate_voltage_L(self, time, current, L):
        """
        Calcula el voltaje en el inductor: V_L = L·di/dt
        """
        di_dt = np.gradient(current, time)
        return L * di_dt
        
    def _calculate_voltage_C(self, time, current, C):
        """
        Calcula el voltaje en el capacitor: V_C = (1/C)·∫i·dt
        Usando integración numérica (trapecio)
        """
        dt = time[1] - time[0]
        v_c = np.zeros_like(current)
        
        for i in range(1, len(current)):
            v_c[i] = v_c[i-1] + (current[i] + current[i-1]) / 2 * dt / C
            
        return v_c
        
    def _get_duration(self, signal_type, params):
        """
        Determina la duración apropiada de la simulación
        """
        if signal_type == 'pulse':
            a = params.get('a', 0.001)
            return max(a * 10, 0.01)  # 10 veces la duración del pulso
        elif signal_type == 'delayed':
            t0 = params.get('t0', 0.001)
            return max(t0 * 10, 0.01)
        else:
            return 0.02  # 20 ms por defecto