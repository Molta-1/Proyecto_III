# ============================================================
# GESTOR DE DATOS
# Proyecto: Predicción de la gravedad de accidentes de tránsito
#
# Este archivo contiene la clase encargada de:
# 1. Localizar las carpetas del proyecto.
# 2. Cargar el archivo CSV original.
# 3. Limpiar y preparar los datos.
# 4. Guardar el CSV procesado.
# 5. Volver a cargar el archivo procesado para comprobarlo.
# ============================================================

import os
import pandas as pd


# ============================================================
# CLASE GESTORDATOS
#
# Esta clase administra la carga, limpieza y almacenamiento
# de los datos utilizados en el proyecto.
# ============================================================

class GestorDatos:

    # --------------------------------------------------------
    # CONSTRUCTOR DE LA CLASE
    #
    # Identifica automáticamente la carpeta principal del
    # proyecto y crea las rutas hacia data/raw y data/processed.
    # --------------------------------------------------------

    def __init__(self):
        """
        Define las rutas de las carpetas raw y processed.

        La ruta se construye automáticamente para que el proyecto
        pueda ejecutarse en diferentes computadoras.
        """

        # Obtener la ruta completa de este archivo
        ruta_archivo = os.path.abspath(__file__)

        # Obtener la carpeta src/datos
        carpeta_datos = os.path.dirname(ruta_archivo)

        # Subir desde src/datos hasta src
        carpeta_src = os.path.dirname(carpeta_datos)

        # Subir desde src hasta la carpeta principal del proyecto
        carpeta_proyecto = os.path.dirname(carpeta_src)

        # Crear la ruta hacia la carpeta de datos originales
        self.ruta_raw = os.path.join(
            carpeta_proyecto,
            "data",
            "raw"
        )

        # Crear la ruta hacia la carpeta de datos procesados
        self.ruta_processed = os.path.join(
            carpeta_proyecto,
            "data",
            "processed"
        )

        # Crear las carpetas si no existen
        os.makedirs(self.ruta_raw, exist_ok=True)
        os.makedirs(self.ruta_processed, exist_ok=True)

    # --------------------------------------------------------
    # MÉTODO: CARGAR CSV ORIGINAL
    #
    # Busca y carga un archivo CSV almacenado en data/raw.
    # Devuelve los datos en forma de DataFrame de Pandas.
    # --------------------------------------------------------

    def cargar_csv(self, nombre_archivo):
        """
        Carga un archivo CSV desde la carpeta data/raw.

        Parámetro:
            nombre_archivo: nombre del archivo CSV que se cargará.

        Retorna:
            DataFrame con los datos originales.
        """

        # Construir la ruta completa del archivo
        ruta_completa = os.path.join(
            self.ruta_raw,
            nombre_archivo
        )

        # Comprobar que el archivo exista
        if not os.path.exists(ruta_completa):
            raise FileNotFoundError(
                f"No se encontró el archivo: {ruta_completa}"
            )

        # Leer el archivo CSV con Pandas
        datos = pd.read_csv(
            ruta_completa,
            sep=";",
            encoding="utf-8",
            low_memory=False
        )

        return datos

    # --------------------------------------------------------
    # MÉTODO: LIMPIAR DATOS
    #
    # Realiza la limpieza inicial del DataFrame:
    # 1. Limpia los nombres de las columnas.
    # 2. Renombra las columnas.
    # 3. Elimina registros duplicados.
    # 4. Crea la variable objetivo gravedad.
    # --------------------------------------------------------

    def limpiar_datos(self, datos):
        """
        Realiza la limpieza inicial de los datos.

        Parámetro:
            datos: DataFrame original que se desea limpiar.

        Retorna:
            DataFrame limpio con la variable gravedad.
        """

        # Crear una copia para no modificar los datos originales
        datos_limpios = datos.copy()

        # Eliminar espacios al inicio y al final de los encabezados
        datos_limpios.columns = datos_limpios.columns.str.strip()

        # Renombrar las columnas para facilitar su uso
        # en Python y SQL Server
        nuevos_nombres = {
            "Clase de accidente": "clase_accidente",
            "Tipo de accidente": "tipo_accidente",
            "Año": "anio",
            "Hora": "hora",
            "Hora recodificada": "hora_recodificada",
            "Provincia": "provincia",
            "Cantón": "canton",
            "Distrito": "distrito",
            "Ruta": "ruta",
            "Kilómetro": "kilometro",
            "Rural o urbano": "zona",
            "Calzada vertical": "calzada_vertical",
            "Calzada horizontal": "calzada_horizontal",
            "Tipo de calzada": "tipo_calzada",
            "Tipo de circulación": "tipo_circulacion",
            "Estado del tiempo": "estado_tiempo",
            "Estado de la calzada": "estado_calzada",
            "Región Mideplan": "region_mideplan",
            "Tipo ruta": "tipo_ruta",
            "Día": "dia",
            "Mes": "mes"
        }

        # Aplicar los nombres nuevos
        datos_limpios = datos_limpios.rename(
            columns=nuevos_nombres
        )

        # Guardar la cantidad de filas antes de eliminar duplicados
        cantidad_antes = len(datos_limpios)

        # Eliminar filas completamente duplicadas
        datos_limpios = datos_limpios.drop_duplicates()

        # Guardar la cantidad de filas después de la limpieza
        cantidad_despues = len(datos_limpios)

        # Calcular cuántos duplicados fueron eliminados
        duplicados_eliminados = (
            cantidad_antes - cantidad_despues
        )

        # Crear la variable objetivo del modelo:
        # 0 representa un accidente con heridos leves
        # 1 representa un accidente con muertos o heridos graves
        datos_limpios["gravedad"] = datos_limpios[
            "clase_accidente"
        ].map({
            "Solo heridos leves": 0,
            "Con muertos o graves": 1
        })

        print("\nLimpieza inicial terminada.")
        print(f"Duplicados eliminados: {duplicados_eliminados}")

        return datos_limpios

    # --------------------------------------------------------
    # MÉTODO: GUARDAR CSV PROCESADO
    #
    # Guarda el DataFrame limpio como un nuevo archivo CSV
    # dentro de la carpeta data/processed.
    # --------------------------------------------------------

    def guardar_csv(
            self,
            datos,
            nombre_archivo="accidentes_victimas_limpio.csv"
    ):
        """
        Guarda un DataFrame en la carpeta data/processed.

        Parámetros:
            datos: DataFrame que se desea guardar.
            nombre_archivo: nombre que tendrá el archivo generado.
        """

        # Construir la ruta completa del archivo de salida
        ruta_completa = os.path.join(
            self.ruta_processed,
            nombre_archivo
        )

        # Guardar el DataFrame como archivo CSV
        datos.to_csv(
            ruta_completa,
            sep=";",
            encoding="utf-8-sig",
            index=False
        )

        print("\nArchivo procesado guardado en:")
        print(ruta_completa)

    # --------------------------------------------------------
    # MÉTODO: CARGAR CSV PROCESADO
    #
    # Carga nuevamente el archivo guardado en data/processed.
    # Este método se utiliza para comprobar que el archivo
    # procesado se creó correctamente.
    # --------------------------------------------------------

    def cargar_csv_procesado(
            self,
            nombre_archivo="accidentes_victimas_limpio.csv"
    ):
        """
        Carga un archivo CSV desde la carpeta data/processed.

        Parámetro:
            nombre_archivo: nombre del archivo procesado.

        Retorna:
            DataFrame con los datos procesados.
        """

        # Construir la ruta completa del archivo procesado
        ruta_completa = os.path.join(
            self.ruta_processed,
            nombre_archivo
        )

        # Comprobar que el archivo procesado exista
        if not os.path.exists(ruta_completa):
            raise FileNotFoundError(
                f"No se encontró el archivo procesado: "
                f"{ruta_completa}"
            )

        # Leer el archivo procesado con Pandas
        datos = pd.read_csv(
            ruta_completa,
            sep=";",
            encoding="utf-8-sig",
            low_memory=False
        )

        return datos