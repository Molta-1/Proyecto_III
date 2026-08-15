# ============================================================
# GESTOR DE BASE DE DATOS
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Este archivo contiene la clase encargada de:
# 1. Leer la configuracion de SQL Server.
# 2. Crear la conexion con la base de datos.
# 3. Comprobar que la conexion funciona.
# 4. Contar los registros de las tablas.
# 5. Insertar los accidentes procesados.
# 6. Insertar el resumen climatico mensual.
# 7. Evitar cargas duplicadas.
# 8. Cerrar la conexion correctamente.
# ============================================================

import os
import pyodbc

from dotenv import load_dotenv


# ============================================================
# CLASE GESTORBASEDATOS
#
# Esta clase administra la conexion y las operaciones
# principales entre Python y SQL Server.
# ============================================================

class GestorBaseDatos:

    # --------------------------------------------------------
    # CONSTRUCTOR DE LA CLASE
    #
    # Localiza el archivo .env y carga la configuracion
    # necesaria para conectarse con SQL Server.
    # --------------------------------------------------------

    def __init__(self):
        """
        Carga la configuracion necesaria para establecer
        la conexion con SQL Server.
        """

        # Obtener la ruta completa de este archivo
        ruta_archivo = os.path.abspath(__file__)

        # Obtener la carpeta src/basedatos
        carpeta_basedatos = os.path.dirname(ruta_archivo)

        # Subir desde src/basedatos hasta src
        carpeta_src = os.path.dirname(carpeta_basedatos)

        # Subir desde src hasta la carpeta principal del proyecto
        carpeta_proyecto = os.path.dirname(carpeta_src)

        # Construir la ruta completa del archivo .env
        ruta_env = os.path.join(
            carpeta_proyecto,
            ".env"
        )

        # Cargar las variables guardadas en .env
        load_dotenv(ruta_env)

        # Obtener los datos necesarios para la conexion
        self.servidor = os.getenv("DB_SERVER")
        self.base_datos = os.getenv("DB_DATABASE")
        self.controlador = os.getenv("DB_DRIVER")

        # La conexion comienza vacia
        self.conexion = None

    # --------------------------------------------------------
    # METODO: CONECTAR
    #
    # Establece una conexion con SQL Server utilizando
    # autenticacion de Windows.
    # --------------------------------------------------------

    def conectar(self):
        """
        Establece la conexion con SQL Server.

        Retorna:
            Conexion activa con la base de datos.
        """

        # Comprobar que el archivo .env tenga la configuracion
        if not self.servidor:
            raise ValueError(
                "No se encontro DB_SERVER en el archivo .env."
            )

        if not self.base_datos:
            raise ValueError(
                "No se encontro DB_DATABASE en el archivo .env."
            )

        if not self.controlador:
            raise ValueError(
                "No se encontro DB_DRIVER en el archivo .env."
            )

        # Construir la cadena de conexion
        cadena_conexion = (
            f"DRIVER={{{self.controlador}}};"
            f"SERVER={self.servidor};"
            f"DATABASE={self.base_datos};"
            "Trusted_Connection=yes;"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
        )

        # Crear la conexion
        self.conexion = pyodbc.connect(
            cadena_conexion
        )

        print(
            "Conexion con SQL Server realizada correctamente."
        )

        return self.conexion

    # --------------------------------------------------------
    # METODO: PROBAR CONEXION
    #
    # Consulta el nombre de la base de datos actual para
    # confirmar que Python se conecto con la base correcta.
    # --------------------------------------------------------

    def probar_conexion(self):
        """
        Comprueba la conexion consultando la base actual.

        Retorna:
            Nombre de la base de datos conectada.
        """

        # Conectarse si todavia no existe una conexion
        if self.conexion is None:
            self.conectar()

        # Crear un cursor
        cursor = self.conexion.cursor()

        # Consultar el nombre de la base de datos actual
        cursor.execute(
            "SELECT DB_NAME() AS base_datos_actual"
        )

        # Recuperar el resultado
        resultado = cursor.fetchone()

        # Cerrar el cursor
        cursor.close()

        return resultado[0]

    # ========================================================
    # SECCION: TABLA DE ACCIDENTES
    # ========================================================

    # --------------------------------------------------------
    # METODO: CONTAR REGISTROS DE ACCIDENTES
    #
    # Consulta la cantidad de registros almacenados
    # actualmente en la tabla dbo.accidentes.
    # --------------------------------------------------------

    def contar_registros(self):
        """
        Cuenta los registros existentes en dbo.accidentes.

        Retorna:
            Cantidad de accidentes almacenados.
        """

        # Conectarse si todavia no existe una conexion
        if self.conexion is None:
            self.conectar()

        # Crear un cursor
        cursor = self.conexion.cursor()

        # Contar todos los registros
        cursor.execute(
            "SELECT COUNT(*) FROM dbo.accidentes"
        )

        # Recuperar la cantidad
        cantidad = cursor.fetchone()[0]

        # Cerrar el cursor
        cursor.close()

        return cantidad

    # --------------------------------------------------------
    # METODO: INSERTAR ACCIDENTES
    #
    # Inserta las 24 columnas del CSV procesado en la tabla.
    # La columna id_accidente no se incluye porque SQL Server
    # la crea automaticamente.
    # --------------------------------------------------------

    def insertar_accidentes(self, datos):
        """
        Inserta un DataFrame en la tabla dbo.accidentes.

        Parametro:
            datos: DataFrame con los accidentes procesados.

        Retorna:
            Cantidad de accidentes insertados.
        """

        # Conectarse si todavia no existe una conexion
        if self.conexion is None:
            self.conectar()

        # Comprobar si la tabla ya contiene registros
        registros_actuales = self.contar_registros()

        if registros_actuales > 0:
            print(
                "\nLa tabla accidentes ya contiene "
                f"{registros_actuales} registros."
            )

            print("No se realizara una nueva carga.")

            return 0

        # Definir el orden exacto de las columnas
        columnas_insertar = [
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

        # Comprobar que el DataFrame tenga las columnas
        columnas_faltantes = [
            columna
            for columna in columnas_insertar
            if columna not in datos.columns
        ]

        if columnas_faltantes:
            raise ValueError(
                "Faltan estas columnas en el DataFrame: "
                f"{columnas_faltantes}"
            )

        # Seleccionar las columnas en el orden correcto
        datos_insertar = datos[columnas_insertar]

        # Consulta para insertar las 24 columnas
        consulta = """
        INSERT INTO dbo.accidentes
        (
            clase_accidente,
            tipo_accidente,
            anio,
            hora,
            hora_recodificada,
            provincia,
            canton,
            distrito,
            ruta,
            kilometro,
            zona,
            calzada_vertical,
            calzada_horizontal,
            tipo_calzada,
            tipo_circulacion,
            estado_tiempo,
            estado_calzada,
            region_mideplan,
            tipo_ruta,
            dia_numero,
            dia,
            mes_numero,
            mes,
            gravedad
        )
        VALUES
        (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """

        # Convertir el DataFrame en una lista de filas
        filas = list(
            datos_insertar.itertuples(
                index=False,
                name=None
            )
        )

        # Crear un cursor
        cursor = self.conexion.cursor()

        # Acelerar la insercion de muchos registros
        cursor.fast_executemany = True

        print(
            f"\nIniciando carga de {len(filas)} accidentes "
            "en SQL Server..."
        )

        try:

            # Insertar todas las filas
            cursor.executemany(
                consulta,
                filas
            )

            # Confirmar los cambios
            self.conexion.commit()

            print(
                "Carga de accidentes terminada correctamente."
            )

            cantidad_insertada = len(filas)

        except Exception:

            # Cancelar la carga si ocurre un error
            self.conexion.rollback()

            print(
                "Ocurrio un error durante la carga "
                "de accidentes."
            )

            print("Los cambios fueron cancelados.")

            raise

        finally:

            # Cerrar el cursor
            cursor.close()

        return cantidad_insertada

    # ========================================================
    # SECCION: TABLA DE CLIMA MENSUAL
    # ========================================================

    # --------------------------------------------------------
    # METODO: CONTAR REGISTROS CLIMATICOS
    #
    # Consulta la cantidad de registros almacenados
    # actualmente en dbo.clima_mensual.
    # --------------------------------------------------------

    def contar_registros_clima(self):
        """
        Cuenta los registros existentes en dbo.clima_mensual.

        Retorna:
            Cantidad de registros climaticos almacenados.
        """

        # Conectarse si todavia no existe una conexion
        if self.conexion is None:
            self.conectar()

        # Crear un cursor
        cursor = self.conexion.cursor()

        # Contar los registros climaticos
        cursor.execute(
            "SELECT COUNT(*) FROM dbo.clima_mensual"
        )

        # Recuperar la cantidad
        cantidad = cursor.fetchone()[0]

        # Cerrar el cursor
        cursor.close()

        return cantidad

    # --------------------------------------------------------
    # METODO: INSERTAR CLIMA MENSUAL
    #
    # Inserta las ocho columnas del resumen climatico.
    # La columna id_clima no se incluye porque SQL Server
    # la genera automaticamente.
    # --------------------------------------------------------

    def insertar_clima_mensual(self, datos_clima):
        """
        Inserta el resumen climatico en dbo.clima_mensual.

        Parametro:
            datos_clima: DataFrame con el resumen mensual.

        Retorna:
            Cantidad de registros climaticos insertados.
        """

        # Conectarse si todavia no existe una conexion
        if self.conexion is None:
            self.conectar()

        # Comprobar si la tabla ya contiene registros
        registros_actuales = self.contar_registros_clima()

        if registros_actuales > 0:
            print(
                "\nLa tabla clima_mensual ya contiene "
                f"{registros_actuales} registros."
            )

            print(
                "No se realizara una nueva carga climatica."
            )

            return 0

        # Definir el orden exacto de las columnas
        columnas_insertar = [
            "provincia",
            "anio",
            "mes_numero",
            "mes",
            "precipitacion_total_mm",
            "precipitacion_promedio_mm",
            "precipitacion_maxima_mm",
            "dias_con_lluvia"
        ]

        # Comprobar que el DataFrame tenga las columnas
        columnas_faltantes = [
            columna
            for columna in columnas_insertar
            if columna not in datos_clima.columns
        ]

        if columnas_faltantes:
            raise ValueError(
                "Faltan estas columnas climaticas: "
                f"{columnas_faltantes}"
            )

        # Seleccionar las columnas en el orden correcto
        datos_insertar = datos_clima[columnas_insertar]

        # Consulta para insertar las ocho columnas
        consulta = """
        INSERT INTO dbo.clima_mensual
        (
            provincia,
            anio,
            mes_numero,
            mes,
            precipitacion_total_mm,
            precipitacion_promedio_mm,
            precipitacion_maxima_mm,
            dias_con_lluvia
        )
        VALUES
        (
            ?, ?, ?, ?, ?, ?, ?, ?
        )
        """

        # Convertir el DataFrame en una lista de filas
        filas = list(
            datos_insertar.itertuples(
                index=False,
                name=None
            )
        )

        # Crear un cursor
        cursor = self.conexion.cursor()

        # Acelerar la insercion
        cursor.fast_executemany = True

        print(
            f"\nIniciando carga de {len(filas)} registros "
            "climaticos en SQL Server..."
        )

        try:

            # Insertar todos los registros
            cursor.executemany(
                consulta,
                filas
            )

            # Confirmar los cambios
            self.conexion.commit()

            print(
                "Carga de datos climaticos terminada "
                "correctamente."
            )

            cantidad_insertada = len(filas)

        except Exception:

            # Cancelar la carga completa si ocurre un error
            self.conexion.rollback()

            print(
                "Ocurrio un error durante la carga "
                "de datos climaticos."
            )

            print("Los cambios fueron cancelados.")

            raise

        finally:

            # Cerrar el cursor
            cursor.close()

        return cantidad_insertada

    # ========================================================
    # SECCION: CIERRE DE LA CONEXION
    # ========================================================

    # --------------------------------------------------------
    # METODO: CERRAR CONEXION
    #
    # Cierra la conexion activa con SQL Server.
    # --------------------------------------------------------

    def cerrar_conexion(self):
        """
        Cierra la conexion con SQL Server si esta activa.
        """

        if self.conexion is not None:
            self.conexion.close()
            self.conexion = None

            print(
                "Conexion con SQL Server cerrada correctamente."
            )