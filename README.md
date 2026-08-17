# Proyecto_III

## Integrantes: Sebastián Calvo Solano, Carlos Cambronero Zuñiga

### Profesor: Osvaldo Gonzalez Cháves

### Materia: Programación II

### Función del README
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
├── modelos_entrenados/                   # Almacenamiento de los modelos entrenados
│
├── graficos/                             # Gráficos generados  
│
├── .streamlit/                           # Configuración visual del streamlit
│    └── config.toml 
│
├──launcher.py                            # Ejecutador del Streamlit
├──streamlit_app.py                       # Archivo de streamit, se encuentra en raíz para poder 
│
└── data/                                 # Archivos (CSV, Excel, JSON, etc.)
    ├── raw/                              # Archivos en crudo
    └── processed/                        # Archivos procesados
```

## Instalación

### 1. Requisitos previos

- Python 3.11 o superior
- SQL Server (local o remoto) con el driver ODBC 17/18 instalado, **solo si se quiere usar la Sección 3 de `main.py`** (integración con SQL Server). El resto del proyecto (limpieza, EDA, gráficos, modelo, Streamlit) funciona sin SQL Server.

### 2. Crear el entorno virtual e instalar dependencias

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install pandas numpy scikit-learn matplotlib seaborn folium requests python-dotenv pyodbc joblib streamlit plotly
```

| Paquete | Para qué se usa |
|---|---|
| `pandas` | Manipulación de datos en todo el proyecto |
| `scikit-learn` | Preprocesamiento y modelos de clasificación |
| `matplotlib` / `seaborn` | Gráficos estáticos (`Visualizador`, notebook) |
| `folium` | Mapa interactivo por provincia |
| `requests` | Consultas a la API de Open-Meteo |
| `python-dotenv` | Carga de credenciales desde `.env` |
| `pyodbc` | Conexión con SQL Server |
| `joblib` | Guardar el modelo entrenado (`.joblib`) |
| `streamlit` / `plotly` | Dashboard interactivo (`streamlit_app.py`) |

### 3. Configurar el archivo `.env`

Solo necesario si se va a usar la integración con SQL Server. Crear un archivo `.env` en la raíz del proyecto con:

```env
DB_SERVER=localhost\SQLEXPRESS
DB_DATABASE=nombre_de_la_base
DB_DRIVER=ODBC Driver 17 for SQL Server
```

### 4. Datos de entrada

El proyecto espera encontrar el CSV original en:

```text
data/raw/accidentes_victimas_2018_2024.csv
```

(el Anuario Estadístico de Accidentes de Tránsito con Víctimas, del COSEVI). El CSV limpio y el resumen climático se generan/guardan automáticamente en `data/processed/` la primera vez que se corre `main.py`.

---

## Cómo correr el proyecto

### Opción A: pipeline completo (`main.py`)

```bash
cd src
python main.py
```

Ejecuta en orden:

1. Carga y limpia el CSV de accidentes.
2. Guarda y comprueba el CSV procesado.
3. Consulta la API de Open-Meteo (o carga el CSV climático si ya existe) y genera el resumen mensual.
4. Se conecta a SQL Server y carga ambas tablas (si la conexión falla, el proceso continúa igual con el resto de los pasos).
5. Genera el análisis exploratorio (EDA).
6. Genera el mapa interactivo por provincia (`graficos/11_mapa_accidentes_provincia.html`).
7. Entrena y compara los 3 modelos de clasificación (Regresión Logística, Árbol de Decisión, KNN).
8. Guarda el mejor modelo (`modelos_entrenados/modelo_gravedad_accidentes.joblib`) y sus métricas.

> **Nota:** `main.py` no muestra los gráficos de `Visualizador` (usan `plt.show()`, que bloquea la ejecución esperando que se cierre cada ventana). Esos gráficos se revisan desde el notebook.

### Opción B: notebook de exploración

```bash
jupyter notebook notebooks/exploracion_inicial.ipynb
```

Recorre, celda por celda, el mismo flujo de EDA, visualización (con los 10 gráficos visibles inline) y un primer entrenamiento de modelos — pensado para desarrollo y presentación.

### Opción C: dashboard interactivo (Streamlit)

```bash
streamlit run streamlit_app.py
```

Abre una app en el navegador con pestañas de resumen general, análisis temporal, geográfico, gravedad, clima, y un modelo predictivo que se entrena en vivo (una sola vez por sesión) con un formulario para probar predicciones.

---

## Modelado

`EntrenadorModelos` entrena y compara tres algoritmos de clasificación sobre la variable `gravedad` (0 = solo heridos leves, 1 = con muertos o graves):

- Regresión Logística
- Árbol de Decisión
- K-Nearest Neighbors (KNN)

El criterio principal de selección del mejor modelo es el **recall de la clase "grave"** (minimizar los accidentes graves que el modelo no detecta), seguido de F1-score y ROC-AUC. `OptimizadorModelos` permite además ajustar hiperparámetros por `GridSearchCV` sobre el modelo seleccionado.

---

