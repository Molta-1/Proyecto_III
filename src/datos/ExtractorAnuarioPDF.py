import os # Intercatúa con el sistema operativo (unir rutas, comprobar archivos etc)
import re # Permite trabajar sobre patrones complejos de texto
import pdfplumber # Permite la lectura y extracción de información en PDF
import pandas as pd # Librería para análisis y manipulación de datos


color_encabezado = (0.0863, 0.2, 0.337) # Color de los encabezados del PDF
tolerancia_color = 0.01 # Margen de error permitido a la hora de detectar los colores


tabla_config = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "snap_tolerance": 6,
    "join_tolerance": 6,
    "edge_min_length": 10,
    "intersection_tolerance": 6,
}
# Reglas para reconstrucción de la tabla con el PDF

class GestorDatos:
    def __init__(self, ruta_raw: str = None):
        if ruta_raw is None:
            dir_actual = os.path.dirname(os.path.abspath(__file__))
            self.ruta_raw = os.path.abspath(
                os.path.join(dir_actual, "..", "..", "data", "raw")
            # ".." significa que sube un nivel en la ruta hasta que coincida con "data/raw"
            )
        # Esto permite que al compartir el proyecto se pueda usar en cualquier equipo que posea "data/raw"
        else:
            self.ruta_raw = ruta_raw
        os.makedirs(self.ruta_raw, exist_ok=True)
        # En caso de no existir "data/raw", se crean en el disco

    @staticmethod
    # al no modificar la variable entonces se utiliza "staticmethod", ya que esta función es auxiliar

    def _es_color_encabezado(color) -> bool: #  "-> bool:" Es un type hint que indica el valor que debe de retornar
        if not isinstance(color, (tuple, list)) or len(color) < 3:
            return False
        return all(abs(color[i] - color_encabezado[i]) < tolerancia_color for i in range(3)) # "range(3)" es para que trabaje sobre los tres número del RGB
    # Determina el color es igual al azul marino de los encabezados

    def _num_filas_encabezado(self, pagina, tabla_obj) -> int:
        x0, top, x1, bottom = tabla_obj.bbox
        # Coordenadas de los límites de la tabla
        rects_encabezado = [
            r for r in pagina.rects
            if self._es_color_encabezado(r.get("non_stroking_color"))
            and r["x0"] >= x0 - 2 and r["x1"] <= x1 + 2
        ]
        # Filtra si posee el color del encabezado y si poseen el mismo ancho con un margen de seguridad
        if not rects_encabezado:
            return 1  # fallback conservador

        banda_inferior = max(r["bottom"] for r in rects_encabezado)
        # Encuentra el límite inferior del encabezado

        n_filas = 0
        for fila in tabla_obj.rows:
            fila_top = fila.bbox[1]
            if fila_top < banda_inferior - 1:  # margen de 1pt
                n_filas += 1
            else:
                break
        return max(n_filas, 1)
    # Cuenta la cantidad total de filas dentro del encabezado, lo cual permite un mejor resultado que leer las palabras

    @staticmethod
    def _limpiar_celda(valor):
        if valor is None:
            return ""
        return str(valor).replace("\n", " ").strip()
    # Si no hay datos los devuelve vacíos y si hay datos los convierte en string

    def _construir_encabezado(self, filas_encabezado_raw):
        n_filas = len(filas_encabezado_raw)
        n_cols = max(len(f) for f in filas_encabezado_raw)

        filas = [[self._limpiar_celda(c) for c in f] + [""] * (n_cols - len(f))
                 for f in filas_encabezado_raw]
        # Calcula las dimensiones, limpia la celda y agrega cadenas vacías para asegurar una matriz perfecta

        rellenas = [[""] * n_cols for _ in range(n_filas)]
        for i in range(n_filas):
            for j in range(n_cols):
                val = filas[i][j]
                if val:
                    rellenas[i][j] = val
                elif i > 0 and rellenas[i - 1][j]:
                    rellenas[i][j] = rellenas[i - 1][j]
                    # No hay valor propio: hereda el de la fila de encabezado de arriba
                    # (celda combinada verticalmente, ej. una etiqueta que ocupa dos filas de alto)
                elif j > 0 and rellenas[i][j - 1]:
                    rellenas[i][j] = rellenas[i][j - 1]
                    # Si tampoco hay nada arriba, hereda el de la celda de la izquierda
                    # (celda combinada horizontalmente, ej. un título que abarca varias columnas)
                else:
                    rellenas[i][j] = ""
        # Con este doble "elif" se reconstruyen los colspan/rowspan que pdfplumber
        # entrega como None, sin mezclar el título de un grupo con el de otro

        encabezados = []
        for j in range(n_cols):
            partes = []
            anterior = None
            for i in range(n_filas):
                v = rellenas[i][j]
                if v and v != anterior:
                    partes.append(v)
                anterior = v if v else anterior
            nombre = " - ".join(partes).strip().upper()
            encabezados.append(nombre if nombre else f"COL_{j + 1}")
        # Junta verticalmente los niveles de encabezado de cada columna en un solo nombre,
        # sin repetir el mismo texto dos veces seguidas

        # Desambiguar duplicados (p. ej. varias columnas "N" o "%")
        vistos = {}
        for idx, nombre in enumerate(encabezados):
            vistos[nombre] = vistos.get(nombre, 0) + 1
            if vistos[nombre] > 1:
                encabezados[idx] = f"{nombre} ({vistos[nombre]})"

        return tuple(encabezados), n_cols


    @staticmethod
    def _fila_vacia_o_ruido(fila) -> bool:
        celdas = [str(c).strip() for c in fila if c not in (None, "")]
        if not celdas:
            return True
        texto = " ".join(celdas).upper()
        if "FUENTE:" in texto or texto.startswith("NOTA"):
            return True
        return False


    # Descarta filas totalmente vacías o notas al pie ("Fuente: ..." / "Nota: ...")
    # que a veces quedan mezcladas dentro del cuerpo de la tabla extraída

    _PATRON_NUMERICO = re.compile(r"\d")


    @classmethod
    def _fila_tiene_dato_numerico(cls, fila) -> bool:
        return any(cls._PATRON_NUMERICO.search(str(c)) for c in fila if c)
    # Una fila de datos real del Anuario siempre trae al menos un número (conteo, % o tasa).
    # Sirve de filtro final para descartar restos de encabezado partidos entre dos páginas

    def _limites_columnas(self, tabla_obj, x1_tabla):
        limites = set()
        for fila in tabla_obj.rows:
            for c in fila.cells:
                if c:
                    limites.add(round(c[0], 1))
        limites.add(round(x1_tabla, 1))
        return sorted(limites)
    # Reúne las coordenadas x0 de las celdas de encabezado ya detectadas (el nivel
    # más fino disponible) más el borde derecho de la tabla, para usarlas como
    # límites de columna explícitos al reconstruir el cuerpo por texto

    def _extraer_cuerpo_por_texto(self, pagina, tabla_obj):
        x0, top, x1, bottom = tabla_obj.bbox
        xs = self._limites_columnas(tabla_obj, x1)
        if len(xs) < 2:
            return None
        # Sin al menos 2 límites no se puede armar ninguna columna

        candidatos_fin = []
        navy_siguiente = [
            r["top"] for r in pagina.rects
            if self._es_color_encabezado(r.get("non_stroking_color")) and r["top"] > bottom + 3
        ]
        if navy_siguiente:
            candidatos_fin.append(min(navy_siguiente))
        # Si hay otro cuadro más abajo en la misma página, su encabezado azul marca
        # dónde debe terminar el recorte de este
        try:
            palabras = pagina.extract_words()
            fuente_tops = [w["top"] for w in palabras
                           if w["text"].upper().startswith("FUENTE") and w["top"] > bottom]
            if fuente_tops:
                candidatos_fin.append(min(fuente_tops))
        except Exception:
            pass
        # Si no hay otro cuadro, la nota "Fuente:" al pie de la tabla también sirve de límite
        fin = min(candidatos_fin) if candidatos_fin else pagina.height - 40
        # Si no se encontró ninguna referencia, se usa el margen inferior de la página
        if fin <= top:
            return None

        crop = pagina.crop((x0, top, x1, fin))
        settings2 = {
            "vertical_strategy": "explicit",
            "explicit_vertical_lines": xs,
            "horizontal_strategy": "text",
            "snap_tolerance": 4,
            "intersection_tolerance": 6,
        }
        # A diferencia de tabla_config, aquí las columnas se fijan a mano (xs) y las
        # filas se detectan por posición de texto ("text"), no por líneas/rects,
        # porque el cuerpo de estos cuadros no tiene ningún borde dibujado
        try:
            grid = crop.extract_table(settings2)
        except Exception:
            return None
        if not grid:
            return None

        grid = [[self._limpiar_celda(c) for c in fila] for fila in grid]
        grid = [fila for fila in grid if any(fila)]
        return grid


    # Reconstruye encabezado + cuerpo de una tabla cuando pdfplumber, con líneas/rects,
    # solo alcanzó a delimitar el encabezado (algunos cuadros del tipo "Continuación
    # del cuadro X.Y" no tienen ninguna línea ni sombreado en el cuerpo de datos)

    def _dividir_columnas_n_porcentaje(self, grid, n_header, n_cols):
        columnas_a_dividir = set()
        for i in range(min(n_header, len(grid))):
            for j in range(n_cols):
                celda = grid[i][j].strip().lower() if j < len(grid[i]) else ""
                if re.fullmatch(r"n\s*%", celda):
                    columnas_a_dividir.add(j)
        # Revisa las filas de encabezado buscando una celda que sea literalmente "n %":
        # esa columna quedó combinada en el cuerpo por texto y hay que separarla en dos

        if not columnas_a_dividir:
            return grid, n_header
        # Si ninguna columna lo necesita, se devuelve la tabla tal cual

        patron = re.compile(r"^(.*\S)\s+(-?\d+[.,]\d+|-)$")
        # Separa el último número con coma decimal  del resto de la celda ya que no se puede usar un simple split()
        nueva_grid = []
        for i, fila in enumerate(grid):
            es_encabezado = i < n_header
            nueva_fila = []
            for j in range(n_cols):
                val = (fila[j] if j < len(fila) else "").strip()
                if j in columnas_a_dividir:
                    if es_encabezado:
                        if re.fullmatch(r"n\s*%", val, re.IGNORECASE):
                            nueva_fila.extend(["N", "%"])
                        else:
                            nueva_fila.extend([val, val])  # repite el título del grupo
                    else:
                        m = patron.match(val)
                        if m:
                            nueva_fila.extend([m.group(1).strip(), m.group(2).strip()])
                        else:
                            nueva_fila.extend([val, ""])
                else:
                    nueva_fila.append(val)
            nueva_grid.append(nueva_fila)
        return nueva_grid, n_header
    # Al dividir una columna en dos, todas las filas  deben crecer una columna extra en el mismo punto, o el resto de la tabla queda desalineada

    def extraer_todas_las_tablas_dinamicas(
            self,
            nombre_pdf_local: str = "Anuario_2024.pdf",
            pagina_inicio: int = 50,
            pagina_fin: int = None,
            nombre_excel_salida: str = "Anuario_2024_Procesado.xlsx",
    ) -> None:
        ruta_pdf = os.path.join(self.ruta_raw, nombre_pdf_local)
        if not os.path.exists(ruta_pdf):
            print(f"[ERROR] No se encontró el archivo en la ruta: {ruta_pdf}")
            return

        tablas_agrupadas = {}
        titulos_por_encabezado = {}

        print(f"[INFO] Leyendo '{nombre_pdf_local}' desde la página {pagina_inicio}...")

        with pdfplumber.open(ruta_pdf) as pdf:
            fin = pagina_fin if pagina_fin else len(pdf.pages)
            paginas_a_procesar = pdf.pages[pagina_inicio - 1: fin]

            for num_pagina, pagina in enumerate(paginas_a_procesar, start=pagina_inicio):
                texto_pagina = pagina.extract_text()
                if not texto_pagina or len(texto_pagina.strip()) < 50:
                    continue
                # Página sin contenido útil (portada, separador de capítulo, etc.)

                # Título del cuadro (para referencia, primera línea "Cuadro X-Y ...")
                primera_linea = texto_pagina.strip().split("\n")[0]

                tablas_obj = pagina.find_tables(tabla_config)
                for tabla_obj in tablas_obj:
                    tabla = tabla_obj.extract()
                    if not tabla or len(tabla) < 1:
                        continue

                    n_filas_enc = self._num_filas_encabezado(pagina, tabla_obj)

                    # Si las líneas/rects solo delimitan el encabezado (tabla sin cuerpo detectado, o cuerpo == encabezado), el cuerpo de datos se reconstruye a partir del texto de la página.
                    if n_filas_enc >= len(tabla):
                        grid_texto = self._extraer_cuerpo_por_texto(pagina, tabla_obj)
                        if grid_texto and len(grid_texto) > len(tabla):
                            tabla = grid_texto
                            # Encabezado = filas iniciales sin dato numérico
                            n_filas_enc = 0
                            for fila in tabla:
                                if self._fila_tiene_dato_numerico(fila):
                                    break
                                n_filas_enc += 1
                            n_filas_enc = max(n_filas_enc, 1)

                    n_filas_enc = min(n_filas_enc, len(tabla) - 1) if len(tabla) > 1 else 1
                    # Nunca deja que TODAS las filas cuenten como encabezado

                    tabla = [[self._limpiar_celda(c) for c in fila] for fila in tabla]
                    n_cols_bruto = max(len(f) for f in tabla)
                    tabla, n_filas_enc = self._dividir_columnas_n_porcentaje(tabla, n_filas_enc, n_cols_bruto)
                    filas_encabezado_raw = tabla[:n_filas_enc]
                    encabezado, n_cols = self._construir_encabezado(filas_encabezado_raw)

                    if "...................." in str(encabezado):
                        continue
                    # Tabla de índice/contenido, no es un cuadro de datos

                    clave = encabezado
                    if clave not in tablas_agrupadas:
                        tablas_agrupadas[clave] = []
                        titulos_por_encabezado[clave] = primera_linea
                    # Misma estructura de encabezado = misma pestaña de Excel al final

                    for fila in tabla[n_filas_enc:]:
                        if self._fila_vacia_o_ruido(fila):
                            continue
                        fila_limpia = [self._limpiar_celda(c) for c in fila]
                        # Normalizar longitud de fila al número de columnas del encabezado
                        if len(fila_limpia) < n_cols:
                            fila_limpia += [""] * (n_cols - len(fila_limpia))
                        elif len(fila_limpia) > n_cols:
                            fila_limpia = fila_limpia[:n_cols]
                        tablas_agrupadas[clave].append(fila_limpia)

        ruta_excel = os.path.join(self.ruta_raw, nombre_excel_salida)
        print(f"[INFO] Exportando {len(tablas_agrupadas)} estructuras a Excel...")

        with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
            contador_hojas = 1
            for encabezado, filas in tablas_agrupadas.items():
                filas = [f for f in filas if self._fila_tiene_dato_numerico(f)]
                # Filtro final: descarta cualquier fila residual sin ningún dato numérico
                if len(filas) < 1:
                    continue
                df = pd.DataFrame(filas, columns=encabezado)
                df = df.dropna(how="all")
                # eliminar columnas totalmente vacías generadas por ruido residual
                df = df.loc[:, ~(df.apply(lambda c: (c.astype(str).str.strip() == "").all()))]
                if df.empty or df.shape[1] == 0:
                    continue

                nombre_hoja = f"Estructura_{contador_hojas}"
                df.to_excel(writer, sheet_name=nombre_hoja, index=False)
                print(f"  -> Pestaña '{nombre_hoja}' ({titulos_por_encabezado[encabezado][:60]}) "
                      f"con {len(df)} filas.")
                contador_hojas += 1

        print(f"[EXITO] Proceso finalizado. Archivo generado: {ruta_excel}")


    def cargar_excel(self, nombre_excel: str = "Anuario_2024_Procesado.xlsx", hoja: str = "Estructura_1") -> pd.DataFrame:
        ruta = os.path.join(self.ruta_raw, nombre_excel)
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"El archivo {ruta} no existe.")
        return pd.read_excel(ruta, sheet_name=hoja)
    # Carga una pestaña ya procesada del Excel como DataFrame, para seguir trabajando con ella