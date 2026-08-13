# ============================================================
# PROCESADOR DE ANALISIS EXPLORATORIO DE DATOS
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Esta clase realiza el analisis exploratorio de los accidentes:
# 1. Resume las caracteristicas generales de los datos.
# 2. Revisa tipos de datos, vacios y duplicados.
# 3. Analiza accidentes por tiempo y ubicacion.
# 4. Analiza la gravedad según diferentes condiciones.
# 5. Crea una tabla cruzada de dia y franja horaria.
# 6. Relaciona accidentes y precipitacion mensual.
# ============================================================

import pandas as pd


# ============================================================
# CLASE PROCESADOREDA
#
# Esta clase recibe el DataFrame limpio de accidentes
# y genera diferentes tablas para el EDA.
# ============================================================

class ProcesadorEDA:

    # --------------------------------------------------------
    # CONSTRUCTOR
    #
    # Recibe y guarda una copia del DataFrame de accidentes.
    # --------------------------------------------------------

    def __init__(self, datos):
        """
        Guarda una copia de los datos para realizar el EDA.

        Parametro:
            datos: DataFrame limpio de accidentes.
        """

        if not isinstance(datos, pd.DataFrame):
            raise TypeError(
                "Los datos deben ser un DataFrame de Pandas."
            )

        if datos.empty:
            raise ValueError(
                "El DataFrame recibido esta vacio."
            )

        self.datos = datos.copy()

    # ========================================================
    # SECCION 1: COMPROBACION GENERAL DE LOS DATOS
    # ========================================================

    # --------------------------------------------------------
    # METODO: RESUMEN GENERAL
    # --------------------------------------------------------

    def resumen_general(self):
        """
        Crea un resumen general del conjunto de datos.

        Retorna:
            Diccionario con las principales cantidades.
        """

        resumen = {
            "cantidad_filas": self.datos.shape[0],
            "cantidad_columnas": self.datos.shape[1],
            "cantidad_duplicados": (
                self.datos.duplicated().sum()
            ),
            "total_valores_vacios": (
                self.datos.isna().sum().sum()
            ),
            "anio_inicial": int(
                self.datos["anio"].min()
            ),
            "anio_final": int(
                self.datos["anio"].max()
            ),
            "cantidad_provincias": (
                self.datos["provincia"].nunique()
            )
        }

        return resumen

    # --------------------------------------------------------
    # METODO: OBTENER TIPOS DE DATOS
    # --------------------------------------------------------

    def obtener_tipos_datos(self):
        """
        Obtiene el tipo de dato de cada columna.

        Retorna:
            DataFrame con columna y tipo de dato.
        """

        tipos = pd.DataFrame({
            "columna": self.datos.columns,
            "tipo_dato": [
                str(tipo)
                for tipo in self.datos.dtypes
            ]
        })

        return tipos

    # --------------------------------------------------------
    # METODO: ANALIZAR VALORES VACIOS
    # --------------------------------------------------------

    def analizar_valores_vacios(self):
        """
        Cuenta los valores vacios por columna.

        Retorna:
            DataFrame con cantidad y porcentaje de vacios.
        """

        cantidad_filas = len(self.datos)

        resultado = pd.DataFrame({
            "columna": self.datos.columns,
            "cantidad_vacios": (
                self.datos.isna().sum().values
            )
        })

        resultado["porcentaje_vacios"] = (
            resultado["cantidad_vacios"]
            / cantidad_filas
            * 100
        ).round(2)

        return resultado

    # ========================================================
    # SECCION 2: ANALISIS TEMPORAL Y GEOGRAFICO
    # ========================================================

    # --------------------------------------------------------
    # METODO: ACCIDENTES POR AÑO
    # --------------------------------------------------------

    def accidentes_por_anio(self):
        """
        Cuenta los accidentes registrados por año.

        Retorna:
            DataFrame ordenado cronologicamente.
        """

        resultado = (
            self.datos
            .groupby("anio")
            .size()
            .reset_index(name="cantidad_accidentes")
            .sort_values("anio")
            .reset_index(drop=True)
        )

        return resultado

    # --------------------------------------------------------
    # METODO: ACCIDENTES POR PROVINCIA
    # --------------------------------------------------------

    def accidentes_por_provincia(self):
        """
        Cuenta los accidentes registrados por provincia.

        Retorna:
            DataFrame ordenado de mayor a menor.
        """

        resultado = (
            self.datos
            .groupby("provincia")
            .size()
            .reset_index(name="cantidad_accidentes")
            .sort_values(
                "cantidad_accidentes",
                ascending=False
            )
            .reset_index(drop=True)
        )

        return resultado

    # --------------------------------------------------------
    # METODO: ACCIDENTES POR MES
    # --------------------------------------------------------

    def accidentes_por_mes(self):
        """
        Cuenta los accidentes registrados por mes.

        Retorna:
            DataFrame ordenado de enero a diciembre.
        """

        resultado = (
            self.datos
            .groupby(
                [
                    "mes_numero",
                    "mes"
                ]
            )
            .size()
            .reset_index(name="cantidad_accidentes")
            .sort_values("mes_numero")
            .reset_index(drop=True)
        )

        return resultado

    # --------------------------------------------------------
    # METODO: ACCIDENTES POR DIA
    # --------------------------------------------------------

    def accidentes_por_dia(self):
        """
        Cuenta los accidentes por dia de la semana.

        Retorna:
            DataFrame ordenado por numero del dia.
        """

        resultado = (
            self.datos
            .groupby(
                [
                    "dia_numero",
                    "dia"
                ]
            )
            .size()
            .reset_index(name="cantidad_accidentes")
            .sort_values("dia_numero")
            .reset_index(drop=True)
        )

        return resultado

    # --------------------------------------------------------
    # METODO: ACCIDENTES POR HORA
    # --------------------------------------------------------

    def accidentes_por_hora(self):
        """
        Cuenta los accidentes por franja horaria.

        Retorna:
            DataFrame con cantidad por franja.
        """

        resultado = (
            self.datos
            .groupby("hora_recodificada")
            .size()
            .reset_index(name="cantidad_accidentes")
            .sort_values("hora_recodificada")
            .reset_index(drop=True)
        )

        return resultado

    # --------------------------------------------------------
    # METODO: TABLA CRUZADA DIA Y HORA
    #
    # Muestra la cantidad de accidentes para cada combinacion
    # de dia de la semana y franja horaria.
    # --------------------------------------------------------

    def tabla_dia_hora(self):
        """
        Crea una tabla cruzada de dia y franja horaria.

        Retorna:
            DataFrame con dias en filas y horas en columnas.
        """

        tabla = pd.crosstab(
            index=[
                self.datos["dia_numero"],
                self.datos["dia"]
            ],
            columns=self.datos["hora_recodificada"],
            values=self.datos["gravedad"],
            aggfunc="count"
        )

        # Reemplazar valores vacios por cero
        tabla = tabla.fillna(0).astype(int)

        # Convertir los indices en columnas normales
        tabla = tabla.reset_index()

        # Eliminar el nombre interno de las columnas
        tabla.columns.name = None

        # Ordenar por numero del dia
        tabla = (
            tabla
            .sort_values("dia_numero")
            .reset_index(drop=True)
        )

        return tabla

    # ========================================================
    # SECCION 3: DISTRIBUCION Y GRAVEDAD
    # ========================================================

    # --------------------------------------------------------
    # METODO: DISTRIBUCION DE GRAVEDAD
    # --------------------------------------------------------

    def distribucion_gravedad(self):
        """
        Calcula la distribucion de la variable gravedad.

        Retorna:
            DataFrame con cantidad y porcentaje.
        """

        resultado = (
            self.datos
            .groupby(
                [
                    "gravedad",
                    "clase_accidente"
                ]
            )
            .size()
            .reset_index(name="cantidad_accidentes")
            .sort_values("gravedad")
            .reset_index(drop=True)
        )

        total_accidentes = resultado[
            "cantidad_accidentes"
        ].sum()

        resultado["porcentaje"] = (
            resultado["cantidad_accidentes"]
            / total_accidentes
            * 100
        ).round(2)

        return resultado

    # --------------------------------------------------------
    # METODO AUXILIAR: RESUMEN DE GRAVEDAD
    #
    # Calcula total, accidentes graves, leves y porcentaje
    # grave para una columna categorica.
    # --------------------------------------------------------

    def _resumir_gravedad_por(self, columna):
        """
        Calcula la gravedad agrupada por una columna.

        Parametro:
            columna: nombre de la columna utilizada para agrupar.

        Retorna:
            DataFrame con totales y porcentaje grave.
        """

        if columna not in self.datos.columns:
            raise ValueError(
                f"La columna {columna} no existe."
            )

        resultado = (
            self.datos
            .groupby(columna)
            .agg(
                total_accidentes=(
                    "gravedad",
                    "count"
                ),
                accidentes_graves=(
                    "gravedad",
                    "sum"
                )
            )
            .reset_index()
        )

        resultado["accidentes_leves"] = (
            resultado["total_accidentes"]
            - resultado["accidentes_graves"]
        )

        resultado["porcentaje_graves"] = (
            resultado["accidentes_graves"]
            / resultado["total_accidentes"]
            * 100
        ).round(2)

        resultado = (
            resultado
            .sort_values(
                "porcentaje_graves",
                ascending=False
            )
            .reset_index(drop=True)
        )

        return resultado

    # --------------------------------------------------------
    # METODO: GRAVEDAD POR PROVINCIA
    # --------------------------------------------------------

    def gravedad_por_provincia(self):
        """
        Analiza la gravedad por provincia.

        Retorna:
            DataFrame con totales y porcentaje grave.
        """

        return self._resumir_gravedad_por(
            "provincia"
        )

    # --------------------------------------------------------
    # METODO: GRAVEDAD POR TIPO DE ACCIDENTE
    # --------------------------------------------------------

    def gravedad_por_tipo_accidente(self):
        """
        Analiza la gravedad por tipo de accidente.

        Retorna:
            DataFrame con totales y porcentaje grave.
        """

        return self._resumir_gravedad_por(
            "tipo_accidente"
        )

    # --------------------------------------------------------
    # METODO: GRAVEDAD POR ZONA
    # --------------------------------------------------------

    def gravedad_por_zona(self):
        """
        Compara la gravedad entre zona rural y urbana.

        Retorna:
            DataFrame con totales y porcentaje grave.
        """

        return self._resumir_gravedad_por(
            "zona"
        )

    # --------------------------------------------------------
    # METODO: GRAVEDAD POR TIPO DE RUTA
    # --------------------------------------------------------

    def gravedad_por_tipo_ruta(self):
        """
        Analiza la gravedad por tipo de ruta.

        Retorna:
            DataFrame con totales y porcentaje grave.
        """

        return self._resumir_gravedad_por(
            "tipo_ruta"
        )

    # --------------------------------------------------------
    # METODO: GRAVEDAD POR ESTADO DEL TIEMPO
    # --------------------------------------------------------

    def gravedad_por_estado_tiempo(self):
        """
        Analiza la gravedad según el estado del tiempo.

        Retorna:
            DataFrame con totales y porcentaje grave.
        """

        return self._resumir_gravedad_por(
            "estado_tiempo"
        )

    # --------------------------------------------------------
    # METODO: GRAVEDAD POR ESTADO DE LA CALZADA
    # --------------------------------------------------------

    def gravedad_por_estado_calzada(self):
        """
        Analiza la gravedad según el estado de la calzada.

        Retorna:
            DataFrame con totales y porcentaje grave.
        """

        return self._resumir_gravedad_por(
            "estado_calzada"
        )

    # ========================================================
    # SECCION 4: FRECUENCIAS POR CATEGORIA
    # ========================================================

    # --------------------------------------------------------
    # METODO: ACCIDENTES POR TIPO
    # --------------------------------------------------------

    def accidentes_por_tipo(self):
        """
        Cuenta los accidentes por tipo.

        Retorna:
            DataFrame ordenado de mayor a menor.
        """

        resultado = (
            self.datos
            .groupby("tipo_accidente")
            .size()
            .reset_index(name="cantidad_accidentes")
            .sort_values(
                "cantidad_accidentes",
                ascending=False
            )
            .reset_index(drop=True)
        )

        return resultado

    # --------------------------------------------------------
    # METODO: ACCIDENTES POR CLIMA
    # --------------------------------------------------------

    def accidentes_por_clima(self):
        """
        Cuenta los accidentes por estado del tiempo.

        Retorna:
            DataFrame ordenado de mayor a menor.
        """

        resultado = (
            self.datos
            .groupby("estado_tiempo")
            .size()
            .reset_index(name="cantidad_accidentes")
            .sort_values(
                "cantidad_accidentes",
                ascending=False
            )
            .reset_index(drop=True)
        )

        return resultado

    # --------------------------------------------------------
    # METODO: ACCIDENTES POR ZONA
    # --------------------------------------------------------

    def accidentes_por_zona(self):
        """
        Cuenta los accidentes según zona rural o urbana.

        Retorna:
            DataFrame ordenado de mayor a menor.
        """

        resultado = (
            self.datos
            .groupby("zona")
            .size()
            .reset_index(name="cantidad_accidentes")
            .sort_values(
                "cantidad_accidentes",
                ascending=False
            )
            .reset_index(drop=True)
        )

        return resultado

    # --------------------------------------------------------
    # METODO: ACCIDENTES POR TIPO DE RUTA
    # --------------------------------------------------------

    def accidentes_por_tipo_ruta(self):
        """
        Cuenta los accidentes según el tipo de ruta.

        Retorna:
            DataFrame ordenado de mayor a menor.
        """

        resultado = (
            self.datos
            .groupby("tipo_ruta")
            .size()
            .reset_index(name="cantidad_accidentes")
            .sort_values(
                "cantidad_accidentes",
                ascending=False
            )
            .reset_index(drop=True)
        )

        return resultado

    # --------------------------------------------------------
    # METODO: ACCIDENTES POR ESTADO DE CALZADA
    # --------------------------------------------------------

    def accidentes_por_estado_calzada(self):
        """
        Cuenta los accidentes según el estado de la calzada.

        Retorna:
            DataFrame ordenado de mayor a menor.
        """

        resultado = (
            self.datos
            .groupby("estado_calzada")
            .size()
            .reset_index(name="cantidad_accidentes")
            .sort_values(
                "cantidad_accidentes",
                ascending=False
            )
            .reset_index(drop=True)
        )

        return resultado

    # ========================================================
    # SECCION 5: RELACION ENTRE ACCIDENTES Y CLIMA
    # ========================================================

    # --------------------------------------------------------
    # METODO: RELACION MENSUAL CON CLIMA
    #
    # Agrupa los accidentes por provincia, año y mes.
    # Luego los relaciona con el resumen mensual de Open-Meteo.
    # --------------------------------------------------------

    def relacion_accidentes_clima(self, datos_clima):
        """
        Relaciona accidentes y precipitacion mensual.

        Parametro:
            datos_clima: DataFrame con el resumen climático
                         mensual de Open-Meteo.

        Retorna:
            DataFrame mensual con clima, accidentes y gravedad.
        """

        if not isinstance(datos_clima, pd.DataFrame):
            raise TypeError(
                "Los datos climaticos deben ser un DataFrame."
            )

        if datos_clima.empty:
            raise ValueError(
                "El DataFrame climatico esta vacio."
            )

        # Columnas necesarias del resumen climatico
        columnas_clima = [
            "provincia",
            "anio",
            "mes_numero",
            "mes",
            "precipitacion_total_mm",
            "precipitacion_promedio_mm",
            "precipitacion_maxima_mm",
            "dias_con_lluvia"
        ]

        columnas_faltantes = [
            columna
            for columna in columnas_clima
            if columna not in datos_clima.columns
        ]

        if columnas_faltantes:
            raise ValueError(
                "Faltan columnas climaticas: "
                f"{columnas_faltantes}"
            )

        # Agrupar los accidentes por provincia, año y mes
        resumen_accidentes = (
            self.datos
            .groupby(
                [
                    "provincia",
                    "anio",
                    "mes_numero"
                ]
            )
            .agg(
                cantidad_accidentes=(
                    "id_temporal",
                    "count"
                )
                if "id_temporal" in self.datos.columns
                else (
                    "gravedad",
                    "count"
                ),
                accidentes_graves=(
                    "gravedad",
                    "sum"
                )
            )
            .reset_index()
        )

        # Calcular accidentes leves
        resumen_accidentes["accidentes_leves"] = (
            resumen_accidentes["cantidad_accidentes"]
            - resumen_accidentes["accidentes_graves"]
        )

        # Calcular porcentaje de accidentes graves
        resumen_accidentes["porcentaje_graves"] = (
            resumen_accidentes["accidentes_graves"]
            / resumen_accidentes["cantidad_accidentes"]
            * 100
        ).round(2)

        # Relacionar ambos DataFrames
        resultado = datos_clima[columnas_clima].merge(
            resumen_accidentes,
            on=[
                "provincia",
                "anio",
                "mes_numero"
            ],
            how="left"
        )

        # Si una combinación no tiene accidentes, colocar cero
        columnas_accidentes = [
            "cantidad_accidentes",
            "accidentes_graves",
            "accidentes_leves",
            "porcentaje_graves"
        ]

        resultado[columnas_accidentes] = (
            resultado[columnas_accidentes]
            .fillna(0)
        )

        columnas_enteras = [
            "cantidad_accidentes",
            "accidentes_graves",
            "accidentes_leves"
        ]

        resultado[columnas_enteras] = (
            resultado[columnas_enteras]
            .astype(int)
        )

        # Ordenar cronologicamente
        resultado = (
            resultado
            .sort_values(
                [
                    "provincia",
                    "anio",
                    "mes_numero"
                ]
            )
            .reset_index(drop=True)
        )

        return resultado