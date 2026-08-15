/* ============================================================
   CREACION DE LA TABLA DE ACCIDENTES
   Proyecto: Prediccion de la gravedad de accidentes de transito

   Este script:
   1. Selecciona la base de datos del proyecto.
   2. Comprueba si la tabla ya existe.
   3. Crea la tabla solamente si no existe.
   4. Agrega una llave primaria automatica.
   5. Guarda por separado el numero y nombre del dia.
   6. Guarda por separado el numero y nombre del mes.
   7. Valida los valores de dia, mes y gravedad.
   ============================================================ */


/* ------------------------------------------------------------
   PASO 1: SELECCIONAR LA BASE DE DATOS
   ------------------------------------------------------------ */

USE AccidentesTransitoCR;
GO


/* ------------------------------------------------------------
   PASO 2: CREAR LA TABLA SI TODAVIA NO EXISTE
   ------------------------------------------------------------ */

IF OBJECT_ID('dbo.accidentes', 'U') IS NULL
BEGIN

    CREATE TABLE dbo.accidentes
    (
        /* Llave primaria creada automaticamente por SQL Server */
        id_accidente INT IDENTITY(1,1) NOT NULL,

        /* Informacion general del accidente */
        clase_accidente NVARCHAR(50) NOT NULL,
        tipo_accidente NVARCHAR(100) NOT NULL,
        anio INT NOT NULL,
        hora NVARCHAR(20) NOT NULL,
        hora_recodificada NVARCHAR(20) NOT NULL,

        /* Informacion geografica */
        provincia NVARCHAR(50) NOT NULL,
        canton NVARCHAR(100) NOT NULL,
        distrito NVARCHAR(150) NOT NULL,
        ruta NVARCHAR(30) NOT NULL,
        kilometro NVARCHAR(30) NOT NULL,
        region_mideplan NVARCHAR(50) NOT NULL,

        /* Informacion de la via */
        zona NVARCHAR(30) NOT NULL,
        calzada_vertical NVARCHAR(50) NOT NULL,
        calzada_horizontal NVARCHAR(50) NOT NULL,
        tipo_calzada NVARCHAR(50) NOT NULL,
        tipo_circulacion NVARCHAR(100) NOT NULL,
        estado_calzada NVARCHAR(100) NOT NULL,
        tipo_ruta NVARCHAR(50) NOT NULL,

        /* Informacion climatica */
        estado_tiempo NVARCHAR(50) NOT NULL,

        /* Informacion temporal */
        dia_numero TINYINT NOT NULL,
        dia NVARCHAR(20) NOT NULL,
        mes_numero TINYINT NOT NULL,
        mes NVARCHAR(20) NOT NULL,

        /* Variable objetivo del modelo */
        gravedad TINYINT NOT NULL,

        /* Llave primaria */
        CONSTRAINT PK_accidentes
            PRIMARY KEY (id_accidente),

        /* El numero del dia debe estar entre 1 y 7 */
        CONSTRAINT CK_accidentes_dia_numero
            CHECK (dia_numero BETWEEN 1 AND 7),

        /* El numero del mes debe estar entre 1 y 12 */
        CONSTRAINT CK_accidentes_mes_numero
            CHECK (mes_numero BETWEEN 1 AND 12),

        /* La gravedad solamente puede contener 0 o 1 */
        CONSTRAINT CK_accidentes_gravedad
            CHECK (gravedad IN (0, 1))
    );

    PRINT 'Tabla accidentes creada correctamente.';

END
ELSE
BEGIN

    PRINT 'La tabla accidentes ya existe.';

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
AND TABLE_NAME = 'accidentes';
GO


/* ------------------------------------------------------------
   PASO 4: MOSTRAR LA ESTRUCTURA DE LA TABLA
   ------------------------------------------------------------ */

SELECT
    ORDINAL_POSITION AS posicion,
    COLUMN_NAME AS columna,
    DATA_TYPE AS tipo_dato,
    CHARACTER_MAXIMUM_LENGTH AS longitud_maxima,
    IS_NULLABLE AS permite_nulos
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
AND TABLE_NAME = 'accidentes'
ORDER BY ORDINAL_POSITION;
GO