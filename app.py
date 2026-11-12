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

MAPA_EDUCACION = {
    'ninguno': 'Sin educación formal',
    'primaria_inc': 'Primaria incompleta',
    'primaria_com': 'Primaria completa',
    'secundaria_inc': 'Secundaria incompleta',
    'secundaria_com': 'Secundaria completa',
    'terciario_univ': 'Técnico superior Universitario',
    'univ_incomp': 'Universitario incompleto',
    'univ_comp': 'Universitario completo'
}

MAPA_PUEBLOS_INDIGENAS = {
    'ind_01': 'Akawayo', 'ind_02': 'Añú (Paraujano)', 'ind_03': 'Arawako', 'ind_04': 'Baniva',
    'ind_05': 'Barí', 'ind_06': 'Chaima', 'ind_07': 'Eñepá (Panare)', 'ind_08': 'Hoti',
    'ind_09': 'Jivi (Guajibo)', 'ind_10': 'Kariña', 'ind_11': 'Mapoyo', 'ind_12': 'Pemón',
    'ind_13': 'Piaroa', 'ind_14': 'Puinave', 'ind_15': 'Pumé (Yaruro)', 'ind_16': 'Sanemá',
    'ind_17': 'Sapé', 'ind_18': 'Uruak (Arutani)', 'ind_19': 'Warao', 'ind_20': 'Warekena',
    'ind_21': 'Wayúu (Guajiro)', 'ind_22': 'Yabarana', 'ind_23': 'Yanomami', 'ind_24': 'Yekuana', 'ind_25': 'Yukpa'
}

MAPA_DISCAPACIDADES = {
    'audi': 'Auditiva', 'coogni': 'Cognitiva', 'habla': 'En el habla',
    'moto': 'Motora', 'no': 'No posee', 'ns_ns': 'Ns/Nc', 'vis': 'Visual',
    'audi vis': 'Auditiva y Visual', 'moto vis': 'Motora y Visual', 'audi moto': 'Auditiva y Motora',
    'cogini vis': 'Cognitiva y Visual', 'audi habla': 'Auditiva y En el habla',
    'audi moto vis': 'Auditiva, Motora y Visual', 'audi vis habla': 'Auditiva, Visual y En el habla',
    'audi moto vis habla': 'Auditiva, Motora, Visual y En el habla', 'moto audi': 'Motora y Auditiva',
    'cogini moto': 'Cognitiva y Motora', 'cogini audi': 'Cognitiva y Auditiva'
}

