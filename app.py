import os
import requests
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILOS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Tablero Evaluación de Necesidades - Consorcio ÍNTEGRAS (ECHO HIP 2027)",
    page_icon="📊",
    layout="wide"
)

# Paleta oficial Consorcio ÍNTEGRAS
COLOR_AZUL_OSCURO = '#08327D'
COLOR_TURQUESA = '#00C2C7'
COLOR_MORADO = '#D89FE3'
COLOR_NARANJA = '#FFB84D'
PALETA_INTEGRAS = [COLOR_AZUL_OSCURO, COLOR_TURQUESA, COLOR_MORADO, COLOR_NARANJA, '#28A745', '#E5B130']

st.markdown("""
<style>
    .titulo-principal {
        color: #08327D !important;
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

# --- DICCIONARIOS DE TRADUCCIÓN OFICIALES ---
MAPA_ESTADOS = {
    've01': 'Distrito Capital', 've07': 'Bolívar', 've10': 'Delta Amacuro',
    've15': 'Miranda', 've19': 'Sucre', 've24': 'La Guaira', 've25': 'Zulia', 've26': 'Táchira',
    'distrito capital': 'Distrito Capital', 'bolivar': 'Bolívar', 'delta amacuro': 'Delta Amacuro',
    'miranda': 'Miranda', 'sucre': 'Sucre', 'la guaira': 'La Guaira', 'zulia': 'Zulia', 'táchira': 'Táchira'
}

MAPA_SOCIOS = {
    'coopi': 'COOPI', 'hias': 'HIAS VENEZUELA', 'flm': 'FEDERACIÓN LUTERANA MUNDIAL (FLM)',
    'paluz': 'PALUZ', 'plafam': 'PLAFAM', 'otro': 'Otra organización'
}

MAPA_MUNICIPIOS = {
    've0101': 'Libertador', 've0701': 'Caroní', 've0702': 'Cedeño', 've0703': 'El Callao',
    've0704': 'Gran Sabana', 've0705': 'Heres', 've0706': 'Piar', 've0707': 'Boliv. Angostura',
    've0708': 'Roscio', 've0709': 'Sifontes', 've1001': 'Antonio Díaz', 've1002': 'Casacoima',
    've1003': 'Pedernales', 've1004': 'Tucupita', 've1501': 'Acevedo', 've1502': 'Andrés Bello',
    've1503': 'Baruta', 've1504': 'Brión', 've1505': 'Buroz', 've1506': 'Carrizal',
    've1507': 'Chacao', 've1508': 'Cristóbal Rojas', 've1509': 'El Hatillo', 've1510': 'Guaicaipuro',
    've1511': 'Independencia', 've1512': 'Lander', 've1513': 'Los Salias', 've1514': 'Páez',
    've1515': 'Paz Castillo', 've1516': 'Pedro Gual', 've1517': 'Plaza', 've1518': 'Simón Bolívar',
    've1519': 'Sucre', 've1520': 'Urdaneta', 've1521': 'Zamora', 've1901': 'Andrés Eloy Blanco',
    've1902': 'Andrés Mata', 've1903': 'Arismendi', 've1904': 'Benítez', 've1905': 'Bermúdez',
    've1906': 'Bolívar', 've1907': 'Cajigal', 've1908': 'Cruz Salmerón Acosta', 've1909': 'Libertador',
    've1910': 'Mariño', 've1911': 'Mejía', 've1912': 'Montes', 've1913': 'Ribero', 've1914': 'Sucre',
    've1915': 'Valdéz', 've2401': 'Vargas', 've2501': 'Almirante Padilla', 've2502': 'Baralt',
    've2503': 'Cabimas', 've2504': 'Catatumbo', 've2505': 'Colón', 've2506': 'Pulgar',
    've2507': 'Jesús Enrique Lossada', 've2508': 'Jesús María Semprún', 've2509': 'La Cañada de Urdaneta',
    've2510': 'Lagunillas', 've2511': 'Machiques de Perijá', 've2512': 'Mara', 've2513': 'Maracaibo',
    've2514': 'Miranda', 've2515': 'Insular Padilla', 've2516': 'Rosario de Perijá', 've2517': 'San Francisco',
    've2518': 'Santa Rita', 've2519': 'Simón Bolívar', 've2520': 'Sucre', 've2521': 'Valmore Rodríguez',
    've2601': 'Andrés Bello', 've2602': 'Antonio Rómulo Costa', 've2603': 'Ayacucho', 've2604': 'Bolívar',
    've2605': 'Cárdenas', 've2606': 'Córdoba', 've2607': 'Fernández Feo', 've2608': 'Francisco de Miranda',
    've2609': 'García de Hevia', 've2610': 'Guásimos', 've2611': 'Independencia', 've2612': 'Jáuregui',
    've2613': 'José María Vargas', 've2614': 'Junín', 've2615': 'Libertad', 've2616': 'Libertador',
    've2617': 'Lobatera', 've2618': 'Michelena', 've2619': 'Panamericano', 've2620': 'Pedro María Ureña',
    've2621': 'Rafael Urdaneta', 've2622': 'Samuel Darío Maldonado', 've2623': 'San Cristóbal',
    've2624': 'Seboruco', 've2625': 'Simón Rodríguez', 've2626': 'Sucre', 've2627': 'Torbes',
    've2628': 'Uribante', 've2629': 'Entre Ríos'
}

MAPA_PARROQUIAS = {
    've010101': 'Altagracia', 've010102': 'Antímano', 've010103': 'Candelaria',
    've010104': 'Caricuao', 've010105': 'Catedral', 've010106': 'Coche',
    've010107': 'El Junquito', 've010108': 'El Paraíso', 've010109': 'El Recreo',
    've010110': 'El Valle', 've010111': 'La Candelaria', 've010112': 'La Pastora',
    've010113': 'La Vega', 've010114': 'Macarao', 've010115': 'San Agustín',
    've010116': 'San Bernardino', 've010117': 'San José', 've010118': 'San Juan',
    've010119': 'San Pedro', 've010120': 'Santa Rosalía', 've010121': 'Santa Teresa',
    've010122': 'Sucre', 've240101': 'Caraballeda', 've240102': 'Carayaca',
    've240103': 'Catia La Mar', 've240104': 'El Junco', 've240105': 'La Guaira',
    've240106': 'Macuto', 've240107': 'Maiquetía', 've240108': 'Naiguatá',
    've240109': 'Caruao', 've240110': 'Urimare'
}

# --- PROCEDIMIENTO ROBUSTO DE NORMALIZACIÓN Y LIMPIEZA KOBO ---
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

def limpiar_codigo(val, diccionario):
    if pd.isna(val):
        return 'No especificado'
    v_str = str(val).strip().lower()
    if v_str in diccionario:
        return diccionario[v_str]
    elif v_str in ['', 'nan', 'none', 'nat']:
        return 'No especificado'
    else:
        return str(val).title()

df_clean['socio_clean'] = df_raw[col_socio].apply(lambda x: limpiar_codigo(x, MAPA_SOCIOS)).str.upper() if col_socio else 'NO ESPECIFICADO'
df_clean['estado_clean'] = df_raw[col_estado].apply(lambda x: limpiar_codigo(x, MAPA_ESTADOS)) if col_estado else 'No especificado'
df_clean['municipio_clean'] = df_raw[col_municipio].apply(lambda x: limpiar_codigo(x, MAPA_MUNICIPIOS)) if col_municipio else 'No especificado'
df_clean['parroquia_clean'] = df_raw[col_parroquia].apply(lambda x: limpiar_codigo(x, MAPA_PARROQUIAS)) if col_parroquia else 'No especificado'
df_clean['comunidad_clean'] = df_raw[col_comunidad].astype(str).str.strip() if col_comunidad else 'No especificado'
df_clean['sexo_clean'] = df_raw[col_sexo].astype(str).str.title() if col_sexo else 'No especificado'
df_clean['edu_clean'] = df_raw[col_edu].astype(str).str.title() if col_edu else 'No especificado'

cols_num_familia = ['i1', 'i2', 'i3', 'i12', 'i13', 'i14', 'i23', 'i24', 'i25', 'personas_vivienda']
for col_num in cols_num_familia:
    target_col = col_num
    if col_num not in df_clean.columns:
        match = find_col(df_clean, [col_num])
        if match:
            target_col = match
    
    if target_col in df_clean.columns:
        df_clean[col_num] = pd.to_numeric(df_clean[target_col], errors='coerce').fillna(0)
    else:
        df_clean[col_num] = 0

st.success(f"✅ Kobo normalizado con éxito. Total de registros analizados: {len(df_clean)}")

# --- SECCIÓN 1: FILTROS LATERALES EN CASCADA ---
st.sidebar.header("Filtros de Localización y Socios")

if st.sidebar.button('Actualizar Datos', use_container_width=True):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")

socios_disp = sorted(df_clean['socio_clean'].dropna().unique().tolist())
selected_socio = st.sidebar.multiselect("Organización Socio", options=socios_disp, default=socios_disp)

estados_disp = sorted(df_clean['estado_clean'].dropna().unique().tolist())
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
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Sociodemografía & Vivienda",
    "Socioeconómico & Ingresos",
    "Seguridad Alimentaria & Nutrición",
    "Acceso a Derechos",
    "Protección NNA",
    "VBG y Género",
    "Educación en Emergencias",
    "Salud & Discapacidad"
])

with tab1:
    st.subheader("Análisis Sociodemográfico y Grupo Familiar")
    
    mujeres_0_17 = df_filtered['i1'].sum()
    mujeres_18_49 = df_filtered['i2'].sum()
    mujeres_50_plus = df_filtered['i3'].sum()
    
    hombres_0_17 = df_filtered['i12'].sum()
    hombres_18_49 = df_filtered['i13'].sum()
    hombres_50_plus = df_filtered['i14'].sum()
    
    otro_0_17 = df_filtered['i23'].sum()
    otro_18_49 = df_filtered['i24'].sum()
    otro_50_plus = df_filtered['i25'].sum()

    total_mujeres = mujeres_0_17 + mujeres_18_49 + mujeres_50_plus
    total_hombres = hombres_0_17 + hombres_18_49 + hombres_50_plus
    total_niños = mujeres_0_17 + hombres_0_17 + otro_0_17
    total_otro = otro_0_17 + otro_18_49 + otro_50_plus

    c_m1, c_m2, c_m3, c_m4 = st.columns(4)
    c_m1.metric("Mujeres Totales (Familias)", f"{int(total_mujeres):,}")
    c_m2.metric("Hombres Totales (Familias)", f"{int(total_hombres):,}")
    c_m3.metric("Niños y Niñas (0-17 años)", f"{int(total_niños):,}")
    c_m4.metric("Otro Género / No Binario", f"{int(total_otro):,}")

    st.markdown("---")

    col_pyr1, col_pyr2 = st.columns(2)
    with col_pyr1:
        st.markdown("#### Pirámide Poblacional del Grupo Familiar")
        pyramid_data = pd.DataFrame({
            'Rango Etario': ['0 a 17 años', '18 a 49 años', '50+ años', '0 a 17 años', '18 a 49 años', '50+ años'],
            'Género': ['Hombre', 'Hombre', 'Hombre', 'Mujer', 'Mujer', 'Mujer'],
            'Cantidad': [-hombres_0_17, -hombres_18_49, -hombres_50_plus, mujeres_0_17, mujeres_18_49, mujeres_50_plus]
        })
        fig_pyramid = px.bar(
            pyramid_data, x='Cantidad', y='Rango Etario', color='Género', orientation='h',
            title="Distribución por Edad y Género",
            color_discrete_sequence=[COLOR_AZUL_OSCURO, COLOR_TURQUESA]
        )
        fig_pyramid.update_layout(bargap=0.1)
        st.plotly_chart(fig_pyramid, use_container_width=True)

    with col_pyr2:
        st.markdown("#### Nivel Educativo de los Participantes")
        if 'edu_clean' in df_filtered.columns:
            edu_counts = df_filtered['edu_clean'].value_counts().reset_index()
            edu_counts.columns = ['Nivel Educativo', 'Cantidad']
            fig_edu = px.bar(edu_counts, x='Nivel Educativo', y='Cantidad', color_discrete_sequence=[COLOR_TURQUESA])
            st.plotly_chart(fig_edu, use_container_width=True)

    st.markdown("---")
    
    col_v1, col_v2, col_v3, col_v4 = st.columns(4)
    
    lgbti_col = find_col(df_filtered, ['igtbiq', 'lgbti'])
    lgbti_count = df_filtered[lgbti_col].dropna().astype(str).str.lower().isin(['si', 'sí', '1', 'true']).sum() if lgbti_col else 0
    
    indigena_col = find_col(df_filtered, ['etnia_indigena', 'indigena'])
    indigena_count = df_filtered[indigena_col].dropna().count() if indigena_col else 0
    
    disc_col = find_col(df_filtered, ['discapacidad_selec', 'discapacidad'])
    disc_count = df_filtered[disc_col].dropna().count() if disc_col else 0
    
    viv_col = find_col(df_filtered, ['personas_vivienda'])
    if viv_col:
        valid_hogares = pd.to_numeric(df_filtered[viv_col], errors='coerce').fillna(0)
        valid_hogares = valid_hogares[valid_hogares > 0]
        avg_hogar = valid_hogares.mean() if not valid_hogares.empty else 0.0
    else:
        avg_hogar = 0.0

    col_v1.metric("Población LGBTIQ+", f"{int(lgbti_count):,}")
    col_v2.metric("Población Indígena", f"{int(indigena_count):,}")
    col_v3.metric("Personas con Discapacidad", f"{int(disc_count):,}")
    col_v4.metric("Promedio Personas por Hogar", f"{avg_hogar:.1f}")

with tab2:
    st.subheader("Características Socioeconómicas y Medios de Vida")
    st.markdown("Evaluación de fuentes de ingresos, impacto de la crisis económica y estrategias de afrontamiento.")

with tab3:
    st.subheader("Seguridad Alimentaria y Nutrición")
    st.markdown("Patrones de consumo alimentario, acceso a raciones y tamizaje nutricional en menores de 5 años.")

with tab4:
    st.subheader("Acceso a Derechos y Servicios")
    st.markdown("Pérdida de documentación de identidad por sismos y barreras de acceso a la asistencia humanitaria.")

with tab5:
    st.subheader("Protección de Niñas, Niños y Adolescentes (NNA)")
    st.markdown("Riesgos de protección infantil, trabajo infantil y separación en albergues temporales.")

with tab6:
    st.subheader("Violencia Basada en Género (VBG) y Enfoque de Género")
    st.markdown("Percepción de seguridad, riesgos en espacios comunitarios y barreras para la atención.")

with tab7:
    st.subheader("Educación en Emergencias (EiE)")
    st.markdown("Afectación estructural en escuelas, uso como refugios y continuidad escolar.")

with tab8:
    st.subheader("Salud, Salud Sexual y Reproductiva (SSR) y Discapacidad")
    st.markdown("Acceso a medicamentos para hipertensión/diabetes, métodos anticonceptivos y salud mental.")

# Footer
st.markdown("---")
st.markdown("**Sistema MEAL COOPI Venezuela** | Consorcio ÍNTEGRAS - ECHO HIP 2027")
