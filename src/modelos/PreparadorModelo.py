# ============================================================
# PREPARADOR DE DATOS PARA MACHINE LEARNING
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Esta clase contiene las operaciones necesarias para:
# 1. Relacionar los accidentes con el clima mensual.
# 2. Seleccionar las variables predictoras.
# 3. Separar las variables X y la variable objetivo y.
# 4. Dividir los datos en entrenamiento y prueba.
# 5. Mantener la proporcion de accidentes leves y graves.
# 6. Preparar variables numericas y categoricas.
#
# IMPORTANTE:
# Esta clase todavia no entrena modelos.
# ============================================================

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


# ============================================================
# CLASE PREPARADORMODELO
#
# Esta clase prepara los datos antes de entrenar
# los algoritmos de clasificacion.
# ============================================================

class PreparadorModelo:

    # --------------------------------------------------------
    # CONSTRUCTOR
    #
    # Define las variables que se utilizaran en el modelo.
    # --------------------------------------------------------

    def __init__(self):
        """
        Define la variable objetivo y las variables predictoras.
        """

        # Variable que el modelo intentara predecir
        self.variable_objetivo = "gravedad"

        # Variables numericas
        self.variables_numericas = [
            "anio",
            "dia_numero",
            "mes_numero",
            "precipitacion_total_mm",
            "precipitacion_promedio_mm",
            "precipitacion_maxima_mm",
            "dias_con_lluvia"
        ]

        # Variables categoricas
        self.variables_categoricas = [
            "tipo_accidente",
            "hora_recodificada",
            "provincia",
            "zona",
            "calzada_vertical",
            "calzada_horizontal",
            "tipo_calzada",
            "tipo_circulacion",
            "estado_tiempo",
            "estado_calzada",
            "region_mideplan",
            "tipo_ruta",
            "dia",
            "mes"
        ]

        # Unir todas las variables predictoras
        self.variables_predictoras = (
            self.variables_numericas
            + self.variables_categoricas
        )

        # El preprocesador se creara posteriormente
        self.preprocesador = None

    # --------------------------------------------------------
    # METODO AUXILIAR: VALIDAR DATAFRAME
    #
    # Comprueba que los datos recibidos sean validos.
    # --------------------------------------------------------

    @staticmethod
    def _validar_dataframe(datos, nombre):
        """
        Comprueba que un objeto sea un DataFrame con datos.

        Parametros:
            datos: objeto que se desea comprobar.
            nombre: nombre utilizado en los mensajes de error.
        """

        if not isinstance(datos, pd.DataFrame):
            raise TypeError(
                f"{nombre} debe ser un DataFrame de Pandas."
            )

        if datos.empty:
            raise ValueError(
                f"{nombre} esta vacio."
            )

    # --------------------------------------------------------
    # METODO: RELACIONAR ACCIDENTES Y CLIMA
    #
    # Agrega los indicadores climaticos mensuales
    # a cada accidente mediante provincia, año y mes.
    # --------------------------------------------------------

    def relacionar_con_clima(
            self,
            datos_accidentes,
            datos_clima
    ):
        """
        Relaciona los accidentes con el clima mensual.

        Parametros:
            datos_accidentes: DataFrame limpio de accidentes.
            datos_clima: DataFrame con el resumen mensual.

        Retorna:
            DataFrame de accidentes con variables climaticas.
        """

        self._validar_dataframe(
            datos_accidentes,
            "El DataFrame de accidentes"
        )

        self._validar_dataframe(
            datos_clima,
            "El DataFrame climatico"
        )

        # Crear copias para proteger los datos originales
        accidentes = datos_accidentes.copy()
        clima = datos_clima.copy()

        # Columnas necesarias para realizar la union
        llaves_union = [
            "provincia",
            "anio",
            "mes_numero"
        ]

        # Indicadores climaticos que se agregaran
        columnas_clima = [
            "provincia",
            "anio",
            "mes_numero",
            "precipitacion_total_mm",
            "precipitacion_promedio_mm",
            "precipitacion_maxima_mm",
            "dias_con_lluvia"
        ]

        # Comprobar las columnas de union
        for columna in llaves_union:

            if columna not in accidentes.columns:
                raise ValueError(
                    "Falta la columna "
                    f"{columna} en los accidentes."
                )

            if columna not in clima.columns:
                raise ValueError(
                    "Falta la columna "
                    f"{columna} en el clima."
                )

        # Comprobar los indicadores climaticos
        columnas_faltantes_clima = [
            columna
            for columna in columnas_clima
            if columna not in clima.columns
        ]

        if columnas_faltantes_clima:
            raise ValueError(
                "Faltan columnas climaticas: "
                f"{columnas_faltantes_clima}"
            )

        # Seleccionar solamente las columnas necesarias
        clima_modelo = clima[columnas_clima].copy()

        # Comprobar que no existan meses climaticos duplicados
        duplicados_clima = clima_modelo.duplicated(
            subset=llaves_union
        ).sum()

        if duplicados_clima > 0:
            raise ValueError(
                "El resumen climatico contiene "
                f"{duplicados_clima} combinaciones duplicadas."
            )

        # Relacionar cada accidente con su contexto climatico
        datos_modelo = accidentes.merge(
            clima_modelo,
            on=llaves_union,
            how="left"
        )

        # Comprobar los indicadores climaticos vacios
        indicadores_clima = [
            "precipitacion_total_mm",
            "precipitacion_promedio_mm",
            "precipitacion_maxima_mm",
            "dias_con_lluvia"
        ]

        vacios_clima = (
            datos_modelo[indicadores_clima]
            .isna()
            .sum()
            .sum()
        )

        if vacios_clima > 0:
            raise ValueError(
                "La relacion entre accidentes y clima "
                f"genero {vacios_clima} valores vacios."
            )

        print(
            "Accidentes y clima relacionados correctamente."
        )

        print(
            f"Filas despues de la relacion: "
            f"{datos_modelo.shape[0]}"
        )

        print(
            f"Columnas despues de la relacion: "
            f"{datos_modelo.shape[1]}"
        )

        return datos_modelo

    # --------------------------------------------------------
    # METODO: SEPARAR VARIABLES
    #
    # Separa las variables predictoras X
    # y la variable objetivo y.
    # --------------------------------------------------------

    def separar_variables(self, datos):
        """
        Separa las variables predictoras y la gravedad.

        Parametro:
            datos: DataFrame relacionado con clima.

        Retorna:
            X: variables predictoras.
            y: variable objetivo gravedad.
        """

        self._validar_dataframe(
            datos,
            "El DataFrame para el modelo"
        )

        # Comprobar la variable objetivo
        if self.variable_objetivo not in datos.columns:
            raise ValueError(
                "No se encontro la variable objetivo gravedad."
            )

        # Comprobar las variables predictoras
        variables_faltantes = [
            variable
            for variable in self.variables_predictoras
            if variable not in datos.columns
        ]

        if variables_faltantes:
            raise ValueError(
                "Faltan variables predictoras: "
                f"{variables_faltantes}"
            )

        # Crear X con las variables predictoras
        X = datos[
            self.variables_predictoras
        ].copy()

        # Crear y con la variable objetivo
        y = datos[
            self.variable_objetivo
        ].astype(int).copy()

        # Comprobar que gravedad contenga solamente 0 y 1
        valores_objetivo = sorted(
            y.unique().tolist()
        )

        if valores_objetivo != [0, 1]:
            raise ValueError(
                "La variable gravedad debe contener "
                "solamente los valores 0 y 1."
            )

        print("\nVariables separadas correctamente.")

        print(
            f"Filas de X: "
            f"{X.shape[0]}"
        )

        print(
            f"Columnas de X: "
            f"{X.shape[1]}"
        )

        print(
            f"Filas de y: "
            f"{y.shape[0]}"
        )

        return X, y

    # --------------------------------------------------------
    # METODO: DIVIDIR DATOS
    #
    # Divide el conjunto en 80 % entrenamiento
    # y 20 % prueba utilizando estratificacion.
    # --------------------------------------------------------

    def dividir_datos(
            self,
            X,
            y,
            tamanio_prueba=0.20,
            semilla=42
    ):
        """
        Divide los datos en entrenamiento y prueba.

        Parametros:
            X: variables predictoras.
            y: variable objetivo.
            tamanio_prueba: proporcion reservada para prueba.
            semilla: valor para reproducir la division.

        Retorna:
            X_entrenamiento
            X_prueba
            y_entrenamiento
            y_prueba
        """

        if len(X) != len(y):
            raise ValueError(
                "X y y deben tener la misma cantidad de filas."
            )

        if not 0 < tamanio_prueba < 1:
            raise ValueError(
                "El tamaño de prueba debe estar entre 0 y 1."
            )

        # Dividir los datos conservando la proporcion de clases
        (
            X_entrenamiento,
            X_prueba,
            y_entrenamiento,
            y_prueba
        ) = train_test_split(
            X,
            y,
            test_size=tamanio_prueba,
            random_state=semilla,
            stratify=y
        )

        print("\nDivision de datos terminada.")

        print(
            f"Filas de entrenamiento: "
            f"{X_entrenamiento.shape[0]}"
        )

        print(
            f"Filas de prueba: "
            f"{X_prueba.shape[0]}"
        )

        return (
            X_entrenamiento,
            X_prueba,
            y_entrenamiento,
            y_prueba
        )

    # --------------------------------------------------------
    # METODO: CREAR PREPROCESADOR
    #
    # Las variables numericas se escalan.
    # Las variables categoricas se convierten en columnas 0 y 1.
    # --------------------------------------------------------

    def crear_preprocesador(self):
        """
        Crea el preprocesamiento para el modelo.

        Retorna:
            ColumnTransformer con los pasos de preparacion.
        """

        # Proceso para las variables numericas
        proceso_numerico = Pipeline(
            steps=[
                (
                    "completar_vacios",
                    SimpleImputer(
                        strategy="median"
                    )
                ),
                (
                    "escalar",
                    StandardScaler()
                )
            ]
        )

        # Proceso para las variables categoricas
        proceso_categorico = Pipeline(
            steps=[
                (
                    "completar_vacios",
                    SimpleImputer(
                        strategy="most_frequent"
                    )
                ),
                (
                    "codificar",
                    OneHotEncoder(
                        handle_unknown="ignore"
                    )
                )
            ]
        )

        # Combinar ambos procesos
        self.preprocesador = ColumnTransformer(
            transformers=[
                (
                    "numericas",
                    proceso_numerico,
                    self.variables_numericas
                ),
                (
                    "categoricas",
                    proceso_categorico,
                    self.variables_categoricas
                )
            ]
        )

        print(
            "\nPreprocesador creado correctamente."
        )

        return self.preprocesador

    # --------------------------------------------------------
    # METODO: OBTENER DISTRIBUCION
    #
    # Calcula la cantidad y el porcentaje de cada clase.
    # --------------------------------------------------------

    @staticmethod
    def obtener_distribucion(y):
        """
        Calcula la distribucion de una variable objetivo.

        Parametro:
            y: serie con valores 0 y 1.

        Retorna:
            DataFrame con cantidad y porcentaje.
        """

        resultado = (
            y
            .value_counts()
            .sort_index()
            .rename_axis("gravedad")
            .reset_index(name="cantidad")
        )

        resultado["porcentaje"] = (
            resultado["cantidad"]
            / resultado["cantidad"].sum()
            * 100
        ).round(2)

        return resultado