MAPA_NACIONALIDAD = {
    'venezolana': 'Venezolana', 'extranjera': 'Extranjera'
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

col_nac = find_col(df_raw, ['nacionalidad'])
col_ind = find_col(df_raw, ['etnia_indigena'])
col_disc = find_col(df_raw, ['discapacidad_selec'])
col_gestantes = find_col(df_raw, ['num_gestantes'])
lgbti_col = find_col(df_raw, ['igtbiq', 'lgbti'])

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
        for k, v in [('audi', 'Auditiva'), ('moto', 'Motora'), ('vis', 'Visual'), ('coogni', 'Cognitiva'), ('habla', 'En el habla')]:
            v_str = v_str.replace(k, v)
        return v_str.title()

df_clean['socio_clean'] = df_raw[col_socio].apply(lambda x: limpiar_codigo(x, MAPA_SOCIOS)).str.upper() if col_socio else 'NO ESPECIFICADO'
df_clean['estado_clean'] = df_raw[col_estado].apply(lambda x: limpiar_codigo(x, MAPA_ESTADOS)) if col_estado else 'No especificado'
df_clean['municipio_clean'] = df_raw[col_municipio].apply(lambda x: limpiar_codigo(x, MAPA_MUNICIPIOS)) if col_municipio else 'No especificado'
df_clean['parroquia_clean'] = df_raw[col_parroquia].apply(lambda x: limpiar_codigo(x, MAPA_PARROQUIAS)) if col_parroquia else 'No especificado'
df_clean['comunidad_clean'] = df_raw[col_comunidad].astype(str).str.strip() if col_comunidad else 'No especificado'
df_clean['sexo_clean'] = df_raw[col_sexo].apply(lambda x: limpiar_codigo(x, { 'masculino': 'Hombre', 'femenino': 'Mujer' })) if col_sexo else 'No especificado'
df_clean['edu_clean'] = df_raw[col_edu].apply(lambda x: limpiar_codigo(x, MAPA_EDUCACION)) if col_edu else 'No especificado'

df_clean['nacionalidad_clean'] = df_raw[col_nac].apply(lambda x: limpiar_codigo(x, MAPA_NACIONALIDAD)) if col_nac else 'No especificado'
df_clean['pueblo_indigena_clean'] = df_raw[col_ind].apply(lambda x: limpiar_codigo(x, MAPA_PUEBLOS_INDIGENAS)) if col_ind else 'No especificado'
df_clean['discapacidad_clean'] = df_raw[col_disc].apply(lambda x: limpiar_codigo(x, MAPA_DISCAPACIDADES)) if col_disc else 'No especificado'
df_clean['gestantes_val'] = pd.to_numeric(df_raw[col_gestantes], errors='coerce').fillna(0) if col_gestantes else 0

df_clean['lgbti_clean'] = df_raw[lgbti_col].apply(lambda x: 'Sí' if str(x).strip().lower() in ['si', 'sí', '1', 'true'] else 'No') if lgbti_col else 'No'
df_clean['indigena_filtro'] = df_clean['pueblo_indigena_clean'].apply(lambda x: 'Sí (Pueblo Indígena)' if x not in ['No Especificado', 'No especificado'] else 'No')
df_clean['disc_filtro'] = df_clean['discapacidad_clean'].apply(lambda x: 'Sí (Con Discapacidad)' if x not in ['No Especificado', 'No especificado', 'No Posee', 'No posee'] else 'No')
df_clean['gestantes_filtro'] = df_clean['gestantes_val'].apply(lambda x: 'Sí (Con Gestantes)' if x > 0 else 'No')

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

# --- SECCIÓN 1: FILTROS LATERALES EN CASCADA Y LOGO DEL CONSORCIO ---
if os.path.exists("integras.jpg"):
    st.sidebar.image("integras.jpg", use_column_width=True)
else:
    st.sidebar.markdown("### Consorcio ÍNTEGRAS")

st.sidebar.markdown("---")
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

st.sidebar.markdown("---")
st.sidebar.subheader("Filtros de Vulnerabilidad")
selected_lgbti = st.sidebar.multiselect("Comunidad LGBTIQ+", options=['Sí', 'No'], default=['Sí', 'No'])
selected_indigena = st.sidebar.multiselect("Comunidad Indígena", options=['Sí (Pueblo Indígena)', 'No'], default=['Sí (Pueblo Indígena)', 'No'])
selected_disc = st.sidebar.multiselect("Personas con Discapacidad", options=['Sí (Con Discapacidad)', 'No'], default=['Sí (Con Discapacidad)', 'No'])
selected_gestantes = st.sidebar.multiselect("Mujeres Embarazadas (Gestantes)", options=['Sí (Con Gestantes)', 'No'], default=['Sí (Con Gestantes)', 'No'])

if selected_lgbti:
    df_filtered = df_filtered[df_filtered['lgbti_clean'].isin(selected_lgbti)]
if selected_indigena:
    df_filtered = df_filtered[df_filtered['indigena_filtro'].isin(selected_indigena)]
if selected_disc:
    df_filtered = df_filtered[df_filtered['disc_filtro'].isin(selected_disc)]
if selected_gestantes:
    df_filtered = df_filtered[df_filtered['gestantes_filtro'].isin(selected_gestantes)]

# Cálculo del total de participantes (suma de todo el grupo familiar)
total_participantes = (
    df_filtered['i1'].sum() + df_filtered['i2'].sum() + df_filtered['i3'].sum() +
    df_filtered['i12'].sum() + df_filtered['i13'].sum() + df_filtered['i14'].sum() +
    df_filtered['i23'].sum() + df_filtered['i24'].sum() + df_filtered['i25'].sum()
)

# Cálculo de Promedio Personas por Hogar
viv_col = find_col(df_filtered, ['personas_vivienda'])
if viv_col:
    valid_hogares = pd.to_numeric(df_filtered[viv_col], errors='coerce').fillna(0)
    valid_hogares = valid_hogares[valid_hogares > 0]
    avg_hogar = valid_hogares.mean() if not valid_hogares.empty else 0.0
else:
    avg_hogar = 0.0

# KPIs Principales (4 columnas arriba incluyendo Total Participantes y Promedio Hogar)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Encuestas Aplicadas", f"{len(df_filtered):,}")
col2.metric("Total Participantes", f"{int(total_participantes):,}")
col3.metric("Estados Monitoreados", f"{df_filtered['estado_clean'].nunique():,}")
col4.metric("Promedio Personas por Hogar", f"{avg_hogar:.1f}")

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

    total_extranjeros = (df_filtered['nacionalidad_clean'] == 'Extranjera').sum()
    total_venezolanos = (df_filtered['nacionalidad_clean'] == 'Venezolana').sum()
    total_embarazadas = df_filtered['gestantes_val'].sum()
    total_indigenas_reg = (df_filtered['pueblo_indigena_clean'] != 'No Especificado').sum()

    st.markdown("#### Indicadores Clave de Población y Vulnerabilidad")
    k_e1, k_e2, k_e3, k_e4 = st.columns(4)
    k_e1.metric("Población Venezolana", f"{int(total_venezolanos):,}")
    k_e2.metric("Población Extranjera", f"{int(total_extranjeros):,}")
    k_e3.metric("Mujeres Embarazadas (Gestantes)", f"{int(total_embarazadas):,}")
    k_e4.metric("Población Indígena Identificada", f"{int(total_indigenas_reg):,}")

    st.markdown("---")

    col_pyr1, col_pyr2 = st.columns(2)
    with col_pyr1:
        st.markdown("#### Pirámide Poblacional del Grupo Familiar")
        total_pob_fam = hombres_0_17 + hombres_18_49 + hombres_50_plus + mujeres_0_17 + mujeres_18_49 + mujeres_50_plus
        if total_pob_fam == 0: total_pob_fam = 1
        
        pyramid_data = pd.DataFrame({
            'Rango Etario': ['0 a 17 años', '18 a 49 años', '50+ años', '0 a 17 años', '18 a 49 años', '50+ años'],
            'Género': ['Hombre', 'Hombre', 'Hombre', 'Mujer', 'Mujer', 'Mujer'],
            'ValorAbs': [hombres_0_17, hombres_18_49, hombres_50_plus, mujeres_0_17, mujeres_18_49, mujeres_50_plus],
            'Cantidad': [-hombres_0_17, -hombres_18_49, -hombres_50_plus, mujeres_0_17, mujeres_18_49, mujeres_50_plus]
        })
        pyramid_data['Porcentaje'] = (pyramid_data['ValorAbs'] / total_pob_fam) * 100
        pyramid_data['TextoEtiqueta'] = pyramid_data.apply(lambda row: f"{int(row['ValorAbs']):,} ({row['Porcentaje']:.1f}%)", axis=1)

        fig_pyramid = px.bar(
            pyramid_data, x='Cantidad', y='Rango Etario', color='Género', orientation='h',
            text='TextoEtiqueta',
            title="Distribución por Edad y Género",
            color_discrete_sequence=[COLOR_AZUL_OSCURO, COLOR_TURQUESA]
        )
        fig_pyramid.update_traces(textposition='outside')
        fig_pyramid.update_layout(bargap=0.1, uniformtext_minsize=8, uniformtext_mode='hide')
        st.plotly_chart(fig_pyramid, use_container_width=True)

    with col_pyr2:
        st.markdown("#### Nivel Educativo de los Participantes")
        if 'edu_clean' in df_filtered.columns:
            edu_counts = df_filtered['edu_clean'].value_counts().reset_index()
            edu_counts.columns = ['Nivel Educativo', 'Cantidad']
            total_edu = edu_counts['Cantidad'].sum()
            if total_edu == 0: total_edu = 1
            edu_counts['Porcentaje'] = (edu_counts['Cantidad'] / total_edu) * 100
            edu_counts['TextoEtiqueta'] = edu_counts.apply(lambda row: f"{int(row['Cantidad']):,} ({row['Porcentaje']:.1f}%)", axis=1)

            fig_edu = px.bar(
                edu_counts, x='Nivel Educativo', y='Cantidad',
                text='TextoEtiqueta',
                color_discrete_sequence=[COLOR_TURQUESA]
            )
            fig_edu.update_traces(textposition='outside')
            fig_edu.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=-30)
            st.plotly_chart(fig_edu, use_container_width=True)

    st.markdown("---")

    # Gráficos de Pueblos Indígenas y Principales Discapacidades optimizados
    col_ind_g, col_disc_g = st.columns(2)
    
    with col_ind_g:
        st.markdown("#### Principales Pueblos Indígenas")
        df_ind = df_filtered[~df_filtered['pueblo_indigena_clean'].isin(['No Especificado', 'No especificado'])]
        if not df_ind.empty:
            ind_counts = df_ind['pueblo_indigena_clean'].value_counts().reset_index()
            ind_counts.columns = ['Pueblo Indígena', 'Cantidad']
            tot_ind = ind_counts['Cantidad'].sum()
            ind_counts['Porcentaje'] = (ind_counts['Cantidad'] / (tot_ind if tot_ind > 0 else 1)) * 100
            ind_counts['Etiqueta'] = ind_counts.apply(lambda r: f"{int(r['Cantidad']):,} ({r['Porcentaje']:.1f}%)", axis=1)
            
            fig_ind = px.bar(ind_counts, x='Cantidad', y='Pueblo Indígena', orientation='h', text='Etiqueta', color_discrete_sequence=[COLOR_AZUL_OSCURO])
            fig_ind.update_traces(textposition='outside')
            st.plotly_chart(fig_ind, use_container_width=True)
        else:
            st.info("No hay registros de pueblos indígenas para los filtros seleccionados.")

    with col_disc_g:
        st.markdown("#### Principales Discapacidades (Top 5)")
        excluir_disc = ['No Especificado', 'No especificado', 'No Posee', 'No posee', 'Ns/Nc', 'Ns/Nc']
        df_disc = df_filtered[~df_filtered['discapacidad_clean'].isin(excluir_disc)]
        if not df_disc.empty:
            disc_counts = df_disc['discapacidad_clean'].value_counts().head(5).reset_index()
            disc_counts.columns = ['Tipo de Discapacidad', 'Cantidad']
            tot_disc = disc_counts['Cantidad'].sum()
            disc_counts['Porcentaje'] = (disc_counts['Cantidad'] / (tot_disc if tot_disc > 0 else 1)) * 100
            disc_counts['Etiqueta'] = disc_counts.apply(lambda r: f"{int(r['Cantidad']):,} ({r['Porcentaje']:.1f}%)", axis=1)
            
            fig_disc = px.bar(disc_counts, x='Cantidad', y='Tipo de Discapacidad', orientation='h', text='Etiqueta', color_discrete_sequence=[COLOR_TURQUESA])
            fig_disc.update_traces(textposition='outside')
            st.plotly_chart(fig_disc, use_container_width=True)
        else:
            st.info("No hay registros de discapacidad para los filtros seleccionados.")

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
