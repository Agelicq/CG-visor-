# CG Visor

Visor de imágenes desarrollado para la asignatura de Computación Gráfica.

## Descripción

Aplicación de escritorio construida con Python para cargar, visualizar y aplicar transformaciones sobre imágenes mediante una interfaz gráfica.

## Funcionalidades

- Carga y visualización de imágenes
- Ajuste de brillo
- Ajuste de contraste
- Rotación
- Binarización mediante umbral
- Negativo
- Separación de canales RGB
- Separación de canales CMY
- Fusión de imágenes
- Zoom por área
- Generación de histogramas
- Restauración de la imagen original
- Guardado de imágenes procesadas

## Requisitos

- Python 3.10 o superior

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Agelicq/CG-visor-.git
cd CG-visor-
```

### 2. Crear entorno virtual

En Windows (PowerShell):

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Estructura del proyecto

```text
CG-visor-/
├── auxVisor.py        # Funciones auxiliares de procesamiento
├── visor.py           # Interfaz gráfica principal
├── requirements.txt   # Dependencias del proyecto
└── README.md          # Documentación
```

## Tecnologías

- Python
- NumPy
- Matplotlib
- Tkinter
- ttkbootstrap
- Pillow

## Limitaciones conocidas

- Algunas operaciones (por ejemplo, fusión) requieren que las imágenes tengan el mismo tamaño.
- El rendimiento puede variar según la resolución de la imagen.

## Autoría

María Angélica Álvarez Giraldo

## Licencia

Proyecto de uso académico.

