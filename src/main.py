# Archivo donde se va a ejecutar el código

import os
from datos.GestorDatos import GestorDatos  # Ajusta según el nombre de tu script


NOMBRE_PDF_LOCAL = "Anuario_2024.pdf"

gestor_datos = GestorDatos()
# Se instancia la clase para asegurar la existencia de "data/raw


print("Tablas desde el Archivo Local")
gestor_datos.extraer_todas_las_tablas_dinamicas(NOMBRE_PDF_LOCAL)
print("Fin del Proceso")
