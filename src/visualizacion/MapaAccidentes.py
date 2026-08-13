# ============================================================
# MAPA INTERACTIVO DE ACCIDENTES
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Esta clase crea un mapa interactivo de Costa Rica con:
# 1. Una ubicacion representativa por provincia.
# 2. Marcadores proporcionales al total de accidentes.
# 3. Colores segun el porcentaje de accidentes graves.
# 4. Ventanas con informacion detallada.
# 5. Un archivo HTML que puede abrirse en el navegador.
# ============================================================

import os
import folium
import pandas as pd


# ============================================================
# CLASE MAPAACCIDENTES
#
# Esta clase utiliza los resultados del EDA para mostrar
# los accidentes y su gravedad en un mapa interactivo.
# ============================================================

class MapaAccidentes:

    # --------------------------------------------------------
    # CONSTRUCTOR
    #
    # Define las coordenadas representativas de las provincias
    # y la carpeta donde se guardara el mapa.
    # --------------------------------------------------------

    def __init__(self):
        """
        Define las coordenadas provinciales y la ruta
        donde se guardara el mapa HTML.
        """

        # Coordenadas representativas de las provincias
        self.coordenadas = {
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

        carpeta_visualizacion = os.path.dirname(
            ruta_archivo
        )

        carpeta_src = os.path.dirname(
            carpeta_visualizacion
        )

        carpeta_proyecto = os.path.dirname(
            carpeta_src
        )

        # Utilizar la misma carpeta de los graficos
        self.ruta_graficos = os.path.join(
            carpeta_proyecto,
            "graficos"
        )

        # Crear la carpeta si no existe
        os.makedirs(
            self.ruta_graficos,
            exist_ok=True
        )

    # --------------------------------------------------------
    # METODO AUXILIAR: VALIDAR DATOS
    #
    # Comprueba que la tabla recibida tenga las columnas
    # necesarias para crear el mapa.
    # --------------------------------------------------------

    @staticmethod
    def _validar_datos(datos):
        """
        Comprueba que los datos sean validos.

        Parametro:
            datos: resultado de gravedad_por_provincia().
        """

        if not isinstance(datos, pd.DataFrame):
            raise TypeError(
                "Los datos deben ser un DataFrame de Pandas."
            )

        if datos.empty:
            raise ValueError(
                "El DataFrame recibido esta vacio."
            )

        columnas_necesarias = [
            "provincia",
            "total_accidentes",
            "accidentes_graves",
            "accidentes_leves",
            "porcentaje_graves"
        ]

        columnas_faltantes = [
            columna
            for columna in columnas_necesarias
            if columna not in datos.columns
        ]

        if columnas_faltantes:
            raise ValueError(
                "Faltan estas columnas para crear el mapa: "
                f"{columnas_faltantes}"
            )

    # --------------------------------------------------------
    # METODO AUXILIAR: OBTENER COLOR
    #
    # Asigna un color segun el porcentaje de accidentes graves.
    # --------------------------------------------------------

    @staticmethod
    def _obtener_color(porcentaje_graves):
        """
        Obtiene el color del marcador según la gravedad.

        Parametro:
            porcentaje_graves: porcentaje grave de la provincia.

        Retorna:
            Nombre del color utilizado por Folium.
        """

        if porcentaje_graves >= 20:
            return "darkred"

        if porcentaje_graves >= 17:
            return "red"

        if porcentaje_graves >= 14:
            return "orange"

        return "green"

    # --------------------------------------------------------
    # METODO AUXILIAR: CALCULAR RADIO
    #
    # Convierte la cantidad de accidentes en un tamaño
    # adecuado para el marcador.
    # --------------------------------------------------------

    @staticmethod
    def _calcular_radio(
            total_accidentes,
            maximo_accidentes
    ):
        """
        Calcula el radio proporcional del marcador.

        Parametros:
            total_accidentes: accidentes de la provincia.
            maximo_accidentes: mayor total provincial.

        Retorna:
            Radio del marcador entre 8 y 30 pixeles.
        """

        radio_minimo = 8
        radio_maximo = 30

        proporcion = (
            total_accidentes
            / maximo_accidentes
        )

        radio = (
            radio_minimo
            + proporcion
            * (radio_maximo - radio_minimo)
        )

        return round(radio, 2)

    # --------------------------------------------------------
    # METODO: CREAR MAPA POR PROVINCIA
    #
    # Crea el mapa interactivo y lo guarda como HTML.
    # --------------------------------------------------------

    def crear_mapa_provincias(
            self,
            datos,
            nombre_archivo=(
                "11_mapa_accidentes_provincia.html"
            )
    ):
        """
        Crea un mapa interactivo de accidentes por provincia.

        Parametros:
            datos: resultado de gravedad_por_provincia().
            nombre_archivo: nombre del mapa HTML.

        Retorna:
            Ruta completa del mapa guardado.
        """

        # Validar la información recibida
        self._validar_datos(datos)

        # Comprobar que todas las provincias tengan coordenadas
        provincias_sin_coordenadas = [
            provincia
            for provincia in datos["provincia"]
            if provincia not in self.coordenadas
        ]

        if provincias_sin_coordenadas:
            raise ValueError(
                "No existen coordenadas para estas provincias: "
                f"{provincias_sin_coordenadas}"
            )

        # Crear el mapa centrado aproximadamente en Costa Rica
        mapa = folium.Map(
            location=[
                9.95,
                -84.15
            ],
            zoom_start=8,
            tiles="OpenStreetMap"
        )

        # Obtener el mayor total provincial
        maximo_accidentes = datos[
            "total_accidentes"
        ].max()

        # Recorrer las provincias
        for _, fila in datos.iterrows():

            provincia = fila["provincia"]

            total_accidentes = int(
                fila["total_accidentes"]
            )

            accidentes_graves = int(
                fila["accidentes_graves"]
            )

            accidentes_leves = int(
                fila["accidentes_leves"]
            )

            porcentaje_graves = float(
                fila["porcentaje_graves"]
            )

            # Obtener las coordenadas
            latitud = self.coordenadas[
                provincia
            ]["latitud"]

            longitud = self.coordenadas[
                provincia
            ]["longitud"]

            # Calcular color y tamaño
            color = self._obtener_color(
                porcentaje_graves
            )

            radio = self._calcular_radio(
                total_accidentes,
                maximo_accidentes
            )

            # Crear el contenido de la ventana emergente
            contenido_popup = f"""
            <div style="font-family: Arial; width: 240px;">
                <h3 style="margin-bottom: 8px;">
                    {provincia}
                </h3>

                <b>Total de accidentes:</b>
                {total_accidentes:,}
                <br>

                <b>Accidentes leves:</b>
                {accidentes_leves:,}
                <br>

                <b>Accidentes graves:</b>
                {accidentes_graves:,}
                <br>

                <b>Porcentaje grave:</b>
                {porcentaje_graves:.2f} %
                <br>

                <hr>

                <small>
                    Periodo analizado: 2018-2024
                </small>
            </div>
            """

            # Crear el marcador circular
            folium.CircleMarker(
                location=[
                    latitud,
                    longitud
                ],
                radius=radio,
                color=color,
                weight=2,
                fill=True,
                fill_color=color,
                fill_opacity=0.65,
                tooltip=(
                    f"{provincia}: "
                    f"{total_accidentes:,} accidentes"
                ),
                popup=folium.Popup(
                    contenido_popup,
                    max_width=300
                )
            ).add_to(mapa)

        # ----------------------------------------------------
        # AGREGAR TITULO AL MAPA
        # ----------------------------------------------------

        titulo_html = """
        <div style="
            position: fixed;
            top: 10px;
            left: 50px;
            width: 430px;
            z-index: 9999;
            background-color: white;
            border: 2px solid #1F4E78;
            border-radius: 6px;
            padding: 10px;
            font-family: Arial;
            font-size: 16px;
            text-align: center;
        ">
            <b>
                Accidentes de tránsito por provincia
            </b>
            <br>
            <span style="font-size: 12px;">
                Costa Rica, periodo 2018-2024
            </span>
        </div>
        """

        mapa.get_root().html.add_child(
            folium.Element(titulo_html)
        )

        # ----------------------------------------------------
        # AGREGAR LEYENDA DE COLORES
        # ----------------------------------------------------

        leyenda_html = """
        <div style="
            position: fixed;
            bottom: 30px;
            left: 30px;
            width: 240px;
            z-index: 9999;
            background-color: white;
            border: 2px solid gray;
            border-radius: 6px;
            padding: 10px;
            font-family: Arial;
            font-size: 12px;
        ">
            <b>Porcentaje de accidentes graves</b>
            <br><br>

            <span style="color: green;">●</span>
            Menos de 14 %
            <br>

            <span style="color: orange;">●</span>
            Entre 14 % y 16,99 %
            <br>

            <span style="color: red;">●</span>
            Entre 17 % y 19,99 %
            <br>

            <span style="color: darkred;">●</span>
            20 % o más
            <br><br>

            <small>
                El tamaño representa el total de accidentes.
            </small>
        </div>
        """

        mapa.get_root().html.add_child(
            folium.Element(leyenda_html)
        )

        # Construir la ruta de salida
        ruta_completa = os.path.join(
            self.ruta_graficos,
            nombre_archivo
        )

        # Guardar el mapa como archivo HTML
        mapa.save(
            ruta_completa
        )

        print(
            f"Mapa guardado correctamente: "
            f"{ruta_completa}"
        )

        return ruta_completa