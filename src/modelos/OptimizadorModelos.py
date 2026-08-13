# ============================================================
# OPTIMIZADOR DE MODELOS DE MACHINE LEARNING
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Esta clase contiene las operaciones necesarias para:
# 1. Optimizar la regresion logistica.
# 2. Optimizar el arbol de decision.
# 3. Probar diferentes hiperparametros.
# 4. Utilizar validacion cruzada.
# 5. Priorizar el recall de accidentes graves.
# 6. Evaluar los mejores modelos sobre el conjunto de prueba.
# 7. Comparar sus metricas finales.
#
# IMPORTANTE:
# Los hiperparametros se seleccionan usando solamente
# los datos de entrenamiento.
# ============================================================

import time
import pandas as pd

from sklearn.base import clone
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


# ============================================================
# CLASE OPTIMIZADORMODELOS
#
# Esta clase busca mejores hiperparametros para regresion
# logistica y arbol de decision.
# ============================================================

class OptimizadorModelos:

    # --------------------------------------------------------
    # CONSTRUCTOR
    #
    # Recibe el preprocesador creado por PreparadorModelo.
    # --------------------------------------------------------

    def __init__(self, preprocesador):
        """
        Guarda el preprocesador y prepara las estructuras
        utilizadas durante la optimizacion.

        Parametro:
            preprocesador: ColumnTransformer con las
                           transformaciones de los datos.
        """

        if preprocesador is None:
            raise ValueError(
                "El preprocesador no puede ser None."
            )

        # Guardar el preprocesador
        self.preprocesador = preprocesador

        # Guardar las busquedas realizadas
        self.busquedas = {}

        # Guardar los mejores modelos
        self.mejores_modelos = {}

        # Guardar los mejores parametros
        self.mejores_parametros = {}

        # Guardar las metricas finales
        self.resultados = {}

        # Guardar las matrices de confusion
        self.matrices_confusion = {}

        # Guardar los reportes de clasificacion
        self.reportes_clasificacion = {}

        # Guardar el mejor modelo final
        self.nombre_mejor_modelo = None
        self.mejor_modelo = None

    # ========================================================
    # SECCION 1: VALIDACION CRUZADA
    # ========================================================

    # --------------------------------------------------------
    # METODO: CREAR VALIDACION CRUZADA
    #
    # Divide internamente el entrenamiento en tres partes
    # y conserva la proporcion de accidentes graves.
    # --------------------------------------------------------

    @staticmethod
    def crear_validacion_cruzada():
        """
        Crea una validacion cruzada estratificada de 3 partes.

        Retorna:
            StratifiedKFold configurado.
        """

        validacion = StratifiedKFold(
            n_splits=3,
            shuffle=True,
            random_state=42
        )

        return validacion

    # ========================================================
    # SECCION 2: PIPELINES
    # ========================================================

    # --------------------------------------------------------
    # METODO: CREAR PIPELINE
    #
    # Combina el preprocesamiento con un modelo.
    # --------------------------------------------------------

    def crear_pipeline(self, modelo):
        """
        Crea un Pipeline con preprocesamiento y modelo.

        Parametro:
            modelo: algoritmo que sera optimizado.

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
    # SECCION 3: OPTIMIZAR REGRESION LOGISTICA
    # ========================================================

    # --------------------------------------------------------
    # METODO: OPTIMIZAR REGRESION
    #
    # Prueba diferentes valores de regularizacion
    # y pesos para la clase grave.
    # --------------------------------------------------------

    def optimizar_regresion(
            self,
            X_entrenamiento,
            y_entrenamiento
    ):
        """
        Optimiza los hiperparametros de regresion logistica.

        Parametros:
            X_entrenamiento: variables de entrenamiento.
            y_entrenamiento: objetivo de entrenamiento.

        Retorna:
            GridSearchCV ajustado.
        """

        print("\n====================================================")
        print("OPTIMIZACION DE REGRESION LOGISTICA")
        print("====================================================")

        # Crear el modelo base
        modelo = LogisticRegression(
            max_iter=1000,
            solver="liblinear",
            random_state=42
        )

        # Crear el Pipeline
        pipeline = self.crear_pipeline(
            modelo
        )

        # Definir los hiperparametros que se probaran
        parametros = {
            "modelo__C": [
                0.1,
                1.0,
                10.0
            ],

            "modelo__class_weight": [
                "balanced",
                {
                    0: 1,
                    1: 3
                },
                {
                    0: 1,
                    1: 5
                }
            ]
        }

        # Crear la validacion cruzada
        validacion = self.crear_validacion_cruzada()

        # Crear la busqueda
        busqueda = GridSearchCV(
            estimator=pipeline,
            param_grid=parametros,
            scoring="recall",
            cv=validacion,
            n_jobs=-1,
            refit=True,
            verbose=1
        )

        print(
            "Combinaciones de regresion que se probaran: 9"
        )

        print(
            "Entrenamientos con validacion cruzada: 27"
        )

        # Registrar el tiempo inicial
        tiempo_inicio = time.time()

        # Ejecutar la busqueda usando solo entrenamiento
        busqueda.fit(
            X_entrenamiento,
            y_entrenamiento
        )

        # Calcular el tiempo total
        tiempo_total = (
            time.time() - tiempo_inicio
        )

        # Guardar los resultados
        nombre_modelo = "Regresion Logistica Optimizada"

        self.busquedas[nombre_modelo] = busqueda

        self.mejores_modelos[nombre_modelo] = (
            busqueda.best_estimator_
        )

        self.mejores_parametros[nombre_modelo] = (
            busqueda.best_params_
        )

        print(
            f"\nOptimizacion terminada en "
            f"{tiempo_total:.2f} segundos."
        )

        print("\nMejores parametros:")

        for parametro, valor in (
                busqueda.best_params_.items()
        ):
            print(f"- {parametro}: {valor}")

        print(
            f"\nMejor recall promedio "
            f"de validacion cruzada: "
            f"{busqueda.best_score_:.4f}"
        )

        return busqueda

    # ========================================================
    # SECCION 4: OPTIMIZAR ARBOL DE DECISION
    # ========================================================

    # --------------------------------------------------------
    # METODO: OPTIMIZAR ARBOL
    #
    # Prueba diferentes profundidades y cantidades
    # minimas de registros en nodos y hojas.
    # --------------------------------------------------------

    def optimizar_arbol(
            self,
            X_entrenamiento,
            y_entrenamiento
    ):
        """
        Optimiza los hiperparametros del arbol de decision.

        Parametros:
            X_entrenamiento: variables de entrenamiento.
            y_entrenamiento: objetivo de entrenamiento.

        Retorna:
            GridSearchCV ajustado.
        """

        print("\n====================================================")
        print("OPTIMIZACION DEL ARBOL DE DECISION")
        print("====================================================")

        # Crear el modelo base
        modelo = DecisionTreeClassifier(
            class_weight="balanced",
            random_state=42
        )

        # Crear el Pipeline
        pipeline = self.crear_pipeline(
            modelo
        )

        # Definir los hiperparametros
        parametros = {
            "modelo__criterion": [
                "gini",
                "entropy"
            ],

            "modelo__max_depth": [
                6,
                10,
                14
            ],

            "modelo__min_samples_split": [
                10,
                20
            ],

            "modelo__min_samples_leaf": [
                5,
                10
            ]
        }

        # Crear la validacion cruzada
        validacion = self.crear_validacion_cruzada()

        # Crear la busqueda
        busqueda = GridSearchCV(
            estimator=pipeline,
            param_grid=parametros,
            scoring="recall",
            cv=validacion,
            n_jobs=-1,
            refit=True,
            verbose=1
        )

        print(
            "Combinaciones del arbol que se probaran: 24"
        )

        print(
            "Entrenamientos con validacion cruzada: 72"
        )

        # Registrar el tiempo inicial
        tiempo_inicio = time.time()

        # Ejecutar la busqueda usando solo entrenamiento
        busqueda.fit(
            X_entrenamiento,
            y_entrenamiento
        )

        # Calcular el tiempo total
        tiempo_total = (
            time.time() - tiempo_inicio
        )

        # Guardar los resultados
        nombre_modelo = "Arbol de Decision Optimizado"

        self.busquedas[nombre_modelo] = busqueda

        self.mejores_modelos[nombre_modelo] = (
            busqueda.best_estimator_
        )

        self.mejores_parametros[nombre_modelo] = (
            busqueda.best_params_
        )

        print(
            f"\nOptimizacion terminada en "
            f"{tiempo_total:.2f} segundos."
        )

        print("\nMejores parametros:")

        for parametro, valor in (
                busqueda.best_params_.items()
        ):
            print(f"- {parametro}: {valor}")

        print(
            f"\nMejor recall promedio "
            f"de validacion cruzada: "
            f"{busqueda.best_score_:.4f}"
        )

        return busqueda

    # ========================================================
    # SECCION 5: EVALUACION SOBRE PRUEBA
    # ========================================================

    # --------------------------------------------------------
    # METODO: EVALUAR MODELO
    #
    # Evalua un modelo optimizado sobre el conjunto
    # independiente de prueba.
    # --------------------------------------------------------

    def evaluar_modelo(
            self,
            nombre_modelo,
            X_prueba,
            y_prueba
    ):
        """
        Evalua un modelo optimizado sobre datos de prueba.

        Parametros:
            nombre_modelo: nombre del modelo optimizado.
            X_prueba: variables del conjunto de prueba.
            y_prueba: valores reales de gravedad.

        Retorna:
            Diccionario con las metricas.
        """

        if nombre_modelo not in self.mejores_modelos:
            raise ValueError(
                f"No existe un modelo optimizado llamado "
                f"{nombre_modelo}."
            )

        modelo = self.mejores_modelos[
            nombre_modelo
        ]

        print("\n====================================================")
        print(f"EVALUACION FINAL: {nombre_modelo}")
        print("====================================================")

        # Generar predicciones
        y_predicho = modelo.predict(
            X_prueba
        )

        # Obtener probabilidades de la clase grave
        probabilidades = modelo.predict_proba(
            X_prueba
        )[:, 1]

        # Calcular las metricas
        metricas = {
            "accuracy": round(
                accuracy_score(
                    y_prueba,
                    y_predicho
                ),
                4
            ),

            "precision": round(
                precision_score(
                    y_prueba,
                    y_predicho,
                    zero_division=0
                ),
                4
            ),

            "recall": round(
                recall_score(
                    y_prueba,
                    y_predicho,
                    zero_division=0
                ),
                4
            ),

            "f1_score": round(
                f1_score(
                    y_prueba,
                    y_predicho,
                    zero_division=0
                ),
                4
            ),

            "roc_auc": round(
                roc_auc_score(
                    y_prueba,
                    probabilidades
                ),
                4
            )
        }

        # Crear la matriz de confusion
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

        # Guardar los resultados
        self.resultados[nombre_modelo] = metricas

        self.matrices_confusion[
            nombre_modelo
        ] = matriz

        self.reportes_clasificacion[
            nombre_modelo
        ] = reporte

        print("\nMetricas sobre el conjunto de prueba:")

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

        return metricas

    # ========================================================
    # SECCION 6: EVALUAR LOS DOS MODELOS
    # ========================================================

    # --------------------------------------------------------
    # METODO: EVALUAR OPTIMIZADOS
    # --------------------------------------------------------

    def evaluar_optimizados(
            self,
            X_prueba,
            y_prueba
    ):
        """
        Evalua todos los modelos optimizados.

        Parametros:
            X_prueba: variables del conjunto de prueba.
            y_prueba: valores reales.

        Retorna:
            DataFrame con la comparacion.
        """

        if not self.mejores_modelos:
            raise ValueError(
                "Todavia no existen modelos optimizados."
            )

        # Limpiar evaluaciones anteriores
        self.resultados = {}
        self.matrices_confusion = {}
        self.reportes_clasificacion = {}

        # Evaluar cada modelo
        for nombre_modelo in self.mejores_modelos:

            self.evaluar_modelo(
                nombre_modelo=nombre_modelo,
                X_prueba=X_prueba,
                y_prueba=y_prueba
            )

        return self.obtener_comparacion()

    # ========================================================
    # SECCION 7: COMPARACION
    # ========================================================

    # --------------------------------------------------------
    # METODO: OBTENER COMPARACION
    # --------------------------------------------------------

    def obtener_comparacion(self):
        """
        Crea una tabla comparativa de modelos optimizados.

        Retorna:
            DataFrame con las metricas finales.
        """

        if not self.resultados:
            raise ValueError(
                "Todavia no existen evaluaciones finales."
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

        # Ordenar primero por recall
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
    # Selecciona el modelo con mayor recall.
    # En caso de empate, considera F1 y ROC-AUC.
    # --------------------------------------------------------

    def seleccionar_mejor_modelo(self):
        """
        Selecciona el mejor modelo optimizado.

        Retorna:
            Nombre y Pipeline del modelo seleccionado.
        """

        comparacion = self.obtener_comparacion()

        nombre_mejor = comparacion.iloc[0][
            "modelo"
        ]

        self.nombre_mejor_modelo = nombre_mejor

        self.mejor_modelo = self.mejores_modelos[
            nombre_mejor
        ]

        print("\n====================================================")
        print("MEJOR MODELO OPTIMIZADO")
        print("====================================================")

        print(
            f"Modelo seleccionado: "
            f"{nombre_mejor}"
        )

        print(
            f"Recall de graves: "
            f"{comparacion.iloc[0]['recall']:.4f}"
        )

        print(
            f"F1-score de graves: "
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
    # SECCION 8: CONSULTAR RESULTADOS
    # ========================================================

    # --------------------------------------------------------
    # METODO: OBTENER MATRIZ
    # --------------------------------------------------------

    def obtener_matriz_confusion(
            self,
            nombre_modelo
    ):
        """
        Obtiene la matriz de confusion de un modelo.

        Parametro:
            nombre_modelo: nombre del modelo consultado.

        Retorna:
            Matriz de confusion.
        """

        if nombre_modelo not in self.matrices_confusion:
            raise ValueError(
                f"No existe matriz para {nombre_modelo}."
            )

        return self.matrices_confusion[
            nombre_modelo
        ]

    # --------------------------------------------------------
    # METODO: OBTENER REPORTE
    # --------------------------------------------------------

    def obtener_reporte(self, nombre_modelo):
        """
        Obtiene el reporte de clasificacion de un modelo.

        Parametro:
            nombre_modelo: nombre del modelo consultado.

        Retorna:
            DataFrame con las metricas por clase.
        """

        if nombre_modelo not in (
                self.reportes_clasificacion
        ):
            raise ValueError(
                f"No existe reporte para {nombre_modelo}."
            )

        reporte = pd.DataFrame(
            self.reportes_clasificacion[
                nombre_modelo
            ]
        ).transpose()

        return reporte