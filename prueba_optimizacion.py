# ============================================================
# PRUEBA DE OPTIMIZACION DE MODELOS
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Este archivo comprueba:
# 1. La carga de los datos procesados.
# 2. La preparacion de las variables.
# 3. La division estratificada 80 % y 20 %.
# 4. La optimizacion de la regresion logistica.
# 5. La optimizacion del arbol de decision.
# 6. La evaluacion sobre el conjunto de prueba.
# 7. La comparacion con los modelos originales.
# 8. La seleccion del mejor modelo optimizado.
#
# IMPORTANTE:
# Los parametros se seleccionan usando solamente entrenamiento.
# El conjunto de prueba se utiliza al final para evaluar.
# Este archivo no modifica SQL Server.
# ============================================================

import os
import pandas as pd

from src.modelos.PreparadorModelo import PreparadorModelo
from src.modelos.OptimizadorModelos import OptimizadorModelos


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
# Prepara los datos, optimiza los modelos
# y comprueba sus resultados finales.
# ============================================================

def main():
    """
    Optimiza y compara regresion logistica
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

    # Comprobar que exista el archivo de accidentes
    if not os.path.exists(ruta_accidentes):
        raise FileNotFoundError(
            f"No se encontro el archivo de accidentes: "
            f"{ruta_accidentes}"
        )

    # Comprobar que exista el archivo climatico
    if not os.path.exists(ruta_clima):
        raise FileNotFoundError(
            f"No se encontro el archivo climatico: "
            f"{ruta_clima}"
        )

    # Cargar los accidentes procesados
    datos_accidentes = pd.read_csv(
        ruta_accidentes,
        sep=";",
        encoding="utf-8-sig",
        low_memory=False
    )

    # Cargar el resumen climatico
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

    # Relacionar cada accidente con el clima
    datos_modelo = preparador.relacionar_con_clima(
        datos_accidentes=datos_accidentes,
        datos_clima=datos_clima
    )

    # Separar variables predictoras y objetivo
    X, y = preparador.separar_variables(
        datos_modelo
    )

    # Dividir los datos
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
        f"Registros de entrenamiento: "
        f"{X_entrenamiento.shape[0]}"
    )

    print(
        f"Registros de prueba: "
        f"{X_prueba.shape[0]}"
    )

    print(
        f"Variables predictoras: "
        f"{X_entrenamiento.shape[1]}"
    )

    # ========================================================
    # SECCION 3: CREAR EL OPTIMIZADOR
    # ========================================================

    mostrar_titulo("CREACION DEL OPTIMIZADOR")

    optimizador = OptimizadorModelos(
        preprocesador=preprocesador
    )

    print("OptimizadorModelos creado correctamente.")

    # ========================================================
    # SECCION 4: OPTIMIZAR REGRESION LOGISTICA
    # ========================================================

    mostrar_titulo("BUSQUEDA DE PARAMETROS DE REGRESION")

    print(
        "Se probaran 9 configuraciones mediante "
        "validacion cruzada."
    )

    busqueda_regresion = (
        optimizador.optimizar_regresion(
            X_entrenamiento=X_entrenamiento,
            y_entrenamiento=y_entrenamiento
        )
    )

    # ========================================================
    # SECCION 5: OPTIMIZAR ARBOL DE DECISION
    # ========================================================

    mostrar_titulo("BUSQUEDA DE PARAMETROS DEL ARBOL")

    print(
        "Se probaran 24 configuraciones mediante "
        "validacion cruzada."
    )

    busqueda_arbol = (
        optimizador.optimizar_arbol(
            X_entrenamiento=X_entrenamiento,
            y_entrenamiento=y_entrenamiento
        )
    )

    # ========================================================
    # SECCION 6: MOSTRAR LOS MEJORES PARAMETROS
    # ========================================================

    mostrar_titulo("MEJORES PARAMETROS ENCONTRADOS")

    print("Regresion Logistica Optimizada:")

    for parametro, valor in (
            busqueda_regresion.best_params_.items()
    ):
        print(f"- {parametro}: {valor}")

    print(
        f"Recall promedio de validacion: "
        f"{busqueda_regresion.best_score_:.4f}"
    )

    print("\nArbol de Decision Optimizado:")

    for parametro, valor in (
            busqueda_arbol.best_params_.items()
    ):
        print(f"- {parametro}: {valor}")

    print(
        f"Recall promedio de validacion: "
        f"{busqueda_arbol.best_score_:.4f}"
    )

    # ========================================================
    # SECCION 7: EVALUAR SOBRE EL CONJUNTO DE PRUEBA
    # ========================================================

    mostrar_titulo("EVALUACION FINAL SOBRE PRUEBA")

    comparacion_optimizados = (
        optimizador.evaluar_optimizados(
            X_prueba=X_prueba,
            y_prueba=y_prueba
        )
    )

    print("\nComparacion de los modelos optimizados:")

    print(
        comparacion_optimizados.to_string(
            index=False
        )
    )

    # ========================================================
    # SECCION 8: MATRICES DE CONFUSION
    # ========================================================

    mostrar_titulo("MATRICES DE CONFUSION")

    nombres_modelos = [
        "Regresion Logistica Optimizada",
        "Arbol de Decision Optimizado"
    ]

    for nombre_modelo in nombres_modelos:

        matriz = (
            optimizador.obtener_matriz_confusion(
                nombre_modelo
            )
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
    # SECCION 9: REPORTES DE CLASIFICACION
    # ========================================================

    mostrar_titulo("REPORTES DE CLASIFICACION")

    for nombre_modelo in nombres_modelos:

        reporte = optimizador.obtener_reporte(
            nombre_modelo
        )

        print(f"\n{nombre_modelo}:")

        print(
            reporte.round(4).to_string()
        )

    # ========================================================
    # SECCION 10: COMPARAR CON MODELOS ORIGINALES
    # ========================================================

    mostrar_titulo(
        "COMPARACION CON LAS CONFIGURACIONES ORIGINALES"
    )

    # Resultados obtenidos anteriormente
    resultados_originales = pd.DataFrame({
        "modelo": [
            "Regresion Logistica Original",
            "Arbol de Decision Original",
            "KNN Original"
        ],
        "accuracy": [
            0.7031,
            0.6739,
            0.8370
        ],
        "precision": [
            0.2792,
            0.2590,
            0.3466
        ],
        "recall": [
            0.6554,
            0.6649,
            0.1335
        ],
        "f1_score": [
            0.3916,
            0.3728,
            0.1928
        ],
        "roc_auc": [
            0.0,
            0.7209,
            0.6354
        ]
    })

    # Copiar la comparación optimizada
    resultados_optimizados = (
        comparacion_optimizados.copy()
    )

    # Unir resultados originales y optimizados
    comparacion_completa = pd.concat(
        [
            resultados_originales,
            resultados_optimizados
        ],
        ignore_index=True
    )

    # Ordenar por recall, F1 y ROC-AUC
    comparacion_completa = (
        comparacion_completa
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

    print(
        comparacion_completa.to_string(
            index=False
        )
    )

    print(
        "\nNota: el ROC-AUC de la regresion original "
        "se muestra como 0 porque no se recupero de la "
        "captura anterior. Este valor no se utilizara "
        "para seleccionarla."
    )

    # ========================================================
    # SECCION 11: SELECCIONAR EL MEJOR OPTIMIZADO
    # ========================================================

    mostrar_titulo("SELECCION DEL MEJOR MODELO OPTIMIZADO")

    (
        nombre_mejor_modelo,
        mejor_modelo
    ) = optimizador.seleccionar_mejor_modelo()

    print(
        f"\nModelo optimizado seleccionado: "
        f"{nombre_mejor_modelo}"
    )

    print(
        f"Tipo del objeto seleccionado: "
        f"{type(mejor_modelo).__name__}"
    )

    # ========================================================
    # SECCION 12: ANALIZAR EL EQUILIBRIO
    # ========================================================

    mostrar_titulo("ANALISIS DEL EQUILIBRIO DE METRICAS")

    fila_mejor = comparacion_optimizados.loc[
        comparacion_optimizados["modelo"]
        == nombre_mejor_modelo
    ].iloc[0]

    recall_mejor = float(
        fila_mejor["recall"]
    )

    precision_mejor = float(
        fila_mejor["precision"]
    )

    f1_mejor = float(
        fila_mejor["f1_score"]
    )

    roc_auc_mejor = float(
        fila_mejor["roc_auc"]
    )

    print(
        f"Recall del mejor modelo: "
        f"{recall_mejor:.4f}"
    )

    print(
        f"Precision del mejor modelo: "
        f"{precision_mejor:.4f}"
    )

    print(
        f"F1-score del mejor modelo: "
        f"{f1_mejor:.4f}"
    )

    print(
        f"ROC-AUC del mejor modelo: "
        f"{roc_auc_mejor:.4f}"
    )

    if recall_mejor >= 0.70:
        print(
            "\nEl modelo detecta al menos el 70 % "
            "de los accidentes graves."
        )
    else:
        print(
            "\nEl modelo detecta menos del 70 % "
            "de los accidentes graves."
        )

    if precision_mejor < 0.20:
        print(
            "Advertencia: la precision de casos graves "
            "es inferior al 20 %."
        )

        print(
            "El aumento del recall produce demasiados "
            "falsos positivos."
        )
    else:
        print(
            "La precision de accidentes graves se mantiene "
            "por encima del 20 %."
        )

    # ========================================================
    # SECCION 13: COMPROBACIONES FINALES
    # ========================================================

    mostrar_titulo("COMPROBACION FINAL")

    busquedas_correctas = (
        len(optimizador.busquedas) == 2
    )

    parametros_correctos = (
        len(optimizador.mejores_parametros) == 2
    )

    modelos_correctos = (
        len(optimizador.mejores_modelos) == 2
    )

    resultados_correctos = (
        len(optimizador.resultados) == 2
    )

    matrices_correctas = all(
        optimizador.matrices_confusion[
            nombre_modelo
        ].shape == (2, 2)
        for nombre_modelo in nombres_modelos
    )

    mejor_modelo_correcto = (
        nombre_mejor_modelo in nombres_modelos
        and mejor_modelo is not None
    )

    metricas_validas = all(
        0 <= float(
            comparacion_optimizados.loc[
                indice,
                metrica
            ]
        ) <= 1
        for indice in comparacion_optimizados.index
        for metrica in [
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "roc_auc"
        ]
    )

    print(
        f"Dos busquedas completadas: "
        f"{busquedas_correctas}"
    )

    print(
        f"Parametros encontrados: "
        f"{parametros_correctos}"
    )

    print(
        f"Dos modelos optimizados: "
        f"{modelos_correctos}"
    )

    print(
        f"Dos evaluaciones finales: "
        f"{resultados_correctos}"
    )

    print(
        f"Matrices correctas: "
        f"{matrices_correctas}"
    )

    print(
        f"Mejor modelo seleccionado: "
        f"{mejor_modelo_correcto}"
    )

    print(
        f"Metricas en rango valido: "
        f"{metricas_validas}"
    )

    if (
        busquedas_correctas
        and parametros_correctos
        and modelos_correctos
        and resultados_correctos
        and matrices_correctas
        and mejor_modelo_correcto
        and metricas_validas
    ):
        print(
            "\nLa optimizacion de hiperparametros fue "
            "realizada correctamente."
        )
    else:
        print(
            "\nAdvertencia: revise los resultados "
            "de la optimizacion."
        )


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
#
# Esta condicion ejecuta main() cuando el archivo
# se inicia directamente.
# ============================================================

if __name__ == "__main__":
    main()