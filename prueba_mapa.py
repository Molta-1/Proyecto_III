# ============================================================
# PRUEBA DEL MAPA INTERACTIVO DE ACCIDENTES
# Proyecto: Prediccion de la gravedad de accidentes de transito
#
# Este archivo comprueba:
# 1. La carga del CSV procesado de accidentes.
# 2. El calculo de la gravedad por provincia.
# 3. La generacion del mapa interactivo.
# 4. La existencia del archivo HTML.
# 5. Que el archivo tenga contenido.
# 6. Que las siete provincias esten representadas.
#
# IMPORTANTE:
# Este archivo no modifica SQL Server.
# ============================================================

import os
import webbrowser
import pandas as pd

from src.eda.ProcesadorEDA import ProcesadorEDA
from src.visualizacion.MapaAccidentes import MapaAccidentes


# ============================================================
# FUNCION AUXILIAR: MOSTRAR TITULO
#
# Muestra un encabezado para organizar la salida.
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
# Carga los datos, genera el mapa provincial y comprueba
# el archivo HTML resultante.
# ============================================================

def main():
    """
    Genera y comprueba el mapa interactivo de accidentes.
    """

    # ========================================================
    # SECCION 1: CARGAR LOS DATOS
    # ========================================================

    mostrar_titulo("CARGA DE LOS DATOS DE ACCIDENTES")

    # --------------------------------------------------------
    # PASO 1: OBTENER LA CARPETA DEL PROYECTO
    # --------------------------------------------------------

    carpeta_proyecto = os.path.dirname(
        os.path.abspath(__file__)
    )

    # --------------------------------------------------------
    # PASO 2: CONSTRUIR LA RUTA DEL CSV PROCESADO
    # --------------------------------------------------------

    ruta_accidentes = os.path.join(
        carpeta_proyecto,
        "data",
        "processed",
        "accidentes_victimas_limpio.csv"
    )

    # --------------------------------------------------------
    # PASO 3: COMPROBAR QUE EL CSV EXISTA
    # --------------------------------------------------------

    if not os.path.exists(ruta_accidentes):
        raise FileNotFoundError(
            f"No se encontro el archivo de accidentes: "
            f"{ruta_accidentes}"
        )

    print("Archivo de accidentes encontrado correctamente.")
    print(ruta_accidentes)

    # --------------------------------------------------------
    # PASO 4: CARGAR EL CSV
    # --------------------------------------------------------

    datos_accidentes = pd.read_csv(
        ruta_accidentes,
        sep=";",
        encoding="utf-8-sig",
        low_memory=False
    )

    print("\nDatos de accidentes cargados correctamente.")

    print(
        f"Cantidad de filas: "
        f"{datos_accidentes.shape[0]}"
    )

    print(
        f"Cantidad de columnas: "
        f"{datos_accidentes.shape[1]}"
    )

    # ========================================================
    # SECCION 2: PREPARAR LOS DATOS DEL MAPA
    # ========================================================

    mostrar_titulo("PREPARACION DE LOS DATOS DEL MAPA")

    # --------------------------------------------------------
    # PASO 5: CREAR EL PROCESADOR EDA
    # --------------------------------------------------------

    procesador_eda = ProcesadorEDA(
        datos_accidentes
    )

    # --------------------------------------------------------
    # PASO 6: CALCULAR LA GRAVEDAD POR PROVINCIA
    # --------------------------------------------------------

    gravedad_provincia = (
        procesador_eda.gravedad_por_provincia()
    )

    print("Resumen provincial creado correctamente.")

    print("\nDatos utilizados para el mapa:")

    print(
        gravedad_provincia.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # PASO 7: COMPROBAR LA CANTIDAD DE PROVINCIAS
    # --------------------------------------------------------

    cantidad_provincias = (
        gravedad_provincia["provincia"].nunique()
    )

    print(
        f"\nCantidad de provincias encontradas: "
        f"{cantidad_provincias}"
    )

    if cantidad_provincias != 7:
        raise ValueError(
            "El resumen no contiene las siete provincias."
        )

    # --------------------------------------------------------
    # PASO 8: COMPROBAR EL TOTAL DE ACCIDENTES
    # --------------------------------------------------------

    total_mapa = int(
        gravedad_provincia[
            "total_accidentes"
        ].sum()
    )

    total_datos = len(datos_accidentes)

    print(
        f"Total de accidentes en el mapa: "
        f"{total_mapa}"
    )

    print(
        f"Total de accidentes en el CSV: "
        f"{total_datos}"
    )

    if total_mapa != total_datos:
        raise ValueError(
            "El total provincial no coincide con el CSV."
        )

    # ========================================================
    # SECCION 3: GENERAR EL MAPA
    # ========================================================

    mostrar_titulo("GENERACION DEL MAPA INTERACTIVO")

    # --------------------------------------------------------
    # PASO 9: CREAR EL OBJETO DEL MAPA
    # --------------------------------------------------------

    mapa_accidentes = MapaAccidentes()

    # --------------------------------------------------------
    # PASO 10: CREAR EL MAPA PROVINCIAL
    # --------------------------------------------------------

    ruta_mapa = (
        mapa_accidentes.crear_mapa_provincias(
            gravedad_provincia,
            nombre_archivo=(
                "11_mapa_accidentes_provincia.html"
            )
        )
    )

    # ========================================================
    # SECCION 4: COMPROBAR EL ARCHIVO HTML
    # ========================================================

    mostrar_titulo("COMPROBACION DEL ARCHIVO HTML")

    archivo_existe = os.path.exists(
        ruta_mapa
    )

    if archivo_existe:
        tamanio_bytes = os.path.getsize(
            ruta_mapa
        )
    else:
        tamanio_bytes = 0

    tiene_contenido = tamanio_bytes > 0

    nombre_correcto = (
        os.path.basename(ruta_mapa)
        == "11_mapa_accidentes_provincia.html"
    )

    print(f"Mapa generado: {ruta_mapa}")
    print(f"Existe: {archivo_existe}")
    print(f"Tamanio en bytes: {tamanio_bytes}")
    print(f"Tiene contenido: {tiene_contenido}")
    print(f"Nombre correcto: {nombre_correcto}")

    # ========================================================
    # SECCION 5: COMPROBACION FINAL
    # ========================================================

    mostrar_titulo("COMPROBACION FINAL DEL MAPA")

    mapa_correcto = (
        archivo_existe
        and tiene_contenido
        and nombre_correcto
        and cantidad_provincias == 7
        and total_mapa == total_datos
    )

    if mapa_correcto:
        print(
            "El mapa interactivo fue generado "
            "correctamente."
        )

        print(
            "\nEl archivo se encuentra en:"
        )

        print(ruta_mapa)

    else:
        print(
            "Advertencia: revise la generacion del mapa."
        )

        return

    # ========================================================
    # SECCION 6: ABRIR EL MAPA EN EL NAVEGADOR
    # ========================================================

    mostrar_titulo("APERTURA DEL MAPA")

    # Convertir la ruta local en una direccion compatible
    # con el navegador.
    direccion_mapa = "file:///" + ruta_mapa.replace(
        "\\",
        "/"
    )

    mapa_abierto = webbrowser.open(
        direccion_mapa
    )

    print(
        f"Solicitud de apertura enviada al navegador: "
        f"{mapa_abierto}"
    )

    print(
        "\nSi el navegador no se abre automaticamente, "
        "abra manualmente el archivo HTML."
    )


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
#
# Esta condicion ejecuta main() cuando el archivo
# se inicia directamente.
# ============================================================

if __name__ == "__main__":
    main()