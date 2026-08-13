# ============================================================
# PROGRAMA PRINCIPAL
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Este archivo coordina el proceso principal del proyecto:
# 1. Carga el CSV original.
# 2. Limpia y transforma los datos.
# 3. Separa el numero y nombre del dia y del mes.
# 4. Guarda el CSV procesado.
# 5. Comprueba el archivo procesado.
# 6. Se conecta con SQL Server.
# 7. Inserta los accidentes en la base de datos.
# 8. Comprueba la cantidad de registros almacenados.
# ============================================================

from datos.GestorDatos import GestorDatos
from basedatos.GestorBaseDatos import GestorBaseDatos


# ============================================================
# FUNCION PRINCIPAL
#
# Ejecuta en orden la carga, limpieza, almacenamiento
# y comprobacion de los datos de accidentes.
# ============================================================

def main():
    """
    Ejecuta el proceso principal de gestion de datos
    e integracion con SQL Server.
    """

    # --------------------------------------------------------
    # PASO 1: CREAR EL GESTOR DE DATOS
    # --------------------------------------------------------

    gestor_datos = GestorDatos()

    # --------------------------------------------------------
    # PASO 2: CARGAR EL ARCHIVO CSV ORIGINAL
    # --------------------------------------------------------

    datos = gestor_datos.cargar_csv(
        "accidentes_victimas_2018_2024.csv"
    )

    print("Archivo original cargado correctamente.")
    print(f"Cantidad de filas originales: {datos.shape[0]}")
    print(f"Cantidad de columnas originales: {datos.shape[1]}")

    # --------------------------------------------------------
    # PASO 3: REALIZAR LA LIMPIEZA INICIAL
    # --------------------------------------------------------

    datos_limpios = gestor_datos.limpiar_datos(datos)

    print("\nDimensiones despues de la limpieza:")
    print(f"Cantidad de filas limpias: {datos_limpios.shape[0]}")
    print(
        f"Cantidad de columnas limpias: "
        f"{datos_limpios.shape[1]}"
    )

    # --------------------------------------------------------
    # PASO 4: MOSTRAR LOS NOMBRES DE LAS COLUMNAS
    # --------------------------------------------------------

    print("\nColumnas del archivo procesado:")

    for columna in datos_limpios.columns:
        print(f"- {columna}")

    # --------------------------------------------------------
    # PASO 5: COMPROBAR LA VARIABLE GRAVEDAD
    # --------------------------------------------------------

    print("\nDistribucion de la variable gravedad:")

    print(
        datos_limpios["gravedad"].value_counts(
            dropna=False
        )
    )

    valores_gravedad = sorted(
        datos_limpios["gravedad"]
        .astype(int)
        .unique()
        .tolist()
    )

    print(f"Valores de gravedad encontrados: {valores_gravedad}")

    # --------------------------------------------------------
    # PASO 6: COMPROBAR LOS VALORES DEL DIA
    # --------------------------------------------------------

    relacion_dias = (
        datos_limpios[
            ["dia_numero", "dia"]
        ]
        .drop_duplicates()
        .sort_values("dia_numero")
    )

    print("\nRelacion entre numero y nombre del dia:")
    print(relacion_dias.to_string(index=False))

    # --------------------------------------------------------
    # PASO 7: COMPROBAR LOS VALORES DEL MES
    # --------------------------------------------------------

    relacion_meses = (
        datos_limpios[
            ["mes_numero", "mes"]
        ]
        .drop_duplicates()
        .sort_values("mes_numero")
    )

    print("\nRelacion entre numero y nombre del mes:")
    print(relacion_meses.to_string(index=False))

    # --------------------------------------------------------
    # PASO 8: GUARDAR EL ARCHIVO PROCESADO
    # --------------------------------------------------------

    gestor_datos.guardar_csv(
        datos_limpios,
        "accidentes_victimas_limpio.csv"
    )

    # --------------------------------------------------------
    # PASO 9: VOLVER A CARGAR EL ARCHIVO PROCESADO
    # --------------------------------------------------------

    datos_comprobacion = gestor_datos.cargar_csv_procesado(
        "accidentes_victimas_limpio.csv"
    )

    # --------------------------------------------------------
    # PASO 10: COMPROBAR EL ARCHIVO PROCESADO
    # --------------------------------------------------------

    print("\nComprobacion del archivo procesado:")

    print(
        f"Filas recuperadas: "
        f"{datos_comprobacion.shape[0]}"
    )

    print(
        f"Columnas recuperadas: "
        f"{datos_comprobacion.shape[1]}"
    )

    columnas_temporales = [
        "dia_numero",
        "dia",
        "mes_numero",
        "mes"
    ]

    valores_vacios = (
        datos_comprobacion[columnas_temporales]
        .isna()
        .sum()
    )

    print("\nValores vacios en las columnas de dia y mes:")
    print(valores_vacios)

    # --------------------------------------------------------
    # PASO 11: CREAR EL GESTOR DE BASE DE DATOS
    # --------------------------------------------------------

    gestor_bd = GestorBaseDatos()

    try:

        # ----------------------------------------------------
        # PASO 12: PROBAR LA CONEXION CON SQL SERVER
        # ----------------------------------------------------

        nombre_base = gestor_bd.probar_conexion()

        print("\nComprobacion de SQL Server:")
        print(f"Base de datos conectada: {nombre_base}")

        # ----------------------------------------------------
        # PASO 13: INSERTAR LOS DATOS EN SQL SERVER
        # ----------------------------------------------------

        cantidad_insertada = gestor_bd.insertar_accidentes(
            datos_comprobacion
        )

        if cantidad_insertada > 0:
            print(
                f"Registros insertados: "
                f"{cantidad_insertada}"
            )

        # ----------------------------------------------------
        # PASO 14: COMPROBAR LOS REGISTROS ALMACENADOS
        # ----------------------------------------------------

        total_sql = gestor_bd.contar_registros()

        print("\nComprobacion de la tabla accidentes:")

        print(
            f"Registros almacenados en SQL Server: "
            f"{total_sql}"
        )

        # Comparar las filas del CSV con las filas de SQL Server
        if total_sql == len(datos_comprobacion):
            print(
                "La cantidad de registros del CSV y SQL Server "
                "coincide correctamente."
            )
        else:
            print(
                "Advertencia: la cantidad de registros del CSV "
                "y SQL Server no coincide."
            )

    except Exception as error:

        # Mostrar el error en caso de que ocurra un problema
        print("\nOcurrio un error al trabajar con SQL Server:")
        print(error)

    finally:

        # ----------------------------------------------------
        # PASO 15: CERRAR LA CONEXION
        # ----------------------------------------------------

        gestor_bd.cerrar_conexion()


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
#
# Ejecuta main() solamente cuando este archivo se inicia
# directamente.
# ============================================================

if __name__ == "__main__":
    main()
