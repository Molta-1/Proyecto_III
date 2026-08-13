# ============================================================
# PRUEBA DEL MODELO KNN
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Este archivo comprueba:
# 1. La carga de los archivos procesados.
# 2. La relacion entre accidentes y clima.
# 3. La preparacion de las variables.
# 4. La division estratificada 80 % y 20 %.
# 5. El entrenamiento del modelo KNN.
# 6. El calculo de metricas.
# 7. La matriz de confusion.
# 8. El reporte de clasificacion.
#
# IMPORTANTE:
# Este archivo no modifica SQL Server.
# ============================================================

import os
import time
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier

from src.modelos.PreparadorModelo import PreparadorModelo
from src.modelos.EntrenadorModelos import EntrenadorModelos


# ============================================================
# FUNCION AUXILIAR: MOSTRAR TITULO
#
# Organiza los resultados presentados en la consola.
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
# Prepara los datos y evalua el modelo KNN.
# ============================================================

def main():
    """
    Entrena y evalua el modelo KNN.
    """

    # ========================================================
    # SECCION 1: CARGAR LOS ARCHIVOS PROCESADOS
    # ========================================================

    mostrar_titulo("CARGA DE LOS ARCHIVOS PROCESADOS")

    # Obtener la carpeta principal del proyecto
    carpeta_proyecto = os.path.dirname(
        os.path.abspath(__file__)
    )

    # Construir la ruta del archivo de accidentes
    ruta_accidentes = os.path.join(
        carpeta_proyecto,
        "data",
        "processed",
        "accidentes_victimas_limpio.csv"
    )

    # Construir la ruta del archivo climatico
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

    # Cargar el CSV de accidentes
    datos_accidentes = pd.read_csv(
        ruta_accidentes,
        sep=";",
        encoding="utf-8-sig",
        low_memory=False
    )

    # Cargar el CSV climatico mensual
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

    # Relacionar cada accidente con el clima mensual
    datos_modelo = preparador.relacionar_con_clima(
        datos_accidentes=datos_accidentes,
        datos_clima=datos_clima
    )

    # Separar variables predictoras y objetivo
    X, y = preparador.separar_variables(
        datos_modelo
    )

    # Dividir 80 % entrenamiento y 20 % prueba
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
        f"Variables predictoras originales: "
        f"{X_entrenamiento.shape[1]}"
    )

    # ========================================================
    # SECCION 3: CREAR EL MODELO KNN
    # ========================================================

    mostrar_titulo("CREACION DEL MODELO KNN")

    # Crear el entrenador
    entrenador = EntrenadorModelos(
        preprocesador=preprocesador
    )

    # Crear KNN con cinco vecinos
    modelo_knn = KNeighborsClassifier(
        n_neighbors=5,
        weights="distance",
        n_jobs=-1
    )

    print("Modelo KNN creado correctamente.")

    print("\nConfiguracion utilizada:")
    print("Cantidad de vecinos: 5")
    print("Tipo de pesos: distance")
    print("Procesadores disponibles: todos")

    # ========================================================
    # SECCION 4: ENTRENAR Y EVALUAR KNN
    # ========================================================

    mostrar_titulo("ENTRENAMIENTO Y EVALUACION DE KNN")

    print(
        "KNN puede tardar más que los modelos anteriores."
    )

    print(
        "No cierre PyCharm ni ejecute nuevamente "
        "el archivo mientras está trabajando."
    )

    tiempo_inicio_total = time.time()

    entrenador.entrenar_modelo(
        nombre_modelo="KNN",
        modelo=modelo_knn,
        X_entrenamiento=X_entrenamiento,
        y_entrenamiento=y_entrenamiento,
        X_prueba=X_prueba,
        y_prueba=y_prueba
    )

    tiempo_total = (
        time.time() - tiempo_inicio_total
    )

    print(
        f"\nTiempo total de entrenamiento y evaluacion: "
        f"{tiempo_total:.2f} segundos."
    )

    # ========================================================
    # SECCION 5: MOSTRAR LAS METRICAS
    # ========================================================

    mostrar_titulo("METRICAS DEL MODELO KNN")

    comparacion = entrenador.obtener_comparacion()

    print(
        comparacion.to_string(
            index=False
        )
    )

    metricas_knn = entrenador.resultados["KNN"]

    print("\nInterpretacion de las metricas:")

    print(
        f"Accuracy general: "
        f"{metricas_knn['accuracy'] * 100:.2f} %"
    )

    print(
        f"Precision de accidentes graves: "
        f"{metricas_knn['precision'] * 100:.2f} %"
    )

    print(
        f"Recall de accidentes graves: "
        f"{metricas_knn['recall'] * 100:.2f} %"
    )

    print(
        f"F1-score de accidentes graves: "
        f"{metricas_knn['f1_score'] * 100:.2f} %"
    )

    print(
        f"ROC-AUC: "
        f"{metricas_knn['roc_auc'] * 100:.2f} %"
    )

    # ========================================================
    # SECCION 6: MATRIZ DE CONFUSION
    # ========================================================

    mostrar_titulo("MATRIZ DE CONFUSION DE KNN")

    matriz = entrenador.obtener_matriz_confusion(
        "KNN"
    )

    print(matriz)

    verdaderos_leves = int(matriz[0][0])
    falsos_graves = int(matriz[0][1])
    falsos_leves = int(matriz[1][0])
    verdaderos_graves = int(matriz[1][1])

    print("\nInterpretacion:")

    print(
        f"Leves detectados correctamente: "
        f"{verdaderos_leves}"
    )

    print(
        f"Leves clasificados como graves: "
        f"{falsos_graves}"
    )

    print(
        f"Graves clasificados como leves: "
        f"{falsos_leves}"
    )

    print(
        f"Graves detectados correctamente: "
        f"{verdaderos_graves}"
    )

    total_matriz = int(matriz.sum())

    print(
        f"\nTotal de registros en la matriz: "
        f"{total_matriz}"
    )

    # ========================================================
    # SECCION 7: REPORTE DE CLASIFICACION
    # ========================================================

    mostrar_titulo("REPORTE DE CLASIFICACION DE KNN")

    reporte = entrenador.obtener_reporte(
        "KNN"
    )

    print(
        reporte.round(4).to_string()
    )

    # ========================================================
    # SECCION 8: COMPROBACIONES FINALES
    # ========================================================

    mostrar_titulo("COMPROBACION FINAL DE KNN")

    modelo_entrenado = (
        "KNN" in entrenador.modelos
    )

    metricas_completas = all(
        metrica in metricas_knn
        for metrica in [
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "roc_auc",
            "tiempo_segundos"
        ]
    )

    matriz_correcta = (
        matriz.shape == (2, 2)
        and total_matriz == len(y_prueba)
    )

    reporte_correcto = (
        "Leve" in reporte.index
        and "Grave" in reporte.index
    )

    probabilidades_validas = (
        0 <= metricas_knn["roc_auc"] <= 1
    )

    print(
        f"Modelo entrenado: "
        f"{modelo_entrenado}"
    )

    print(
        f"Metricas completas: "
        f"{metricas_completas}"
    )

    print(
        f"Matriz correcta: "
        f"{matriz_correcta}"
    )

    print(
        f"Reporte correcto: "
        f"{reporte_correcto}"
    )

    print(
        f"ROC-AUC valido: "
        f"{probabilidades_validas}"
    )

    if (
        modelo_entrenado
        and metricas_completas
        and matriz_correcta
        and reporte_correcto
        and probabilidades_validas
    ):
        print(
            "\nEl modelo KNN fue entrenado y evaluado "
            "correctamente."
        )
    else:
        print(
            "\nAdvertencia: revise los resultados de KNN."
        )


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
#
# Esta condicion ejecuta main() cuando el archivo
# se inicia directamente.
# ============================================================

if __name__ == "__main__":
    main()