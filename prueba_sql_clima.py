# ============================================================
# PRUEBA TEMPORAL DE CARGA CLIMATICA EN SQL SERVER
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Este archivo comprueba:
# 1. La existencia del CSV climatico procesado.
# 2. La lectura de los 588 registros mensuales.
# 3. La conexion con SQL Server.
# 4. La insercion en dbo.clima_mensual.
# 5. La cantidad final de registros almacenados.
# 6. La proteccion contra cargas duplicadas.
#
# IMPORTANTE:
# Este archivo no consulta nuevamente la API.
# ============================================================

import os
import pandas as pd

from src.basedatos.GestorBaseDatos import GestorBaseDatos


# ============================================================
# FUNCION PRINCIPAL
#
# Carga el CSV climatico procesado e inserta sus registros
# en la tabla dbo.clima_mensual de SQL Server.
# ============================================================

def main():
    """
    Prueba la carga del resumen climatico mensual
    en SQL Server.
    """

    # --------------------------------------------------------
    # PASO 1: OBTENER LA RUTA PRINCIPAL DEL PROYECTO
    # --------------------------------------------------------

    carpeta_proyecto = os.path.dirname(
        os.path.abspath(__file__)
    )

    # --------------------------------------------------------
    # PASO 2: CONSTRUIR LA RUTA DEL CSV CLIMATICO
    # --------------------------------------------------------

    ruta_clima = os.path.join(
        carpeta_proyecto,
        "data",
        "processed",
        "clima_mensual_2018_2024.csv"
    )

    # --------------------------------------------------------
    # PASO 3: COMPROBAR QUE EL ARCHIVO EXISTA
    # --------------------------------------------------------

    if not os.path.exists(ruta_clima):
        raise FileNotFoundError(
            f"No se encontro el archivo climatico: "
            f"{ruta_clima}"
        )

    print("Archivo climatico encontrado correctamente.")
    print(ruta_clima)

    # --------------------------------------------------------
    # PASO 4: CARGAR EL CSV CLIMATICO
    # --------------------------------------------------------

    datos_clima = pd.read_csv(
        ruta_clima,
        sep=";",
        encoding="utf-8-sig"
    )

    print("\nArchivo climatico cargado correctamente.")

    print(
        f"Cantidad de filas: "
        f"{datos_clima.shape[0]}"
    )

    print(
        f"Cantidad de columnas: "
        f"{datos_clima.shape[1]}"
    )

    # --------------------------------------------------------
    # PASO 5: MOSTRAR LAS COLUMNAS RECUPERADAS
    # --------------------------------------------------------

    print("\nColumnas del archivo climatico:")

    for columna in datos_clima.columns:
        print(f"- {columna}")

    # --------------------------------------------------------
    # PASO 6: COMPROBAR LAS DIMENSIONES ESPERADAS
    # --------------------------------------------------------

    filas_esperadas = 588
    columnas_esperadas = 8

    if datos_clima.shape[0] != filas_esperadas:
        raise ValueError(
            "La cantidad de filas climaticas no es la esperada. "
            f"Esperadas: {filas_esperadas}. "
            f"Encontradas: {datos_clima.shape[0]}."
        )

    if datos_clima.shape[1] != columnas_esperadas:
        raise ValueError(
            "La cantidad de columnas climaticas no es la esperada. "
            f"Esperadas: {columnas_esperadas}. "
            f"Encontradas: {datos_clima.shape[1]}."
        )

    print(
        "\nLas dimensiones del archivo climatico "
        "son correctas."
    )

    # --------------------------------------------------------
    # PASO 7: COMPROBAR VALORES VACIOS
    # --------------------------------------------------------

    valores_vacios = datos_clima.isna().sum()

    print("\nValores vacios por columna:")

    print(valores_vacios)

    if valores_vacios.sum() > 0:
        raise ValueError(
            "El archivo climatico contiene valores vacios."
        )

    print(
        "\nEl archivo climatico no contiene valores vacios."
    )

    # --------------------------------------------------------
    # PASO 8: CREAR EL GESTOR DE BASE DE DATOS
    # --------------------------------------------------------

    gestor_bd = GestorBaseDatos()

    try:

        # ----------------------------------------------------
        # PASO 9: PROBAR LA CONEXION
        # ----------------------------------------------------

        nombre_base = gestor_bd.probar_conexion()

        print("\nComprobacion de SQL Server:")

        print(
            f"Base de datos conectada: "
            f"{nombre_base}"
        )

        # ----------------------------------------------------
        # PASO 10: CONTAR LOS REGISTROS ANTES DE LA CARGA
        # ----------------------------------------------------

        registros_antes = gestor_bd.contar_registros_clima()

        print("\nEstado inicial de la tabla clima_mensual:")

        print(
            f"Registros antes de la carga: "
            f"{registros_antes}"
        )

        # ----------------------------------------------------
        # PASO 11: INSERTAR EL RESUMEN CLIMATICO
        # ----------------------------------------------------

        cantidad_insertada = (
            gestor_bd.insertar_clima_mensual(
                datos_clima
            )
        )

        if cantidad_insertada > 0:
            print(
                f"Registros climaticos insertados: "
                f"{cantidad_insertada}"
            )

        # ----------------------------------------------------
        # PASO 12: CONTAR LOS REGISTROS DESPUES DE LA CARGA
        # ----------------------------------------------------

        registros_despues = (
            gestor_bd.contar_registros_clima()
        )

        print("\nComprobacion de la tabla clima_mensual:")

        print(
            f"Registros despues de la carga: "
            f"{registros_despues}"
        )

        # ----------------------------------------------------
        # PASO 13: COMPARAR EL CSV CON SQL SERVER
        # ----------------------------------------------------

        if registros_despues == len(datos_clima):
            print(
                "La cantidad de registros climaticos del CSV "
                "y SQL Server coincide correctamente."
            )
        else:
            print(
                "Advertencia: la cantidad de registros "
                "climaticos no coincide."
            )

    except Exception as error:

        # Mostrar cualquier error de SQL Server
        print(
            "\nOcurrio un error al trabajar con "
            "la tabla climatica:"
        )

        print(error)

    finally:

        # ----------------------------------------------------
        # PASO 14: CERRAR LA CONEXION
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