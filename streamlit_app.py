# Carga de Librerías
import os
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
# Librerías a utilizar


CARPETA_PROYECTO = os.path.dirname(os.path.abspath(__file__))
CARPETA_SRC = os.path.join(CARPETA_PROYECTO, "src")
# Al estar en la raíz del proyecto se agrega las direcciones de las carpetas


if CARPETA_SRC not in sys.path:
    sys.path.insert(0, CARPETA_SRC)

from datos.GestorDatos import GestorDatos
from eda.ProcesadorEDA import ProcesadorEDA
from visualizacion.MapaAccidentes import MapaAccidentes
from modelos.PreparadorModelo import PreparadorModelo
from modelos.EntrenadorModelos import EntrenadorModelos
# Se invocan las distintas clases donde tomará la información


# *******************************
# CONFIGURACIÓN DE LA PÁGINA

st.set_page_config(
    page_title="Accidentes de tránsito con víctimas - Costa Rica", # Título de la página (usado también en la pestaña)
    layout="wide",
)

COLOR_PRINCIPAL = "#FEFFD3"
COLOR_GRAVE = "#BF4646"
COLOR_LEVE = "#FEFFD3"
# Colores para los gráficos del dashboard

# ============================================================
# SECCION 1: CARGA DE DATOS (con cache para no releer el CSV
# cada vez que el usuario cambia un filtro)
# ============================================================

@st.cache_data(show_spinner="Cargando datos procesados...")
def cargar_datos():
    """
    Carga el CSV limpio de accidentes y el resumen climático
    mensual, ambos ya generados por el pipeline del proyecto
    (GestorDatos / ClienteAPI). No vuelve a limpiar ni a
    consultar la API: solo lee lo que ya está en data/.

    Retorna:
        accidentes: DataFrame limpio de accidentes.
        clima: DataFrame con el resumen climático mensual.
    """

    gestor_datos = GestorDatos()

    accidentes = gestor_datos.cargar_csv_procesado(
        "accidentes_victimas_limpio.csv"
    )

    ruta_clima = os.path.join(
        gestor_datos.ruta_processed,
        "clima_mensual_2018_2024.csv"
    )

    clima = pd.read_csv(
        ruta_clima,
        sep=";",
        encoding="utf-8-sig"
    )

    return accidentes, clima


# ============================================================
# SECCION 2: ENTRENAMIENTO DEL MODELO (se cachea como recurso
# para que solo se entrene una vez por sesión, no en cada clic)
# ============================================================

@st.cache_resource(show_spinner="Entrenando los 3 modelos (Regresión Logística, Árbol y KNN)...")
def entrenar_modelos(accidentes, clima):
    """
    Ejecuta exactamente el mismo flujo que usaría main.py para
    modelar: relacionar con clima, separar variables, dividir
    en entrenamiento/prueba, preprocesar y entrenar los 3
    algoritmos definidos en EntrenadorModelos.

    Se entrena siempre sobre el 100% de los datos limpios
    (no sobre los filtros de la barra lateral), para que el
    modelo sea comparable con el que generaría main.py.

    Retorna:
        preparador: instancia de PreparadorModelo ya usada.
        entrenador: instancia de EntrenadorModelos con los
                    3 modelos entrenados y sus métricas.
        comparacion: DataFrame comparativo de los 3 modelos.
        X_prueba, y_prueba: conjunto de prueba (para mostrar
                    ejemplos y matrices de confusión).
    """

    preparador = PreparadorModelo()

    datos_modelo = preparador.relacionar_con_clima(
        accidentes,
        clima
    )

    X, y = preparador.separar_variables(datos_modelo)

    X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = (
        preparador.dividir_datos(X, y)
    )

    preprocesador = preparador.crear_preprocesador()

    entrenador = EntrenadorModelos(preprocesador)

    comparacion = entrenador.entrenar_todos(
        X_entrenamiento,
        y_entrenamiento,
        X_prueba,
        y_prueba
    )

    return preparador, entrenador, comparacion, X_prueba, y_prueba


