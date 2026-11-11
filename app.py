import os
import requests
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILOS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Tablero Evaluación de Necesidades - Consorcio ÍNTEGRAS (ECHO HIP 2027)",
    page_icon="📊",
    layout="wide"
)

COLOR_AZUL_COOPI = '#0072CE'
COLOR_VERDE_COOPI = '#28A745'
PALETA_COOPI = [COLOR_AZUL_COOPI, COLOR_VERDE_COOPI, '#17C3B2', '#D89FE3', '#E5B130', '#08327D']

st.markdown("""
<style>
    .titulo-principal {
        color: #0072CE !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Constantes de conexión API KoboToolbox (Europa)
KOBO_URL = "https://eu.kobotoolbox.org/api/v2/assets/aDLGup9ApcZVFUy8JTo7qZ/data/?format=json"
TOKEN = "a18c017a2e697f4ea1272375dae261ccec6b19d7"

@st.cache_data(ttl=300)
def load_kobo_data():
    headers = {"Authorization": f"Token {TOKEN}"}
    all_results = []
    url = KOBO_URL
    try:
        while url:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                all_results.extend(results)
                url = data.get('next')
            else:
                break
        if all_results:
            return pd.DataFrame(all_results)
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

df_raw = load_kobo_data()

# Título principal
st.markdown("<h1 class='titulo-principal'>📊 Tablero Dinámico de Evaluación de Necesidades - ECHO HIP 2027</h1>", unsafe_allow_html=True)
st.markdown("**Consorcio ÍNTEGRAS:** COOPI, HIAS, FLM, PLAFAM, PALUZ | Monitoreo Multisectorial Post-Sismos y Crisis Estructural")

if df_raw.empty:
    st.error("⚠️ No se pudieron extraer datos de la API de KoboToolbox.")
    st.stop()

# --- CARGAR DICCIONARIOS DESDE LA HOJA CHOICES ---
@st.cache_data
def cargar_diccionarios_kobo():
    excel_path = 'aDLGup9ApcZVFUy8JTo7qZ(3).xlsx'
    if os.path.exists(excel_path):
        try:
            choices_df = pd.read_excel(excel_path, sheet_name='choices')
            est_dict = dict(zip(choices_df[choices_df['list_name']=='Estado']['name'].astype(str).str.strip(), choices_df[choices_df['list_name']=='Estado']['label']))
            mun_dict = dict(zip(choices_df[choices_df['list_name']=='Municipio']['name'].astype(str).str.strip(), choices_df[choices_df['list_name']=='Municipio']['label']))
            par_dict = dict(zip(choices_df[choices_df['list_name']=='Parroquia']['name'].astype(str).str.strip(), choices_df[choices_df['list_name']=='Parroquia']['label']))
            soc_dict = dict(zip(choices_df[choices_df['list_name']=='socio']['name'].astype(str).str.strip(), choices_df[choices_df['list_name']=='socio']['label']))
            return est_dict, mun_dict, par_dict, soc_dict
        except Exception:
            pass
    return {}, {}, {}, {}

est_dict, mun_dict, par_dict, soc_dict = cargar_diccionarios_kobo()

# --- LIMPIEZA Y MAPEO INTELIGENTE DE COLUMNAS ---
def find_col(df, keywords):
    for col in df.columns:
        for kw in keywords:
            if kw.lower() in col.lower():
                return col
    return None

col_socio = find_col(df_raw, ['socio'])
col_estado = find_col(df_raw, ['estado'])
col_municipio = find_col(df_raw, ['municipio'])
col_parroquia = find_col(df_raw, ['parroquia'])
col_comunidad = find_col(df_raw, ['comunidad'])
col_sexo = find_col(df_raw, ['sexo', 'biologico'])
col_edu = find_col(df_raw, ['nivel_educativo', 'educacion'])

df_clean = df_raw.copy()

def limpiar_y_mapear(serie, diccionario):
    if serie is None:
        return pd.Series(['No especificado'] * len(df_raw))
    
    res = []
    for val in serie:
        v_str = str(val).strip()
        # Si está en el diccionario de códigos de Kobo, lo traducimos
        if v_str in diccionario:
            res.append(str(diccionario[v_str]))
        elif v_str.lower() in ['nan', 'none', '', 'nat']:
            res.append('No especificado')
        else:
            # Si ya venía en texto plano, lo conservamos capitalizado
            res.append(v_str.title() if not v_str.isupper() else v_str)
    return pd.Series(res)

df_clean['socio_clean'] = limpiar_y_mapear(df_raw[col_socio] if col_socio else None, soc_dict).str.upper()
df_clean['estado_clean'] = limpiar_y_mapear(df_raw[col_estado] if col_estado else None, est_dict)
df_clean['municipio_clean'] = limpiar_y_mapear(df_raw[col_municipio] if col_municipio else None, mun_dict)
df_clean['parroquia_clean'] = limpiar_y_mapear(df_raw[col_parroquia] if col_parroquia else None, par_dict)
df_clean['comunidad_clean'] = df_raw[col_comunidad].astype(str).str.strip() if col_comunidad else 'No especificado'
df_clean['sexo_clean'] = df_raw[col_sexo].astype(str).str.title() if col_sexo else 'No especificado'
df_clean['edu_clean'] = df_raw[col_edu].astype(str).str.title() if col_edu else 'No especificado'

st.success(f"✅ Kobo sincronizado con éxito. Total de registros analizados: {len(df_clean)}")

# --- PROCESAMIENTO DE COORDENADAS GPS ---
gps_col = find_col(df_raw, ['ubicacion_gps', 'geopoint', 'gps'])
if gps_col:
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
    df_clean['lat'] = df_raw[gps_col].apply(parse_lat)
    df_clean['lon'] = df_raw[gps_col].apply(parse_lon)
else:
    df_clean['lat'] = 10.4806
    df_clean['lon'] = -66.9036

COORD_MUNICIPIOS_DEF = {
    'Libertador': [10.50, -66.91], 'Sucre': [10.48, -66.81], 'Chacao': [10.49, -66.85],
    'Baruta': [10.44, -66.87], 'El Hatillo': [10.42, -66.82], 'Vargas': [10.60, -66.93],
    'Carayaca': [10.60, -67.03], 'Urimare': [10.59, -66.98]
}

# --- SECCIÓN 1: FILTROS LATERALES EN CASCADA ---
st.sidebar.header("🎛️ Filtros de Localización y Socios")

if st.sidebar.button('🔄 Actualizar Datos', use_container_width=True):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")

socios_disp = sorted(df_clean['socio_clean'][df_clean['socio_clean'] != 'NO ESPECIFICADO'].dropna().unique().tolist())
if not socios_disp: socios_disp = sorted(df_clean['socio_clean'].dropna().unique().tolist())
selected_socio = st.sidebar.multiselect("Organización Socio", options=socios_disp, default=socios_disp)

estados_disp = sorted(df_clean['estado_clean'][df_clean['estado_clean'] != 'No Especificado'].dropna().unique().tolist())
if not estados_disp: estados_disp = sorted(df_clean['estado_clean'].dropna().unique().tolist())
selected_estado = st.sidebar.multiselect("Estado", options=estados_disp, default=estados_disp)

df_filtered = df_clean.copy()
if selected_socio:
    df_filtered = df_filtered[df_filtered['socio_clean'].isin(selected_socio)]
if selected_estado:
    df_filtered = df_filtered[df_filtered['estado_clean'].isin(selected_estado)]

municipios_disp = sorted(df_filtered['municipio_clean'].dropna().unique().tolist())
selected_municipio = st.sidebar.multiselect("Municipio", options=municipios_disp, default=municipios_disp)
if selected_municipio:
    df_filtered = df_filtered[df_filtered['municipio_clean'].isin(selected_municipio)]

parroquias_disp = sorted(df_filtered['parroquia_clean'].dropna().unique().tolist())
selected_parroquia = st.sidebar.multiselect("Parroquia", options=parroquias_disp, default=parroquias_disp)
if selected_parroquia:
    df_filtered = df_filtered[df_filtered['parroquia_clean'].isin(selected_parroquia)]

# KPIs Principales
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Encuestas Aplicadas", f"{len(df_filtered):,}")
col2.metric("Estados Monitoreados", f"{df_filtered['estado_clean'].nunique():,}")
col3.metric("Municipios Afectados", f"{df_filtered['municipio_clean'].nunique():,}")
col4.metric("Comunidades / Albergues", f"{df_filtered['comunidad_clean'].nunique():,}")

st.markdown("---")

# --- PESTAÑAS DE ANÁLISIS MULTISECTORIAL ---
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
    mapa = folium.Map(location=[10.48, -66.90], zoom_start=9, tiles='OpenStreetMap')
    
    map_df = df_filtered.copy()
    if not map_df.empty:
        for _, row in map_df.iterrows():
            lat = row['lat']
            lon = row['lon']
            if pd.isna(lat) or pd.isna(lon) or (lat == 10.4806 and lon == -66.9036):
                muni_name = str(row['municipio_clean'])
                default_coord = COORD_MUNICIPIOS_DEF.get(muni_name, [10.48, -66.90])
                lat = default_coord[0] + np.random.uniform(-0.02, 0.02)
                lon = default_coord[1] + np.random.uniform(-0.02, 0.02)
            
            comunidad = row['comunidad_clean']
            muni = row['municipio_clean']
            est = row['estado_clean']
            socio = row['socio_clean']
            
            popup_html = f"""
            <div style='font-family: sans-serif; font-size: 12px; width: 220px;'>
                <b>Socio:</b> {socio}<br>
                <b>Estado:</b> {est}<br>
                <b>Municipio:</b> {muni}<br>
                <b>Comunidad:</b> {comunidad}
            </div>
            """
            folium.CircleMarker(
                location=[lat, lon],
                radius=6,
                popup=folium.Popup(popup_html, max_width=240),
                color=COLOR_AZUL_COOPI,
                fill=True,
                fill_color=COLOR_AZUL_COOPI,
                fill_opacity=0.7
            ).add_to(mapa)
    
    st_folium(mapa, width='100%', height=450)

with tab2:
    st.subheader("Condiciones Sociodemográficas, Vivienda y WASH")
    c1, c2 = st.columns(2)
    with c1:
        sex_counts = df_filtered['sexo_clean'].value_counts().reset_index()
        sex_counts.columns = ['sexo', 'count']
        fig = px.pie(sex_counts, names='sexo', values='count', title="Distribución por Sexo Biológico", hole=0.4, color_discrete_sequence=PALETA_COOPI)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        edu_counts = df_filtered['edu_clean'].value_counts().reset_index()
        edu_counts.columns = ['nivel', 'count']
        fig = px.bar(edu_counts, x='nivel', y='count', title="Nivel Educativo Principal", color_discrete_sequence=[COLOR_AZUL_COOPI])
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
