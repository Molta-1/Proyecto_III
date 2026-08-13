/* ============================================================
   CREACIÓN DE LA BASE DE DATOS
   Proyecto: Predicción de la gravedad de accidentes de tránsito

   Este script:
   1. Comprueba si la base de datos ya existe.
   2. Crea la base solamente si todavía no existe.
   3. Selecciona la base para trabajar con ella.
   ============================================================ */


/* ------------------------------------------------------------
   PASO 1: CREAR LA BASE DE DATOS
   ------------------------------------------------------------ */

IF DB_ID('AccidentesTransitoCR') IS NULL
BEGIN
    CREATE DATABASE AccidentesTransitoCR;

    PRINT 'Base de datos creada correctamente.';
END
ELSE
BEGIN
    PRINT 'La base de datos ya existe.';
END;
GO


/* ------------------------------------------------------------
   PASO 2: SELECCIONAR LA BASE DE DATOS
   ------------------------------------------------------------ */

USE AccidentesTransitoCR;
GO


/* ------------------------------------------------------------
   PASO 3: MOSTRAR LA BASE DE DATOS ACTUAL
   ------------------------------------------------------------ */

SELECT DB_NAME() AS base_datos_actual;
GO