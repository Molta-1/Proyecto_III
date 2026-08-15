# ============================================================
# CLIENTE DE API CLIMATICA
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Este archivo contiene la clase encargada de:
# 1. Conectarse con la API historica de Open-Meteo.
# 2. Solicitar datos diarios de precipitacion.
# 3. Consultar las siete provincias de Costa Rica.
# 4. Convertir la respuesta JSON en un DataFrame.
# 5. Unir los resultados de todas las provincias.
# 6. Crear un resumen climatico mensual.
# 7. Guardar el resumen mensual en un archivo CSV.
# ============================================================

import os
import requests
import pandas as pd


# ============================================================
# CLASE CLIENTEAPI
#
# Esta clase administra las consultas realizadas a la API
# historica de Open-Meteo y el procesamiento del clima.
# ============================================================

class ClienteAPI:

    # --------------------------------------------------------
    # CONSTRUCTOR DE LA CLASE
    #
    # Guarda la direccion principal de Open-Meteo,
    # las coordenadas de las provincias y la ruta de salida.
    # --------------------------------------------------------

    def __init__(self):
        """
        Define la direccion de Open-Meteo, las coordenadas
        provinciales y la carpeta de datos procesados.
        """

        # Direccion principal de la API historica
        self.url_base = (
            "https://archive-api.open-meteo.com/v1/archive"
        )

        # Coordenadas de las capitales provinciales
        self.ubicaciones = {
            "San José": {
                "latitud": 9.93388,
                "longitud": -84.08489
            },
            "Alajuela": {
                "latitud": 10.01723,
                "longitud": -84.21275
            },
            "Cartago": {
                "latitud": 9.86371,
                "longitud": -83.91950
            },
            "Heredia": {
                "latitud": 9.99872,
                "longitud": -84.11587
            },
            "Guanacaste": {
                "latitud": 10.63517,
                "longitud": -85.43779
            },
            "Puntarenas": {
                "latitud": 9.97691,
                "longitud": -84.83790
            },
            "Limón": {
                "latitud": 9.99074,
                "longitud": -83.03596
            }
        }

        # Obtener la carpeta principal del proyecto
        ruta_archivo = os.path.abspath(__file__)
        carpeta_api = os.path.dirname(ruta_archivo)
        carpeta_src = os.path.dirname(carpeta_api)
        carpeta_proyecto = os.path.dirname(carpeta_src)

        # Crear la ruta hacia data/processed
        self.ruta_processed = os.path.join(
            carpeta_proyecto,
            "data",
            "processed"
        )

        # Crear la carpeta si no existe
        os.makedirs(
            self.ruta_processed,
            exist_ok=True
        )

    # --------------------------------------------------------
    # METODO: CONSULTAR PRECIPITACION
    #
    # Consulta la precipitacion diaria para una provincia
    # y un periodo determinado.
    # --------------------------------------------------------

    def consultar_precipitacion(
            self,
            provincia,
            latitud,
            longitud,
            fecha_inicio,
            fecha_fin
    ):
        """
        Consulta la precipitacion diaria en Open-Meteo.

        Parametros:
            provincia: nombre de la provincia consultada.
            latitud: coordenada geografica de latitud.
            longitud: coordenada geografica de longitud.
            fecha_inicio: primera fecha de la consulta.
            fecha_fin: ultima fecha de la consulta.

        Retorna:
            DataFrame con los datos climaticos diarios.
        """

        parametros = {
            "latitude": latitud,
            "longitude": longitud,
            "start_date": fecha_inicio,
            "end_date": fecha_fin,
            "daily": "precipitation_sum",
            "timezone": "America/Costa_Rica"
        }

        print(
            f"Consultando datos climaticos para "
            f"{provincia}..."
        )

        respuesta = requests.get(
            self.url_base,
            params=parametros,
            timeout=30
        )

        respuesta.raise_for_status()

        datos_json = respuesta.json()

        if "daily" not in datos_json:
            raise ValueError(
                f"La respuesta para {provincia} no contiene "
                "datos diarios."
            )

        datos_diarios = datos_json["daily"]

        datos_clima = pd.DataFrame({
            "fecha": datos_diarios["time"],
            "precipitacion_mm": datos_diarios[
                "precipitation_sum"
            ]
        })

        datos_clima["provincia"] = provincia
        datos_clima["latitud"] = latitud
        datos_clima["longitud"] = longitud

        datos_clima["fecha"] = pd.to_datetime(
            datos_clima["fecha"]
        )

        datos_clima["anio"] = datos_clima["fecha"].dt.year

        datos_clima["mes_numero"] = (
            datos_clima["fecha"].dt.month
        )

        orden_columnas = [
            "provincia",
            "latitud",
            "longitud",
            "fecha",
            "anio",
            "mes_numero",
            "precipitacion_mm"
        ]

        datos_clima = datos_clima[orden_columnas]

        print(
            f"Consulta de {provincia} terminada: "
            f"{len(datos_clima)} dias recuperados."
        )

        return datos_clima

    # --------------------------------------------------------
    # METODO: CONSULTAR TODAS LAS PROVINCIAS
    #
    # Consulta las siete provincias y une sus resultados.
    # --------------------------------------------------------

    def consultar_todas_provincias(
            self,
            fecha_inicio,
            fecha_fin
    ):
        """
        Consulta la precipitacion de las siete provincias.

        Parametros:
            fecha_inicio: primera fecha del periodo.
            fecha_fin: ultima fecha del periodo.

        Retorna:
            DataFrame unido con todas las provincias.
        """

        resultados = []

        for provincia, coordenadas in self.ubicaciones.items():

            datos_provincia = self.consultar_precipitacion(
                provincia=provincia,
                latitud=coordenadas["latitud"],
                longitud=coordenadas["longitud"],
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )

            resultados.append(datos_provincia)

        datos_completos = pd.concat(
            resultados,
            ignore_index=True
        )

        print(
            "\nConsulta de las siete provincias "
            "terminada correctamente."
        )

        print(
            f"Total de registros climaticos recuperados: "
            f"{len(datos_completos)}"
        )

        return datos_completos

    # --------------------------------------------------------
    # METODO: RESUMIR CLIMA MENSUAL
    #
    # Agrupa los datos diarios por provincia, año y mes.
    # --------------------------------------------------------

    def resumir_clima_mensual(self, datos_clima):
        """
        Crea un resumen mensual de la precipitacion.

        Parametro:
            datos_clima: DataFrame con los datos diarios.

        Retorna:
            DataFrame con el resumen mensual por provincia.
        """

        datos_trabajo = datos_clima.copy()

        # Identificar los dias con precipitacion
        datos_trabajo["hubo_lluvia"] = (
            datos_trabajo["precipitacion_mm"] > 0
        ).astype(int)

        # Crear el resumen mensual
        resumen_mensual = (
            datos_trabajo
            .groupby(
                [
                    "provincia",
                    "anio",
                    "mes_numero"
                ],
                as_index=False
            )
            .agg(
                precipitacion_total_mm=(
                    "precipitacion_mm",
                    "sum"
                ),
                precipitacion_promedio_mm=(
                    "precipitacion_mm",
                    "mean"
                ),
                precipitacion_maxima_mm=(
                    "precipitacion_mm",
                    "max"
                ),
                dias_con_lluvia=(
                    "hubo_lluvia",
                    "sum"
                )
            )
        )

        # Redondear los indicadores decimales
        columnas_decimales = [
            "precipitacion_total_mm",
            "precipitacion_promedio_mm",
            "precipitacion_maxima_mm"
        ]

        resumen_mensual[columnas_decimales] = (
            resumen_mensual[columnas_decimales]
            .round(2)
        )

        # Relacionar el numero con el nombre del mes
        nombres_meses = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Setiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre"
        }

        resumen_mensual["mes"] = (
            resumen_mensual["mes_numero"]
            .map(nombres_meses)
        )

        # Definir el orden de las columnas
        orden_columnas = [
            "provincia",
            "anio",
            "mes_numero",
            "mes",
            "precipitacion_total_mm",
            "precipitacion_promedio_mm",
            "precipitacion_maxima_mm",
            "dias_con_lluvia"
        ]

        resumen_mensual = resumen_mensual[orden_columnas]

        # Ordenar el resultado
        resumen_mensual = (
            resumen_mensual
            .sort_values(
                [
                    "provincia",
                    "anio",
                    "mes_numero"
                ]
            )
            .reset_index(drop=True)
        )

        print(
            "\nResumen climatico mensual creado "
            "correctamente."
        )

        print(
            f"Registros mensuales generados: "
            f"{len(resumen_mensual)}"
        )

        return resumen_mensual

    # --------------------------------------------------------
    # METODO: GUARDAR RESUMEN CLIMATICO
    #
    # Guarda el resumen mensual en data/processed.
    # --------------------------------------------------------

    def guardar_resumen_climatico(
            self,
            resumen_mensual,
            nombre_archivo="clima_mensual_2018_2024.csv"
    ):
        """
        Guarda el resumen climatico mensual en formato CSV.

        Parametros:
            resumen_mensual: DataFrame mensual que se guardara.
            nombre_archivo: nombre del archivo generado.

        Retorna:
            Ruta completa del archivo creado.
        """

        # Construir la ruta completa del archivo
        ruta_completa = os.path.join(
            self.ruta_processed,
            nombre_archivo
        )

        # Guardar el resumen mensual
        resumen_mensual.to_csv(
            ruta_completa,
            sep=";",
            encoding="utf-8-sig",
            index=False
        )

        print("\nResumen climatico guardado en:")
        print(ruta_completa)

        return ruta_completa