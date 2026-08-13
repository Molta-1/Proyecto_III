# ============================================================
# PRUEBA DE PREDICCION CON EL MODELO FINAL
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Este archivo comprueba:
# 1. La carga del Pipeline final.
# 2. La creacion de un registro nuevo.
# 3. La presencia de las 21 variables predictoras.
# 4. La clasificacion estimada del accidente.
# 5. La probabilidad de accidente leve.
# 6. La probabilidad de accidente grave.
# 7. Que las probabilidades sumen aproximadamente 100 %.
#
# IMPORTANTE:
# Este archivo no reentrena el modelo.
# Este archivo no modifica SQL Server.
# ============================================================

import os
import numpy as np
import pandas as pd

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
# Carga el Pipeline final y realiza una prediccion
# utilizando un registro nuevo.
# ============================================================

def main():
    """
    Realiza una prediccion de prueba con el modelo final.
    """

    # ========================================================
    # SECCION 1: CARGAR EL MODELO FINAL
    # ========================================================

    mostrar_titulo("CARGA DEL MODELO FINAL")

    # Crear el objeto encargado de cargar el modelo
    guardador = GuardadorModelo()

    # Cargar el Pipeline completo
    modelo = guardador.cargar_modelo(
        nombre_archivo=(
            "modelo_gravedad_accidentes.joblib"
        )
    )

    print(
        f"\nTipo del modelo cargado: "
        f"{type(modelo).__name__}"
    )

    # Comprobar que el objeto cargado sea un Pipeline
    if type(modelo).__name__ != "Pipeline":
        raise TypeError(
            "El archivo cargado no contiene un Pipeline."
        )

    # ========================================================
    # SECCION 2: CREAR UN REGISTRO NUEVO
    # ========================================================

    mostrar_titulo("CREACION DEL REGISTRO DE PRUEBA")

    # Este registro utiliza las mismas 21 variables
    # predictoras empleadas durante el entrenamiento.
    nuevo_accidente = pd.DataFrame({
        # Variables numericas
        "anio": [2024],
        "dia_numero": [6],
        "mes_numero": [10],
        "precipitacion_total_mm": [320.50],
        "precipitacion_promedio_mm": [10.34],
        "precipitacion_maxima_mm": [58.20],
        "dias_con_lluvia": [24],

        # Variables categoricas
        "tipo_accidente": [
            "Colisión con motocicleta"
        ],
        "hora_recodificada": [
            "18:00-23:59"
        ],
        "provincia": [
            "Cartago"
        ],
        "zona": [
            "Urbano"
        ],
        "calzada_vertical": [
            "Plano"
        ],
        "calzada_horizontal": [
            "Recta"
        ],
        "tipo_calzada": [
            "Asfalto"
        ],
        "tipo_circulacion": [
            "Doble sentido"
        ],
        "estado_tiempo": [
            "Lluvia"
        ],
        "estado_calzada": [
            "Resbaladiza"
        ],
        "region_mideplan": [
            "Central"
        ],
        "tipo_ruta": [
            "Nacional"
        ],
        "dia": [
            "Viernes"
        ],
        "mes": [
            "Octubre"
        ]
    })

    print("Registro nuevo creado correctamente.")

    print("\nDatos del accidente de prueba:")

    print(
        nuevo_accidente.to_string(
            index=False
        )
    )

    # ========================================================
    # SECCION 3: COMPROBAR LAS VARIABLES
    # ========================================================

    mostrar_titulo("COMPROBACION DE LAS VARIABLES")

    variables_esperadas = [
        "anio",
        "dia_numero",
        "mes_numero",
        "precipitacion_total_mm",
        "precipitacion_promedio_mm",
        "precipitacion_maxima_mm",
        "dias_con_lluvia",
        "tipo_accidente",
        "hora_recodificada",
        "provincia",
        "zona",
        "calzada_vertical",
        "calzada_horizontal",
        "tipo_calzada",
        "tipo_circulacion",
        "estado_tiempo",
        "estado_calzada",
        "region_mideplan",
        "tipo_ruta",
        "dia",
        "mes"
    ]

    variables_faltantes = [
        variable
        for variable in variables_esperadas
        if variable not in nuevo_accidente.columns
    ]

    variables_adicionales = [
        columna
        for columna in nuevo_accidente.columns
        if columna not in variables_esperadas
    ]

    cantidad_variables = nuevo_accidente.shape[1]

    print(
        f"Cantidad de variables encontradas: "
        f"{cantidad_variables}"
    )

    print(
        f"Cantidad de variables esperadas: "
        f"{len(variables_esperadas)}"
    )

    print(
        f"Variables faltantes: "
        f"{variables_faltantes}"
    )

    print(
        f"Variables adicionales: "
        f"{variables_adicionales}"
    )

    if variables_faltantes:
        raise ValueError(
            "El registro no contiene todas las variables "
            "necesarias."
        )

    if variables_adicionales:
        raise ValueError(
            "El registro contiene variables adicionales."
        )

    # Ordenar las columnas exactamente como fueron entrenadas
    nuevo_accidente = nuevo_accidente[
        variables_esperadas
    ]

    print(
        "\nLas 21 variables predictoras "
        "estan presentes correctamente."
    )

    # ========================================================
    # SECCION 4: REALIZAR LA PREDICCION
    # ========================================================

    mostrar_titulo("PREDICCION DE LA GRAVEDAD")

    # Obtener la clasificacion
    prediccion = modelo.predict(
        nuevo_accidente
    )[0]

    # Obtener las probabilidades de las dos clases
    probabilidades = modelo.predict_proba(
        nuevo_accidente
    )[0]

    probabilidad_leve = float(
        probabilidades[0]
    )

    probabilidad_grave = float(
        probabilidades[1]
    )

    # Interpretar la clasificación
    if int(prediccion) == 1:

        clasificacion = (
            "Con muertos o graves"
        )

    else:

        clasificacion = (
            "Solo heridos leves"
        )

    print(
        f"Clasificacion numerica: "
        f"{int(prediccion)}"
    )

    print(
        f"Clasificacion estimada: "
        f"{clasificacion}"
    )

    print(
        f"\nProbabilidad estimada de caso leve: "
        f"{probabilidad_leve * 100:.2f} %"
    )

    print(
        f"Probabilidad estimada de caso grave: "
        f"{probabilidad_grave * 100:.2f} %"
    )

    # ========================================================
    # SECCION 5: COMPROBAR LAS PROBABILIDADES
    # ========================================================

    mostrar_titulo("COMPROBACION DE LAS PROBABILIDADES")

    suma_probabilidades = (
        probabilidad_leve
        + probabilidad_grave
    )

    probabilidades_en_rango = (
        0 <= probabilidad_leve <= 1
        and 0 <= probabilidad_grave <= 1
    )

    suma_correcta = np.isclose(
        suma_probabilidades,
        1.0
    )

    prediccion_valida = (
        int(prediccion) in [0, 1]
    )

    clase_mayor_probabilidad = int(
        np.argmax(probabilidades)
    )

    prediccion_coincide = (
        int(prediccion)
        == clase_mayor_probabilidad
    )

    print(
        f"Suma de probabilidades: "
        f"{suma_probabilidades:.6f}"
    )

    print(
        f"Probabilidades entre 0 y 1: "
        f"{probabilidades_en_rango}"
    )

    print(
        f"Las probabilidades suman 1: "
        f"{suma_correcta}"
    )

    print(
        f"La prediccion es 0 o 1: "
        f"{prediccion_valida}"
    )

    print(
        f"La prediccion coincide con la mayor "
        f"probabilidad: {prediccion_coincide}"
    )

    # ========================================================
    # SECCION 6: CREAR UN RESULTADO PARA STREAMLIT
    # ========================================================

    mostrar_titulo("RESULTADO PARA EL DASHBOARD")

    resultado_dashboard = {
        "clasificacion_numerica": int(
            prediccion
        ),
        "clasificacion_texto": clasificacion,
        "probabilidad_leve": round(
            probabilidad_leve,
            4
        ),
        "probabilidad_grave": round(
            probabilidad_grave,
            4
        )
    }

    print("Resultado que puede utilizar Streamlit:")

    for nombre, valor in (
            resultado_dashboard.items()
    ):
        print(f"- {nombre}: {valor}")

    # ========================================================
    # SECCION 7: COMPROBACION FINAL
    # ========================================================

    mostrar_titulo("COMPROBACION FINAL DE LA PREDICCION")

    modelo_cargado = (
        modelo is not None
        and type(modelo).__name__ == "Pipeline"
    )

    variables_correctas = (
        cantidad_variables == 21
        and not variables_faltantes
        and not variables_adicionales
    )

    resultado_correcto = (
        probabilidades_en_rango
        and suma_correcta
        and prediccion_valida
        and prediccion_coincide
    )

    resultado_dashboard_correcto = (
        len(resultado_dashboard) == 4
        and "clasificacion_texto"
        in resultado_dashboard
        and "probabilidad_grave"
        in resultado_dashboard
    )

    print(
        f"Pipeline cargado correctamente: "
        f"{modelo_cargado}"
    )

    print(
        f"Variables correctas: "
        f"{variables_correctas}"
    )

    print(
        f"Resultado matematicamente correcto: "
        f"{resultado_correcto}"
    )

    print(
        f"Resultado preparado para Streamlit: "
        f"{resultado_dashboard_correcto}"
    )

    if (
        modelo_cargado
        and variables_correctas
        and resultado_correcto
        and resultado_dashboard_correcto
    ):
        print(
            "\nLa prediccion con un registro nuevo "
            "fue realizada correctamente."
        )

        print(
            "\nEl Pipeline esta listo para integrarse "
            "en el formulario de Streamlit."
        )

    else:
        print(
            "\nAdvertencia: revise la prueba "
            "de prediccion."
        )


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
#
# Esta condicion ejecuta main() cuando el archivo
# se inicia directamente.
# ============================================================

if __name__ == "__main__":
    main()