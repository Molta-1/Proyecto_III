import os # Librería que permite interración con el sistema operativo
import pandas as pd # Librería para manejo de datos

from datos.GestorDatos import GestorDatos
from api.ClienteAPI import ClienteAPI
from basedatos.GestorBaseDatos import GestorBaseDatos
from eda.ProcesadorEDA import ProcesadorEDA
from visualizacion.MapaAccidentes import MapaAccidentes
from modelos.PreparadorModelo import PreparadorModelo
from modelos.EntrenadorModelos import EntrenadorModelos
from modelos.GuardadorModelo import GuardadorModelo
# Llamado de las distintas clases del proyecto


def main():
    # Sección 1: Procesamiento de Accidentes
    print("Procesamiento de los Accidentes") # Texto meramente informativo, para indicar inicio de la sección

    gestor_datos = GestorDatos()
    # Instancia el gestor encargado de cargar, limpiar y guardar datos de accidentes


    datos_originales = gestor_datos.cargar_csv(
        "accidentes_victimas_2018_2024.csv"
    )
    # Carga el archivo CSV con los datos crudos de accidentes

    print("\nArchivo original cargado correctamente.")

    print(
        f"Cantidad de filas originales: "
        f"{datos_originales.shape[0]}"
    )

    print(
        f"Cantidad de columnas originales: "
        f"{datos_originales.shape[1]}"
    )


    datos_accidentes = gestor_datos.limpiar_datos(
        datos_originales
    )
    # Aplica las reglas de limpieza y transformacion a los datos originales

    print("\nDimensiones despues de la limpieza:")

    print(
        f"Cantidad de filas limpias: "
        f"{datos_accidentes.shape[0]}"
    )

    print(
        f"Cantidad de columnas limpias: "
        f"{datos_accidentes.shape[1]}"
    )


    valores_gravedad = sorted(
        datos_accidentes["gravedad"]
        .astype(int)
        .unique()
        .tolist()
    )
    # Obtiene y ordena los valores unicos de la variable objetivo gravedad

    print("\nValores de gravedad encontrados:")
    print(valores_gravedad)

    print("\nDistribucion de la gravedad:")

    print(
        datos_accidentes["gravedad"]
        .value_counts()
        .sort_index()
    )


    gestor_datos.guardar_csv(
        datos_accidentes,
        "accidentes_victimas_limpio.csv"
    )
    # Guarda el dataset limpio en un nuevo archivo CSV


    accidentes_comprobacion = (
        gestor_datos.cargar_csv_procesado(
            "accidentes_victimas_limpio.csv"
        )
    )
    # Vuelve a cargar el archivo procesado para verificar su integridades

    print("\nComprobacion del archivo de accidentes:")

    print(
        f"Filas recuperadas: "
        f"{accidentes_comprobacion.shape[0]}"
    )

    print(
        f"Columnas recuperadas: "
        f"{accidentes_comprobacion.shape[1]}"
    )


    columnas_temporales = [
        "dia_numero",
        "dia",
        "mes_numero",
        "mes"
    ]

    vacios_temporales = (
        accidentes_comprobacion[columnas_temporales]
        .isna()
        .sum()
    )
    # Evalua la presencia de valores nulos en las variables temporales

    print("\nValores vacios en las columnas de dia y mes:")

    print(vacios_temporales)



    # Sección 2: Procesamiento de Datos Climáticos (API)
    print("Procesamiento de Datos Climáticos (API)") # Texto meramente informativo, para indicar inicio de la sección

    cliente_api = ClienteAPI()
    # Instancia el cliente encargado de consultar y resumir la API climatica


    carpeta_src = os.path.dirname(
        os.path.abspath(__file__)
    )

    carpeta_proyecto = os.path.dirname(
        carpeta_src
    )

    ruta_clima = os.path.join(
        carpeta_proyecto,
        "data",
        "processed",
        "clima_mensual_2018_2024.csv"
    )
    # Construye la ruta absoluta hacia el archivo del resumen climatico


    if os.path.exists(ruta_clima):

        print(
            "\nEl archivo climatico ya existe."
        )

        print(
            "Se cargara el archivo sin consultar "
            "nuevamente la API."
        )

        resumen_clima = pd.read_csv(
            ruta_clima,
            sep=";",
            encoding="utf-8-sig"
        )
        # Carga el archivo climatico directamente desde el almacenamiento local

    else:

        print(
            "\nEl archivo climatico no existe."
        )

        print(
            "Se consultara la API historica de Open-Meteo."
        )

        datos_clima_diarios = (
            cliente_api.consultar_todas_provincias(
                fecha_inicio="2018-01-01",
                fecha_fin="2024-12-31"
            )
        )
        # Consulta los registros diarios de clima mediante la API


        resumen_clima = (
            cliente_api.resumir_clima_mensual(
                datos_clima_diarios
            )
        )
        # Agrupa y calcula el resumen de variables climaticas a nivel mensual


        cliente_api.guardar_resumen_climatico(
            resumen_mensual=resumen_clima,
            nombre_archivo="clima_mensual_2018_2024.csv"
        )
        # Guarda el resumen mensual generado en disco


    print("\nComprobacion del resumen climatico:")

    print(
        f"Filas climaticas: "
        f"{resumen_clima.shape[0]}"
    )

    print(
        f"Columnas climaticas: "
        f"{resumen_clima.shape[1]}"
    )

    valores_vacios_clima = resumen_clima.isna().sum()

    print("\nValores vacios en los datos climaticos:")

    print(valores_vacios_clima)


    provincias_clima = sorted(
        resumen_clima["provincia"]
        .unique()
        .tolist()
    )
    # Extrae el listado unico de provincias en la informacion climatica

    print("\nProvincias climaticas encontradas:")

    for provincia in provincias_clima:
        print(f"- {provincia}")


    anios_clima = sorted(
        resumen_clima["anio"]
        .unique()
        .tolist()
    )
    # Lista los años procesados dentro del resumen de clima

    print("\nAños climaticos encontrados:")
    print(anios_clima)


    if resumen_clima.shape[0] != 588:
        raise ValueError(
            "El resumen climatico no contiene "
            "los 588 registros esperados."
        )

    if resumen_clima.shape[1] != 8:
        raise ValueError(
            "El resumen climatico no contiene "
            "las 8 columnas esperadas."
        )

    if valores_vacios_clima.sum() > 0:
        raise ValueError(
            "El resumen climatico contiene valores vacios."
        )
    # Valida la coherencia de dimensiones y la ausencia de nulos en el clima

    print(
        "\nEl resumen climatico tiene las dimensiones "
        "correctas."
    )



    # Sección 3: Base de Datos

    print("Integración con SQL Server") # Texto meramente informativo, para indicar inicio de la sección

    gestor_bd = GestorBaseDatos()
    # Instancia el conector y manejador de la base de datos SQL Server

    try:

        nombre_base = gestor_bd.probar_conexion()
        # Verifica la conexion con el servidor SQL Server

        print("\nComprobacion de SQL Server:")

        print(
            f"Base de datos conectada: "
            f"{nombre_base}"
        )


        accidentes_insertados = (
            gestor_bd.insertar_accidentes(
                accidentes_comprobacion
            )
        )
        # Inserta los accidentes limpios en la tabla correspondiente de SQL Server

        if accidentes_insertados > 0:
            print(
                f"Accidentes insertados: "
                f"{accidentes_insertados}"
            )


        total_accidentes_sql = (
            gestor_bd.contar_registros()
        )
        # Cuenta los registros almacenados en la tabla de accidentes

        print("\nComprobacion de la tabla accidentes:")

        print(
            f"Registros almacenados: "
            f"{total_accidentes_sql}"
        )

        if total_accidentes_sql == len(
                accidentes_comprobacion
        ):
            print(
                "El CSV y la tabla accidentes "
                "coinciden correctamente."
            )
        else:
            print(
                "Advertencia: el CSV y la tabla accidentes "
                "no tienen la misma cantidad."
            )


        clima_insertado = (
            gestor_bd.insertar_clima_mensual(
                resumen_clima
            )
        )
        # Inserta la informacion del resumen climatico en SQL Server

        if clima_insertado > 0:
            print(
                f"Registros climaticos insertados: "
                f"{clima_insertado}"
            )


        total_clima_sql = (
            gestor_bd.contar_registros_clima()
        )
        # Obtiene la cantidad de filas cargadas en la tabla clima_mensual

        print("\nComprobacion de la tabla clima_mensual:")

        print(
            f"Registros almacenados: "
            f"{total_clima_sql}"
        )

        if total_clima_sql == len(resumen_clima):
            print(
                "El CSV climatico y la tabla clima_mensual "
                "coinciden correctamente."
            )
        else:
            print(
                "Advertencia: el CSV climatico y SQL Server "
                "no tienen la misma cantidad."
            )

        print("Resumen del Proceso") # Una última comprobación

        print(
            f"Accidentes procesados: "
            f"{len(accidentes_comprobacion)}"
        )

        print(
            f"Accidentes en SQL Server: "
            f"{total_accidentes_sql}"
        )

        print(
            f"Registros climaticos procesados: "
            f"{len(resumen_clima)}"
        )

        print(
            f"Registros climaticos en SQL Server: "
            f"{total_clima_sql}"
        )

        if (
            total_accidentes_sql
            == len(accidentes_comprobacion)
            and total_clima_sql
            == len(resumen_clima)
        ):
            print(
                "\nEl procesamiento de datos y la integracion "
                "con SQL Server finalizaron correctamente."
            )
        else:
            print(
                "\nAdvertencia: se encontraron diferencias "
                "en las cantidades almacenadas."
            )

    except Exception as error:

        print(
            "\nOcurrio un error durante la integracion "
            "con SQL Server:"
        )

        print(error)

    finally:

        gestor_bd.cerrar_conexion()
        # Garantiza el cierre de la conexion con SQL Server



    # Sección 4: Análsis Explotatorio de Datos (EDA)
    print("Análsis Explotatorio de Datos (EDA)") # Texto meramente informativo, para indicar inicio de la sección

    procesador_eda = ProcesadorEDA(accidentes_comprobacion)
    # Prepara el modulo para generar estadisticas explicativas y tablas de resumen


    resumen_general = procesador_eda.resumen_general()
    # Genera un resumen estadistico descriptivo basico sobre el conjunto de datos

    print("\nResumen general del dataset:")
    print(resumen_general)

    print("\nTipos de dato por columna:")
    print(procesador_eda.obtener_tipos_datos())

    print("\nValores vacios por columna:")
    print(procesador_eda.analizar_valores_vacios())


    tabla_por_anio = procesador_eda.accidentes_por_anio()
    tabla_por_mes = procesador_eda.accidentes_por_mes()
    tabla_por_dia = procesador_eda.accidentes_por_dia()
    tabla_por_hora = procesador_eda.accidentes_por_hora()
    tabla_por_provincia = procesador_eda.accidentes_por_provincia()
    tabla_por_tipo = procesador_eda.accidentes_por_tipo()
    tabla_distribucion_gravedad = (
        procesador_eda.distribucion_gravedad()
    )
    tabla_gravedad_provincia = (
        procesador_eda.gravedad_por_provincia()
    )
    tabla_dia_hora = procesador_eda.tabla_dia_hora()
    tabla_clima_accidentes = (
        procesador_eda.relacion_accidentes_clima(resumen_clima)
    )
    # Construye las aglomeraciones y tablas necesarias para el EDA

    print("\nAccidentes por provincia:")
    print(tabla_por_provincia)

    print("\nDistribucion de la gravedad:")
    print(tabla_distribucion_gravedad)

    print("\nPorcentaje de accidentes graves por provincia:")
    print(tabla_gravedad_provincia)


    print("Mapa Interactivo")
    mapa_accidentes = MapaAccidentes()

    ruta_mapa = mapa_accidentes.crear_mapa_provincias(
        tabla_gravedad_provincia
    )
    # Construye y exporta un archivo HTML con el mapa de severidad por provincia

    print(
        f"\nMapa interactivo generado en: "
        f"{ruta_mapa}"
    )


    # Sección 5: Modelado Predictivo

    print("Entrenamiento del Modelo Predictivo") # Texto meramente informativo, para indicar inicio de la sección

    preparador_modelo = PreparadorModelo()

    datos_modelo = preparador_modelo.relacionar_con_clima(
        accidentes_comprobacion,
        resumen_clima
    )
    # Relaciona el clima con los accidentes


    variables_predictoras, variable_objetivo = (
        preparador_modelo.separar_variables(datos_modelo)
    )
    # Separa las variables predictorias y las objetivo


    (
        X_entrenamiento,
        X_prueba,
        y_entrenamiento,
        y_prueba
    ) = preparador_modelo.dividir_datos(
        variables_predictoras,
        variable_objetivo
    )
    # Divide el modelo entre el entrenamiento y la prueba


    preprocesador = (
        preparador_modelo.crear_preprocesador()
    )
    # Selecciona el preprocesador del modelo


    entrenador_modelos = EntrenadorModelos(preprocesador)

    tabla_comparacion = entrenador_modelos.entrenar_todos(
        X_entrenamiento,
        y_entrenamiento,
        X_prueba,
        y_prueba
    )
    # Entrena y evalua todos los modelos configurados

    print("\nComparacion de los tres modelos:")
    print(tabla_comparacion)

    nombre_mejor_modelo, mejor_pipeline = (
        entrenador_modelos.seleccionar_mejor_modelo()
    )
    # Entrena, compara y selecciona el mejor modelo


    guardador_modelo = GuardadorModelo()

    ruta_modelo_guardado = guardador_modelo.guardar_modelo(
        mejor_pipeline
    )

    ruta_metricas_guardadas = (
        guardador_modelo.guardar_metricas(
            nombre_modelo=nombre_mejor_modelo,
            metricas=entrenador_modelos.resultados[
                nombre_mejor_modelo
            ]
        )
    )
    # Se guarda el mejor modelo y sus métricas

    comprobacion_modelo = guardador_modelo.comprobar_archivo(
        ruta_modelo_guardado
    )

    comprobacion_metricas = guardador_modelo.comprobar_archivo(
        ruta_metricas_guardadas
    )
    # Comprueba la existencia y estado de los archivos guardados

    print("\nComprobacion del modelo guardado:")
    print(comprobacion_modelo)

    print("\nComprobacion de las metricas guardadas:")
    print(comprobacion_metricas)

    print("Fin del Proceso")
    # Archivos generados (modelos entrenados)


if __name__ == "__main__":
    main()
# Solo se utiliza cuando se ejecuta, si el código se llama entonces este no toma acción