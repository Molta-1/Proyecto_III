# ============================================================
# PRUEBA DE GUARDADO DEL RESUMEN CLIMATICO
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Este archivo comprueba:
# 1. La consulta climatica de 2018 a 2024.
# 2. La creacion del resumen mensual.
# 3. El guardado del resumen en formato CSV.
# 4. La lectura del archivo guardado.
# 5. La cantidad de filas y columnas recuperadas.
# 6. La ausencia de valores vacios.
#
# IMPORTANTE:
# Este archivo todavia no modifica SQL Server.
# ============================================================

import os
import pandas as pd

from src.api.ClienteAPI import ClienteAPI


# ============================================================
# FUNCION PRINCIPAL
#
# Consulta, resume, guarda y comprueba los datos climaticos
# mensuales del periodo comprendido entre 2018 y 2024.
# ============================================================

def main():
    """
    Genera y comprueba el archivo climático mensual
    de las siete provincias entre 2018 y 2024.
    """

    # --------------------------------------------------------
    # PASO 1: CREAR EL CLIENTE DE LA API
    # --------------------------------------------------------

    cliente_api = ClienteAPI()

    # --------------------------------------------------------
    # PASO 2: CONSULTAR LOS DATOS CLIMATICOS DIARIOS
    # --------------------------------------------------------

    datos_diarios = cliente_api.consultar_todas_provincias(
        fecha_inicio="2018-01-01",
        fecha_fin="2024-12-31"
    )

    print("\nDimensiones de los datos diarios:")

    print(f"Filas: {datos_diarios.shape[0]}")
    print(f"Columnas: {datos_diarios.shape[1]}")

    # --------------------------------------------------------
    # PASO 3: CREAR EL RESUMEN CLIMATICO MENSUAL
    # --------------------------------------------------------

    resumen_mensual = cliente_api.resumir_clima_mensual(
        datos_diarios
    )

    print("\nDimensiones del resumen mensual:")

    print(f"Filas: {resumen_mensual.shape[0]}")
    print(f"Columnas: {resumen_mensual.shape[1]}")

    # --------------------------------------------------------
    # PASO 4: GUARDAR EL RESUMEN EN FORMATO CSV
    # --------------------------------------------------------

    ruta_archivo = cliente_api.guardar_resumen_climatico(
        resumen_mensual=resumen_mensual,
        nombre_archivo="clima_mensual_2018_2024.csv"
    )

    # --------------------------------------------------------
    # PASO 5: COMPROBAR QUE EL ARCHIVO EXISTA
    # --------------------------------------------------------

    archivo_existe = os.path.exists(ruta_archivo)

    print("\nComprobacion de existencia del archivo:")

    if archivo_existe:
        print("El archivo climatico fue creado correctamente.")
    else:
        print("No se encontro el archivo climatico generado.")

    # --------------------------------------------------------
    # PASO 6: VOLVER A CARGAR EL ARCHIVO GUARDADO
    # --------------------------------------------------------

    resumen_recuperado = pd.read_csv(
        ruta_archivo,
        sep=";",
        encoding="utf-8-sig"
    )

    print("\nDimensiones del archivo recuperado:")

    print(f"Filas recuperadas: {resumen_recuperado.shape[0]}")
    print(
        f"Columnas recuperadas: "
        f"{resumen_recuperado.shape[1]}"
    )

    # --------------------------------------------------------
    # PASO 7: MOSTRAR LAS COLUMNAS RECUPERADAS
    # --------------------------------------------------------

    print("\nColumnas recuperadas:")

    for columna in resumen_recuperado.columns:
        print(f"- {columna}")

    # --------------------------------------------------------
    # PASO 8: COMPROBAR LAS PROVINCIAS
    # --------------------------------------------------------

    provincias = sorted(
        resumen_recuperado["provincia"]
        .unique()
        .tolist()
    )

    print("\nProvincias recuperadas:")

    for provincia in provincias:
        print(f"- {provincia}")

    print(
        f"\nCantidad de provincias: "
        f"{len(provincias)}"
    )

    # --------------------------------------------------------
    # PASO 9: COMPROBAR LOS AÑOS
    # --------------------------------------------------------

    anios = sorted(
        resumen_recuperado["anio"]
        .unique()
        .tolist()
    )

    print("\nAños recuperados:")

    print(anios)

    print(
        f"Cantidad de años: "
        f"{len(anios)}"
    )

    # --------------------------------------------------------
    # PASO 10: COMPROBAR LOS MESES
    # --------------------------------------------------------

    meses = (
        resumen_recuperado[
            ["mes_numero", "mes"]
        ]
        .drop_duplicates()
        .sort_values("mes_numero")
    )

    print("\nRelacion entre numero y nombre del mes:")

    print(
        meses.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 11: MOSTRAR UNA MUESTRA DEL ARCHIVO
    # --------------------------------------------------------

    print("\nPrimeros 15 registros recuperados:")

    print(
        resumen_recuperado
        .head(15)
        .to_string(index=False)
    )

    # --------------------------------------------------------
    # PASO 12: COMPROBAR VALORES VACIOS
    # --------------------------------------------------------

    valores_vacios = resumen_recuperado.isna().sum()

    print("\nValores vacios en el archivo recuperado:")

    print(valores_vacios)

    # --------------------------------------------------------
    # PASO 13: COMPROBAR LA CANTIDAD POR PROVINCIA
    #
    # Cada provincia debe tener:
    # 7 años por 12 meses = 84 registros.
    # --------------------------------------------------------

    registros_por_provincia = (
        resumen_recuperado
        .groupby("provincia")
        .size()
        .reset_index(name="cantidad_registros")
        .sort_values("provincia")
    )

    print("\nRegistros mensuales por provincia:")

    print(
        registros_por_provincia.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 14: VALIDAR LOS DIAS CON LLUVIA
    # --------------------------------------------------------

    dias_lluvia_validos = resumen_recuperado[
        "dias_con_lluvia"
    ].between(0, 31).all()

    print("\nValidacion de dias con lluvia:")

    if dias_lluvia_validos:
        print(
            "Todos los valores estan entre 0 y 31 dias."
        )
    else:
        print(
            "Advertencia: existen valores fuera del rango."
        )

    # --------------------------------------------------------
    # PASO 15: REALIZAR LA COMPROBACION FINAL
    # --------------------------------------------------------

    filas_esperadas = 588
    columnas_esperadas = 8

    print("\nComprobacion final:")

    print(f"Filas esperadas: {filas_esperadas}")
    print(f"Filas recuperadas: {len(resumen_recuperado)}")

    print(f"Columnas esperadas: {columnas_esperadas}")
    print(
        f"Columnas recuperadas: "
        f"{resumen_recuperado.shape[1]}"
    )

    if (
        archivo_existe
        and len(resumen_recuperado) == filas_esperadas
        and resumen_recuperado.shape[1] == columnas_esperadas
        and len(provincias) == 7
        and len(anios) == 7
        and valores_vacios.sum() == 0
        and dias_lluvia_validos
    ):
        print(
            "\nEl archivo climatico mensual fue guardado "
            "y comprobado correctamente."
        )
    else:
        print(
            "\nAdvertencia: revise el archivo climatico "
            "generado."
        )


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
#
# Ejecuta main() solamente cuando este archivo
# se inicia directamente.
# ============================================================

if __name__ == "__main__":
    main()