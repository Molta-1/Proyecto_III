# Proyecto_III

## Integrantes: Sebastián Calvo Solano, Carlos Cambronero Zuñiga

### Profesor: Osvaldo Gonzalez Cháves

### Materia: Programación II

#### Función del README
Este es el archivo de texto que resume el proyecto en la parte técnica.


# Propósito del Proyecto

La función de este proyecto es aplicar lo visto en clase para solucionar un problema de la vida real, es decir, poder obtener información real de una API, csv, excel etc para realizar en este caso el entrenamiento de un modelo de aprendizaje automático (o machine learning) con el objetivo de poder encontrar una solución a dicho problema, esto siguiendo claramente distintas etapas como lo son:

- Recolección de datos: (API, archivos csv, base de datos).
- Almacenamiento y limpieza de datos: Almacenar los datos en una base de datos para poder tratarlos (agregar columnas, tratar nulos, enriquecer con mas información).
- EDA: Análisis que permite observar de manera superficial relaciones o patrones que pueden tener los datos.
- Modelado: Etapa donde un modelo que analiza los datos que se seleccionen para que de un resultado a base de lo que se busca.

Todo estos pasos deben de poseer sus propias clases.

# Distribución de Carpetas

El proyecto va a presentar la siguiente distribución de carpetas de trabajo en donde estarán las distintas funciones que se van a manejar, estas son:

```text
proyecto_nombre/
├── src/                                  # Código fuente principal
│   ├── datos/                            # Gestión de archivos y transformación de datos
│   ├── basedatos/                        # Módulos para conexión a bases de datos
│   ├── api/                              # Clientes para llamadas a APIs externas
│   ├── eda/                              # Exploración de datos y estadísticas descriptivas
│   ├── visualizacion/                    # Visualización de datos y mapas
│   ├── modelos/                          # Entrenamiento y evaluación de modelos ML
│   ├── helpers/                          # Funciones auxiliares reutilizables
│   └── main.py                           # Punto de entrada del proyecto
│
├── notebooks/                            # Jupyter notebooks para desarrollo y presentación
│   └── exploracion_inicial.ipynb
│
└── data/                                 # Archivos (CSV, Excel, JSON, etc.)
    ├── raw/                              # Archivos en crudo
    └── processed/                        # Archivos procesados
```