# ============================================================
# SECCION 3: FILTROS DE LA BARRA LATERAL
#
# Los filtros afectan las pestañas de EDA (1 a 5), pero NO al
# entrenamiento del modelo, que siempre usa el 100% de los
# datos limpios (igual que main.py).
# ============================================================

def aplicar_filtros(accidentes):
    """
    Muestra los controles de filtro en la barra lateral y
    devuelve el DataFrame de accidentes ya filtrado.

    Parametro:
        accidentes: DataFrame limpio completo.

    Retorna:
        DataFrame filtrado según lo que elija el usuario.
    """

    st.sidebar.header("Filtros")

    anios_disponibles = sorted(accidentes["anio"].unique().tolist())

    anios_seleccionados = st.sidebar.multiselect(
        "Año",
        options=anios_disponibles,
        default=anios_disponibles,
    )

    provincias_disponibles = sorted(
        accidentes["provincia"].unique().tolist()
    )

    provincias_seleccionadas = st.sidebar.multiselect(
        "Provincia",
        options=provincias_disponibles,
        default=provincias_disponibles,
    )

    zonas_disponibles = sorted(accidentes["zona"].unique().tolist())

    zonas_seleccionadas = st.sidebar.multiselect(
        "Zona",
        options=zonas_disponibles,
        default=zonas_disponibles,
    )

    st.sidebar.caption(
        "Estos filtros afectan las pestañas de análisis. "
        "El modelo predictivo siempre se entrena con el 100% "
        "de los datos limpios."
    )

    datos_filtrados = accidentes[
        accidentes["anio"].isin(anios_seleccionados)
        & accidentes["provincia"].isin(provincias_seleccionadas)
        & accidentes["zona"].isin(zonas_seleccionadas)
    ]

    return datos_filtrados


# ============================================================
# SECCION 4: PESTAÑA 1 - RESUMEN GENERAL
# ============================================================

def pestania_resumen(eda):
    resumen = eda.resumen_general()
    distribucion = eda.distribucion_gravedad()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Accidentes registrados", f"{resumen['cantidad_filas']:,}")
    col2.metric("Provincias", resumen["cantidad_provincias"])
    col3.metric(
        "Período",
        f"{resumen['anio_inicial']}-{resumen['anio_final']}"
    )

    porcentaje_grave = distribucion.loc[
        distribucion["gravedad"] == 1, "porcentaje"
    ]

    col4.metric(
        "% accidentes graves",
        f"{porcentaje_grave.iloc[0]:.1f} %" if not porcentaje_grave.empty else "—"
    )

    st.divider()

    col_izq, col_der = st.columns([1, 1])

    with col_izq:
        st.subheader("Distribución de la gravedad")
        figura = px.pie(
            distribucion,
            names="clase_accidente",
            values="cantidad_accidentes",
            color="clase_accidente",
            color_discrete_map={
                "Solo heridos leves": COLOR_LEVE,
                "Con muertos o graves": COLOR_GRAVE,
            },
            hole=0.45,
        )
        st.plotly_chart(figura, use_container_width=True)

    with col_der:
        st.subheader("Tipos de dato y valores vacíos")
        tipos = eda.obtener_tipos_datos()
        vacios = eda.analizar_valores_vacios()
        tabla = tipos.merge(vacios, on="columna")
        st.dataframe(tabla, use_container_width=True, height=380)


# ============================================================
# SECCION 5: PESTAÑA 2 - ANALISIS TEMPORAL
# ============================================================

