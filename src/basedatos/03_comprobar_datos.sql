/* ============================================================
   COMPROBACION DE LOS DATOS
   Proyecto: Prediccion de la gravedad de accidentes de transito

   Este script comprueba:
   1. La cantidad total de registros.
   2. La distribucion de la gravedad.
   3. La relacion entre numero y nombre del dia.
   4. La relacion entre numero y nombre del mes.
   5. Los primeros registros almacenados.
   ============================================================ */


/* ------------------------------------------------------------
   PASO 1: SELECCIONAR LA BASE DE DATOS
   ------------------------------------------------------------ */

USE AccidentesTransitoCR;
GO


/* ------------------------------------------------------------
   PASO 2: CONTAR TODOS LOS REGISTROS
   ------------------------------------------------------------ */

SELECT
    COUNT(*) AS total_registros
FROM dbo.accidentes;
GO


/* ------------------------------------------------------------
   PASO 3: CONTAR LOS REGISTROS POR GRAVEDAD
   ------------------------------------------------------------ */

SELECT
    gravedad,
    clase_accidente,
    COUNT(*) AS cantidad
FROM dbo.accidentes
GROUP BY
    gravedad,
    clase_accidente
ORDER BY
    gravedad;
GO


/* ------------------------------------------------------------
   PASO 4: COMPROBAR LOS DIAS
   ------------------------------------------------------------ */

SELECT DISTINCT
    dia_numero,
    dia
FROM dbo.accidentes
ORDER BY
    dia_numero;
GO


/* ------------------------------------------------------------
   PASO 5: COMPROBAR LOS MESES
   ------------------------------------------------------------ */

SELECT DISTINCT
    mes_numero,
    mes
FROM dbo.accidentes
ORDER BY
    mes_numero;
GO


/* ------------------------------------------------------------
   PASO 6: MOSTRAR LOS PRIMEROS 10 REGISTROS
   ------------------------------------------------------------ */

SELECT TOP 10
    id_accidente,
    clase_accidente,
    tipo_accidente,
    anio,
    hora,
    provincia,
    canton,
    distrito,
    estado_tiempo,
    dia_numero,
    dia,
    mes_numero,
    mes,
    gravedad
FROM dbo.accidentes
ORDER BY
    id_accidente;
GO