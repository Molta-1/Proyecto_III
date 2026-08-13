# ============================================================
# PROGRAMA PRINCIPAL
# Proyecto: Predicción de la gravedad de accidentes de tránsito
#
# Este archivo coordina el proceso inicial del proyecto:
# 1. Crea un objeto de la clase GestorDatos.
# 2. Carga el CSV original.
# 3. Limpia los datos.
# 4. Muestra los resultados de la limpieza.
# 5. Guarda el archivo procesado.
# 6. Comprueba que el archivo se guardó correctamente.
# ============================================================

from datos.GestorDatos import GestorDatos


# ============================================================
# FUNCIÓN PRINCIPAL
#
# Ejecuta en orden las operaciones necesarias para cargar,
# limpiar, guardar y comprobar los datos de accidentes.
# ============================================================

def main():
    """
    Ejecuta el proceso principal de gestión de datos.
    """

    # --------------------------------------------------------
    # PASO 1: CREAR EL GESTOR DE DATOS
    # --------------------------------------------------------

    gestor = GestorDatos()

    # --------------------------------------------------------
    # PASO 2: CARGAR EL ARCHIVO CSV ORIGINAL
    # --------------------------------------------------------

    datos = gestor.cargar_csv(
        "accidentes_victimas_2018_2024.csv"
    )

    # Mostrar las dimensiones del archivo original
    print("Archivo cargado correctamente.")
    print(f"Cantidad de filas originales: {datos.shape[0]}")
    print(f"Cantidad de columnas originales: {datos.shape[1]}")

    # --------------------------------------------------------
    # PASO 3: REALIZAR LA LIMPIEZA INICIAL
    # --------------------------------------------------------

    datos_limpios = gestor.limpiar_datos(datos)

    # Mostrar las dimensiones después de la limpieza
    print(f"\nCantidad de filas limpias: {datos_limpios.shape[0]}")
    print(
        f"Cantidad de columnas limpias: "
        f"{datos_limpios.shape[1]}"
    )

    # --------------------------------------------------------
    # PASO 4: MOSTRAR LOS NOMBRES DE LAS COLUMNAS
    # --------------------------------------------------------

    print("\nNombres de las columnas limpias:")

    for columna in datos_limpios.columns:
        print(f"- {columna}")

    # --------------------------------------------------------
    # PASO 5: MOSTRAR LA DISTRIBUCIÓN DE LA GRAVEDAD
    # --------------------------------------------------------

    print("\nDistribución de la variable gravedad:")

    print(
        datos_limpios["gravedad"].value_counts(
            dropna=False
        )
    )

    # --------------------------------------------------------
    # PASO 6: GUARDAR EL ARCHIVO PROCESADO
    # --------------------------------------------------------

    gestor.guardar_csv(
        datos_limpios,
        "accidentes_victimas_limpio.csv"
    )

    # --------------------------------------------------------
    # PASO 7: VOLVER A CARGAR EL ARCHIVO PROCESADO
    # --------------------------------------------------------

    datos_comprobacion = gestor.cargar_csv_procesado(
        "accidentes_victimas_limpio.csv"
    )

    # --------------------------------------------------------
    # PASO 8: COMPROBAR EL ARCHIVO PROCESADO
    # --------------------------------------------------------

    print("\nComprobación del archivo procesado:")
    print(
        f"Filas recuperadas: "
        f"{datos_comprobacion.shape[0]}"
    )
    print(
        f"Columnas recuperadas: "
        f"{datos_comprobacion.shape[1]}"
    )

    # Convertir los valores de NumPy a números enteros normales
    # para mostrarlos de una forma más fácil de leer
    valores_gravedad = sorted(
        datos_comprobacion["gravedad"]
        .astype(int)
        .unique()
        .tolist()
    )

    print(f"Valores de gravedad: {valores_gravedad}")


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
#
# Esta condición ejecuta main() solamente cuando este archivo
# se inicia directamente.
# ============================================================

if __name__ == "__main__":
    main()