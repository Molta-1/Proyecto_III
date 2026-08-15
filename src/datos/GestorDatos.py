# ============================================================
# GESTOR DE DATOS
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Este archivo contiene la clase encargada de:
# 1. Localizar las carpetas del proyecto.
# 2. Cargar el archivo CSV original.
# 3. Limpiar y preparar los datos.
# 4. Separar el numero y el nombre del dia y del mes.
# 5. Guardar el CSV procesado.
# 6. Volver a cargar el archivo procesado para comprobarlo.
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
    # Identifica automaticamente la carpeta principal del
    # proyecto y crea las rutas hacia data/raw y data/processed.
    # --------------------------------------------------------

    def __init__(self):
        """
        Define las rutas de las carpetas raw y processed.

        La ruta se construye automaticamente para que el proyecto
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
    # METODO: CARGAR CSV ORIGINAL
    #
    # Busca y carga un archivo CSV almacenado en data/raw.
    # Devuelve los datos como un DataFrame de Pandas.
    # --------------------------------------------------------

    def cargar_csv(self, nombre_archivo):
        """
        Carga un archivo CSV desde la carpeta data/raw.

        Parametro:
            nombre_archivo: nombre del archivo CSV que se cargara.

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
                f"No se encontro el archivo: {ruta_completa}"
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
    # METODO: LIMPIAR DATOS
    #
    # Realiza la limpieza inicial del DataFrame:
    # 1. Limpia los nombres de las columnas.
    # 2. Renombra las columnas.
    # 3. Elimina registros duplicados.
    # 4. Separa el numero y el nombre del dia.
    # 5. Separa el numero y el nombre del mes.
    # 6. Crea la variable objetivo gravedad.
    # --------------------------------------------------------

    def limpiar_datos(self, datos):
        """
        Realiza la limpieza inicial de los datos.

        Parametro:
            datos: DataFrame original que se desea limpiar.

        Retorna:
            DataFrame limpio y preparado para el proyecto.
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

        # Guardar la cantidad de filas despues de la limpieza
        cantidad_despues = len(datos_limpios)

        # Calcular cuantos duplicados fueron eliminados
        duplicados_eliminados = (
            cantidad_antes - cantidad_despues
        )

        # ----------------------------------------------------
        # LIMPIAR LA COLUMNA DIA
        #
        # Ejemplo original:
        # 7.Sabado
        #
        # Resultado:
        # dia_numero = 7
        # dia = Sabado
        # ----------------------------------------------------

        dia_separado = datos_limpios["dia"].str.extract(
            r"^(\d+)\.(.+)$"
        )

        # Guardar el numero del dia como entero
        datos_limpios["dia_numero"] = (
            dia_separado[0].astype(int)
        )

        # Conservar solamente el nombre del dia
        datos_limpios["dia"] = (
            dia_separado[1].str.strip()
        )

        # ----------------------------------------------------
        # LIMPIAR LA COLUMNA MES
        #
        # Ejemplo original:
        # D. Abril
        #
        # Resultado:
        # mes_numero = 4
        # mes = Abril
        # ----------------------------------------------------

        mes_separado = datos_limpios["mes"].str.extract(
            r"^([A-L])\.\s*(.+)$"
        )

        # Relacionar cada letra con el numero del mes
        numeros_meses = {
            "A": 1,
            "B": 2,
            "C": 3,
            "D": 4,
            "E": 5,
            "F": 6,
            "G": 7,
            "H": 8,
            "I": 9,
            "J": 10,
            "K": 11,
            "L": 12
        }

        # Convertir la letra del mes en su numero correspondiente
        datos_limpios["mes_numero"] = (
            mes_separado[0]
            .map(numeros_meses)
            .astype(int)
        )

        # Conservar solamente el nombre del mes
        datos_limpios["mes"] = (
            mes_separado[1].str.strip()
        )

        # ----------------------------------------------------
        # CREAR LA VARIABLE OBJETIVO
        #
        # 0 = Solo heridos leves
        # 1 = Con muertos o graves
        # ----------------------------------------------------

        datos_limpios["gravedad"] = datos_limpios[
            "clase_accidente"
        ].map({
            "Solo heridos leves": 0,
            "Con muertos o graves": 1
        })

        # ----------------------------------------------------
        # ORDENAR LAS COLUMNAS
        #
        # Este orden se utilizara posteriormente para insertar
        # los registros en SQL Server.
        # ----------------------------------------------------

        orden_columnas = [
            "clase_accidente",
            "tipo_accidente",
            "anio",
            "hora",
            "hora_recodificada",
            "provincia",
            "canton",
            "distrito",
            "ruta",
            "kilometro",
            "zona",
            "calzada_vertical",
            "calzada_horizontal",
            "tipo_calzada",
            "tipo_circulacion",
            "estado_tiempo",
            "estado_calzada",
            "region_mideplan",
            "tipo_ruta",
            "dia_numero",
            "dia",
            "mes_numero",
            "mes",
            "gravedad"
        ]

        datos_limpios = datos_limpios[orden_columnas]

        print("\nLimpieza inicial terminada.")
        print(f"Duplicados eliminados: {duplicados_eliminados}")

        return datos_limpios

    # --------------------------------------------------------
    # METODO: GUARDAR CSV PROCESADO
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

        Parametros:
            datos: DataFrame que se desea guardar.
            nombre_archivo: nombre que tendra el archivo generado.
        """

        # Construir la ruta completa del archivo de salida
        ruta_completa = os.path.join(
            self.ruta_processed,
            nombre_archivo
        )

        # Guardar el DataFrame como un archivo CSV
        datos.to_csv(
            ruta_completa,
            sep=";",
            encoding="utf-8-sig",
            index=False
        )

        print("\nArchivo procesado guardado en:")
        print(ruta_completa)

    # --------------------------------------------------------
    # METODO: CARGAR CSV PROCESADO
    #
    # Carga nuevamente el archivo guardado en data/processed.
    # Permite comprobar que el archivo se creo correctamente.
    # --------------------------------------------------------

    def cargar_csv_procesado(
            self,
            nombre_archivo="accidentes_victimas_limpio.csv"
    ):
        """
        Carga un archivo CSV desde la carpeta data/processed.

        Parametro:
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
                f"No se encontro el archivo procesado: "
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