# ============================================================
# ENTRENADOR DE MODELOS DE MACHINE LEARNING
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Esta clase contiene las operaciones necesarias para:
# 1. Crear los modelos de clasificacion.
# 2. Entrenar regresion logistica.
# 3. Entrenar arbol de decision.
# 4. Entrenar KNN.
# 5. Generar predicciones.
# 6. Calcular las metricas de evaluacion.
# 7. Crear las matrices de confusion.
# 8. Comparar los modelos.
# 9. Seleccionar el mejor modelo.
# ============================================================

import time
import pandas as pd

from sklearn.base import clone
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


# ============================================================
# CLASE ENTRENADORMODELOS
#
# Esta clase recibe el preprocesador y administra
# el entrenamiento y evaluacion de los algoritmos.
# ============================================================

class EntrenadorModelos:

    # --------------------------------------------------------
    # CONSTRUCTOR
    #
    # Recibe el preprocesador creado por PreparadorModelo.
    # --------------------------------------------------------

    def __init__(self, preprocesador):
        """
        Guarda el preprocesador y prepara las estructuras
        donde se almacenaran los modelos y sus resultados.

        Parametro:
            preprocesador: ColumnTransformer creado
                           por PreparadorModelo.
        """

        if preprocesador is None:
            raise ValueError(
                "El preprocesador no puede ser None."
            )

        # Guardar el preprocesador
        self.preprocesador = preprocesador

        # Diccionario para almacenar los modelos entrenados
        self.modelos = {}

        # Diccionario para almacenar las metricas
        self.resultados = {}

        # Diccionario para almacenar matrices de confusion
        self.matrices_confusion = {}

        # Diccionario para almacenar reportes completos
        self.reportes_clasificacion = {}

        # El mejor modelo se definira despues de comparar
        self.mejor_modelo = None
        self.nombre_mejor_modelo = None

    # ========================================================
    # SECCION 1: CREACION DE LOS MODELOS
    # ========================================================

    # --------------------------------------------------------
    # METODO: CREAR MODELOS
    #
    # Define los tres algoritmos requeridos por el proyecto.
    # --------------------------------------------------------

    def crear_modelos(self):
        """
        Crea los tres algoritmos de clasificacion.

        Retorna:
            Diccionario con los modelos sin entrenar.
        """

        modelos_base = {
            "Regresion Logistica": LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=42
            ),

            "Arbol de Decision": DecisionTreeClassifier(
                max_depth=10,
                min_samples_split=20,
                min_samples_leaf=10,
                class_weight="balanced",
                random_state=42
            ),

            "KNN": KNeighborsClassifier(
                n_neighbors=5,
                weights="distance",
                n_jobs=-1
            )
        }

        print("Modelos creados correctamente.")

        for nombre in modelos_base:
            print(f"- {nombre}")

        return modelos_base

    # ========================================================
    # SECCION 2: CREACION DE PIPELINES
    # ========================================================

    # --------------------------------------------------------
    # METODO: CREAR PIPELINE
    #
    # Combina el preprocesamiento y el modelo.
    # --------------------------------------------------------

    def crear_pipeline(self, modelo):
        """
        Crea un Pipeline con preprocesamiento y modelo.

        Parametro:
            modelo: algoritmo que sera entrenado.

        Retorna:
            Pipeline completo.
        """

        pipeline = Pipeline(
            steps=[
                (
                    "preprocesamiento",
                    clone(self.preprocesador)
                ),
                (
                    "modelo",
                    modelo
                )
            ]
        )

        return pipeline

    # ========================================================
    # SECCION 3: EVALUACION DE LOS MODELOS
    # ========================================================

    # --------------------------------------------------------
    # METODO AUXILIAR: CALCULAR METRICAS
    #
    # Calcula las principales metricas de clasificacion.
    # --------------------------------------------------------

    @staticmethod
    def _calcular_metricas(
            y_real,
            y_predicho,
            probabilidades,
            tiempo_entrenamiento
    ):
        """
        Calcula las metricas de evaluacion.

        Parametros:
            y_real: valores verdaderos.
            y_predicho: predicciones del modelo.
            probabilidades: probabilidad de la clase grave.
            tiempo_entrenamiento: segundos usados para entrenar.

        Retorna:
            Diccionario con las metricas.
        """

        metricas = {
            "accuracy": round(
                accuracy_score(
                    y_real,
                    y_predicho
                ),
                4
            ),

            "precision": round(
                precision_score(
                    y_real,
                    y_predicho,
                    zero_division=0
                ),
                4
            ),

            "recall": round(
                recall_score(
                    y_real,
                    y_predicho,
                    zero_division=0
                ),
                4
            ),

            "f1_score": round(
                f1_score(
                    y_real,
                    y_predicho,
                    zero_division=0
                ),
                4
            ),

            "roc_auc": round(
                roc_auc_score(
                    y_real,
                    probabilidades
                ),
                4
            ),

            "tiempo_segundos": round(
                tiempo_entrenamiento,
                2
            )
        }

        return metricas

    # --------------------------------------------------------
    # METODO: ENTRENAR UN MODELO
    #
    # Entrena, predice y evalua un algoritmo.
    # --------------------------------------------------------

    def entrenar_modelo(
            self,
            nombre_modelo,
            modelo,
            X_entrenamiento,
            y_entrenamiento,
            X_prueba,
            y_prueba
    ):
        """
        Entrena y evalua un modelo de clasificacion.

        Parametros:
            nombre_modelo: nombre descriptivo del algoritmo.
            modelo: algoritmo sin entrenar.
            X_entrenamiento: variables para entrenar.
            y_entrenamiento: objetivo para entrenar.
            X_prueba: variables para evaluar.
            y_prueba: objetivo real de prueba.

        Retorna:
            Pipeline entrenado.
        """

        print("\n====================================================")
        print(f"ENTRENANDO: {nombre_modelo}")
        print("====================================================")

        # Crear un Pipeline independiente para el modelo
        pipeline = self.crear_pipeline(
            modelo
        )

        # Registrar el tiempo inicial
        tiempo_inicio = time.time()

        # Entrenar el Pipeline
        pipeline.fit(
            X_entrenamiento,
            y_entrenamiento
        )

        # Calcular el tiempo de entrenamiento
        tiempo_entrenamiento = (
            time.time() - tiempo_inicio
        )

        print(
            f"Entrenamiento terminado en "
            f"{tiempo_entrenamiento:.2f} segundos."
        )

        # Generar las clasificaciones
        y_predicho = pipeline.predict(
            X_prueba
        )

        # Obtener la probabilidad de la clase grave
        probabilidades = pipeline.predict_proba(
            X_prueba
        )[:, 1]

        # Calcular las metricas
        metricas = self._calcular_metricas(
            y_real=y_prueba,
            y_predicho=y_predicho,
            probabilidades=probabilidades,
            tiempo_entrenamiento=tiempo_entrenamiento
        )

        # Calcular la matriz de confusion
        matriz = confusion_matrix(
            y_prueba,
            y_predicho
        )

        # Crear el reporte detallado
        reporte = classification_report(
            y_prueba,
            y_predicho,
            target_names=[
                "Leve",
                "Grave"
            ],
            zero_division=0,
            output_dict=True
        )

        # Guardar el modelo entrenado
        self.modelos[nombre_modelo] = pipeline

        # Guardar las metricas
        self.resultados[nombre_modelo] = metricas

        # Guardar la matriz de confusion
        self.matrices_confusion[nombre_modelo] = matriz

        # Guardar el reporte
        self.reportes_clasificacion[
            nombre_modelo
        ] = reporte

        print("\nMetricas obtenidas:")

        print(
            f"Accuracy: "
            f"{metricas['accuracy']:.4f}"
        )

        print(
            f"Precision de graves: "
            f"{metricas['precision']:.4f}"
        )

        print(
            f"Recall de graves: "
            f"{metricas['recall']:.4f}"
        )

        print(
            f"F1-score de graves: "
            f"{metricas['f1_score']:.4f}"
        )

        print(
            f"ROC-AUC: "
            f"{metricas['roc_auc']:.4f}"
        )

        print("\nMatriz de confusion:")

        print(matriz)

        return pipeline

    # ========================================================
    # SECCION 4: ENTRENAMIENTO DE TODOS LOS MODELOS
    # ========================================================

    # --------------------------------------------------------
    # METODO: ENTRENAR TODOS LOS MODELOS
    #
    # Entrena regresion logistica, arbol y KNN.
    # --------------------------------------------------------

    def entrenar_todos(
            self,
            X_entrenamiento,
            y_entrenamiento,
            X_prueba,
            y_prueba
    ):
        """
        Entrena y evalua los tres modelos.

        Parametros:
            X_entrenamiento: variables para entrenar.
            y_entrenamiento: objetivo para entrenar.
            X_prueba: variables para evaluar.
            y_prueba: objetivo real de prueba.

        Retorna:
            DataFrame con la comparacion de metricas.
        """

        # Limpiar resultados anteriores
        self.modelos = {}
        self.resultados = {}
        self.matrices_confusion = {}
        self.reportes_clasificacion = {}

        # Crear los modelos
        modelos_base = self.crear_modelos()

        # Entrenar cada algoritmo
        for nombre, modelo in modelos_base.items():

            self.entrenar_modelo(
                nombre_modelo=nombre,
                modelo=modelo,
                X_entrenamiento=X_entrenamiento,
                y_entrenamiento=y_entrenamiento,
                X_prueba=X_prueba,
                y_prueba=y_prueba
            )

        # Crear la tabla comparativa
        comparacion = self.obtener_comparacion()

        return comparacion

    # ========================================================
    # SECCION 5: COMPARACION DE RESULTADOS
    # ========================================================

    # --------------------------------------------------------
    # METODO: OBTENER COMPARACION
    #
    # Convierte las metricas en un DataFrame.
    # --------------------------------------------------------

    def obtener_comparacion(self):
        """
        Crea una tabla comparativa de los modelos.

        Retorna:
            DataFrame con todas las metricas.
        """

        if not self.resultados:
            raise ValueError(
                "Todavia no existen resultados de modelos."
            )

        comparacion = pd.DataFrame.from_dict(
            self.resultados,
            orient="index"
        )

        comparacion = (
            comparacion
            .reset_index()
            .rename(
                columns={
                    "index": "modelo"
                }
            )
        )

        # Ordenar priorizando el recall de accidentes graves
        comparacion = (
            comparacion
            .sort_values(
                by=[
                    "recall",
                    "f1_score",
                    "roc_auc"
                ],
                ascending=False
            )
            .reset_index(drop=True)
        )

        return comparacion

    # --------------------------------------------------------
    # METODO: SELECCIONAR MEJOR MODELO
    #
    # Selecciona principalmente por recall de la clase grave.
    # --------------------------------------------------------

    def seleccionar_mejor_modelo(self):
        """
        Selecciona el modelo con mejor recall de graves.

        En caso de empate, utiliza F1-score y ROC-AUC.

        Retorna:
            Nombre y Pipeline del mejor modelo.
        """

        comparacion = self.obtener_comparacion()

        # La primera fila contiene el mejor resultado
        nombre_mejor = comparacion.iloc[0][
            "modelo"
        ]

        self.nombre_mejor_modelo = nombre_mejor

        self.mejor_modelo = self.modelos[
            nombre_mejor
        ]

        print("\n====================================================")
        print("MEJOR MODELO")
        print("====================================================")

        print(
            f"Modelo seleccionado: "
            f"{self.nombre_mejor_modelo}"
        )

        print(
            f"Recall de accidentes graves: "
            f"{comparacion.iloc[0]['recall']:.4f}"
        )

        print(
            f"F1-score de accidentes graves: "
            f"{comparacion.iloc[0]['f1_score']:.4f}"
        )

        print(
            f"ROC-AUC: "
            f"{comparacion.iloc[0]['roc_auc']:.4f}"
        )

        return (
            self.nombre_mejor_modelo,
            self.mejor_modelo
        )

    # ========================================================
    # SECCION 6: CONSULTAR RESULTADOS INDIVIDUALES
    # ========================================================

    # --------------------------------------------------------
    # METODO: OBTENER MATRIZ DE CONFUSION
    # --------------------------------------------------------

    def obtener_matriz_confusion(self, nombre_modelo):
        """
        Obtiene la matriz de confusion de un modelo.

        Parametro:
            nombre_modelo: nombre del modelo consultado.

        Retorna:
            Matriz de confusion.
        """

        if nombre_modelo not in self.matrices_confusion:
            raise ValueError(
                f"No existen resultados para "
                f"{nombre_modelo}."
            )

        return self.matrices_confusion[
            nombre_modelo
        ]

    # --------------------------------------------------------
    # METODO: OBTENER REPORTE DE CLASIFICACION
    # --------------------------------------------------------

    def obtener_reporte(self, nombre_modelo):
        """
        Obtiene el reporte detallado de un modelo.

        Parametro:
            nombre_modelo: nombre del modelo consultado.

        Retorna:
            DataFrame con precision, recall y F1 por clase.
        """

        if nombre_modelo not in (
                self.reportes_clasificacion
        ):
            raise ValueError(
                f"No existe un reporte para "
                f"{nombre_modelo}."
            )

        reporte = pd.DataFrame(
            self.reportes_clasificacion[
                nombre_modelo
            ]
        ).transpose()

        return reporte