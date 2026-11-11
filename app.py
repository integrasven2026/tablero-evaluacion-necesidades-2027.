import os
import requests
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import pydeck as pdk

# Configuración de la página
st.set_page_config(
    page_title="Tablero Evaluación de Necesidades - Consorcio ÍNTEGRAS (ECHO HIP 2027)",
    page_icon="📊",
    layout="wide"
)

# Constantes de conexión API KoboToolbox proporcionadas
KOBO_URL = "https://eu.kobotoolbox.org/api/v2/assets/aDLGup9ApcZVFUy8JTo7qZ/data/?format=json"
TOKEN = "a18c017a2e697f4ea1272375dae261ccec6b19d7"

@st.cache_data(ttl=600)
def load_kobo_data():
    headers = {"Authorization": f"Token {TOKEN}"}
    try:
        response = requests.get(KOBO_URL, headers=headers)
        if response.status_code == 200:
            data = response.json().get('results', [])
            if data:
                return pd.DataFrame(data)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error conectando con la API de KoboToolbox: {e}")
        return pd.DataFrame()

df_raw = load_kobo_data()

# Título principal
st.title("📊 Tablero Dinámico de Evaluación de Necesidades - ECHO HIP 2027")
st.markdown("**Consorcio ÍNTEGRAS:** COOPI, HIAS, FLM, PLAFAM, PALUZ | Monitoreo Multisectorial Post-Sismos y Crisis Estructural")

if df_raw.empty:
    st.warning("⚠️ No se encontraron registros actualmente en el API de KoboToolbox o el formulario está en fase de levantamiento. Mostrando estructura de análisis interactiva.")
    # Estructura simulada temporal si el API está vacío para que el tablero no falle visualmente
    df_raw = pd.DataFrame({
        'socio': ['coopi', 'hias', 'flm', 'plafam', 'paluz'],
        'Estado': ['Distrito Capital', 'La Guaira', 'Miranda', 'Distrito Capital', 'Miranda'],
        'Municipio': ['Libertador', 'Carayaca', 'Chacao', 'Sucre', 'Paz Castillo'],
        'Parroquia': ['La Vega', 'Carayaca', 'Chacao', 'Petare', 'Santa Lucía'],
        'comunidad': ['Comunidad A', 'Comunidad B', 'Comunidad C', 'Comunidad D', 'Comunidad E'],
        'sexo': ['femenino', 'masculino', 'femenino', 'femenino', 'masculino'],
        'nivel_educativo': ['secundaria', 'universitaria', 'primaria', 'secundaria', 'ninguno'],
        'lat': [10.4806, 10.6000, 10.4900, 10.4850, 10.3200],
        'lon': [-66.9036, -67.0000, -66.8500, -66.8100, -66.6800]
    })

# --- PROCESAMIENTO DE COORDENADAS GPS ---
if 'ubicacion_gps' in df_raw.columns and 'lat' not in df_raw.columns:
    def parse_lat(val):
        try:
            parts = str(val).split()
            return float(parts[0])
        except:
            return np.nan
    def parse_lon(val):
        try:
            parts = str(val).split()
            return float(parts[1])
        except:
            return np.nan
    df_raw['lat'] = df_raw['ubicacion_gps'].apply(parse_lat)
    df_raw['lon'] = df_raw['ubicacion_gps'].apply(parse_lon)

if 'lat' not in df_raw.columns:
    df_raw['lat'] = 10.4806
    df_raw['lon'] = -66.9036

# --- SECCIÓN 1: FILTROS LATERALES EN CASCADA ---
st.sidebar.header("🎛️ Filtros de Localización y Socios")

socios_disp = df_raw['socio'].unique().tolist() if 'socio' in df_raw.columns else []
selected_socio = st.sidebar.multiselect("Organización Socio", options=socios_disp, default=socios_disp)

estados_disp = df_raw['Estado'].unique().tolist() if 'Estado' in df_raw.columns else []
selected_estado = st.sidebar.multiselect("Estado", options=estados_disp, default=estados_disp)

df_filtered = df_raw.copy()
if selected_socio and 'socio' in df_filtered.columns:
    df_filtered = df_filtered[df_filtered['socio'].isin(selected_socio)]
if selected_estado and 'Estado' in df_filtered.columns:
    df_filtered = df_filtered[df_filtered['Estado'].isin(selected_estado)]

municipios_disp = df_filtered['Municipio'].unique().tolist() if 'Municipio' in df_filtered.columns else []
selected_municipio = st.sidebar.multiselect("Municipio", options=municipios_disp, default=municipios_disp)
if selected_municipio and 'Municipio' in df_filtered.columns:
    df_filtered = df_filtered[df_filtered['Municipio'].isin(selected_municipio)]

