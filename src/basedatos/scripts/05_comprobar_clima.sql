/* ============================================================
   COMPROBACION DE LOS DATOS CLIMATICOS
   Proyecto: Prediccion de la gravedad de accidentes de transito

   Este script comprueba:
   1. La cantidad total de registros climaticos.
   2. Los registros por provincia.
   3. Los años disponibles.
   4. Los meses disponibles.
   5. Una muestra de los datos climaticos.
   6. La relacion mensual entre clima y accidentes.
   ============================================================ */


/* ------------------------------------------------------------
   PASO 1: SELECCIONAR LA BASE DE DATOS
   ------------------------------------------------------------ */

USE AccidentesTransitoCR;
GO


/* ------------------------------------------------------------
   PASO 2: CONTAR TODOS LOS REGISTROS CLIMATICOS
   ------------------------------------------------------------ */

SELECT
    COUNT(*) AS total_registros_climaticos
FROM dbo.clima_mensual;
GO


/* ------------------------------------------------------------
   PASO 3: CONTAR LOS REGISTROS POR PROVINCIA
   ------------------------------------------------------------ */

SELECT
    provincia,
    COUNT(*) AS cantidad_registros
FROM dbo.clima_mensual
GROUP BY
    provincia
ORDER BY
    provincia;
GO


/* ------------------------------------------------------------
   PASO 4: MOSTRAR LOS AÑOS DISPONIBLES
   ------------------------------------------------------------ */

SELECT DISTINCT
    anio
FROM dbo.clima_mensual
ORDER BY
    anio;
GO


/* ------------------------------------------------------------
   PASO 5: COMPROBAR LOS MESES
   ------------------------------------------------------------ */

SELECT DISTINCT
    mes_numero,
    mes
FROM dbo.clima_mensual
ORDER BY
    mes_numero;
GO


/* ------------------------------------------------------------
   PASO 6: MOSTRAR LOS PRIMEROS 15 REGISTROS
   ------------------------------------------------------------ */

SELECT TOP 15
    id_clima,
    provincia,
    anio,
    mes_numero,
    mes,
    precipitacion_total_mm,
    precipitacion_promedio_mm,
    precipitacion_maxima_mm,
    dias_con_lluvia
FROM dbo.clima_mensual
ORDER BY
    provincia,
    anio,
    mes_numero;
GO


/* ------------------------------------------------------------
   PASO 7: RESUMEN DE PRECIPITACION POR PROVINCIA
   ------------------------------------------------------------ */

SELECT
    provincia,
    ROUND(
        SUM(precipitacion_total_mm),
        2
    ) AS precipitacion_total_periodo_mm,

    ROUND(
        AVG(precipitacion_promedio_mm),
        2
    ) AS precipitacion_promedio_mensual_mm,

    MAX(
        precipitacion_maxima_mm
    ) AS maxima_precipitacion_diaria_mm,

    SUM(
        dias_con_lluvia
    ) AS dias_con_lluvia_periodo
FROM dbo.clima_mensual
GROUP BY
    provincia
ORDER BY
    provincia;
GO


/* ------------------------------------------------------------
   PASO 8: RELACIONAR ACCIDENTES Y CLIMA
   ------------------------------------------------------------ */

SELECT
    clima.provincia,
    clima.anio,
    clima.mes_numero,
    clima.mes,

    clima.precipitacion_total_mm,
    clima.precipitacion_promedio_mm,
    clima.dias_con_lluvia,

    COUNT(
        accidentes.id_accidente
    ) AS cantidad_accidentes,

    SUM(
        CASE
            WHEN accidentes.gravedad = 1 THEN 1
            ELSE 0
        END
    ) AS accidentes_graves

FROM dbo.clima_mensual AS clima

LEFT JOIN dbo.accidentes AS accidentes
    ON clima.provincia = accidentes.provincia
    AND clima.anio = accidentes.anio
    AND clima.mes_numero = accidentes.mes_numero

GROUP BY
    clima.provincia,
    clima.anio,
    clima.mes_numero,
    clima.mes,
    clima.precipitacion_total_mm,
    clima.precipitacion_promedio_mm,
    clima.dias_con_lluvia

ORDER BY
    clima.provincia,
    clima.anio,
    clima.mes_numero;
GO