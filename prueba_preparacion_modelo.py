# ============================================================
# PRUEBA DE PREPARACION PARA MACHINE LEARNING
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Este archivo comprueba:
# 1. La carga de los accidentes procesados.
# 2. La carga del resumen climatico mensual.
# 3. La relacion entre accidentes y clima.
# 4. La seleccion de las variables predictoras.
# 5. La separacion entre X e y.
# 6. La division 80 % entrenamiento y 20 % prueba.
# 7. La estratificacion de la variable gravedad.
# 8. La creacion del preprocesador.
# 9. La transformacion de los datos de entrenamiento.
#
# IMPORTANTE:
# Este archivo no entrena modelos y no modifica SQL Server.
# ============================================================

import os
import pandas as pd

from src.modelos.PreparadorModelo import PreparadorModelo


# ============================================================
# FUNCION AUXILIAR: MOSTRAR TITULO
#
# Muestra un encabezado para organizar la salida en consola.
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
# Carga los datos y prueba todos los pasos necesarios
# antes de entrenar los modelos de clasificacion.
# ============================================================

def main():
    """
    Comprueba la preparacion de los datos para Machine Learning.
    """

    # ========================================================
    # SECCION 1: CARGAR LOS ARCHIVOS PROCESADOS
    # ========================================================

    mostrar_titulo("CARGA DE LOS ARCHIVOS PROCESADOS")

    # --------------------------------------------------------
    # PASO 1: OBTENER LA CARPETA PRINCIPAL DEL PROYECTO
    # --------------------------------------------------------

    carpeta_proyecto = os.path.dirname(
        os.path.abspath(__file__)
    )

    # --------------------------------------------------------
    # PASO 2: CONSTRUIR LAS RUTAS DE LOS ARCHIVOS
    # --------------------------------------------------------

    ruta_accidentes = os.path.join(
        carpeta_proyecto,
        "data",
        "processed",
        "accidentes_victimas_limpio.csv"
    )

    ruta_clima = os.path.join(
        carpeta_proyecto,
        "data",
        "processed",
        "clima_mensual_2018_2024.csv"
    )

    # --------------------------------------------------------
    # PASO 3: COMPROBAR QUE LOS ARCHIVOS EXISTAN
    # --------------------------------------------------------

    if not os.path.exists(ruta_accidentes):
        raise FileNotFoundError(
            f"No se encontro el archivo de accidentes: "
            f"{ruta_accidentes}"
        )

    if not os.path.exists(ruta_clima):
        raise FileNotFoundError(
            f"No se encontro el archivo climatico: "
            f"{ruta_clima}"
        )

    print("Archivo de accidentes encontrado correctamente.")
    print(ruta_accidentes)

    print("\nArchivo climatico encontrado correctamente.")
    print(ruta_clima)

    # --------------------------------------------------------
    # PASO 4: CARGAR EL CSV DE ACCIDENTES
    # --------------------------------------------------------

    datos_accidentes = pd.read_csv(
        ruta_accidentes,
        sep=";",
        encoding="utf-8-sig",
        low_memory=False
    )

    print("\nDatos de accidentes cargados correctamente.")

    print(
        f"Filas de accidentes: "
        f"{datos_accidentes.shape[0]}"
    )

    print(
        f"Columnas de accidentes: "
        f"{datos_accidentes.shape[1]}"
    )

    # --------------------------------------------------------
    # PASO 5: CARGAR EL CSV CLIMATICO
    # --------------------------------------------------------

    datos_clima = pd.read_csv(
        ruta_clima,
        sep=";",
        encoding="utf-8-sig",
        low_memory=False
    )

    print("\nDatos climaticos cargados correctamente.")

    print(
        f"Filas climaticas: "
        f"{datos_clima.shape[0]}"
    )

    print(
        f"Columnas climaticas: "
        f"{datos_clima.shape[1]}"
    )

    # ========================================================
    # SECCION 2: CREAR EL PREPARADOR
    # ========================================================

    mostrar_titulo("CREACION DEL PREPARADOR DEL MODELO")

    preparador = PreparadorModelo()

    print("PreparadorModelo creado correctamente.")

    print("\nVariable objetivo:")
    print(preparador.variable_objetivo)

    print("\nVariables numericas:")

    for variable in preparador.variables_numericas:
        print(f"- {variable}")

    print(
        f"\nCantidad de variables numericas: "
        f"{len(preparador.variables_numericas)}"
    )

    print("\nVariables categoricas:")

    for variable in preparador.variables_categoricas:
        print(f"- {variable}")

    print(
        f"\nCantidad de variables categoricas: "
        f"{len(preparador.variables_categoricas)}"
    )

    print(
        f"\nTotal de variables predictoras: "
        f"{len(preparador.variables_predictoras)}"
    )

    # ========================================================
    # SECCION 3: RELACIONAR ACCIDENTES Y CLIMA
    # ========================================================

    mostrar_titulo("RELACION ENTRE ACCIDENTES Y CLIMA")

    datos_modelo = preparador.relacionar_con_clima(
        datos_accidentes=datos_accidentes,
        datos_clima=datos_clima
    )

    print("\nDimensiones de los datos relacionados:")

    print(
        f"Filas: "
        f"{datos_modelo.shape[0]}"
    )

    print(
        f"Columnas: "
        f"{datos_modelo.shape[1]}"
    )

    # --------------------------------------------------------
    # PASO 6: COMPROBAR LOS INDICADORES CLIMATICOS
    # --------------------------------------------------------

    indicadores_climaticos = [
        "precipitacion_total_mm",
        "precipitacion_promedio_mm",
        "precipitacion_maxima_mm",
        "dias_con_lluvia"
    ]

    vacios_climaticos = (
        datos_modelo[indicadores_climaticos]
        .isna()
        .sum()
    )

    print("\nValores vacios en indicadores climaticos:")

    print(vacios_climaticos)

    # ========================================================
    # SECCION 4: SEPARAR X E Y
    # ========================================================

    mostrar_titulo("SEPARACION DE VARIABLES")

    X, y = preparador.separar_variables(
        datos_modelo
    )

    print("\nDimensiones de X:")

    print(f"Filas: {X.shape[0]}")
    print(f"Columnas: {X.shape[1]}")

    print("\nDimensiones de y:")

    print(f"Filas: {y.shape[0]}")

    print("\nColumnas utilizadas en X:")

    for columna in X.columns:
        print(f"- {columna}")

    # --------------------------------------------------------
    # PASO 7: COMPROBAR QUE NO EXISTA FUGA DE INFORMACION
    # --------------------------------------------------------

    variables_prohibidas = [
        "clase_accidente",
        "gravedad"
    ]

    variables_prohibidas_en_x = [
        variable
        for variable in variables_prohibidas
        if variable in X.columns
    ]

    print("\nComprobacion de fuga de informacion:")

    if not variables_prohibidas_en_x:
        print(
            "X no contiene clase_accidente ni gravedad."
        )
    else:
        print(
            "Advertencia: X contiene variables prohibidas:"
        )

        print(variables_prohibidas_en_x)

    # ========================================================
    # SECCION 5: DISTRIBUCION ORIGINAL
    # ========================================================

    mostrar_titulo("DISTRIBUCION ORIGINAL DE GRAVEDAD")

    distribucion_original = (
        preparador.obtener_distribucion(y)
    )

    print(
        distribucion_original.to_string(
            index=False
        )
    )

    # ========================================================
    # SECCION 6: DIVIDIR ENTRENAMIENTO Y PRUEBA
    # ========================================================

    mostrar_titulo("DIVISION DE ENTRENAMIENTO Y PRUEBA")

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

    print("\nDimensiones del entrenamiento:")

    print(
        f"X entrenamiento: "
        f"{X_entrenamiento.shape}"
    )

    print(
        f"y entrenamiento: "
        f"{y_entrenamiento.shape}"
    )

    print("\nDimensiones de la prueba:")

    print(
        f"X prueba: "
        f"{X_prueba.shape}"
    )

    print(
        f"y prueba: "
        f"{y_prueba.shape}"
    )

    # ========================================================
    # SECCION 7: COMPROBAR ESTRATIFICACION
    # ========================================================

    mostrar_titulo("COMPROBACION DE LA ESTRATIFICACION")

    distribucion_entrenamiento = (
        preparador.obtener_distribucion(
            y_entrenamiento
        )
    )

    distribucion_prueba = (
        preparador.obtener_distribucion(
            y_prueba
        )
    )

    print("Distribucion del entrenamiento:")

    print(
        distribucion_entrenamiento.to_string(
            index=False
        )
    )

    print("\nDistribucion de la prueba:")

    print(
        distribucion_prueba.to_string(
            index=False
        )
    )

    # Obtener el porcentaje grave de cada conjunto
    porcentaje_grave_original = float(
        distribucion_original.loc[
            distribucion_original["gravedad"] == 1,
            "porcentaje"
        ].iloc[0]
    )

    porcentaje_grave_entrenamiento = float(
        distribucion_entrenamiento.loc[
            distribucion_entrenamiento["gravedad"] == 1,
            "porcentaje"
        ].iloc[0]
    )

    porcentaje_grave_prueba = float(
        distribucion_prueba.loc[
            distribucion_prueba["gravedad"] == 1,
            "porcentaje"
        ].iloc[0]
    )

    print("\nPorcentaje de accidentes graves:")

    print(
        f"Conjunto original: "
        f"{porcentaje_grave_original} %"
    )

    print(
        f"Entrenamiento: "
        f"{porcentaje_grave_entrenamiento} %"
    )

    print(
        f"Prueba: "
        f"{porcentaje_grave_prueba} %"
    )

    # ========================================================
    # SECCION 8: CREAR Y PROBAR EL PREPROCESADOR
    # ========================================================

    mostrar_titulo("CREACION DEL PREPROCESADOR")

    preprocesador = (
        preparador.crear_preprocesador()
    )

    print("\nTipo de preprocesador creado:")

    print(type(preprocesador).__name__)

    # --------------------------------------------------------
    # PASO 8: AJUSTAR Y TRANSFORMAR ENTRENAMIENTO
    #
    # El preprocesador aprende solamente con entrenamiento.
    # Esto evita utilizar informacion del conjunto de prueba.
    # --------------------------------------------------------

    print(
        "\nAjustando y transformando los datos "
        "de entrenamiento..."
    )

    X_entrenamiento_transformado = (
        preprocesador.fit_transform(
            X_entrenamiento
        )
    )

    print(
        "Datos de entrenamiento transformados "
        "correctamente."
    )

    # --------------------------------------------------------
    # PASO 9: TRANSFORMAR PRUEBA
    #
    # En prueba se usa transform(), no fit_transform().
    # --------------------------------------------------------

    print(
        "\nTransformando los datos de prueba..."
    )

    X_prueba_transformado = (
        preprocesador.transform(
            X_prueba
        )
    )

    print(
        "Datos de prueba transformados correctamente."
    )

    print("\nDimensiones despues del preprocesamiento:")

    print(
        f"Entrenamiento transformado: "
        f"{X_entrenamiento_transformado.shape}"
    )

    print(
        f"Prueba transformada: "
        f"{X_prueba_transformado.shape}"
    )

    # ========================================================
    # SECCION 9: COMPROBACIONES FINALES
    # ========================================================

    mostrar_titulo("COMPROBACION FINAL")

    filas_esperadas = 104821
    filas_entrenamiento_esperadas = 83856
    filas_prueba_esperadas = 20965
    variables_predictoras_esperadas = 21

    filas_correctas = (
        datos_modelo.shape[0] == filas_esperadas
        and X.shape[0] == filas_esperadas
        and len(y) == filas_esperadas
    )

    division_correcta = (
        X_entrenamiento.shape[0]
        == filas_entrenamiento_esperadas
        and X_prueba.shape[0]
        == filas_prueba_esperadas
        and len(y_entrenamiento)
        == filas_entrenamiento_esperadas
        and len(y_prueba)
        == filas_prueba_esperadas
    )

    variables_correctas = (
        X.shape[1]
        == variables_predictoras_esperadas
        and not variables_prohibidas_en_x
    )

    clima_correcto = (
        vacios_climaticos.sum() == 0
    )

    estratificacion_correcta = (
        porcentaje_grave_original
        == porcentaje_grave_entrenamiento
        == porcentaje_grave_prueba
    )

    preprocesamiento_correcto = (
        X_entrenamiento_transformado.shape[0]
        == filas_entrenamiento_esperadas
        and X_prueba_transformado.shape[0]
        == filas_prueba_esperadas
        and X_entrenamiento_transformado.shape[1]
        == X_prueba_transformado.shape[1]
    )

    print(f"Filas correctas: {filas_correctas}")
    print(f"Division correcta: {division_correcta}")
    print(f"Variables correctas: {variables_correctas}")
    print(f"Clima relacionado correctamente: {clima_correcto}")

    print(
        f"Estratificacion correcta: "
        f"{estratificacion_correcta}"
    )

    print(
        f"Preprocesamiento correcto: "
        f"{preprocesamiento_correcto}"
    )

    if (
        filas_correctas
        and division_correcta
        and variables_correctas
        and clima_correcto
        and estratificacion_correcta
        and preprocesamiento_correcto
    ):
        print(
            "\nLa preparacion de los datos para "
            "Machine Learning fue realizada correctamente."
        )
    else:
        print(
            "\nAdvertencia: revise la preparacion "
            "de los datos."
        )


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
#
# Esta condicion ejecuta main() cuando el archivo
# se inicia directamente.
# ============================================================

if __name__ == "__main__":
    main()