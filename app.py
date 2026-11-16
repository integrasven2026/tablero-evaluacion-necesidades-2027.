import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Configuración inicial de la página
st.set_page_config(
    page_title="Tablero Evaluación de Necesidades - ECHO HIP 2027",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .titulo-principal {
        color: #08327D !important;
        font-weight: 800 !important;
        font-size: 1.7rem !important;
        margin-bottom: 0px !important;
    }
    .stMetric {
        background-color: #F4F7FC;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #08327D;
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
            response = requests.get(url, headers=headers, timeout=20)
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                all_results.extend(results)
                url = data.get('next')
            else:
                st.error(f"Error HTTP {response.status_code} al conectar con KoboToolbox.")
                break
        if all_results:
            return pd.DataFrame(all_results)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error de conexión con KoboToolbox: {e}")
        return pd.DataFrame()

df_raw = load_kobo_data()

# Título principal
st.markdown("<h1 class='titulo-principal'>📊 Tablero Dinámico de Evaluación de Necesidades - ECHO HIP 2027</h1>", unsafe_allow_html=True)
st.markdown("**Consorcio ÍNTEGRAS:** COOPI, HIAS, FLM, PLAFAM, PALUZ | Monitoreo Multisectorial Post-Sismos y Crisis Estructural")
st.divider()

if df_raw.empty:
    st.error("⚠️ No se pudieron extraer datos de la API de KoboToolbox. Verifica el token o la conexión.")
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
    've0101': 'Libertador',
    've0701': 'Caroní', 've0702': 'Cedeño', 've0703': 'El Callao',
    've0704': 'Gran Sabana', 've0705': 'Heres', 've0706': 'Piar', 've0707': 'Boliv. Angostura',
    've0708': 'Roscio', 've0709': 'Sifontes',
    've1001': 'Antonio Díaz', 've1002': 'Casacoima', 've1003': 'Pedernales', 've1004': 'Tucupita',
    've1501': 'Acevedo', 've1502': 'Andrés Bello', 've1503': 'Baruta', 've1504': 'Brión',
    've1505': 'Buroz', 've1506': 'Carrizal', 've1507': 'Chacao', 've1508': 'Cristóbal Rojas',
    've1509': 'El Hatillo', 've1510': 'Guaicaipuro', 've1511': 'Independencia', 've1512': 'Lander',
    've1513': 'Los Salias', 've1514': 'Páez', 've1515': 'Paz Castillo', 've1516': 'Pedro Gual',
    've1517': 'Plaza', 've1518': 'Simón Bolívar', 've1519': 'Sucre', 've1520': 'Urdaneta', 've1521': 'Zamora',
    've1901': 'Andrés Eloy Blanco', 've1902': 'Andrés Mata', 've1903': 'Arismendi', 've1904': 'Benítez',
    've1905': 'Bermúdez', 've1906': 'Bolívar', 've1907': 'Cajigal', 've1908': 'Cruz Salmerón Acosta',
    've1909': 'Libertador', 've1910': 'Mariño', 've1911': 'Mejía', 've1912': 'Montes',
    've1913': 'Ribero', 've1914': 'Sucre', 've1915': 'Valdéz',
    # La Guaira (Vargas y subdivisiones parroquiales codificadas a 6 dígitos en Kobo)
    've2401': 'Vargas (Caraballeda)',
    've2402': 'Carayaca',
    've2403': 'Catia La Mar',
    've2404': 'El Junko',
    've2405': 'La Guaira',
    've2406': 'Macuto',
    've2407': 'Maiquetía',
    've2408': 'Naiguatá',
    've2409': 'Caruao',
    've2410': 'Urimare',
    've2411': 'Carlos Soublette',
    # Zulia
    've2501': 'Almirante Padilla', 've2502': 'Baralt', 've2503': 'Cabimas', 've2504': 'Catatumbo',
    've2505': 'Colón', 've2506': 'Pulgar', 've2507': 'Jesús Enrique Lossada', 've2508': 'Jesús María Semprún',
    've2509': 'La Cañada de Urdaneta', 've2510': 'Lagunillas', 've2511': 'Machiques de Perijá', 've2512': 'Mara',
    've2513': 'Maracaibo', 've2514': 'Miranda', 've2515': 'Insular Padilla', 've2516': 'Rosario de Perijá',
    've2517': 'San Francisco', 've2518': 'Santa Rita', 've2519': 'Simón Bolívar', 've2520': 'Sucre', 've2521': 'Valmore Rodríguez',
    # Táchira
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
    've010122': 'Sucre',
    've240101': 'Caraballeda', 've240102': 'Carayaca', 've240103': 'Catia La Mar',
    've240104': 'El Junko', 've240105': 'La Guaira', 've240106': 'Macuto',
    've240107': 'Maiquetía', 've240108': 'Naiguatá', 've240109': 'Caruao',
    've240110': 'Urimare', 've240111': 'Carlos Soublette'
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

col_tenencia = find_col(df_raw, ['22', 'tenencia', 'propiedad', 'habita', 'vivienda'])
col_cuartos = find_col(df_raw, ['cuartos', 'habitaciones', 'dormir'])
col_personas_viv = find_col(df_raw, ['personas_vivienda', 'total_personas'])

col_agua_fuente = find_col(df_raw, ['26', 'fuentes_de_agua', 'principales_fuentes_de_agua', 'fuente_agua'])
col_agua_frec = find_col(df_raw, ['27', 'frecuencia', 'frecuencia_reciben_agua', 'frecuencia_servicio_agua'])
col_agua_suf = find_col(df_raw, ['suficiente_agua', 'agua_suficiente'])
col_agua_trat = find_col(df_raw, ['tratamiento_agua', 'trata_agua'])
col_jabon = find_col(df_raw, ['acceso_jabon', 'jabon_manos'])
col_basura = find_col(df_raw, ['disposicion_basura', 'desecho_basura'])

df_clean = df_raw.copy()

def limpiar_codigo(val, diccionario, diccionario_respaldo=None):
    if pd.isna(val):
        return 'No especificado'
    v_str = str(val).strip().lower()
    if v_str in diccionario:
        return diccionario[v_str]
    elif diccionario_respaldo and v_str in diccionario_respaldo:
        return diccionario_respaldo[v_str]
    elif v_str in ['', 'nan', 'none', 'nat']:
        return 'No especificado'
    else:
        for k, v in [('audi', 'Auditiva'), ('moto', 'Motora'), ('vis', 'Visual'), ('coogni', 'Cognitiva'), ('habla', 'En el habla')]:
            v_str = v_str.replace(k, v)
        return v_str.title()

def limpiar_texto_simple(col_name):
    if col_name and col_name in df_raw.columns:
        return df_raw[col_name].fillna('No especificado').astype(str).str.strip().str.replace('_', ' ').str.capitalize()
    return pd.Series(['No especificado'] * len(df_raw))

df_clean['socio_clean'] = df_raw[col_socio].apply(lambda x: limpiar_codigo(x, MAPA_SOCIOS)).str.upper() if col_socio else 'NO ESPECIFICADO'
df_clean['estado_clean'] = df_raw[col_estado].apply(lambda x: limpiar_codigo(x, MAPA_ESTADOS)) if col_estado else 'No especificado'
df_clean['municipio_clean'] = df_raw[col_municipio].apply(lambda x: limpiar_codigo(x, MAPA_MUNICIPIOS, MAPA_PARROQUIAS)) if col_municipio else 'No especificado'
df_clean['parroquia_clean'] = df_raw[col_parroquia].apply(lambda x: limpiar_codigo(x, MAPA_PARROQUIAS, MAPA_MUNICIPIOS)) if col_parroquia else 'No especificado'
df_clean['comunidad_clean'] = df_raw[col_comunidad].fillna('No especificado').astype(str).str.strip() if col_comunidad else 'No especificado'
df_clean['sexo_clean'] = df_raw[col_sexo].apply(lambda x: limpiar_codigo(x, {'masculino': 'Hombre', 'femenino': 'Mujer', 'hombre': 'Hombre', 'mujer': 'Mujer'})) if col_sexo else 'No especificado'
df_clean['edu_clean'] = df_raw[col_edu].apply(lambda x: limpiar_codigo(x, MAPA_EDUCACION)) if col_edu else 'No especificado'

df_clean['nacionalidad_clean'] = df_raw[col_nac].apply(lambda x: limpiar_codigo(x, MAPA_NACIONALIDAD)) if col_nac else 'No especificado'
df_clean['pueblo_indigena_clean'] = df_raw[col_ind].apply(lambda x: limpiar_codigo(x, MAPA_PUEBLOS_INDIGENAS)) if col_ind else 'No especificado'
df_clean['discapacidad_clean'] = df_raw[col_disc].apply(lambda x: limpiar_codigo(x, MAPA_DISCAPACIDADES)) if col_disc else 'No especificado'
df_clean['gestantes_val'] = pd.to_numeric(df_raw[col_gestantes], errors='coerce').fillna(0) if col_gestantes else 0
df_clean['personas_viv_val'] = pd.to_numeric(df_raw[col_personas_viv], errors='coerce').fillna(0) if col_personas_viv else 0
df_clean['cuartos_val'] = pd.to_numeric(df_raw[col_cuartos], errors='coerce').fillna(0) if col_cuartos else 0

df_clean['lgbti_clean'] = df_raw[lgbti_col].apply(lambda x: 'Sí' if str(x).strip().lower() in ['si', 'sí', '1', 'true'] else 'No') if lgbti_col else 'No'
df_clean['indigena_filtro'] = df_clean['pueblo_indigena_clean'].apply(lambda x: 'Sí (Pueblo Indígena)' if x not in ['No Especificado', 'No especificado'] else 'No')
df_clean['disc_filtro'] = df_clean['discapacidad_clean'].apply(
    lambda x: 'Sí (Con Discapacidad)' if x not in ['No posee', 'Ns/Nc', 'No especificado', 'No Especificado'] else 'No'
)

# Columnas Vivienda y WASH limpias
df_clean['tenencia_clean'] = limpiar_texto_simple(col_tenencia)
df_clean['agua_fuente_clean'] = limpiar_texto_simple(col_agua_fuente)
df_clean['agua_frec_clean'] = limpiar_texto_simple(col_agua_frec)
df_clean['agua_suf_clean'] = limpiar_texto_simple(col_agua_suf)
df_clean['agua_trat_clean'] = limpiar_texto_simple(col_agua_trat)
df_clean['jabon_clean'] = limpiar_texto_simple(col_jabon)
df_clean['basura_clean'] = limpiar_texto_simple(col_basura)

# --- BARRA LATERAL DE FILTROS ---
st.sidebar.header("🔍 Filtros del Tablero")
if st.sidebar.button("🔄 Actualizar datos de Kobo"):
    st.cache_data.clear()
    st.rerun()

socios_disp = sorted(df_clean['socio_clean'].unique())
sel_socios = st.sidebar.multiselect("Socio Implementador", socios_disp, default=socios_disp)

estados_disp = sorted(df_clean['estado_clean'].unique())
sel_estados = st.sidebar.multiselect("Estado", estados_disp, default=estados_disp)

df_temp = df_clean[df_clean['socio_clean'].isin(sel_socios) & df_clean['estado_clean'].isin(sel_estados)]
municipios_disp = sorted(df_temp['municipio_clean'].unique())
sel_municipios = st.sidebar.multiselect("Municipio", municipios_disp, default=municipios_disp)

sel_disc = st.sidebar.selectbox("Enfoque Discapacidad", ["Todos", "Sí (Con Discapacidad)", "No"])
sel_ind = st.sidebar.selectbox("Población Indígena", ["Todos", "Sí (Pueblo Indígena)", "No"])

# Aplicar filtros
df_filtered = df_temp[df_temp['municipio_clean'].isin(sel_municipios)].copy()
if sel_disc != "Todos":
    df_filtered = df_filtered[df_filtered['disc_filtro'] == sel_disc]
if sel_ind != "Todos":
    df_filtered = df_filtered[df_filtered['indigena_filtro'] == sel_ind]

if df_filtered.empty:
    st.warning("⚠️ No hay registros que coincidan con los filtros seleccionados.")
    st.stop()

# --- TARJETAS KPI PRINCIPALES ---
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("📋 Encuestas Realizadas", f"{len(df_filtered):,}")
with col2:
    total_pers = int(df_filtered['personas_viv_val'].sum())
    st.metric("👥 Personas en Hogares", f"{total_pers:,}" if total_pers > 0 else "N/D")
with col3:
    total_gest = int(df_filtered['gestantes_val'].sum())
    st.metric("🤰 Mujeres Gestantes", f"{total_gest:,}")
with col4:
    total_disc = (df_filtered['disc_filtro'] == 'Sí (Con Discapacidad)').sum()
    st.metric("♿ Hogares c/ Discapacidad", f"{total_disc:,}")
with col5:
    total_ind = (df_filtered['indigena_filtro'] == 'Sí (Pueblo Indígena)').sum()
    st.metric("🪶 Población Indígena", f"{total_ind:,}")

st.markdown("---")

# --- PESTAÑAS DEL TABLERO ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📍 Cobertura y Demografía",
    "🏠 Vivienda y Habitabilidad",
    "💧 Agua, Saneamiento e Higiene (WASH)",
    "📑 Base de Datos"
])

