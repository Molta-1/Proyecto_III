# ============================================================
# PRUEBA INICIAL DE MODELOS DE MACHINE LEARNING
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Este archivo comprueba:
# 1. La carga de los datos procesados.
# 2. La preparacion de las variables.
# 3. La division estratificada 80 % y 20 %.
# 4. El entrenamiento de regresion logistica.
# 5. El entrenamiento del arbol de decision.
# 6. El calculo de metricas.
# 7. Las matrices de confusion.
# 8. La comparacion inicial de los modelos.
#
# IMPORTANTE:
# KNN se probara despues de forma independiente.
# Este archivo no modifica SQL Server.
# ============================================================

import os
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from src.modelos.PreparadorModelo import PreparadorModelo
from src.modelos.EntrenadorModelos import EntrenadorModelos


# ============================================================
# FUNCION AUXILIAR: MOSTRAR TITULO
#
# Organiza la informacion presentada en la consola.
# ============================================================

def mostrar_titulo(titulo):
    """
    Muestra un titulo organizado en la consola.

    Parametro:
        titulo: texto que se desea mostrar.
    """

    print("\n====================================================")
    print(titulo)
    print("====================================================")


# ============================================================
# FUNCION PRINCIPAL
#
# Prepara los datos, entrena los dos primeros modelos
# y comprueba sus resultados.
# ============================================================

