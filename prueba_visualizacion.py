# ============================================================
# PRUEBA DE VISUALIZACION DE DATOS
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Este archivo comprueba:
# 1. La carga de los archivos procesados.
# 2. La creacion de las tablas necesarias para los graficos.
# 3. La generacion de los diez graficos principales.
# 4. La existencia de cada archivo PNG.
# 5. Que cada grafico tenga contenido.
#
# IMPORTANTE:
# Este archivo no modifica SQL Server.
# ============================================================

import os
import pandas as pd

from src.eda.ProcesadorEDA import ProcesadorEDA
from src.visualizacion.Visualizador import Visualizador


# ============================================================
# FUNCION AUXILIAR: MOSTRAR TITULO
#
# Muestra un encabezado para organizar la salida en consola.
# ============================================================

def mostrar_titulo(titulo):
    """
    Muestra un titulo organizado en la consola.

    Parametro:
        titulo: texto que se desea mostrar.
    """

    print("\n====================================================")
    print(titulo)
    print("====================================================")


# ============================================================
# FUNCION PRINCIPAL
#
# Carga los datos, realiza el EDA necesario y genera
# los diez graficos del proyecto.
# ============================================================

def main():
    """
    Genera y comprueba los graficos principales del proyecto.
    """

    # ========================================================
    # SECCION 1: CARGAR LOS ARCHIVOS PROCESADOS
    # ========================================================

    mostrar_titulo("CARGA DE LOS ARCHIVOS PROCESADOS")

    # --------------------------------------------------------
    # PASO 1: OBTENER LA CARPETA PRINCIPAL DEL PROYECTO
    # --------------------------------------------------------

    carpeta_proyecto = os.path.dirname(
        os.path.abspath(__file__)
    )

    # --------------------------------------------------------
    # PASO 2: CONSTRUIR LAS RUTAS DE LOS ARCHIVOS
    # --------------------------------------------------------

    ruta_accidentes = os.path.join(
        carpeta_proyecto,
        "data",
        "processed",
        "accidentes_victimas_limpio.csv"
    )

    ruta_clima = os.path.join(
        carpeta_proyecto,
        "data",
        "processed",
        "clima_mensual_2018_2024.csv"
    )

    # --------------------------------------------------------
    # PASO 3: COMPROBAR QUE LOS ARCHIVOS EXISTAN
    # --------------------------------------------------------

    if not os.path.exists(ruta_accidentes):
        raise FileNotFoundError(
            f"No se encontro el archivo de accidentes: "
            f"{ruta_accidentes}"
        )

    if not os.path.exists(ruta_clima):
        raise FileNotFoundError(
            f"No se encontro el archivo climatico: "
            f"{ruta_clima}"
        )

    print("Archivo de accidentes encontrado correctamente.")
    print(ruta_accidentes)

    print("\nArchivo climatico encontrado correctamente.")
    print(ruta_clima)

    # --------------------------------------------------------
    # PASO 4: CARGAR EL CSV DE ACCIDENTES
    # --------------------------------------------------------

    datos_accidentes = pd.read_csv(
        ruta_accidentes,
        sep=";",
        encoding="utf-8-sig",
        low_memory=False
    )

    print("\nDatos de accidentes cargados correctamente.")

    print(
        f"Filas de accidentes: "
        f"{datos_accidentes.shape[0]}"
    )

    print(
        f"Columnas de accidentes: "
        f"{datos_accidentes.shape[1]}"
    )

    # --------------------------------------------------------
    # PASO 5: CARGAR EL CSV CLIMATICO
    # --------------------------------------------------------

    datos_clima = pd.read_csv(
        ruta_clima,
        sep=";",
        encoding="utf-8-sig",
        low_memory=False
    )

    print("\nDatos climaticos cargados correctamente.")

    print(
        f"Filas climaticas: "
        f"{datos_clima.shape[0]}"
    )

    print(
        f"Columnas climaticas: "
        f"{datos_clima.shape[1]}"
    )

    # ========================================================
    # SECCION 2: CREAR LOS OBJETOS
    # ========================================================

    mostrar_titulo("CREACION DE LOS OBJETOS")

    procesador_eda = ProcesadorEDA(
        datos_accidentes
    )

    visualizador = Visualizador()

    print("ProcesadorEDA creado correctamente.")
    print("Visualizador creado correctamente.")

    print("\nCarpeta de salida de los graficos:")
    print(visualizador.ruta_graficos)

    # ========================================================
    # SECCION 3: CREAR LAS TABLAS PARA LOS GRAFICOS
    # ========================================================

    mostrar_titulo("CREACION DE LAS TABLAS PARA LOS GRAFICOS")

    por_anio = procesador_eda.accidentes_por_anio()

    por_provincia = (
        procesador_eda.accidentes_por_provincia()
    )

    distribucion_gravedad = (
        procesador_eda.distribucion_gravedad()
    )

    por_mes = procesador_eda.accidentes_por_mes()

    por_dia = procesador_eda.accidentes_por_dia()

    por_hora = procesador_eda.accidentes_por_hora()

    por_tipo = procesador_eda.accidentes_por_tipo()

    gravedad_provincia = (
        procesador_eda.gravedad_por_provincia()
    )

    tabla_dia_hora = procesador_eda.tabla_dia_hora()

    relacion_clima = (
        procesador_eda.relacion_accidentes_clima(
            datos_clima
        )
    )

    print("Las tablas del EDA fueron creadas correctamente.")

    # ========================================================
    # SECCION 4: GENERAR LOS GRAFICOS
    # ========================================================

    mostrar_titulo("GENERACION DE LOS GRAFICOS")

    # Lista donde se guardaran las rutas de los graficos
    rutas_graficos = []

    # --------------------------------------------------------
    # GRAFICO 1: ACCIDENTES POR AÑO
    # --------------------------------------------------------

    rutas_graficos.append(
        visualizador.grafico_accidentes_por_anio(
            por_anio
        )
    )

    # --------------------------------------------------------
    # GRAFICO 2: ACCIDENTES POR PROVINCIA
    # --------------------------------------------------------

    rutas_graficos.append(
        visualizador.grafico_accidentes_por_provincia(
            por_provincia
        )
    )

    # --------------------------------------------------------
    # GRAFICO 3: DISTRIBUCION DE GRAVEDAD
    # --------------------------------------------------------

    rutas_graficos.append(
        visualizador.grafico_distribucion_gravedad(
            distribucion_gravedad
        )
    )

    # --------------------------------------------------------
    # GRAFICO 4: ACCIDENTES POR MES
    # --------------------------------------------------------

    rutas_graficos.append(
        visualizador.grafico_accidentes_por_mes(
            por_mes
        )
    )

    # --------------------------------------------------------
    # GRAFICO 5: ACCIDENTES POR DIA
    # --------------------------------------------------------

    rutas_graficos.append(
        visualizador.grafico_accidentes_por_dia(
            por_dia
        )
    )

    # --------------------------------------------------------
    # GRAFICO 6: ACCIDENTES POR HORA
    # --------------------------------------------------------

    rutas_graficos.append(
        visualizador.grafico_accidentes_por_hora(
            por_hora
        )
    )

    # --------------------------------------------------------
    # GRAFICO 7: TIPOS DE ACCIDENTE
    # --------------------------------------------------------

    rutas_graficos.append(
        visualizador.grafico_tipos_accidente(
            por_tipo
        )
    )

    # --------------------------------------------------------
    # GRAFICO 8: GRAVEDAD POR PROVINCIA
    # --------------------------------------------------------

    rutas_graficos.append(
        visualizador.grafico_gravedad_por_provincia(
            gravedad_provincia
        )
    )

    # --------------------------------------------------------
    # GRAFICO 9: MAPA DE CALOR DE DIA Y HORA
    # --------------------------------------------------------

    rutas_graficos.append(
        visualizador.mapa_calor_dia_hora(
            tabla_dia_hora
        )
    )

    # --------------------------------------------------------
    # GRAFICO 10: CLIMA Y ACCIDENTES POR AÑO
    # --------------------------------------------------------

    rutas_graficos.append(
        visualizador.grafico_clima_accidentes_anual(
            relacion_clima
        )
    )

    # ========================================================
    # SECCION 5: COMPROBAR LOS ARCHIVOS GENERADOS
    # ========================================================

    mostrar_titulo("COMPROBACION DE LOS GRAFICOS")

    cantidad_esperada = 10
    cantidad_generada = len(rutas_graficos)

    print(
        f"Cantidad de graficos esperados: "
        f"{cantidad_esperada}"
    )

    print(
        f"Cantidad de rutas generadas: "
        f"{cantidad_generada}"
    )

    todos_existen = True
    todos_tienen_contenido = True

    for numero, ruta in enumerate(
            rutas_graficos,
            start=1
    ):

        archivo_existe = os.path.exists(ruta)

        if archivo_existe:
            tamanio_bytes = os.path.getsize(ruta)
        else:
            tamanio_bytes = 0

        tiene_contenido = tamanio_bytes > 0

        print(
            f"\nGrafico {numero}: "
            f"{os.path.basename(ruta)}"
        )

        print(
            f"Existe: "
            f"{archivo_existe}"
        )

        print(
            f"Tamanio en bytes: "
            f"{tamanio_bytes}"
        )

        print(
            f"Tiene contenido: "
            f"{tiene_contenido}"
        )

        if not archivo_existe:
            todos_existen = False

        if not tiene_contenido:
            todos_tienen_contenido = False

    # ========================================================
    # SECCION 6: COMPROBAR LOS NOMBRES ESPERADOS
    # ========================================================

    nombres_esperados = [
        "01_accidentes_por_anio.png",
        "02_accidentes_por_provincia.png",
        "03_distribucion_gravedad.png",
        "04_accidentes_por_mes.png",
        "05_accidentes_por_dia.png",
        "06_accidentes_por_hora.png",
        "07_tipos_accidente.png",
        "08_gravedad_por_provincia.png",
        "09_mapa_calor_dia_hora.png",
        "10_clima_accidentes_anual.png"
    ]

    nombres_generados = [
        os.path.basename(ruta)
        for ruta in rutas_graficos
    ]

    nombres_correctos = (
        nombres_generados == nombres_esperados
    )

    print("\nNombres de los archivos correctos:")
    print(nombres_correctos)

    # ========================================================
    # SECCION 7: COMPROBACION FINAL
    # ========================================================

    mostrar_titulo("COMPROBACION FINAL DE VISUALIZACION")

    if (
        cantidad_generada == cantidad_esperada
        and todos_existen
        and todos_tienen_contenido
        and nombres_correctos
    ):
        print(
            "Los diez graficos fueron generados "
            "correctamente."
        )

        print("\nLos graficos se encuentran en:")
        print(visualizador.ruta_graficos)

    else:
        print(
            "Advertencia: revise la generacion "
            "de los graficos."
        )


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
#
# Esta condicion ejecuta main() cuando este archivo
# se inicia directamente.
# ============================================================

if __name__ == "__main__":
    main()