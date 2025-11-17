# ⚡ Simulador de Circuito RLC en Serie

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-Qt6-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Un simulador gráfico profesional para análisis de circuitos RLC utilizando Transformada de Laplace**

[Características](#-características) •
[Instalación](#-instalación) •
[Uso](#-uso) •
[Ejemplos](#-ejemplos) •
[Documentación](#-documentación)

<img src="https://via.placeholder.com/800x450.png?text=RLC+Simulator+Screenshot" alt="Screenshot" width="800"/>

</div>

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Uso](#-uso)
- [Fundamento Matemático](#-fundamento-matemático)
- [Ejemplos de Circuitos](#-ejemplos-de-circuitos)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Solución de Problemas](#-solución-de-problemas)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## 🔬 Descripción

Este simulador permite analizar el comportamiento dinámico de circuitos RLC en serie mediante la resolución de ecuaciones diferenciales usando **Transformada de Laplace**. Proporciona soluciones tanto simbólicas como numéricas, visualizando en tiempo real la corriente y voltajes en cada componente del circuito.

### ¿Qué es un Circuito RLC?

Un circuito RLC en serie contiene:
- **R**: Resistencia (Ω)
- **L**: Inductancia (H)
- **C**: Capacitancia (F)

La ecuación diferencial que gobierna el circuito es:

```
L·di/dt + R·i + (1/C)·∫i·dt = V(t)
```

---

## ✨ Características

### 🎯 Funcionalidades Principales

- ✅ **Solución Simbólica** mediante Transformada de Laplace con SymPy
- ✅ **Solución Numérica** usando métodos de integración (Euler)
- ✅ **Interfaz Gráfica Moderna** desarrollada con PySide6 (Qt6)
- ✅ **Múltiples Señales de Entrada**:
  - Escalón unitario `U(t)`
  - Pulso rectangular `U(t) - U(t-a)`
  - Rampa lineal `t·U(t)`
  - Señal retardada `U(t-t₀)`
  - Impulso de Dirac `δ(t)` (simulado numéricamente)
  
### 📊 Visualización

- 📈 Gráfica de corriente `i(t)` en tiempo real
- 📉 Voltajes individuales: `V_R(t)`, `V_L(t)`, `V_C(t)`
- 🔄 Señal de entrada `V(t)`
- 📐 Gráficos sincronizados con escala temporal

### 💾 Gestión de Datos

- 💾 **Exportar gráficas** en formatos PNG, PDF y SVG
- 📝 **Guardar parámetros** de circuitos en archivos JSON
- 📂 **Cargar configuraciones** previamente guardadas

### 🎨 Interfaz de Usuario

- 🖥️ Diseño limpio y minimalista
- 🎛️ Controles intuitivos para parámetros
- 📊 Visualización profesional de resultados
- ✏️ Solución simbólica formateada con símbolos matemáticos elegantes

---

## 🔧 Requisitos Previos

### Software Necesario

- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)

### Verificar Instalación de Python

```bash
python --version
# o
python3 --version
```

Si no tienes Python instalado, descárgalo desde [python.org](https://www.python.org/downloads/)

---

## 🚀 Instalación

### Opción 1: Clonar el Repositorio (Recomendado)

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/rlc-simulator.git

# 2. Navegar al directorio
cd rlc-simulator

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python main.py
```

### Opción 2: Descarga Manual

1. **Descargar el código**
   - Haz clic en el botón verde "Code" → "Download ZIP"
   - Extrae el archivo ZIP

2. **Instalar dependencias**
   ```bash
   cd rlc-simulator
   pip install -r requirements.txt
   ```

3. **Ejecutar**
   ```bash
   python main.py
   ```

### Instalación de Dependencias Individual

Si prefieres instalar las dependencias una por una:

```bash
pip install PySide6>=6.5.0
pip install sympy>=1.12
pip install numpy>=1.24.0
pip install matplotlib>=3.7.0
```

---

## 📁 Estructura del Proyecto

```
rlc-simulator/
├── 📄 main.py                    # Punto de entrada de la aplicación
├── 📄 requirements.txt           # Dependencias del proyecto
├── 📄 README.md                  # Este archivo
│
├── 📁 ui/                        # Interfaz gráfica (Qt6)
│   ├── __init__.py
│   ├── main_window.py           # Ventana principal
│   └── parameter_form.py        # Formulario de parámetros
│
├── 📁 core/                      # Lógica matemática del simulador
│   ├── __init__.py
│   ├── laplace_solver.py        # Transformada de Laplace
│   ├── rlc_model.py             # Modelo del circuito RLC
│   └── signals.py               # Generador de señales
│
└── 📁 plots/                     # Módulo de graficación
    ├── __init__.py
    └── plotter.py               # Graficador con Matplotlib
```

### Arquitectura Modular

El proyecto sigue principios de **separación de responsabilidades**:

- **`ui/`**: Toda la lógica de interfaz gráfica
- **`core/`**: Procesamiento matemático y resolución de ecuaciones
- **`plots/`**: Generación y exportación de gráficos

---

## 📖 Uso

### 1️⃣ Iniciar la Aplicación

```bash
python main.py
```

### 2️⃣ Configurar el Circuito

En el panel izquierdo, ingresa los valores del circuito:

- **Resistencia R** (Ω): Por ejemplo, `100`
- **Inductancia L** (H): Por ejemplo, `0.1`
- **Capacitancia C** (F): Por ejemplo, `0.00001` (10 µF)

### 3️⃣ Seleccionar Señal de Entrada

Elige el tipo de señal:

| Señal | Descripción | Parámetros |
|-------|-------------|------------|
| **Escalón U(t)** | Voltaje constante desde t=0 | Amplitud |
| **Pulso** | Pulso rectangular de duración `a` | Amplitud, Duración `a` |
| **Rampa** | Voltaje que crece linealmente | Amplitud |
| **Retardada** | Escalón que inicia en `t₀` | Amplitud, Retardo `t₀` |
| **Impulso δ(t)** | Impulso de Dirac (simulado) | Amplitud |

### 4️⃣ Simular

Haz clic en el botón **🚀 Simular**

### 5️⃣ Analizar Resultados

La aplicación mostrará:

- ✅ **Solución simbólica** `i(t)` en el panel izquierdo
- ✅ **Gráficas** en el panel derecho:
  - Señal de entrada `V(t)`
  - Corriente `i(t)`
  - Voltajes `V_R`, `V_L`, `V_C`

### 6️⃣ Exportar/Guardar

- **💾 Exportar Gráfica**: Guarda las gráficas en PNG/PDF/SVG
- **📝 Guardar Parámetros**: Exporta la configuración en JSON
- **📂 Cargar Parámetros**: Importa configuraciones previas

---

## 🧮 Fundamento Matemático

### Ecuación Diferencial del Circuito RLC

```
L·di/dt + R·i + (1/C)·∫i·dt = V(t)
```

### Transformada de Laplace

Aplicando la transformada de Laplace a ambos lados:

```
L·s·I(s) + R·I(s) + I(s)/(s·C) = V(s)
```

Despejando la corriente en el dominio de Laplace:

```
I(s) = V(s) / Z(s)
```

Donde la impedancia es:

```
Z(s) = R + s·L + 1/(s·C)
```

### Parámetros Característicos

El comportamiento del circuito depende de:

1. **Frecuencia natural**:
   ```
   ω₀ = 1/√(L·C)
   ```

2. **Factor de amortiguamiento**:
   ```
   ζ = (R/2)·√(C/L)
   ```

3. **Tipo de respuesta**:
   - **ζ < 1**: Subamortiguado (oscilatorio)
   - **ζ = 1**: Críticamente amortiguado
   - **ζ > 1**: Sobreamortiguado

### Transformadas de Laplace de Señales Comunes

| Señal | Transformada de Laplace |
|-------|------------------------|
| `U(t)` | `1/s` |
| `U(t) - U(t-a)` | `(1/s)·[1 - e^(-as)]` |
| `t·U(t)` | `1/s²` |
| `U(t-t₀)` | `(1/s)·e^(-t₀s)` |
| `δ(t)` | `1` |

---

## 💡 Ejemplos de Circuitos

### Ejemplo 1: Circuito Subamortiguado (Oscilatorio)

**Configuración:**
```
R = 100 Ω
L = 0.1 H
C = 10 µF (0.00001 F)
Señal: Escalón de 10V
```

**Resultado esperado:**
- Factor de amortiguamiento: ζ ≈ 0.5
- Respuesta oscilatoria con decaimiento exponencial

### Ejemplo 2: Circuito Críticamente Amortiguado

**Configuración:**
```
R = 632 Ω
L = 0.1 H
C = 10 µF
Señal: Pulso de 10V, duración 1ms
```

**Resultado esperado:**
- Factor de amortiguamiento: ζ = 1
- Respuesta más rápida sin oscilaciones

### Ejemplo 3: Circuito Sobreamortiguado

**Configuración:**
```
R = 2000 Ω
L = 0.1 H
C = 10 µF
Señal: Rampa de 10V
```

**Resultado esperado:**
- Factor de amortiguamiento: ζ > 1
- Respuesta lenta sin oscilaciones

### Ejemplo 4: Respuesta al Impulso

**Configuración:**
```
R = 100 Ω
L = 0.1 H
C = 10 µF
Señal: Impulso δ(t) con amplitud 10
```

**Resultado esperado:**
- Oscilación amortiguada que representa la respuesta natural del sistema

---

## 📸 Capturas de Pantalla

### Interfaz Principal
```
┌─────────────────────────────────────────────────────────────┐
│  🔌 Simulador de Circuito RLC en Serie                      │
├──────────────┬──────────────────────────────────────────────┤
│ PARÁMETROS   │  GRÁFICAS                                    │
│              │                                              │
│ R = 100 Ω    │  [Gráfica de señal de entrada]              │
│ L = 0.1 H    │  [Gráfica de corriente i(t)]                │
│ C = 10 µF    │  [Gráficas de voltajes]                     │
│              │                                              │
│ 🚀 Simular   │                                              │
│ 💾 Exportar  │                                              │
│              │                                              │
│ SOLUCIÓN:    │                                              │
│ i(t) = ...   │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

---

## 🛠️ Solución de Problemas

### Problema: "No module named 'PySide6'"

**Solución:**
```bash
pip install --upgrade PySide6
```

### Problema: "No module named 'ui'"

**Solución:**
- Asegúrate de ejecutar `main.py` desde la carpeta raíz del proyecto
- Verifica que existan los archivos `__init__.py` en cada carpeta

```bash
# Crear archivos __init__.py si no existen
touch ui/__init__.py
touch core/__init__.py
touch plots/__init__.py
```

### Problema: Gráficas no se muestran

**Solución:**
```bash
pip install --upgrade matplotlib
```

Si usas **macOS** y hay problemas con matplotlib:
```bash
pip install --upgrade matplotlib
# Si persiste:
python -m pip install --upgrade --force-reinstall matplotlib
```

### Problema: Error con SymPy en Windows

**Solución:**
```bash
pip install --upgrade sympy mpmath
```

### Problema: La aplicación se cierra inmediatamente

**Solución:**
- Verifica la versión de Python: `python --version`
- Debe ser Python 3.8 o superior
- Reinstala las dependencias:
  ```bash
  pip uninstall -y PySide6 sympy numpy matplotlib
  pip install -r requirements.txt
  ```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si deseas mejorar el proyecto:

1. **Fork** el repositorio
2. Crea una **rama** para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. **Commit** tus cambios (`git commit -m 'Agregar nueva característica'`)
4. **Push** a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un **Pull Request**

### Ideas para Contribuir

- 🎨 Mejorar la interfaz gráfica
- 📊 Agregar más tipos de señales
- 🔧 Optimizar algoritmos numéricos
- 📚 Mejorar la documentación
- 🌐 Agregar internacionalización (i18n)
- 🧪 Agregar pruebas unitarias

---

## 📚 Tecnologías Utilizadas

| Tecnología | Propósito |
|-----------|-----------|
| **PySide6** | Interfaz gráfica (Qt6) |
| **SymPy** | Cálculo simbólico y Transformada de Laplace |
| **NumPy** | Cálculo numérico y arrays |
| **Matplotlib** | Graficación científica |

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2024 [Tu Nombre]

Se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia
de este software y archivos de documentación asociados (el "Software"), para 
utilizar el Software sin restricciones...
```

---

## 👨‍💻 Autor

**[Tu Nombre]**

- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@ejemplo.com

---

## 🙏 Agradecimientos

- A la comunidad de **Python** por las excelentes bibliotecas
- A **Anthropic** por Claude, que ayudó en el desarrollo
- A todos los contribuidores del proyecto

---

## 📞 Contacto y Soporte

Si tienes preguntas o necesitas ayuda:

- 📧 **Email**: tu-email@ejemplo.com
- 💬 **Issues**: [Reportar un problema](https://github.com/tu-usuario/rlc-simulator/issues)
- 📖 **Wiki**: [Documentación detallada](https://github.com/tu-usuario/rlc-simulator/wiki)

---

## 🔄 Versiones

### v1.0.0 (Actual)
- ✅ Implementación inicial
- ✅ Soporte para 5 tipos de señales
- ✅ Solución simbólica y numérica
- ✅ Interfaz gráfica completa
- ✅ Exportación de gráficas y parámetros

### Roadmap (Futuras Versiones)

- 🔜 v1.1.0: Análisis en frecuencia (Bode plots)
- 🔜 v1.2.0: Circuitos RLC paralelo
- 🔜 v1.3.0: Múltiples circuitos simultáneos
- 🔜 v2.0.0: Simulación de circuitos complejos

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐**

[![GitHub stars](https://img.shields.io/github/stars/tu-usuario/rlc-simulator?style=social)](https://github.com/tu-usuario/rlc-simulator/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/tu-usuario/rlc-simulator?style=social)](https://github.com/tu-usuario/rlc-simulator/network/members)

---

**Hecho con ❤️ para la comunidad de ingeniería eléctrica**

</div>