def main():
    """
    Entrena y evalua regresion logistica
    y arbol de decision.
    """

    # ========================================================
    # SECCION 1: CARGAR LOS ARCHIVOS PROCESADOS
    # ========================================================

    mostrar_titulo("CARGA DE LOS ARCHIVOS PROCESADOS")

    # Obtener la carpeta principal del proyecto
    carpeta_proyecto = os.path.dirname(
        os.path.abspath(__file__)
    )

    # Construir la ruta del CSV de accidentes
    ruta_accidentes = os.path.join(
        carpeta_proyecto,
        "data",
        "processed",
        "accidentes_victimas_limpio.csv"
    )

    # Construir la ruta del CSV climatico
    ruta_clima = os.path.join(
        carpeta_proyecto,
        "data",
        "processed",
        "clima_mensual_2018_2024.csv"
    )

    # Comprobar que el archivo de accidentes exista
    if not os.path.exists(ruta_accidentes):
        raise FileNotFoundError(
            f"No se encontro el archivo de accidentes: "
            f"{ruta_accidentes}"
        )

    # Comprobar que el archivo climatico exista
    if not os.path.exists(ruta_clima):
        raise FileNotFoundError(
            f"No se encontro el archivo climatico: "
            f"{ruta_clima}"
        )

    # Cargar los accidentes
    datos_accidentes = pd.read_csv(
        ruta_accidentes,
        sep=";",
        encoding="utf-8-sig",
        low_memory=False
    )

    # Cargar el clima mensual
    datos_clima = pd.read_csv(
        ruta_clima,
        sep=";",
        encoding="utf-8-sig",
        low_memory=False
    )

    print("Archivos procesados cargados correctamente.")

    print(
        f"\nAccidentes: "
        f"{datos_accidentes.shape[0]} filas y "
        f"{datos_accidentes.shape[1]} columnas"
    )

    print(
        f"Clima mensual: "
        f"{datos_clima.shape[0]} filas y "
        f"{datos_clima.shape[1]} columnas"
    )

    # ========================================================
    # SECCION 2: PREPARAR LOS DATOS
    # ========================================================

    mostrar_titulo("PREPARACION DE LOS DATOS")

    # Crear el preparador
    preparador = PreparadorModelo()

    # Agregar el contexto climatico a cada accidente
    datos_modelo = preparador.relacionar_con_clima(
        datos_accidentes=datos_accidentes,
        datos_clima=datos_clima
    )

    # Separar variables predictoras y objetivo
    X, y = preparador.separar_variables(
        datos_modelo
    )

    # Dividir entrenamiento y prueba
    (
        X_entrenamiento,
        X_prueba,
        y_entrenamiento,
        y_prueba
    ) = preparador.dividir_datos(
        X=X,
        y=y,
        tamanio_prueba=0.20,
        semilla=42
    )

    # Crear el preprocesador
    preprocesador = preparador.crear_preprocesador()

    print("\nDatos preparados correctamente.")

    print(
        f"Entrenamiento: "
        f"{X_entrenamiento.shape[0]} registros"
    )

    print(
        f"Prueba: "
        f"{X_prueba.shape[0]} registros"
    )

    # ========================================================
    # SECCION 3: CREAR EL ENTRENADOR
    # ========================================================

    mostrar_titulo("CREACION DEL ENTRENADOR")

    entrenador = EntrenadorModelos(
        preprocesador=preprocesador
    )

    print("EntrenadorModelos creado correctamente.")

    # ========================================================
    # SECCION 4: REGRESION LOGISTICA
    # ========================================================

    mostrar_titulo("MODELO 1: REGRESION LOGISTICA")

    regresion_logistica = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    )

    entrenador.entrenar_modelo(
        nombre_modelo="Regresion Logistica",
        modelo=regresion_logistica,
        X_entrenamiento=X_entrenamiento,
        y_entrenamiento=y_entrenamiento,
        X_prueba=X_prueba,
        y_prueba=y_prueba
    )

    # ========================================================
    # SECCION 5: ARBOL DE DECISION
    # ========================================================

    mostrar_titulo("MODELO 2: ARBOL DE DECISION")

    arbol_decision = DecisionTreeClassifier(
        max_depth=10,
        min_samples_split=20,
        min_samples_leaf=10,
        class_weight="balanced",
        random_state=42
    )

    entrenador.entrenar_modelo(
        nombre_modelo="Arbol de Decision",
        modelo=arbol_decision,
        X_entrenamiento=X_entrenamiento,
        y_entrenamiento=y_entrenamiento,
        X_prueba=X_prueba,
        y_prueba=y_prueba
    )

    # ========================================================
    # SECCION 6: COMPARAR LOS MODELOS
    # ========================================================

    mostrar_titulo("COMPARACION DE LOS MODELOS")

    comparacion = entrenador.obtener_comparacion()

    print(
        comparacion.to_string(
            index=False
        )
    )

    # ========================================================
    # SECCION 7: MATRICES DE CONFUSION
    # ========================================================

    mostrar_titulo("MATRICES DE CONFUSION")

    nombres_modelos = [
        "Regresion Logistica",
        "Arbol de Decision"
    ]

    for nombre_modelo in nombres_modelos:

        matriz = entrenador.obtener_matriz_confusion(
            nombre_modelo
        )

        print(f"\n{nombre_modelo}:")

        print(matriz)

        print("\nInterpretacion:")

        print(
            f"Leves detectados correctamente: "
            f"{matriz[0][0]}"
        )

        print(
            f"Leves clasificados como graves: "
            f"{matriz[0][1]}"
        )

        print(
            f"Graves clasificados como leves: "
            f"{matriz[1][0]}"
        )

        print(
            f"Graves detectados correctamente: "
            f"{matriz[1][1]}"
        )

    # ========================================================
    # SECCION 8: REPORTES DE CLASIFICACION
    # ========================================================

    mostrar_titulo("REPORTES DE CLASIFICACION")

    for nombre_modelo in nombres_modelos:

        reporte = entrenador.obtener_reporte(
            nombre_modelo
        )

        print(f"\n{nombre_modelo}:")

        print(
            reporte.round(4).to_string()
        )

    # ========================================================
    # SECCION 9: SELECCION PRELIMINAR
    # ========================================================

    mostrar_titulo("SELECCION PRELIMINAR")

    (
        nombre_mejor_modelo,
        mejor_modelo
    ) = entrenador.seleccionar_mejor_modelo()

    print(
        f"\nMejor modelo entre los dos evaluados: "
        f"{nombre_mejor_modelo}"
    )

    print(
        f"Tipo del modelo seleccionado: "
        f"{type(mejor_modelo).__name__}"
    )

    # ========================================================
    # SECCION 10: COMPROBACIONES FINALES
    # ========================================================

    mostrar_titulo("COMPROBACION FINAL")

    cantidad_modelos = len(
        entrenador.modelos
    )

    cantidad_resultados = len(
        entrenador.resultados
    )

    cantidad_matrices = len(
        entrenador.matrices_confusion
    )

    resultados_completos = (
        cantidad_modelos == 2
        and cantidad_resultados == 2
        and cantidad_matrices == 2
    )

    columnas_metricas = [
        "modelo",
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
        "tiempo_segundos"
    ]

    metricas_correctas = all(
        columna in comparacion.columns
        for columna in columnas_metricas
    )

    matrices_correctas = all(
        entrenador.matrices_confusion[nombre].shape
        == (2, 2)
        for nombre in nombres_modelos
    )

    mejor_modelo_correcto = (
        nombre_mejor_modelo in nombres_modelos
        and mejor_modelo is not None
    )

    print(
        f"Dos modelos entrenados: "
        f"{resultados_completos}"
    )

    print(
        f"Metricas completas: "
        f"{metricas_correctas}"
    )

    print(
        f"Matrices correctas: "
        f"{matrices_correctas}"
    )

    print(
        f"Mejor modelo seleccionado: "
        f"{mejor_modelo_correcto}"
    )

    if (
        resultados_completos
        and metricas_correctas
        and matrices_correctas
        and mejor_modelo_correcto
    ):
        print(
            "\nLa regresion logistica y el arbol de decision "
            "fueron entrenados y evaluados correctamente."
        )
    else:
        print(
            "\nAdvertencia: revise los resultados "
            "de los modelos iniciales."
        )


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
#
# Esta condicion ejecuta main() cuando el archivo
# se inicia directamente.
# ============================================================

if __name__ == "__main__":
    main()