# TAB 1: COBERTURA Y DEMOGRAFÍA
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Encuestas por Socio Implementador")
        fig_socio = px.bar(
            df_filtered['socio_clean'].value_counts().reset_index(),
            x='socio_clean', y='count', text_auto=True,
            labels={'socio_clean': 'Socio', 'count': 'Encuestas'},
            color_discrete_sequence=['#08327D']
        )
        st.plotly_chart(fig_socio, use_container_width=True)

    with c2:
        st.subheader("Distribución Geográfica por Estado")
        fig_estado = px.bar(
            df_filtered['estado_clean'].value_counts().reset_index(),
            x='count', y='estado_clean', orientation='h', text_auto=True,
            labels={'estado_clean': 'Estado', 'count': 'Encuestas'},
            color_discrete_sequence=['#1E62D0']
        )
        fig_estado.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_estado, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Distribución por Sexo Biológico")
        fig_sexo = px.pie(
            df_filtered, names='sexo_clean', hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_sexo, use_container_width=True)

    with c4:
        st.subheader("Nivel Educativo")
        fig_edu = px.bar(
            df_filtered['edu_clean'].value_counts().reset_index(),
            x='count', y='edu_clean', orientation='h', text_auto=True,
            labels={'edu_clean': 'Nivel Educativo', 'count': 'Cantidad'},
            color_discrete_sequence=['#2B8CBE']
        )
        fig_edu.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_edu, use_container_width=True)

    c5, c6 = st.columns(2)
    with c5:
        st.subheader("Tipos de Discapacidad Reportados")
        df_disc_only = df_filtered[df_filtered['disc_filtro'] == 'Sí (Con Discapacidad)']
        if not df_disc_only.empty:
            fig_disc = px.bar(
                df_disc_only['discapacidad_clean'].value_counts().reset_index(),
                x='count', y='discapacidad_clean', orientation='h', text_auto=True,
                labels={'discapacidad_clean': 'Discapacidad', 'count': 'Cantidad'},
                color_discrete_sequence=['#D95F02']
            )
            fig_disc.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_disc, use_container_width=True)
        else:
            st.info("Sin reportes de discapacidad en la selección actual.")

    with c6:
        st.subheader("Pueblos Indígenas Identificados")
        df_ind_only = df_filtered[df_filtered['indigena_filtro'] == 'Sí (Pueblo Indígena)']
        if not df_ind_only.empty:
            fig_ind = px.bar(
                df_ind_only['pueblo_indigena_clean'].value_counts().reset_index(),
                x='count', y='pueblo_indigena_clean', orientation='h', text_auto=True,
                labels={'pueblo_indigena_clean': 'Pueblo Indígena', 'count': 'Cantidad'},
                color_discrete_sequence=['#1B9E77']
            )
            fig_ind.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_ind, use_container_width=True)
        else:
            st.info("Sin reportes de población indígena en la selección actual.")

