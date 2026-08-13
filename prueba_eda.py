# ============================================================
# PRUEBA DEL ANALISIS EXPLORATORIO DE DATOS
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Este archivo comprueba:
# 1. La carga del CSV procesado de accidentes.
# 2. La carga del CSV climatico mensual.
# 3. El resumen general del conjunto de datos.
# 4. Los valores vacios y duplicados.
# 5. Los accidentes por tiempo y ubicacion.
# 6. La distribucion de la gravedad.
# 7. La gravedad segun diferentes condiciones.
# 8. La tabla cruzada entre dia y franja horaria.
# 9. La relacion mensual entre accidentes y clima.
# 10. La consistencia de todos los resultados.
#
# IMPORTANTE:
# Este archivo no modifica los datos ni SQL Server.
# ============================================================

import os
import pandas as pd

from src.eda.ProcesadorEDA import ProcesadorEDA


# ============================================================
# FUNCION AUXILIAR: MOSTRAR TITULO
#
# Muestra un titulo visual para separar los resultados
# presentados en la consola.
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
# Carga los datos procesados y prueba todos los metodos
# de la clase ProcesadorEDA.
# ============================================================

def main():
    """
    Ejecuta las pruebas completas del EDA.
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
    # SECCION 2: CREAR EL PROCESADOR EDA
    # ========================================================

    procesador_eda = ProcesadorEDA(
        datos_accidentes
    )

    # ========================================================
    # SECCION 3: COMPROBACION GENERAL
    # ========================================================

    # --------------------------------------------------------
    # PASO 6: RESUMEN GENERAL
    # --------------------------------------------------------

    resumen = procesador_eda.resumen_general()

    mostrar_titulo("RESUMEN GENERAL")

    for nombre, valor in resumen.items():
        print(f"{nombre}: {valor}")

    # --------------------------------------------------------
    # PASO 7: TIPOS DE DATOS
    # --------------------------------------------------------

    tipos_datos = procesador_eda.obtener_tipos_datos()

    mostrar_titulo("TIPOS DE DATOS")

    print(
        tipos_datos.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 8: VALORES VACIOS
    # --------------------------------------------------------

    valores_vacios = procesador_eda.analizar_valores_vacios()

    mostrar_titulo("VALORES VACIOS")

    print(
        valores_vacios.to_string(
            index=False
        )
    )

    # ========================================================
    # SECCION 4: ANALISIS TEMPORAL Y GEOGRAFICO
    # ========================================================

    # --------------------------------------------------------
    # PASO 9: ACCIDENTES POR AÑO
    # --------------------------------------------------------

    por_anio = procesador_eda.accidentes_por_anio()

    mostrar_titulo("ACCIDENTES POR AÑO")

    print(
        por_anio.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 10: ACCIDENTES POR PROVINCIA
    # --------------------------------------------------------

    por_provincia = procesador_eda.accidentes_por_provincia()

    mostrar_titulo("ACCIDENTES POR PROVINCIA")

    print(
        por_provincia.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 11: ACCIDENTES POR MES
    # --------------------------------------------------------

    por_mes = procesador_eda.accidentes_por_mes()

    mostrar_titulo("ACCIDENTES POR MES")

    print(
        por_mes.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 12: ACCIDENTES POR DIA
    # --------------------------------------------------------

    por_dia = procesador_eda.accidentes_por_dia()

    mostrar_titulo("ACCIDENTES POR DIA")

    print(
        por_dia.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 13: ACCIDENTES POR FRANJA HORARIA
    # --------------------------------------------------------

    por_hora = procesador_eda.accidentes_por_hora()

    mostrar_titulo("ACCIDENTES POR FRANJA HORARIA")

    print(
        por_hora.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 14: TABLA CRUZADA DIA Y HORA
    # --------------------------------------------------------

    tabla_dia_hora = procesador_eda.tabla_dia_hora()

    mostrar_titulo("TABLA CRUZADA ENTRE DIA Y HORA")

    print(
        tabla_dia_hora.to_string(
            index=False
        )
    )

    # ========================================================
    # SECCION 5: DISTRIBUCION Y GRAVEDAD
    # ========================================================

    # --------------------------------------------------------
    # PASO 15: DISTRIBUCION DE LA GRAVEDAD
    # --------------------------------------------------------

    distribucion_gravedad = (
        procesador_eda.distribucion_gravedad()
    )

    mostrar_titulo("DISTRIBUCION DE LA GRAVEDAD")

    print(
        distribucion_gravedad.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 16: GRAVEDAD POR PROVINCIA
    # --------------------------------------------------------

    gravedad_provincia = (
        procesador_eda.gravedad_por_provincia()
    )

    mostrar_titulo("GRAVEDAD POR PROVINCIA")

    print(
        gravedad_provincia.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 17: GRAVEDAD POR TIPO DE ACCIDENTE
    # --------------------------------------------------------

    gravedad_tipo = (
        procesador_eda.gravedad_por_tipo_accidente()
    )

    mostrar_titulo("GRAVEDAD POR TIPO DE ACCIDENTE")

    print(
        gravedad_tipo.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 18: GRAVEDAD POR ZONA
    # --------------------------------------------------------

    gravedad_zona = (
        procesador_eda.gravedad_por_zona()
    )

    mostrar_titulo("GRAVEDAD POR ZONA")

    print(
        gravedad_zona.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 19: GRAVEDAD POR TIPO DE RUTA
    # --------------------------------------------------------

    gravedad_ruta = (
        procesador_eda.gravedad_por_tipo_ruta()
    )

    mostrar_titulo("GRAVEDAD POR TIPO DE RUTA")

    print(
        gravedad_ruta.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 20: GRAVEDAD POR ESTADO DEL TIEMPO
    # --------------------------------------------------------

    gravedad_tiempo = (
        procesador_eda.gravedad_por_estado_tiempo()
    )

    mostrar_titulo("GRAVEDAD POR ESTADO DEL TIEMPO")

    print(
        gravedad_tiempo.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 21: GRAVEDAD POR ESTADO DE LA CALZADA
    # --------------------------------------------------------

    gravedad_calzada = (
        procesador_eda.gravedad_por_estado_calzada()
    )

    mostrar_titulo("GRAVEDAD POR ESTADO DE LA CALZADA")

    print(
        gravedad_calzada.to_string(
            index=False
        )
    )

    # ========================================================
    # SECCION 6: FRECUENCIAS POR CATEGORIA
    # ========================================================

    # --------------------------------------------------------
    # PASO 22: ACCIDENTES POR TIPO
    # --------------------------------------------------------

    por_tipo = procesador_eda.accidentes_por_tipo()

    mostrar_titulo("ACCIDENTES POR TIPO")

    print(
        por_tipo.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 23: ACCIDENTES POR ESTADO DEL TIEMPO
    # --------------------------------------------------------

    por_clima = procesador_eda.accidentes_por_clima()

    mostrar_titulo("ACCIDENTES POR ESTADO DEL TIEMPO")

    print(
        por_clima.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 24: ACCIDENTES POR ZONA
    # --------------------------------------------------------

    por_zona = procesador_eda.accidentes_por_zona()

    mostrar_titulo("ACCIDENTES POR ZONA")

    print(
        por_zona.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 25: ACCIDENTES POR TIPO DE RUTA
    # --------------------------------------------------------

    por_tipo_ruta = (
        procesador_eda.accidentes_por_tipo_ruta()
    )

    mostrar_titulo("ACCIDENTES POR TIPO DE RUTA")

    print(
        por_tipo_ruta.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 26: ACCIDENTES POR ESTADO DE LA CALZADA
    # --------------------------------------------------------

    por_estado_calzada = (
        procesador_eda.accidentes_por_estado_calzada()
    )

    mostrar_titulo("ACCIDENTES POR ESTADO DE LA CALZADA")

    print(
        por_estado_calzada.to_string(
            index=False
        )
    )

    # ========================================================
    # SECCION 7: RELACION ENTRE ACCIDENTES Y CLIMA
    # ========================================================

    # --------------------------------------------------------
    # PASO 27: RELACIONAR AMBOS CONJUNTOS DE DATOS
    # --------------------------------------------------------

    relacion_clima = (
        procesador_eda.relacion_accidentes_clima(
            datos_clima
        )
    )

    mostrar_titulo("RELACION MENSUAL ENTRE ACCIDENTES Y CLIMA")

    print(
        relacion_clima
        .head(20)
        .to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 28: COMPROBAR LAS DIMENSIONES DE LA RELACION
    # --------------------------------------------------------

    print("\nDimensiones de la relacion mensual:")

    print(
        f"Filas: "
        f"{relacion_clima.shape[0]}"
    )

    print(
        f"Columnas: "
        f"{relacion_clima.shape[1]}"
    )

    # --------------------------------------------------------
    # PASO 29: COMPROBAR LOS VALORES VACIOS
    # --------------------------------------------------------

    vacios_relacion = relacion_clima.isna().sum()

    print("\nValores vacios en la relacion mensual:")

    print(vacios_relacion)

    # --------------------------------------------------------
    # PASO 30: RESUMEN ANUAL DE LA RELACION
    # --------------------------------------------------------

    resumen_anual_clima = (
        relacion_clima
        .groupby("anio")
        .agg(
            precipitacion_total_mm=(
                "precipitacion_total_mm",
                "sum"
            ),
            cantidad_accidentes=(
                "cantidad_accidentes",
                "sum"
            ),
            accidentes_graves=(
                "accidentes_graves",
                "sum"
            )
        )
        .reset_index()
        .sort_values("anio")
    )

    columnas_redondear = [
        "precipitacion_total_mm"
    ]

    resumen_anual_clima[columnas_redondear] = (
        resumen_anual_clima[columnas_redondear]
        .round(2)
    )

    mostrar_titulo(
        "RESUMEN ANUAL DE ACCIDENTES Y PRECIPITACION"
    )

    print(
        resumen_anual_clima.to_string(
            index=False
        )
    )

    # ========================================================
    # SECCION 8: COMPROBACION DE TOTALES
    # ========================================================

    total_esperado = len(datos_accidentes)

    comprobaciones = {
        "accidentes_por_anio": (
            por_anio["cantidad_accidentes"].sum()
        ),
        "accidentes_por_provincia": (
            por_provincia["cantidad_accidentes"].sum()
        ),
        "accidentes_por_mes": (
            por_mes["cantidad_accidentes"].sum()
        ),
        "accidentes_por_dia": (
            por_dia["cantidad_accidentes"].sum()
        ),
        "accidentes_por_hora": (
            por_hora["cantidad_accidentes"].sum()
        ),
        "tabla_dia_hora": (
            tabla_dia_hora
            .drop(
                columns=[
                    "dia_numero",
                    "dia"
                ]
            )
            .sum()
            .sum()
        ),
        "distribucion_gravedad": (
            distribucion_gravedad[
                "cantidad_accidentes"
            ].sum()
        ),
        "gravedad_por_provincia": (
            gravedad_provincia[
                "total_accidentes"
            ].sum()
        ),
        "gravedad_por_tipo": (
            gravedad_tipo[
                "total_accidentes"
            ].sum()
        ),
        "gravedad_por_zona": (
            gravedad_zona[
                "total_accidentes"
            ].sum()
        ),
        "gravedad_por_tipo_ruta": (
            gravedad_ruta[
                "total_accidentes"
            ].sum()
        ),
        "gravedad_por_tiempo": (
            gravedad_tiempo[
                "total_accidentes"
            ].sum()
        ),
        "gravedad_por_calzada": (
            gravedad_calzada[
                "total_accidentes"
            ].sum()
        ),
        "accidentes_por_tipo": (
            por_tipo["cantidad_accidentes"].sum()
        ),
        "accidentes_por_clima": (
            por_clima["cantidad_accidentes"].sum()
        ),
        "accidentes_por_zona": (
            por_zona["cantidad_accidentes"].sum()
        ),
        "accidentes_por_tipo_ruta": (
            por_tipo_ruta[
                "cantidad_accidentes"
            ].sum()
        ),
        "accidentes_por_estado_calzada": (
            por_estado_calzada[
                "cantidad_accidentes"
            ].sum()
        ),
        "relacion_accidentes_clima": (
            relacion_clima[
                "cantidad_accidentes"
            ].sum()
        )
    }

    mostrar_titulo("COMPROBACION DE TOTALES")

    todas_coinciden = True

    for nombre, total_obtenido in comprobaciones.items():

        total_obtenido = int(total_obtenido)

        coincide = total_obtenido == total_esperado

        print(
            f"{nombre}: "
            f"{total_obtenido} "
            f"| coincide: {coincide}"
        )

        if not coincide:
            todas_coinciden = False

    # ========================================================
    # SECCION 9: COMPROBACION FINAL
    # ========================================================

    mostrar_titulo("COMPROBACION FINAL DEL EDA")

    relacion_correcta = (
        relacion_clima.shape[0] == 588
        and vacios_relacion.sum() == 0
        and relacion_clima[
            "cantidad_accidentes"
        ].sum() == total_esperado
    )

    if (
        resumen["cantidad_filas"] == 104821
        and resumen["cantidad_columnas"] == 24
        and resumen["cantidad_duplicados"] == 0
        and resumen["total_valores_vacios"] == 0
        and resumen["anio_inicial"] == 2018
        and resumen["anio_final"] == 2024
        and resumen["cantidad_provincias"] == 7
        and datos_clima.shape[0] == 588
        and datos_clima.shape[1] == 8
        and todas_coinciden
        and relacion_correcta
    ):
        print(
            "El analisis exploratorio ampliado fue "
            "procesado correctamente."
        )
    else:
        print(
            "Advertencia: revise los resultados "
            "del EDA ampliado."
        )


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
#
# Ejecuta main() solamente cuando este archivo
# se inicia directamente.
# ============================================================

if __name__ == "__main__":
    main()
