/* ============================================================
   CREACION DE LA TABLA CLIMATICA
   Proyecto: Prediccion de la gravedad de accidentes de transito

   Este script:
   1. Selecciona la base de datos del proyecto.
   2. Comprueba si la tabla climatica ya existe.
   3. Crea la tabla solamente si no existe.
   4. Valida los años y meses almacenados.
   5. Evita duplicar una provincia, año y mes.
   ============================================================ */


/* ------------------------------------------------------------
   PASO 1: SELECCIONAR LA BASE DE DATOS
   ------------------------------------------------------------ */

USE AccidentesTransitoCR;
GO


/* ------------------------------------------------------------
   PASO 2: CREAR LA TABLA CLIMATICA
   ------------------------------------------------------------ */

IF OBJECT_ID('dbo.clima_mensual', 'U') IS NULL
BEGIN

    CREATE TABLE dbo.clima_mensual
    (
        /* Llave primaria automatica */
        id_clima INT IDENTITY(1,1) NOT NULL,

        /* Ubicacion y periodo */
        provincia NVARCHAR(50) NOT NULL,
        anio INT NOT NULL,
        mes_numero TINYINT NOT NULL,
        mes NVARCHAR(20) NOT NULL,

        /* Indicadores climaticos mensuales */
        precipitacion_total_mm DECIMAL(10,2) NOT NULL,
        precipitacion_promedio_mm DECIMAL(10,2) NOT NULL,
        precipitacion_maxima_mm DECIMAL(10,2) NOT NULL,
        dias_con_lluvia TINYINT NOT NULL,

        /* Llave primaria */
        CONSTRAINT PK_clima_mensual
            PRIMARY KEY (id_clima),

        /* Evitar registros mensuales duplicados */
        CONSTRAINT UQ_clima_provincia_anio_mes
            UNIQUE (
                provincia,
                anio,
                mes_numero
            ),

        /* Validar el periodo del proyecto */
        CONSTRAINT CK_clima_anio
            CHECK (anio BETWEEN 2018 AND 2024),

        /* Validar el número del mes */
        CONSTRAINT CK_clima_mes_numero
            CHECK (mes_numero BETWEEN 1 AND 12),

        /* Validar la cantidad mensual de días con lluvia */
        CONSTRAINT CK_clima_dias_lluvia
            CHECK (dias_con_lluvia BETWEEN 0 AND 31),

        /* Evitar precipitaciones negativas */
        CONSTRAINT CK_clima_precipitacion_total
            CHECK (precipitacion_total_mm >= 0),

        CONSTRAINT CK_clima_precipitacion_promedio
            CHECK (precipitacion_promedio_mm >= 0),

        CONSTRAINT CK_clima_precipitacion_maxima
            CHECK (precipitacion_maxima_mm >= 0)
    );

    PRINT 'Tabla clima_mensual creada correctamente.';

END
ELSE
BEGIN

    PRINT 'La tabla clima_mensual ya existe.';

END;
GO


/* ------------------------------------------------------------
   PASO 3: COMPROBAR QUE LA TABLA EXISTE
   ------------------------------------------------------------ */

SELECT
    TABLE_SCHEMA AS esquema,
    TABLE_NAME AS nombre_tabla
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'dbo'
AND TABLE_NAME = 'clima_mensual';
GO


/* ------------------------------------------------------------
   PASO 4: MOSTRAR LA ESTRUCTURA DE LA TABLA
   ------------------------------------------------------------ */

SELECT
    ORDINAL_POSITION AS posicion,
    COLUMN_NAME AS columna,
    DATA_TYPE AS tipo_dato,
    NUMERIC_PRECISION AS precision_numerica,
    NUMERIC_SCALE AS decimales,
    CHARACTER_MAXIMUM_LENGTH AS longitud_maxima,
    IS_NULLABLE AS permite_nulos
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
AND TABLE_NAME = 'clima_mensual'
ORDER BY ORDINAL_POSITION;
GO