def pestania_temporal(eda):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Accidentes por año")
        datos = eda.accidentes_por_anio()
        figura = px.line(
            datos, x="anio", y="cantidad_accidentes", markers=True
        )
        figura.update_traces(line_color=COLOR_PRINCIPAL)
        st.plotly_chart(figura, use_container_width=True)

    with col2:
        st.subheader("Accidentes por mes")
        datos = eda.accidentes_por_mes()
        figura = px.bar(
            datos, x="mes", y="cantidad_accidentes"
        )
        figura.update_traces(marker_color=COLOR_LEVE)
        st.plotly_chart(figura, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Accidentes por día de la semana")
        datos = eda.accidentes_por_dia()
        figura = px.bar(datos, x="dia", y="cantidad_accidentes")
        figura.update_traces(marker_color="#70AD47")
        st.plotly_chart(figura, use_container_width=True)

    with col4:
        st.subheader("Accidentes por franja horaria")
        datos = eda.accidentes_por_hora()
        figura = px.bar(
            datos, x="hora_recodificada", y="cantidad_accidentes"
        )
        figura.update_traces(marker_color="#EEEEEE")
        st.plotly_chart(figura, use_container_width=True)

    st.subheader("Mapa de calor: día de la semana × franja horaria")
    tabla = eda.tabla_dia_hora()
    columnas_horas = [c for c in tabla.columns if c not in ("dia_numero", "dia")]
    figura = go.Figure(
        data=go.Heatmap(
            z=tabla[columnas_horas].values,
            x=columnas_horas,
            y=tabla["dia"],
            colorscale="YlOrRd",
        )
    )
    st.plotly_chart(figura, use_container_width=True)


# ============================================================
# SECCION 6: PESTAÑA 3 - ANALISIS GEOGRAFICO
# ============================================================

def pestania_geografica(eda):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Accidentes por provincia")
        datos = eda.accidentes_por_provincia()
        figura = px.bar(
            datos.sort_values("cantidad_accidentes"),
            x="cantidad_accidentes",
            y="provincia",
            orientation="h",
        )
        figura.update_traces(marker_color=COLOR_PRINCIPAL)
        st.plotly_chart(figura, use_container_width=True)

    with col2:
        st.subheader("% de accidentes graves por provincia")
        datos_gravedad = eda.gravedad_por_provincia()
        figura = px.bar(
            datos_gravedad.sort_values("porcentaje_graves"),
            x="porcentaje_graves",
            y="provincia",
            orientation="h",
        )
        figura.update_traces(marker_color=COLOR_GRAVE)
        st.plotly_chart(figura, use_container_width=True)

    st.subheader("Mapa interactivo por provincia")

    datos_gravedad = eda.gravedad_por_provincia()

    provincias_disponibles = set(datos_gravedad["provincia"])
    provincias_conocidas = set(MapaAccidentes().coordenadas.keys())

    if not provincias_disponibles.issubset(provincias_conocidas):
        st.info(
            "El mapa no se puede generar: los filtros actuales "
            "dejaron alguna provincia sin datos suficientes."
        )
        return

    mapa = MapaAccidentes()
    # MapaAccidentes.crear_mapa_provincias() guarda el HTML en
    # graficos/; aquí simplemente se vuelve a leer ese archivo
    # para incrustarlo en la app.
    ruta_mapa = mapa.crear_mapa_provincias(datos_gravedad)

    with open(ruta_mapa, "r", encoding="utf-8") as archivo_html:
        html_mapa = archivo_html.read()

    components.html(html_mapa, height=560)


# ============================================================
# SECCION 7: PESTAÑA 4 - GRAVEDAD POR CATEGORIA
# ============================================================

def pestania_gravedad(eda):
    opciones = {
        "Tipo de accidente": eda.gravedad_por_tipo_accidente,
        "Zona (rural / urbana)": eda.gravedad_por_zona,
        "Tipo de ruta": eda.gravedad_por_tipo_ruta,
        "Estado del tiempo": eda.gravedad_por_estado_tiempo,
        "Estado de la calzada": eda.gravedad_por_estado_calzada,
    }

    seleccion = st.selectbox("Comparar gravedad según:", list(opciones.keys()))

    datos = opciones[seleccion]()

    columna_categoria = datos.columns[0]

    figura = px.bar(
        datos.sort_values("porcentaje_graves"),
        x="porcentaje_graves",
        y=columna_categoria,
        orientation="h",
        hover_data=["total_accidentes", "accidentes_graves", "accidentes_leves"],
    )
    figura.update_traces(marker_color=COLOR_GRAVE)
    st.plotly_chart(figura, use_container_width=True)

    st.dataframe(datos, use_container_width=True)

    st.subheader("Diez tipos de accidente más frecuentes")
    datos_tipo = eda.accidentes_por_tipo().head(10)
    figura = px.bar(
        datos_tipo.sort_values("cantidad_accidentes"),
        x="cantidad_accidentes",
        y="tipo_accidente",
        orientation="h",
    )
    figura.update_traces(marker_color="#EEEEEE")
    st.plotly_chart(figura, use_container_width=True)


# ============================================================
# SECCION 8: PESTAÑA 5 - CLIMA Y ACCIDENTES
# ============================================================

def pestania_clima(eda, clima):
    datos = eda.relacion_accidentes_clima(clima)

    resumen_anual = (
        datos.groupby("anio")
        .agg(
            precipitacion_total_mm=("precipitacion_total_mm", "sum"),
            cantidad_accidentes=("cantidad_accidentes", "sum"),
        )
        .reset_index()
        .sort_values("anio")
    )

    figura = go.Figure()

    figura.add_trace(
        go.Scatter(
            x=resumen_anual["anio"],
            y=resumen_anual["cantidad_accidentes"],
            name="Accidentes",
            mode="lines+markers",
            line=dict(color=COLOR_GRAVE, width=3),
        )
    )

    figura.add_trace(
        go.Scatter(
            x=resumen_anual["anio"],
            y=resumen_anual["precipitacion_total_mm"],
            name="Precipitación total (mm)",
            mode="lines+markers",
            line=dict(color=COLOR_PRINCIPAL, width=3),
            yaxis="y2",
        )
    )

    figura.update_layout(
        yaxis=dict(title="Cantidad de accidentes"),
        yaxis2=dict(title="Precipitación (mm)", overlaying="y", side="right"),
        legend=dict(orientation="h", y=1.1),
    )

    st.subheader("Comparación anual: accidentes vs. precipitación")
    st.plotly_chart(figura, use_container_width=True)

    st.subheader("Detalle mensual por provincia")
    provincia = st.selectbox(
        "Provincia", sorted(datos["provincia"].unique().tolist())
    )
    datos_provincia = datos[datos["provincia"] == provincia]
    st.dataframe(datos_provincia, use_container_width=True)


# ============================================================
# SECCION 9: PESTAÑA 6 - MODELO PREDICTIVO
# ============================================================

def pestania_modelo(accidentes_completos, clima):
    st.success(
        "El entrenamiento usa siempre el 100% de los datos limpios "
        "(no los filtros de la barra lateral) para que sea comparable "
        "con lo que produciría main.py. Solo se entrena una vez por sesión."
    )

    preparador, entrenador, comparacion, X_prueba, y_prueba = entrenar_modelos(
        accidentes_completos, clima
    )

    st.subheader("Comparación de los 3 algoritmos")
    st.caption(
        "Ordenado por recall de accidentes graves (criterio principal "
        "del proyecto), luego F1-score y ROC-AUC."
    )
    st.dataframe(comparacion, use_container_width=True)

    nombre_mejor, pipeline_mejor = entrenador.seleccionar_mejor_modelo()
    st.success(f"Mejor modelo según recall de graves: **{nombre_mejor}**")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Matriz de confusión — {nombre_mejor}")
        matriz = entrenador.obtener_matriz_confusion(nombre_mejor)
        figura = px.imshow(
            matriz,
            text_auto=True,
            x=["Predicho: Leve", "Predicho: Grave"],
            y=["Real: Leve", "Real: Grave"],
            color_continuous_scale="Blues",
        )
        st.plotly_chart(figura, use_container_width=True)

    with col2:
        st.subheader("Reporte de clasificación")
        reporte = entrenador.obtener_reporte(nombre_mejor)
        st.dataframe(reporte, use_container_width=True)

    st.divider()

    # --------------------------------------------------------
    # FORMULARIO DE PREDICCION INTERACTIVA
    #
    # Se arma una fila con las mismas variables predictoras
    # que usa PreparadorModelo, usando los valores reales del
    # conjunto de datos para poblar cada control.
    # --------------------------------------------------------

    st.subheader("Probar el modelo con un caso hipotético")

    datos_referencia = X_prueba

    with st.form("formulario_prediccion"):
        col_num, col_cat1, col_cat2 = st.columns(3)

        valores_formulario = {}

        with col_num:
            for variable in preparador.variables_numericas:
                if variable in ("anio", "dia_numero", "mes_numero"):
                    valores_formulario[variable] = st.number_input(
                        variable,
                        value=int(datos_referencia[variable].median()),
                        step=1,
                    )
                else:
                    valores_formulario[variable] = st.number_input(
                        variable,
                        value=float(datos_referencia[variable].median()),
                    )

        variables_categoricas = preparador.variables_categoricas
        mitad = len(variables_categoricas) // 2

        with col_cat1:
            for variable in variables_categoricas[:mitad]:
                opciones = sorted(
                    datos_referencia[variable].dropna().unique().tolist()
                )
                valores_formulario[variable] = st.selectbox(variable, opciones)

        with col_cat2:
            for variable in variables_categoricas[mitad:]:
                opciones = sorted(
                    datos_referencia[variable].dropna().unique().tolist()
                )
                valores_formulario[variable] = st.selectbox(variable, opciones)

        enviado = st.form_submit_button("Predecir gravedad")

    if enviado:
        fila = pd.DataFrame([valores_formulario])[
            preparador.variables_predictoras
        ]

        prediccion = pipeline_mejor.predict(fila)[0]
        probabilidad = pipeline_mejor.predict_proba(fila)[0][1]

        if prediccion == 1:
            st.error(
                f"Predicción: **Con muertos o graves** "
                f"(probabilidad estimada: {probabilidad:.1%})"
            )
        else:
            st.success(
                f"Predicción: **Solo heridos leves** "
                f"(probabilidad de ser grave: {probabilidad:.1%})"
            )


# ============================================================
# PROGRAMA PRINCIPAL DE LA APP
# ============================================================

def main():
    st.title("🚦 Accidentes de tránsito con víctimas en Costa Rica")
    st.caption("Anuario COSEVI 2018-2024 · Proyecto III")

    accidentes_completos, clima = cargar_datos()
    accidentes_filtrados = aplicar_filtros(accidentes_completos)

    if accidentes_filtrados.empty:
        st.warning("No hay datos para la combinación de filtros seleccionada.")
        return

    eda = ProcesadorEDA(accidentes_filtrados)

    (
        tab_resumen,
        tab_temporal,
        tab_geografica,
        tab_gravedad,
        tab_clima,
        tab_modelo,
    ) = st.tabs(
        [
            "Resumen general",
            "Análisis temporal",
            "Análisis geográfico",
            "Gravedad",
            "Clima y accidentes",
            "Modelo predictivo",
        ]
    )

    with tab_resumen:
        pestania_resumen(eda)

    with tab_temporal:
        pestania_temporal(eda)

    with tab_geografica:
        pestania_geografica(eda)

    with tab_gravedad:
        pestania_gravedad(eda)

    with tab_clima:
        pestania_clima(eda, clima)

    with tab_modelo:
        pestania_modelo(accidentes_completos, clima)


if __name__ == "__main__":
    main()