# TAB 2: VIVIENDA
with tab2:
    v1, v2 = st.columns(2)
    with v1:
        st.subheader("Tenencia de la Vivienda")
        fig_ten = px.pie(
            df_filtered, names='tenencia_clean', hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_ten, use_container_width=True)

    with v2:
        st.subheader("Top 10 Municipios Evaluados")
        fig_mun = px.bar(
            df_filtered['municipio_clean'].value_counts().head(10).reset_index(),
            x='count', y='municipio_clean', orientation='h', text_auto=True,
            labels={'municipio_clean': 'Municipio / Parroquia', 'count': 'Encuestas'},
            color_discrete_sequence=['#08327D']
        )
        fig_mun.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_mun, use_container_width=True)

# TAB 3: WASH
with tab3:
    w1, w2 = st.columns(2)
    with w1:
        st.subheader("Principales Fuentes de Agua")
        fig_agua = px.bar(
            df_filtered['agua_fuente_clean'].value_counts().head(10).reset_index(),
            x='count', y='agua_fuente_clean', orientation='h', text_auto=True,
            labels={'agua_fuente_clean': 'Fuente de Agua', 'count': 'Hogares'},
            color_discrete_sequence=['#0077B6']
        )
        fig_agua.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_agua, use_container_width=True)

    with w2:
        st.subheader("Frecuencia del Servicio de Agua")
        fig_frec = px.bar(
            df_filtered['agua_frec_clean'].value_counts().reset_index(),
            x='count', y='agua_frec_clean', orientation='h', text_auto=True,
            labels={'agua_frec_clean': 'Frecuencia', 'count': 'Hogares'},
            color_discrete_sequence=['#00B4D8']
        )
        fig_frec.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_frec, use_container_width=True)

    w3, w4 = st.columns(2)
    with w3:
        st.subheader("Acceso a Jabón para Lavado de Manos")
        fig_jab = px.pie(
            df_filtered, names='jabon_clean', hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_jab, use_container_width=True)

    with w4:
        st.subheader("Disposición de Basura / Desechos")
        fig_bas = px.bar(
            df_filtered['basura_clean'].value_counts().head(8).reset_index(),
            x='count', y='basura_clean', orientation='h', text_auto=True,
            labels={'basura_clean': 'Método de Disposición', 'count': 'Hogares'},
            color_discrete_sequence=['#48CAE4']
        )
        fig_bas.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_bas, use_container_width=True)

# TAB 4: BASE DE DATOS Y DESCARGA
with tab4:
    st.subheader("Vista Previa de Registros Limpios")
    cols_mostrar = [
        'socio_clean', 'estado_clean', 'municipio_clean', 'parroquia_clean',
        'comunidad_clean', 'sexo_clean', 'edu_clean', 'nacionalidad_clean',
        'discapacidad_clean', 'pueblo_indigena_clean', 'gestantes_val'
    ]
    st.dataframe(df_filtered[cols_mostrar], use_container_width=True)

    csv_data = df_filtered[cols_mostrar].to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Descargar Datos Filtrados (CSV)",
        data=csv_data,
        file_name="evaluacion_necesidades_echo_hip_2027.csv",
        mime="text/csv"
    )
