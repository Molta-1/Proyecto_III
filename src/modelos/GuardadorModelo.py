# ============================================================
# GUARDADOR DEL MODELO DE MACHINE LEARNING
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Esta clase contiene las operaciones necesarias para:
# 1. Crear la carpeta de modelos entrenados.
# 2. Guardar el Pipeline del mejor modelo.
# 3. Cargar nuevamente el Pipeline guardado.
# 4. Guardar las metricas finales en formato JSON.
# 5. Guardar los mejores hiperparametros.
# 6. Comprobar que los archivos fueron creados.
#
# El Pipeline incluye:
# - Preparacion de variables numericas.
# - Codificacion de variables categoricas.
# - Modelo de clasificacion entrenado.
# ============================================================

import os
import json
import joblib


# ============================================================
# CLASE GUARDADORMODELO
#
# Esta clase guarda y recupera el modelo final del proyecto.
# ============================================================

class GuardadorModelo:

    # --------------------------------------------------------
    # CONSTRUCTOR
    #
    # Localiza la carpeta principal del proyecto y crea
    # una carpeta para guardar los modelos entrenados.
    # --------------------------------------------------------

    def __init__(self):
        """
        Define la carpeta donde se guardaran el modelo,
        las metricas y los hiperparametros.
        """

        # Obtener la ruta completa de este archivo
        ruta_archivo = os.path.abspath(__file__)

        # Obtener la carpeta src/modelos
        carpeta_modelos = os.path.dirname(
            ruta_archivo
        )

        # Subir desde src/modelos hasta src
        carpeta_src = os.path.dirname(
            carpeta_modelos
        )

        # Subir desde src hasta la carpeta principal
        carpeta_proyecto = os.path.dirname(
            carpeta_src
        )

        # Crear la ruta de salida
        self.ruta_modelos = os.path.join(
            carpeta_proyecto,
            "modelos_entrenados"
        )

        # Crear la carpeta si no existe
        os.makedirs(
            self.ruta_modelos,
            exist_ok=True
        )

    # --------------------------------------------------------
    # METODO: GUARDAR MODELO
    #
    # Guarda el Pipeline completo utilizando Joblib.
    # --------------------------------------------------------

    def guardar_modelo(
            self,
            modelo,
            nombre_archivo=(
                "modelo_gravedad_accidentes.joblib"
            )
    ):
        """
        Guarda el Pipeline entrenado en formato Joblib.

        Parametros:
            modelo: Pipeline entrenado que se desea guardar.
            nombre_archivo: nombre del archivo generado.

        Retorna:
            Ruta completa del modelo guardado.
        """

        if modelo is None:
            raise ValueError(
                "El modelo no puede ser None."
            )

        # Construir la ruta completa
        ruta_completa = os.path.join(
            self.ruta_modelos,
            nombre_archivo
        )

        # Guardar el Pipeline completo
        joblib.dump(
            modelo,
            ruta_completa
        )

        print("\nModelo guardado correctamente en:")

        print(ruta_completa)

        return ruta_completa

    # --------------------------------------------------------
    # METODO: CARGAR MODELO
    #
    # Recupera un Pipeline previamente guardado.
    # --------------------------------------------------------

    def cargar_modelo(
            self,
            nombre_archivo=(
                "modelo_gravedad_accidentes.joblib"
            )
    ):
        """
        Carga un Pipeline guardado en formato Joblib.

        Parametro:
            nombre_archivo: nombre del modelo guardado.

        Retorna:
            Pipeline entrenado.
        """

        # Construir la ruta completa
        ruta_completa = os.path.join(
            self.ruta_modelos,
            nombre_archivo
        )

        # Comprobar que el archivo exista
        if not os.path.exists(ruta_completa):
            raise FileNotFoundError(
                f"No se encontro el modelo: "
                f"{ruta_completa}"
            )

        # Cargar el Pipeline
        modelo = joblib.load(
            ruta_completa
        )

        print("\nModelo cargado correctamente desde:")

        print(ruta_completa)

        return modelo

    # --------------------------------------------------------
    # METODO AUXILIAR: CONVERTIR VALORES
    #
    # Convierte valores especiales de NumPy en tipos
    # normales de Python para poder guardarlos como JSON.
    # --------------------------------------------------------

    @staticmethod
    def _convertir_valor(valor):
        """
        Convierte un valor en un tipo compatible con JSON.

        Parametro:
            valor: dato que se desea convertir.

        Retorna:
            Valor compatible con JSON.
        """

        # Convertir diccionarios de forma recursiva
        if isinstance(valor, dict):

            return {
                str(clave): GuardadorModelo._convertir_valor(
                    contenido
                )
                for clave, contenido in valor.items()
            }

        # Convertir listas y tuplas
        if isinstance(valor, (list, tuple)):

            return [
                GuardadorModelo._convertir_valor(
                    contenido
                )
                for contenido in valor
            ]

        # Convertir valores numericos especiales
        if hasattr(valor, "item"):

            return valor.item()

        return valor

    # --------------------------------------------------------
    # METODO: GUARDAR METRICAS
    #
    # Guarda las metricas finales del modelo seleccionado.
    # --------------------------------------------------------

    def guardar_metricas(
            self,
            nombre_modelo,
            metricas,
            nombre_archivo="metricas_modelo.json"
    ):
        """
        Guarda las metricas finales en un archivo JSON.

        Parametros:
            nombre_modelo: nombre del modelo seleccionado.
            metricas: diccionario con las metricas.
            nombre_archivo: nombre del archivo generado.

        Retorna:
            Ruta completa del archivo JSON.
        """

        if not isinstance(metricas, dict):
            raise TypeError(
                "Las metricas deben estar en un diccionario."
            )

        # Preparar la informacion que se guardara
        contenido = {
            "modelo_seleccionado": nombre_modelo,
            "metricas": self._convertir_valor(
                metricas
            ),
            "criterio_principal": (
                "Recall de accidentes graves"
            ),
            "clase_positiva": {
                "valor": 1,
                "descripcion": (
                    "Con muertos o graves"
                )
            },
            "clase_negativa": {
                "valor": 0,
                "descripcion": (
                    "Solo heridos leves"
                )
            }
        }

        # Construir la ruta completa
        ruta_completa = os.path.join(
            self.ruta_modelos,
            nombre_archivo
        )

        # Guardar el archivo JSON
        with open(
                ruta_completa,
                "w",
                encoding="utf-8"
        ) as archivo:

            json.dump(
                contenido,
                archivo,
                ensure_ascii=False,
                indent=4
            )

        print("\nMetricas guardadas correctamente en:")

        print(ruta_completa)

        return ruta_completa

    # --------------------------------------------------------
    # METODO: GUARDAR HIPERPARAMETROS
    #
    # Guarda los mejores parametros encontrados
    # durante la validacion cruzada.
    # --------------------------------------------------------

    def guardar_hiperparametros(
            self,
            nombre_modelo,
            hiperparametros,
            nombre_archivo=(
                "hiperparametros_modelo.json"
            )
    ):
        """
        Guarda los hiperparametros en formato JSON.

        Parametros:
            nombre_modelo: nombre del modelo seleccionado.
            hiperparametros: diccionario de parametros.
            nombre_archivo: nombre del archivo generado.

        Retorna:
            Ruta completa del archivo JSON.
        """

        if not isinstance(hiperparametros, dict):
            raise TypeError(
                "Los hiperparametros deben estar "
                "en un diccionario."
            )

        # Preparar la informacion
        contenido = {
            "modelo_seleccionado": nombre_modelo,
            "hiperparametros": self._convertir_valor(
                hiperparametros
            )
        }

        # Construir la ruta completa
        ruta_completa = os.path.join(
            self.ruta_modelos,
            nombre_archivo
        )

        # Guardar el archivo
        with open(
                ruta_completa,
                "w",
                encoding="utf-8"
        ) as archivo:

            json.dump(
                contenido,
                archivo,
                ensure_ascii=False,
                indent=4
            )

        print(
            "\nHiperparametros guardados correctamente en:"
        )

        print(ruta_completa)

        return ruta_completa

    # --------------------------------------------------------
    # METODO: COMPROBAR ARCHIVO
    #
    # Comprueba que un archivo exista y tenga contenido.
    # --------------------------------------------------------

    @staticmethod
    def comprobar_archivo(ruta_archivo):
        """
        Comprueba la existencia y tamaño de un archivo.

        Parametro:
            ruta_archivo: ruta del archivo que se comprobara.

        Retorna:
            Diccionario con los resultados.
        """

        archivo_existe = os.path.exists(
            ruta_archivo
        )

        if archivo_existe:

            tamanio_bytes = os.path.getsize(
                ruta_archivo
            )

        else:

            tamanio_bytes = 0

        resultado = {
            "existe": archivo_existe,
            "tamanio_bytes": tamanio_bytes,
            "tiene_contenido": tamanio_bytes > 0
        }

        return resultado