parroquias_disp = df_filtered['Parroquia'].unique().tolist() if 'Parroquia' in df_filtered.columns else []
selected_parroquia = st.sidebar.multiselect("Parroquia", options=parroquias_disp, default=parroquias_disp)
if selected_parroquia and 'Parroquia' in df_filtered.columns:
    df_filtered = df_filtered[df_filtered['Parroquia'].isin(selected_parroquia)]

# KPIs Principales
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Encuestas Aplicadas", len(df_filtered))
col2.metric("Estados Monitoreados", df_filtered['Estado'].nunique() if 'Estado' in df_filtered.columns else 0)
col3.metric("Municipios Afectados", df_filtered['Municipio'].nunique() if 'Municipio' in df_filtered.columns else 0)
col4.metric("Comunidades / Albergues", df_filtered['comunidad'].nunique() if 'comunidad' in df_filtered.columns else 0)

st.markdown("---")

# --- PESTAÑAS DE ANÁLISIS SEGÚN ESTRUCTURA SOLICITADA ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "🗺️ 1. Mapa y Localización",
    "🏠 2. Sociodemografía & Vivienda / WASH",
    "💼 3. Socioeconómico & Ingresos",
    "🍲 4. Seguridad Alimentaria & Nutrición",
    "⚖️ 5. Acceso a Derechos",
    "🧸 6. Protección NNA",
    "🛡️ 7. VBG y Género",
    "📚 8. Educación en Emergencias",
    "🩺 9. Salud & SSR",
    "♿ 10. Discapacidad & Salud Mental"
])

with tab1:
    st.subheader("Mapa Georreferenciado y Cobertura Territorial")
    if 'lat' in df_filtered.columns and not df_filtered['lat'].isna().all():
        map_df = df_filtered.dropna(subset=['lat', 'lon'])
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=map_df['lat'].mean() if not map_df.empty else 10.4806,
                longitude=map_df['lon'].mean() if not map_df.empty else -66.9036,
                zoom=11,
                pitch=40,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=map_df,
                    get_position='[lon, lat]',
                    get_color='[220, 50, 30, 160]',
                    get_radius=250,
                    pickable=True
                )
            ],
            tooltip={"text": "Comunidad: {comunidad}\nMunicipio: {Municipio}\nParroquia: {Parroquia}"}
        ))
    else:
        st.info("No hay coordenadas GPS disponibles en el filtro actual.")

with tab2:
    st.subheader("Condiciones Sociodemográficas, Vivienda y WASH")
    c1, c2 = st.columns(2)
    with c1:
        if 'sexo' in df_filtered.columns:
            fig = px.pie(df_filtered, names='sexo', title="Distribución por Sexo Biológico", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        if 'nivel_educativo' in df_filtered.columns:
            fig = px.bar(df_filtered['nivel_educativo'].value_counts().reset_index(), x='index', y='nivel_educativo', title="Nivel Educativo")
            st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Características Socioeconómicas y Medios de Vida")
    st.markdown("Evaluación de fuentes de ingresos, impacto de la crisis económica y estrategias de afrontamiento.")

with tab4:
    st.subheader("Seguridad Alimentaria y Nutrición")
    st.markdown("Patrones de consumo alimentario, acceso a raciones y tamizaje nutricional en menores de 5 años.")

with tab5:
    st.subheader("Acceso a Derechos y Servicios")
    st.markdown("Pérdida de documentación de identidad por sismos y barreras de acceso a la asistencia humanitaria.")

with tab6:
    st.subheader("Protección de Niñas, Niños y Adolescentes (NNA)")
    st.markdown("Riesgos de protección infantil, trabajo infantil y separación en albergues temporales.")

with tab7:
    st.subheader("Violencia Basada en Género (VBG) y Enfoque de Género")
    st.markdown("Percepción de seguridad, riesgos en espacios comunitarios y barreras para la atención.")

with tab8:
    st.subheader("Educación en Emergencias (EiE)")
    st.markdown("Afectación estructural en escuelas, uso como refugios y continuidad escolar.")

with tab9:
    st.subheader("Salud, Salud Sexual y Reproductiva (SSR) y Crónicos")
    st.markdown("Acceso a medicamentos para hipertensión/diabetes, métodos anticonceptivos y atención materno-infantil.")

with tab10:
    st.subheader("Personas con Discapacidad y Salud Mental")
    st.markdown("Evaluación bajo el enfoque del Grupo de Washington y primeros auxilios psicológicos.")

# Footer
st.markdown("---")
st.markdown("**Sistema MEAL COOPI Venezuela** | Consorcio ÍNTEGRAS - ECHO HIP 2027")