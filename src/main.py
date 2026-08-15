# ============================================================
# PROGRAMA PRINCIPAL
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Este archivo coordina el flujo principal del proyecto:
# 1. Carga y limpia el CSV de accidentes.
# 2. Guarda y comprueba el CSV procesado.
# 3. Consulta o carga los datos climaticos.
# 4. Crea el resumen climatico mensual.
# 5. Guarda el resumen climatico.
# 6. Se conecta con SQL Server.
# 7. Carga los accidentes.
# 8. Carga los datos climaticos.
# 9. Comprueba ambas tablas.
# 10. Cierra la conexion.
# ============================================================

import os
import pandas as pd

from datos.GestorDatos import GestorDatos
from api.ClienteAPI import ClienteAPI
from basedatos.GestorBaseDatos import GestorBaseDatos


# ============================================================
# FUNCION PRINCIPAL
#
# Ejecuta en orden el procesamiento de accidentes,
# la integracion climatica y la carga en SQL Server.
# ============================================================

def main():
    """
    Ejecuta el flujo principal de datos del proyecto.
    """

    # ========================================================
    # SECCION 1: PROCESAMIENTO DE ACCIDENTES
    # ========================================================

    print("\n====================================================")
    print("PROCESAMIENTO DE LOS DATOS DE ACCIDENTES")
    print("====================================================")

    # --------------------------------------------------------
    # PASO 1: CREAR EL GESTOR DE DATOS
    # --------------------------------------------------------

    gestor_datos = GestorDatos()

    # --------------------------------------------------------
    # PASO 2: CARGAR EL CSV ORIGINAL
    # --------------------------------------------------------

    datos_originales = gestor_datos.cargar_csv(
        "accidentes_victimas_2018_2024.csv"
    )

    print("\nArchivo original cargado correctamente.")

    print(
        f"Cantidad de filas originales: "
        f"{datos_originales.shape[0]}"
    )

    print(
        f"Cantidad de columnas originales: "
        f"{datos_originales.shape[1]}"
    )

    # --------------------------------------------------------
    # PASO 3: LIMPIAR LOS DATOS
    # --------------------------------------------------------

    datos_accidentes = gestor_datos.limpiar_datos(
        datos_originales
    )

    print("\nDimensiones despues de la limpieza:")

    print(
        f"Cantidad de filas limpias: "
        f"{datos_accidentes.shape[0]}"
    )

    print(
        f"Cantidad de columnas limpias: "
        f"{datos_accidentes.shape[1]}"
    )

    # --------------------------------------------------------
    # PASO 4: COMPROBAR LA VARIABLE GRAVEDAD
    # --------------------------------------------------------

    valores_gravedad = sorted(
        datos_accidentes["gravedad"]
        .astype(int)
        .unique()
        .tolist()
    )

    print("\nValores de gravedad encontrados:")
    print(valores_gravedad)

    print("\nDistribucion de la gravedad:")

    print(
        datos_accidentes["gravedad"]
        .value_counts()
        .sort_index()
    )

    # --------------------------------------------------------
    # PASO 5: GUARDAR EL CSV DE ACCIDENTES PROCESADO
    # --------------------------------------------------------

    gestor_datos.guardar_csv(
        datos_accidentes,
        "accidentes_victimas_limpio.csv"
    )

    # --------------------------------------------------------
    # PASO 6: VOLVER A CARGAR EL ARCHIVO PROCESADO
    # --------------------------------------------------------

    accidentes_comprobacion = (
        gestor_datos.cargar_csv_procesado(
            "accidentes_victimas_limpio.csv"
        )
    )

    print("\nComprobacion del archivo de accidentes:")

    print(
        f"Filas recuperadas: "
        f"{accidentes_comprobacion.shape[0]}"
    )

    print(
        f"Columnas recuperadas: "
        f"{accidentes_comprobacion.shape[1]}"
    )

    # --------------------------------------------------------
    # PASO 7: COMPROBAR DIA Y MES
    # --------------------------------------------------------

    columnas_temporales = [
        "dia_numero",
        "dia",
        "mes_numero",
        "mes"
    ]

    vacios_temporales = (
        accidentes_comprobacion[columnas_temporales]
        .isna()
        .sum()
    )

    print("\nValores vacios en las columnas de dia y mes:")

    print(vacios_temporales)

    # ========================================================
    # SECCION 2: PROCESAMIENTO DE DATOS CLIMATICOS
    # ========================================================

    print("\n====================================================")
    print("PROCESAMIENTO DE LOS DATOS CLIMATICOS")
    print("====================================================")

    # --------------------------------------------------------
    # PASO 8: CREAR EL CLIENTE DE LA API
    # --------------------------------------------------------

    cliente_api = ClienteAPI()

    # --------------------------------------------------------
    # PASO 9: CONSTRUIR LA RUTA DEL CSV CLIMATICO
    # --------------------------------------------------------

    carpeta_src = os.path.dirname(
        os.path.abspath(__file__)
    )

    carpeta_proyecto = os.path.dirname(
        carpeta_src
    )

    ruta_clima = os.path.join(
        carpeta_proyecto,
        "data",
        "processed",
        "clima_mensual_2018_2024.csv"
    )

    # --------------------------------------------------------
    # PASO 10: CARGAR O GENERAR EL RESUMEN CLIMATICO
    #
    # Si el archivo ya existe, se carga directamente.
    # Si no existe, se consulta Open-Meteo y se genera.
    # --------------------------------------------------------

    if os.path.exists(ruta_clima):

        print(
            "\nEl archivo climatico ya existe."
        )

        print(
            "Se cargara el archivo sin consultar "
            "nuevamente la API."
        )

        resumen_clima = pd.read_csv(
            ruta_clima,
            sep=";",
            encoding="utf-8-sig"
        )

    else:

        print(
            "\nEl archivo climatico no existe."
        )

        print(
            "Se consultara la API historica de Open-Meteo."
        )

        # Consultar los datos diarios de las siete provincias
        datos_clima_diarios = (
            cliente_api.consultar_todas_provincias(
                fecha_inicio="2018-01-01",
                fecha_fin="2024-12-31"
            )
        )

        # Crear el resumen mensual
        resumen_clima = (
            cliente_api.resumir_clima_mensual(
                datos_clima_diarios
            )
        )

        # Guardar el resumen mensual
        cliente_api.guardar_resumen_climatico(
            resumen_mensual=resumen_clima,
            nombre_archivo="clima_mensual_2018_2024.csv"
        )

    # --------------------------------------------------------
    # PASO 11: COMPROBAR EL RESUMEN CLIMATICO
    # --------------------------------------------------------

    print("\nComprobacion del resumen climatico:")

    print(
        f"Filas climaticas: "
        f"{resumen_clima.shape[0]}"
    )

    print(
        f"Columnas climaticas: "
        f"{resumen_clima.shape[1]}"
    )

    valores_vacios_clima = resumen_clima.isna().sum()

    print("\nValores vacios en los datos climaticos:")

    print(valores_vacios_clima)

    # Comprobar las provincias
    provincias_clima = sorted(
        resumen_clima["provincia"]
        .unique()
        .tolist()
    )

    print("\nProvincias climaticas encontradas:")

    for provincia in provincias_clima:
        print(f"- {provincia}")

    # Comprobar los años
    anios_clima = sorted(
        resumen_clima["anio"]
        .unique()
        .tolist()
    )

    print("\nAños climaticos encontrados:")
    print(anios_clima)

    # --------------------------------------------------------
    # PASO 12: VALIDAR LAS DIMENSIONES CLIMATICAS
    # --------------------------------------------------------

    if resumen_clima.shape[0] != 588:
        raise ValueError(
            "El resumen climatico no contiene "
            "los 588 registros esperados."
        )

    if resumen_clima.shape[1] != 8:
        raise ValueError(
            "El resumen climatico no contiene "
            "las 8 columnas esperadas."
        )

    if valores_vacios_clima.sum() > 0:
        raise ValueError(
            "El resumen climatico contiene valores vacios."
        )

    print(
        "\nEl resumen climatico tiene las dimensiones "
        "correctas."
    )

    # ========================================================
    # SECCION 3: INTEGRACION CON SQL SERVER
    # ========================================================

    print("\n====================================================")
    print("INTEGRACION CON SQL SERVER")
    print("====================================================")

    # --------------------------------------------------------
    # PASO 13: CREAR EL GESTOR DE BASE DE DATOS
    # --------------------------------------------------------

    gestor_bd = GestorBaseDatos()

    try:

        # ----------------------------------------------------
        # PASO 14: PROBAR LA CONEXION
        # ----------------------------------------------------

        nombre_base = gestor_bd.probar_conexion()

        print("\nComprobacion de SQL Server:")

        print(
            f"Base de datos conectada: "
            f"{nombre_base}"
        )

        # ====================================================
        # CARGA DE LA TABLA ACCIDENTES
        # ====================================================

        # ----------------------------------------------------
        # PASO 15: INSERTAR LOS ACCIDENTES
        # ----------------------------------------------------

        accidentes_insertados = (
            gestor_bd.insertar_accidentes(
                accidentes_comprobacion
            )
        )

        if accidentes_insertados > 0:
            print(
                f"Accidentes insertados: "
                f"{accidentes_insertados}"
            )

        # ----------------------------------------------------
        # PASO 16: COMPROBAR LA TABLA ACCIDENTES
        # ----------------------------------------------------

        total_accidentes_sql = (
            gestor_bd.contar_registros()
        )

        print("\nComprobacion de la tabla accidentes:")

        print(
            f"Registros almacenados: "
            f"{total_accidentes_sql}"
        )

        if total_accidentes_sql == len(
                accidentes_comprobacion
        ):
            print(
                "El CSV y la tabla accidentes "
                "coinciden correctamente."
            )
        else:
            print(
                "Advertencia: el CSV y la tabla accidentes "
                "no tienen la misma cantidad."
            )

        # ====================================================
        # CARGA DE LA TABLA CLIMA MENSUAL
        # ====================================================

        # ----------------------------------------------------
        # PASO 17: INSERTAR EL RESUMEN CLIMATICO
        # ----------------------------------------------------

        clima_insertado = (
            gestor_bd.insertar_clima_mensual(
                resumen_clima
            )
        )

        if clima_insertado > 0:
            print(
                f"Registros climaticos insertados: "
                f"{clima_insertado}"
            )

        # ----------------------------------------------------
        # PASO 18: COMPROBAR LA TABLA CLIMA MENSUAL
        # ----------------------------------------------------

        total_clima_sql = (
            gestor_bd.contar_registros_clima()
        )

        print("\nComprobacion de la tabla clima_mensual:")

        print(
            f"Registros almacenados: "
            f"{total_clima_sql}"
        )

        if total_clima_sql == len(resumen_clima):
            print(
                "El CSV climatico y la tabla clima_mensual "
                "coinciden correctamente."
            )
        else:
            print(
                "Advertencia: el CSV climatico y SQL Server "
                "no tienen la misma cantidad."
            )

        # ====================================================
        # COMPROBACION FINAL
        # ====================================================

        # ----------------------------------------------------
        # PASO 19: MOSTRAR EL RESUMEN FINAL
        # ----------------------------------------------------

        print("\n====================================================")
        print("RESUMEN FINAL DEL PROCESO")
        print("====================================================")

        print(
            f"Accidentes procesados: "
            f"{len(accidentes_comprobacion)}"
        )

        print(
            f"Accidentes en SQL Server: "
            f"{total_accidentes_sql}"
        )

        print(
            f"Registros climaticos procesados: "
            f"{len(resumen_clima)}"
        )

        print(
            f"Registros climaticos en SQL Server: "
            f"{total_clima_sql}"
        )

        if (
            total_accidentes_sql
            == len(accidentes_comprobacion)
            and total_clima_sql
            == len(resumen_clima)
        ):
            print(
                "\nEl procesamiento de datos y la integracion "
                "con SQL Server finalizaron correctamente."
            )
        else:
            print(
                "\nAdvertencia: se encontraron diferencias "
                "en las cantidades almacenadas."
            )

    except Exception as error:

        # Mostrar cualquier error ocurrido
        print(
            "\nOcurrio un error durante la integracion "
            "con SQL Server:"
        )

        print(error)

    finally:

        # ----------------------------------------------------
        # PASO 20: CERRAR LA CONEXION
        # ----------------------------------------------------

        gestor_bd.cerrar_conexion()


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
#
# Ejecuta main() solamente cuando este archivo
# se inicia directamente.
# ============================================================

if __name__ == "__main__":
    main()