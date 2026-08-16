# ============================================================
# VISUALIZADOR DE DATOS
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Esta clase contiene los graficos principales del proyecto:
# 1. Tendencia de accidentes por año.
# 2. Accidentes por provincia.
# 3. Distribucion de la gravedad.
# 4. Accidentes por mes.
# 5. Accidentes por dia.
# 6. Accidentes por franja horaria.
# 7. Tipos de accidente mas frecuentes.
# 8. Porcentaje de accidentes graves por provincia.
# 9. Mapa de calor entre dia y franja horaria.
# 10. Comparacion anual entre accidentes y precipitacion.
#
# Los metodos reciben las tablas creadas por ProcesadorEDA.
#
# A diferencia de la version anterior, esta clase ya NO guarda
# los graficos como archivos PNG: los muestra directamente
# (con plt.show()), pensados para usarse en un notebook o en
# cualquier entorno con interfaz grafica.
# ============================================================
 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
 
 
# ============================================================
# CLASE VISUALIZADOR
#
# Esta clase recibe los resultados del EDA y los convierte
# en graficos para facilitar su interpretacion.
# ============================================================
 
class Visualizador:
 
    # --------------------------------------------------------
    # METODO AUXILIAR: VALIDAR DATOS
    #
    # Comprueba que cada metodo reciba un DataFrame
    # que contenga información.
    # --------------------------------------------------------
 
    @staticmethod
    def _validar_datos(datos):
        """
        Comprueba que los datos sean un DataFrame valido.
 
        Parametro:
            datos: DataFrame que se desea visualizar.
        """
 
        if not isinstance(datos, pd.DataFrame):
            raise TypeError(
                "Los datos del grafico deben ser "
                "un DataFrame de Pandas."
            )
 
        if datos.empty:
            raise ValueError(
                "El DataFrame recibido esta vacio."
            )
 
    # --------------------------------------------------------
    # METODO AUXILIAR: MOSTRAR GRAFICO
    #
    # Ajusta y muestra el grafico actual, y luego cierra
    # la figura para liberar memoria.
    # --------------------------------------------------------
 
    @staticmethod
    def _mostrar_grafico():
        """
        Muestra el grafico actual en pantalla.
        """
 
        # Ajustar los elementos dentro de la figura
        plt.tight_layout()
 
        # Mostrar el grafico
        plt.show()
 
        # Cerrar la figura para liberar memoria
        plt.close()
 
    # ========================================================
    # SECCION 1: GRAFICOS TEMPORALES
    # ========================================================
 
    # --------------------------------------------------------
    # METODO: GRAFICO DE ACCIDENTES POR AÑO
    #
    # Muestra la tendencia anual mediante un grafico de linea.
    # --------------------------------------------------------
 
    def grafico_accidentes_por_anio(self, datos):
        """
        Crea y muestra un grafico de linea con los
        accidentes por año.
 
        Parametro:
            datos: resultado de accidentes_por_anio().
        """
 
        self._validar_datos(datos)
 
        plt.figure(
            figsize=(10, 6)
        )
 
        sns.lineplot(
            data=datos,
            x="anio",
            y="cantidad_accidentes",
            marker="o",
            linewidth=2.5,
            color="#1F4E78"
        )
 
        plt.title(
            "Accidentes de tránsito por año",
            fontsize=15,
            fontweight="bold"
        )
 
        plt.xlabel(
            "Año",
            fontsize=11
        )
 
        plt.ylabel(
            "Cantidad de accidentes",
            fontsize=11
        )
 
        plt.grid(
            axis="y",
            alpha=0.30
        )
 
        self._mostrar_grafico()
 
    # --------------------------------------------------------
    # METODO: GRAFICO DE ACCIDENTES POR MES
    #
    # Muestra la cantidad acumulada por mes.
    # --------------------------------------------------------
 
    def grafico_accidentes_por_mes(self, datos):
        """
        Crea y muestra un grafico de barras con los
        accidentes por mes.
 
        Parametro:
            datos: resultado de accidentes_por_mes().
        """
 
        self._validar_datos(datos)
 
        plt.figure(
            figsize=(12, 6)
        )
 
        sns.barplot(
            data=datos,
            x="mes",
            y="cantidad_accidentes",
            color="#5B9BD5"
        )
 
        plt.title(
            "Accidentes de tránsito por mes",
            fontsize=15,
            fontweight="bold"
        )
 
        plt.xlabel(
            "Mes",
            fontsize=11
        )
 
        plt.ylabel(
            "Cantidad de accidentes",
            fontsize=11
        )
 
        plt.xticks(
            rotation=45
        )
 
        self._mostrar_grafico()
 
    # --------------------------------------------------------
    # METODO: GRAFICO DE ACCIDENTES POR DIA
    #
    # Muestra la cantidad de accidentes por dia de la semana.
    # --------------------------------------------------------
 
    def grafico_accidentes_por_dia(self, datos):
        """
        Crea y muestra un grafico de barras con los
        accidentes por dia.
 
        Parametro:
            datos: resultado de accidentes_por_dia().
        """
 
        self._validar_datos(datos)
 
        plt.figure(
            figsize=(10, 6)
        )
 
        sns.barplot(
            data=datos,
            x="dia",
            y="cantidad_accidentes",
            color="#70AD47"
        )
 
        plt.title(
            "Accidentes por día de la semana",
            fontsize=15,
            fontweight="bold"
        )
 
        plt.xlabel(
            "Día de la semana",
            fontsize=11
        )
 
        plt.ylabel(
            "Cantidad de accidentes",
            fontsize=11
        )
 
        plt.xticks(
            rotation=30
        )
 
        self._mostrar_grafico()
 
    # --------------------------------------------------------
    # METODO: GRAFICO DE ACCIDENTES POR HORA
    #
    # Muestra las franjas horarias con más accidentes.
    # --------------------------------------------------------
 
    def grafico_accidentes_por_hora(self, datos):
        """
        Crea y muestra un grafico de barras por
        franja horaria.
 
        Parametro:
            datos: resultado de accidentes_por_hora().
        """
 
        self._validar_datos(datos)
 
        plt.figure(
            figsize=(10, 6)
        )
 
        sns.barplot(
            data=datos,
            x="hora_recodificada",
            y="cantidad_accidentes",
            color="#ED7D31"
        )
 
        plt.title(
            "Accidentes por franja horaria",
            fontsize=15,
            fontweight="bold"
        )
 
        plt.xlabel(
            "Franja horaria",
            fontsize=11
        )
 
        plt.ylabel(
            "Cantidad de accidentes",
            fontsize=11
        )
 
        plt.xticks(
            rotation=25
        )
 
        self._mostrar_grafico()
 
    # ========================================================
    # SECCION 2: GRAFICOS GEOGRAFICOS Y DE GRAVEDAD
    # ========================================================
 
    # --------------------------------------------------------
    # METODO: GRAFICO DE ACCIDENTES POR PROVINCIA
    #
    # Muestra las provincias con mayor cantidad de accidentes.
    # --------------------------------------------------------
 
    def grafico_accidentes_por_provincia(self, datos):
        """
        Crea y muestra un grafico horizontal por provincia.
 
        Parametro:
            datos: resultado de accidentes_por_provincia().
        """
 
        self._validar_datos(datos)
 
        # Ordenar de menor a mayor para el grafico horizontal
        datos_ordenados = datos.sort_values(
            "cantidad_accidentes",
            ascending=True
        )
 
        plt.figure(
            figsize=(10, 7)
        )
 
        sns.barplot(
            data=datos_ordenados,
            x="cantidad_accidentes",
            y="provincia",
            color="#4472C4"
        )
 
        plt.title(
            "Accidentes de tránsito por provincia",
            fontsize=15,
            fontweight="bold"
        )
 
        plt.xlabel(
            "Cantidad de accidentes",
            fontsize=11
        )
 
        plt.ylabel(
            "Provincia",
            fontsize=11
        )
 
        self._mostrar_grafico()
 
    # --------------------------------------------------------
    # METODO: GRAFICO DE DISTRIBUCION DE GRAVEDAD
    #
    # Compara los accidentes leves con los graves.
    # --------------------------------------------------------
 
    def grafico_distribucion_gravedad(self, datos):
        """
        Crea y muestra un grafico de barras para la gravedad.
 
        Parametro:
            datos: resultado de distribucion_gravedad().
        """
 
        self._validar_datos(datos)
 
        colores = [
            "#70AD47",
            "#C00000"
        ]
 
        plt.figure(
            figsize=(9, 6)
        )
 
        grafico = sns.barplot(
            data=datos,
            x="clase_accidente",
            y="cantidad_accidentes",
            hue="clase_accidente",
            palette=colores,
            legend=False
        )
 
        plt.title(
            "Distribución de la gravedad de los accidentes",
            fontsize=15,
            fontweight="bold"
        )
 
        plt.xlabel(
            "Clase de accidente",
            fontsize=11
        )
 
        plt.ylabel(
            "Cantidad de accidentes",
            fontsize=11
        )
 
        plt.xticks(
            rotation=10
        )
 
        # Mostrar la cantidad encima de cada barra
        for barra in grafico.patches:
 
            altura = barra.get_height()
 
            grafico.annotate(
                f"{int(altura):,}",
                (
                    barra.get_x()
                    + barra.get_width() / 2,
                    altura
                ),
                ha="center",
                va="bottom",
                fontsize=10
            )
 
        self._mostrar_grafico()
 
    # --------------------------------------------------------
    # METODO: GRAFICO DE GRAVEDAD POR PROVINCIA
    #
    # Compara el porcentaje de accidentes graves.
    # --------------------------------------------------------
 
    def grafico_gravedad_por_provincia(self, datos):
        """
        Crea y muestra un grafico del porcentaje grave
        por provincia.
 
        Parametro:
            datos: resultado de gravedad_por_provincia().
        """
 
        self._validar_datos(datos)
 
        datos_ordenados = datos.sort_values(
            "porcentaje_graves",
            ascending=True
        )
 
        plt.figure(
            figsize=(10, 7)
        )
 
        sns.barplot(
            data=datos_ordenados,
            x="porcentaje_graves",
            y="provincia",
            color="#C00000"
        )
 
        plt.title(
            "Porcentaje de accidentes graves por provincia",
            fontsize=15,
            fontweight="bold"
        )
 
        plt.xlabel(
            "Porcentaje de accidentes graves",
            fontsize=11
        )
 
        plt.ylabel(
            "Provincia",
            fontsize=11
        )
 
        self._mostrar_grafico()
 
    # ========================================================
    # SECCION 3: GRAFICOS POR CATEGORIA
    # ========================================================
 
    # --------------------------------------------------------
    # METODO: TIPOS DE ACCIDENTE MAS FRECUENTES
    #
    # Muestra los diez tipos con mayor cantidad.
    # --------------------------------------------------------
 
    def grafico_tipos_accidente(self, datos):
        """
        Crea y muestra un grafico con los tipos
        mas frecuentes.
 
        Parametro:
            datos: resultado de accidentes_por_tipo().
        """
 
        self._validar_datos(datos)
 
        # Seleccionar los diez tipos mas frecuentes
        datos_top = (
            datos
            .head(10)
            .sort_values(
                "cantidad_accidentes",
                ascending=True
            )
        )
 
        plt.figure(
            figsize=(12, 8)
        )
 
        sns.barplot(
            data=datos_top,
            x="cantidad_accidentes",
            y="tipo_accidente",
            color="#8064A2"
        )
 
        plt.title(
            "Diez tipos de accidente más frecuentes",
            fontsize=15,
            fontweight="bold"
        )
 
        plt.xlabel(
            "Cantidad de accidentes",
            fontsize=11
        )
 
        plt.ylabel(
            "Tipo de accidente",
            fontsize=11
        )
 
        self._mostrar_grafico()
 
    # ========================================================
    # SECCION 4: MAPA DE CALOR
    # ========================================================
 
    # --------------------------------------------------------
    # METODO: MAPA DE CALOR DIA Y HORA
    #
    # Muestra la concentracion de accidentes por dia
    # y franja horaria.
    # --------------------------------------------------------
 
    def mapa_calor_dia_hora(self, datos):
        """
        Crea y muestra un mapa de calor entre dia y
        franja horaria.
 
        Parametro:
            datos: resultado de tabla_dia_hora().
        """
 
        self._validar_datos(datos)
 
        # Guardar los nombres de los dias
        nombres_dias = datos["dia"]
 
        # Eliminar columnas que no pertenecen al mapa
        matriz = datos.drop(
            columns=[
                "dia_numero",
                "dia"
            ]
        )
 
        # Colocar los nombres de los dias como indice
        matriz.index = nombres_dias
 
        plt.figure(
            figsize=(11, 7)
        )
 
        sns.heatmap(
            matriz,
            annot=True,
            fmt="d",
            cmap="YlOrRd",
            linewidths=0.5,
            cbar_kws={
                "label": "Cantidad de accidentes"
            }
        )
 
        plt.title(
            "Mapa de calor de accidentes por día y hora",
            fontsize=15,
            fontweight="bold"
        )
 
        plt.xlabel(
            "Franja horaria",
            fontsize=11
        )
 
        plt.ylabel(
            "Día de la semana",
            fontsize=11
        )
 
        plt.xticks(
            rotation=25
        )
 
        plt.yticks(
            rotation=0
        )
 
        self._mostrar_grafico()
 
    # ========================================================
    # SECCION 5: RELACION ENTRE CLIMA Y ACCIDENTES
    # ========================================================
 
    # --------------------------------------------------------
    # METODO: COMPARACION ANUAL DE CLIMA Y ACCIDENTES
    #
    # Utiliza dos escalas verticales porque la precipitacion
    # y los accidentes manejan unidades diferentes.
    # --------------------------------------------------------
 
    def grafico_clima_accidentes_anual(self, datos):
        """
        Crea y muestra la comparacion entre accidentes
        y precipitacion por año.
 
        Parametro:
            datos: resultado de relacion_accidentes_clima().
        """
 
        self._validar_datos(datos)
 
        # Crear un resumen anual
        resumen_anual = (
            datos
            .groupby("anio")
            .agg(
                precipitacion_total_mm=(
                    "precipitacion_total_mm",
                    "sum"
                ),
                cantidad_accidentes=(
                    "cantidad_accidentes",
                    "sum"
                )
            )
            .reset_index()
            .sort_values("anio")
        )
 
        # Crear figura y primer eje
        figura, eje_accidentes = plt.subplots(
            figsize=(11, 6)
        )
 
        # Linea de accidentes
        eje_accidentes.plot(
            resumen_anual["anio"],
            resumen_anual["cantidad_accidentes"],
            color="#C00000",
            marker="o",
            linewidth=2.5,
            label="Accidentes"
        )
 
        eje_accidentes.set_xlabel(
            "Año",
            fontsize=11
        )
 
        eje_accidentes.set_ylabel(
            "Cantidad de accidentes",
            color="#C00000",
            fontsize=11
        )
 
        eje_accidentes.tick_params(
            axis="y",
            labelcolor="#C00000"
        )
 
        # Crear segundo eje vertical
        eje_clima = eje_accidentes.twinx()
 
        # Linea de precipitacion
        eje_clima.plot(
            resumen_anual["anio"],
            resumen_anual["precipitacion_total_mm"],
            color="#4472C4",
            marker="s",
            linewidth=2.5,
            label="Precipitación"
        )
 
        eje_clima.set_ylabel(
            "Precipitación total acumulada (mm)",
            color="#4472C4",
            fontsize=11
        )
 
        eje_clima.tick_params(
            axis="y",
            labelcolor="#4472C4"
        )
 
        plt.title(
            "Comparación anual entre accidentes y precipitación",
            fontsize=15,
            fontweight="bold"
        )
 
        # Crear una leyenda combinada
        lineas_1, etiquetas_1 = (
            eje_accidentes.get_legend_handles_labels()
        )
 
        lineas_2, etiquetas_2 = (
            eje_clima.get_legend_handles_labels()
        )
 
        eje_accidentes.legend(
            lineas_1 + lineas_2,
            etiquetas_1 + etiquetas_2,
            loc="best"
        )
 
        eje_accidentes.grid(
            axis="y",
            alpha=0.25
        )
 
        figura.tight_layout()
 
        # Mostrar la figura y luego cerrarla
        plt.show()
        plt.close(figura)