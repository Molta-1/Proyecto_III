# ============================================================
# PRUEBA FINAL DE GUARDADO DEL MODELO
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Este archivo realiza el proceso final de Machine Learning:
# 1. Carga los datos procesados.
# 2. Relaciona los accidentes con el clima.
# 3. Divide los datos en entrenamiento y prueba.
# 4. Optimiza regresion logistica y arbol de decision.
# 5. Evalua los modelos optimizados.
# 6. Selecciona el modelo con mayor recall de casos graves.
# 7. Guarda el Pipeline completo.
# 8. Guarda las metricas y los hiperparametros.
# 9. Carga nuevamente el modelo guardado.
# 10. Comprueba que las predicciones sean identicas.
#
# IMPORTANTE:
# La optimizacion utiliza solamente el entrenamiento.
# El conjunto de prueba se utiliza para la evaluacion final.
# ============================================================

import os
import json
import numpy as np
import pandas as pd

from src.modelos.PreparadorModelo import PreparadorModelo
from src.modelos.OptimizadorModelos import OptimizadorModelos
from src.modelos.GuardadorModelo import GuardadorModelo


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
# Optimiza, selecciona, guarda y comprueba
# el modelo final del proyecto.
# ============================================================

def main():
    """
    Ejecuta el proceso final de guardado del modelo.
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

    # Comprobar que exista el CSV de accidentes
    if not os.path.exists(ruta_accidentes):
        raise FileNotFoundError(
            f"No se encontro el archivo de accidentes: "
            f"{ruta_accidentes}"
        )

    # Comprobar que exista el CSV climatico
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

    # Relacionar accidentes y clima mensual
    datos_modelo = preparador.relacionar_con_clima(
        datos_accidentes=datos_accidentes,
        datos_clima=datos_clima
    )

    # Separar las variables X e y
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
        f"Registros de entrenamiento: "
        f"{X_entrenamiento.shape[0]}"
    )

    print(
        f"Registros de prueba: "
        f"{X_prueba.shape[0]}"
    )

    # ========================================================
    # SECCION 3: OPTIMIZAR LOS MODELOS
    # ========================================================

    mostrar_titulo("OPTIMIZACION DE LOS MODELOS")

    print(
        "La optimizacion puede tardar varios minutos."
    )

    print(
        "No ejecute nuevamente el archivo mientras "
        "el proceso esta trabajando."
    )

    # Crear el optimizador
    optimizador = OptimizadorModelos(
        preprocesador=preprocesador
    )

    # Optimizar regresion logistica
    optimizador.optimizar_regresion(
        X_entrenamiento=X_entrenamiento,
        y_entrenamiento=y_entrenamiento
    )

    # Optimizar arbol de decision
    optimizador.optimizar_arbol(
        X_entrenamiento=X_entrenamiento,
        y_entrenamiento=y_entrenamiento
    )

    # ========================================================
    # SECCION 4: EVALUAR LOS MODELOS OPTIMIZADOS
    # ========================================================

    mostrar_titulo("EVALUACION FINAL SOBRE PRUEBA")

    comparacion = optimizador.evaluar_optimizados(
        X_prueba=X_prueba,
        y_prueba=y_prueba
    )

    print("\nComparacion de modelos optimizados:")

    print(
        comparacion.to_string(
            index=False
        )
    )

    # ========================================================
    # SECCION 5: SELECCIONAR EL MEJOR MODELO
    # ========================================================

    mostrar_titulo("SELECCION DEL MODELO FINAL")

    (
        nombre_mejor_modelo,
        mejor_modelo
    ) = optimizador.seleccionar_mejor_modelo()

    print(
        f"\nModelo final seleccionado: "
        f"{nombre_mejor_modelo}"
    )

    # Recuperar las metricas del modelo final
    metricas_finales = optimizador.resultados[
        nombre_mejor_modelo
    ]

    # Recuperar los hiperparametros del modelo final
    hiperparametros_finales = (
        optimizador.mejores_parametros[
            nombre_mejor_modelo
        ]
    )

    print("\nMetricas finales:")

    for metrica, valor in metricas_finales.items():
        print(f"- {metrica}: {valor}")

    print("\nHiperparametros finales:")

    for parametro, valor in (
            hiperparametros_finales.items()
    ):
        print(f"- {parametro}: {valor}")

    # ========================================================
    # SECCION 6: GENERAR PREDICCIONES ANTES DE GUARDAR
    # ========================================================

    mostrar_titulo("PREDICCIONES ANTES DE GUARDAR")

    # Generar predicciones con el modelo en memoria
    predicciones_antes = mejor_modelo.predict(
        X_prueba
    )

    # Obtener probabilidades de la clase grave
    probabilidades_antes = mejor_modelo.predict_proba(
        X_prueba
    )[:, 1]

    print(
        f"Predicciones generadas: "
        f"{len(predicciones_antes)}"
    )

    print(
        f"Probabilidades generadas: "
        f"{len(probabilidades_antes)}"
    )

    print("\nPrimeras 10 predicciones:")

    print(
        predicciones_antes[:10]
    )

    print("\nPrimeras 10 probabilidades de gravedad:")

    print(
        np.round(
            probabilidades_antes[:10],
            4
        )
    )

    # ========================================================
    # SECCION 7: GUARDAR EL MODELO Y SUS RESULTADOS
    # ========================================================

    mostrar_titulo("GUARDADO DEL MODELO FINAL")

    # Crear el guardador
    guardador = GuardadorModelo()

    # Guardar el Pipeline
    ruta_modelo = guardador.guardar_modelo(
        modelo=mejor_modelo,
        nombre_archivo=(
            "modelo_gravedad_accidentes.joblib"
        )
    )

    # Guardar las metricas
    ruta_metricas = guardador.guardar_metricas(
        nombre_modelo=nombre_mejor_modelo,
        metricas=metricas_finales,
        nombre_archivo="metricas_modelo.json"
    )

    # Guardar los hiperparametros
    ruta_hiperparametros = (
        guardador.guardar_hiperparametros(
            nombre_modelo=nombre_mejor_modelo,
            hiperparametros=hiperparametros_finales,
            nombre_archivo=(
                "hiperparametros_modelo.json"
            )
        )
    )

    # ========================================================
    # SECCION 8: COMPROBAR LOS ARCHIVOS
    # ========================================================

    mostrar_titulo("COMPROBACION DE LOS ARCHIVOS")

    archivos_generados = {
        "modelo": ruta_modelo,
        "metricas": ruta_metricas,
        "hiperparametros": ruta_hiperparametros
    }

    archivos_correctos = True

    for nombre, ruta in archivos_generados.items():

        comprobacion = guardador.comprobar_archivo(
            ruta
        )

        print(f"\nArchivo: {nombre}")

        print(f"Ruta: {ruta}")

        print(
            f"Existe: "
            f"{comprobacion['existe']}"
        )

        print(
            f"Tamanio en bytes: "
            f"{comprobacion['tamanio_bytes']}"
        )

        print(
            f"Tiene contenido: "
            f"{comprobacion['tiene_contenido']}"
        )

        if not (
            comprobacion["existe"]
            and comprobacion["tiene_contenido"]
        ):
            archivos_correctos = False

    # ========================================================
    # SECCION 9: CARGAR NUEVAMENTE EL MODELO
    # ========================================================

    mostrar_titulo("CARGA DEL MODELO GUARDADO")

    modelo_cargado = guardador.cargar_modelo(
        nombre_archivo=(
            "modelo_gravedad_accidentes.joblib"
        )
    )

    print(
        f"Tipo del modelo cargado: "
        f"{type(modelo_cargado).__name__}"
    )

    # ========================================================
    # SECCION 10: COMPROBAR LAS PREDICCIONES
    # ========================================================

    mostrar_titulo("COMPROBACION DE LAS PREDICCIONES")

    # Generar predicciones con el modelo cargado
    predicciones_despues = modelo_cargado.predict(
        X_prueba
    )

    # Generar probabilidades con el modelo cargado
    probabilidades_despues = (
        modelo_cargado.predict_proba(
            X_prueba
        )[:, 1]
    )

    # Comparar las predicciones
    predicciones_identicas = np.array_equal(
        predicciones_antes,
        predicciones_despues
    )

    # Comparar las probabilidades
    probabilidades_identicas = np.allclose(
        probabilidades_antes,
        probabilidades_despues
    )

    print(
        f"Predicciones identicas: "
        f"{predicciones_identicas}"
    )

    print(
        f"Probabilidades identicas: "
        f"{probabilidades_identicas}"
    )

    # ========================================================
    # SECCION 11: COMPROBAR LOS ARCHIVOS JSON
    # ========================================================

    mostrar_titulo("COMPROBACION DE LOS ARCHIVOS JSON")

    # Leer las metricas guardadas
    with open(
            ruta_metricas,
            "r",
            encoding="utf-8"
    ) as archivo:

        metricas_guardadas = json.load(
            archivo
        )

    # Leer los hiperparametros guardados
    with open(
            ruta_hiperparametros,
            "r",
            encoding="utf-8"
    ) as archivo:

        parametros_guardados = json.load(
            archivo
        )

    print("Contenido principal de metricas_modelo.json:")

    print(
        f"Modelo: "
        f"{metricas_guardadas['modelo_seleccionado']}"
    )

    print(
        f"Criterio principal: "
        f"{metricas_guardadas['criterio_principal']}"
    )

    print(
        f"Recall guardado: "
        f"{metricas_guardadas['metricas']['recall']}"
    )

    print(
        "\nContenido principal de "
        "hiperparametros_modelo.json:"
    )

    print(
        f"Modelo: "
        f"{parametros_guardados['modelo_seleccionado']}"
    )

    print("Parametros:")

    for parametro, valor in (
            parametros_guardados[
                "hiperparametros"
            ].items()
    ):
        print(f"- {parametro}: {valor}")

    # Comprobar los nombres de modelo
    nombres_json_correctos = (
        metricas_guardadas[
            "modelo_seleccionado"
        ] == nombre_mejor_modelo
        and parametros_guardados[
            "modelo_seleccionado"
        ] == nombre_mejor_modelo
    )

    # ========================================================
    # SECCION 12: COMPROBACION FINAL
    # ========================================================

    mostrar_titulo("COMPROBACION FINAL DEL MODELO GUARDADO")

    modelo_correcto = (
        modelo_cargado is not None
        and type(modelo_cargado).__name__
        == "Pipeline"
    )

    metricas_correctas = (
        "accuracy" in metricas_finales
        and "precision" in metricas_finales
        and "recall" in metricas_finales
        and "f1_score" in metricas_finales
        and "roc_auc" in metricas_finales
    )

    hiperparametros_correctos = (
        len(hiperparametros_finales) > 0
    )

    print(
        f"Archivos creados correctamente: "
        f"{archivos_correctos}"
    )

    print(
        f"Pipeline cargado correctamente: "
        f"{modelo_correcto}"
    )

    print(
        f"Predicciones conservadas: "
        f"{predicciones_identicas}"
    )

    print(
        f"Probabilidades conservadas: "
        f"{probabilidades_identicas}"
    )

    print(
        f"Metricas completas: "
        f"{metricas_correctas}"
    )

    print(
        f"Hiperparametros completos: "
        f"{hiperparametros_correctos}"
    )

    print(
        f"Nombres de modelo correctos en JSON: "
        f"{nombres_json_correctos}"
    )

    if (
        archivos_correctos
        and modelo_correcto
        and predicciones_identicas
        and probabilidades_identicas
        and metricas_correctas
        and hiperparametros_correctos
        and nombres_json_correctos
    ):
        print(
            "\nEl modelo final fue guardado, cargado "
            "y comprobado correctamente."
        )

        print(
            "\nEl Pipeline esta listo para utilizarse "
            "en Streamlit."
        )

    else:
        print(
            "\nAdvertencia: revise el guardado "
            "del modelo final."
        )


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
#
# Esta condicion ejecuta main() cuando el archivo
# se inicia directamente.
# ============================================================

if __name__ == "__main__":
    main()