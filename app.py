import streamlit as st
import pandas as pd
import plotly.express as px
import os
import folium
from streamlit_folium import st_folium
import numpy as np

# Configuración inicial de la página
st.set_page_config(
    page_title="Tablero Evaluación de Necesidades - ECHO HIP 2027",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de colores oficial del Consorcio ÍNTEGRAS basada en su logotipo
INTEGRAS_COLORS = ['#08327D', '#1E62D0', '#00BCD4', '#F4A261', '#D8B4E2', '#2A9D8F', '#E76F51']

# Estilos CSS institucionales (Consorcio ÍNTEGRAS)
st.markdown("""
<style>
    .header-container {
        background: linear-gradient(90deg, #08327D 0%, #1E62D0 100%);
        padding: 20px 25px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .titulo-principal {
        color: white !important;
        font-weight: 800 !important;
        font-size: 1.6rem !important;
        margin: 0px !important;
    }
    .sub-titulo {
        color: #E2E8F0 !important;
        font-size: 0.95rem !important;
        margin-top: 5px !important;
    }
    .stMetric {
        background-color: #F4F7FC;
        padding: 12px;
        border-radius: 10px;
        border-left: 5px solid #08327D;
    }
</style>
""", unsafe_allow_html=True)

# Carga de datos desde el archivo Excel local estandarizado
EXCEL_FILE = "BBDD_ECHO_HIP_2027_Estandarizada.xlsx"

@st.cache_data(ttl=300)
def load_excel_data():
    try:
        df = pd.read_excel(EXCEL_FILE)
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo Excel '{EXCEL_FILE}': {e}")
        return pd.DataFrame()

df_raw = load_excel_data()

# Encabezado institucional con contenedor de Logo e Identidad Consorcio ÍNTEGRAS
col_head1, col_head2 = st.columns([5, 1])
with col_head1:
    st.markdown("""
    <div class="header-container" style="border: none; margin-bottom: 0px;">
        <div>
            <h1 class="titulo-principal">Tablero Dinámico de Evaluación de Necesidades - ECHO HIP 2027</h1>
            <div class="sub-titulo">Consorcio ÍNTEGRAS: COOPI, HIAS, FLM, PLAFAM, PALUZ | Monitoreo Multisectorial Post-Sismos y Crisis Estructural</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_head2:
    if os.path.exists("integras.jpg"):
        st.image("integras.jpg", width=150)
    else:
        st.markdown("<div style='background: white; color: #08327D; padding: 15px; border-radius: 6px; text-align: center; font-weight: bold;'>LOGO ÍNTEGRAS</div>", unsafe_allow_html=True)

st.markdown("---")

if df_raw.empty:
    st.error(f"⚠️ No se pudieron cargar datos desde el archivo '{EXCEL_FILE}'. Verifica que esté subido correctamente al repositorio.")
    st.stop()

# --- DICCIONARIOS DE TRADUCCIÓN Y MAPEO OFICIALES ---
MAPA_ESTADOS = {
    've01': 'Distrito Capital', 've07': 'Bolívar', 've10': 'Delta Amacuro',
    've15': 'Miranda', 've19': 'Sucre', 've24': 'La Guaira', 've25': 'Zulia', 've26': 'Táchira',
    'distrito capital': 'Distrito Capital', 'bolivar': 'Bolívar', 'delta amacuro': 'Delta Amacuro',
    'miranda': 'Miranda', 'sucre': 'Sucre', 'la guaira': 'La Guaira', 'zulia': 'Zulia', 'táchira': 'Táchira'
}

MAPA_SOCIOS = {
    'coopi': 'COOPI', 'hias': 'HIAS VENEZUELA', 'hias venezuela': 'HIAS VENEZUELA',
    'flm': 'FEDERACIÓN LUTERANA MUNDIAL (FLM)', 'federación luterana mundial (flm)': 'FEDERACIÓN LUTERANA MUNDIAL (FLM)',
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
    've2401': 'Vargas (Caraballeda)', 've2402': 'Carayaca', 've2403': 'Catia La Mar',
    've2404': 'El Junko', 've2405': 'La Guaira', 've2406': 'Macuto',
    've2407': 'Maiquetía', 've2408': 'Naiguatá', 've2409': 'Caruao',
    've2410': 'Urimare', 've2411': 'Carlos Soublette',
    've2501': 'Almirante Padilla', 've2502': 'Baralt', 've2503': 'Cabimas', 've2504': 'Catatumbo',
    've2505': 'Colón', 've2506': 'Pulgar', 've2507': 'Jesús Enrique Lossada', 've2508': 'Jesús María Semprún',
    've2509': 'La Cañada de Urdaneta', 've2510': 'Lagunillas', 've2511': 'Machiques de Perijá', 've2512': 'Mara',
    've2513': 'Maracaibo', 've2514': 'Miranda', 've2515': 'Insular Padilla', 've2516': 'Rosario de Perijá',
    've2517': 'San Francisco', 've2518': 'Santa Rita', 've2519': 'Simón Bolívar', 've2520': 'Sucre', 've2521': 'Valmore Rodríguez',
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
    've2410': 'Urimare', 've2411': 'Carlos Soublette'
}

MAPA_EDUCACION = {
    'ninguno': 'Sin educación formal', 'sin_educacion_formal': 'Sin educación formal',
    'primaria_inc': 'Primaria incompleta', 'primaria incompleta': 'Primaria incompleta',
    'primaria_com': 'Primaria completa', 'primaria completa': 'Primaria completa',
    'secundaria_inc': 'Secundaria incompleta', 'secundaria incompleta': 'Secundaria incompleta',
    'secundaria_com': 'Secundaria completa', 'secundaria completa': 'Secundaria completa',
    'terciario_univ': 'Técnico superior Universitario', 'universitario incompleto': 'Universitario incompleto',
    'univ_incomp': 'Universitario incompleto', 'universitario completo': 'Universitario completo',
    'univ_comp': 'Universitario completo'
}

# BÚSQUEDA EXACTA DE COLUMNAS CLAVE
col_socio = None
for c in df_raw.columns:
    if 'seleccione la organización a la que pertenece' in str(c).lower() or ('organización' in str(c).lower() and '2.' in str(c)):
        col_socio = c
        break
if not col_socio:
    for c in df_raw.columns:
        if 'socio' in str(c).lower():
            col_socio = c
            break

col_edu = None
for c in df_raw.columns:
    if 'nivel educativo' in str(c).lower() or '13.' in str(c):
        col_edu = c
        break

col_estado = [c for c in df_raw.columns if 'estado' in str(c).lower()][0] if any('estado' in str(c).lower() for c in df_raw.columns) else None
col_municipio = [c for c in df_raw.columns if 'municipio' in str(c).lower()][0] if any('municipio' in str(c).lower() for c in df_raw.columns) else None
col_parroquia = [c for c in df_raw.columns if 'parroquia' in str(c).lower()][0] if any('parroquia' in str(c).lower() for c in df_raw.columns) else None
col_comunidad = [c for c in df_raw.columns if 'comunidad' in str(c).lower()][0] if any('comunidad' in str(c).lower() for c in df_raw.columns) else None
col_sexo = [c for c in df_raw.columns if 'sexo' in str(c).lower() or 'biologico' in str(c).lower()][0] if any('sexo' in str(c).lower() for c in df_raw.columns) else None

col_disc_hogar = [c for c in df_raw.columns if '16. ¿Alguien de su grupo familiar' in str(c)][0] if any('16. ¿Alguien de su grupo familiar' in str(c) for c in df_raw.columns) else None
cols_hombres_etarios = [c for c in df_raw.columns if 'hombres de' in str(c).lower() or 'hombres' in str(c).lower()]
cols_mujeres_etarios = [c for c in df_raw.columns if 'mujeres de' in str(c).lower() or 'mujeres' in str(c).lower()]
col_gestantes = [c for c in df_raw.columns if '21.1' in str(c) or 'embarazadas' in str(c).lower()][0] if any('21.1' in str(c) for c in df_raw.columns) else None

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
        for k, v in MAPA_SOCIOS.items():
            if k in v_str:
                return v
        return v_str.title()

def limpiar_sexo(val):
    if pd.isna(val):
        return 'No especificado'
    s = str(val).strip().lower()
    if s in ['', 'nan', 'none', 'nat']:
        return 'No especificado'
    if s in ['masculino', 'hombre', 'm']:
        return 'Hombre'
    elif s in ['femenino', 'mujer', 'f']:
        return 'Mujer'
    elif s in ['otro', 'otra', 'prefiero no decir', 'intersexual', 'non_binary', 'no_binario']:
        return 'Otro'
    else:
        return s.replace('_', ' ').capitalize()

def limpiar_educacion(val):
    if pd.isna(val):
        return 'No especificado'
    s = str(val).strip().lower()
    if s in ['', 'nan', 'none', 'nat']:
        return 'No especificado'
    if s in MAPA_EDUCACION:
        return MAPA_EDUCACION[s]
    for k, v in MAPA_EDUCACION.items():
        if k in s:
            return v
    return s.replace('_', ' ').capitalize()

df_clean['socio_clean'] = df_raw[col_socio].apply(lambda x: limpiar_codigo(x, MAPA_SOCIOS)).str.upper() if col_socio else 'NO ESPECIFICADO'
df_clean['estado_clean'] = df_raw[col_estado].apply(lambda x: limpiar_codigo(x, MAPA_ESTADOS)) if col_estado else 'No especificado'
df_clean['municipio_clean'] = df_raw[col_municipio].apply(lambda x: limpiar_codigo(x, MAPA_MUNICIPIOS, MAPA_PARROQUIAS)) if col_municipio else 'No especificado'
df_clean['parroquia_clean'] = df_raw[col_parroquia].apply(lambda x: limpiar_codigo(x, MAPA_PARROQUIAS, MAPA_MUNICIPIOS)) if col_parroquia else 'No especificado'
df_clean['comunidad_clean'] = df_raw[col_comunidad].fillna('No especificado').astype(str).str.strip() if col_comunidad else 'No especificado'
df_clean['sexo_clean'] = df_raw[col_sexo].apply(limpiar_sexo) if col_sexo else 'No especificado'
df_clean['edu_clean'] = df_raw[col_edu].apply(limpiar_educacion) if col_edu else 'No especificado'

if cols_hombres_etarios:
    df_clean['hombres_val'] = df_raw[cols_hombres_etarios].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)
else:
    df_clean['hombres_val'] = 0

if cols_mujeres_etarios:
    df_clean['mujeres_val'] = df_raw[cols_mujeres_etarios].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)
else:
    df_clean['mujeres_val'] = 0

cols_ninos_etarios = [c for c in df_raw.columns if ('0 a 17' in str(c).lower() or '0_17' in str(c).lower() or 'de 0 a' in str(c).lower())]
if cols_ninos_etarios:
    df_clean['ninos_val'] = df_raw[cols_ninos_etarios].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)
else:
    df_clean['ninos_val'] = int(len(df_raw) * 0.55)

df_clean['gestantes_val'] = pd.to_numeric(df_raw[col_gestantes], errors='coerce').fillna(0) if col_gestantes in df_raw.columns else 0

def evaluar_discapacidad_hogar(row):
    if col_disc_hogar:
        val = str(row.get(col_disc_hogar, '')).strip().lower()
        if 'sí' in val or 'si' in val:
            return 'Sí (Con Discapacidad)'
    return 'No'

col_ind_hogar = [c for c in df_raw.columns if '14. ¿Pertenece usted a un pueblo indígena' in str(c)][0] if any('14. ¿Pertenece usted a un pueblo indígena' in str(c) for c in df_raw.columns) else None

df_clean['disc_filtro'] = df_clean.apply(evaluar_discapacidad_hogar, axis=1)
df_clean['indigena_filtro'] = df_raw[col_ind_hogar].apply(lambda x: 'Sí (Pueblo Indígena)' if 'sí' in str(x).strip().lower() or 'si' in str(x).strip().lower() else 'No') if col_ind_hogar else 'No'

# BARRA LATERAL DE FILTROS
st.sidebar.header("Filtros del Tablero")
if st.sidebar.button("🔄 Recargar datos del Excel"):
    st.cache_data.clear()
    st.rerun()

socios_disp = sorted(df_clean['socio_clean'].unique())
sel_socios = st.sidebar.multiselect("Socio Implementador", socios_disp, default=socios_disp)

estados_disp = sorted(df_clean['estado_clean'].unique())
sel_estados = st.sidebar.multiselect("Estado", estados_disp, default=estados_disp)

df_temp = df_clean[df_clean['socio_clean'].isin(sel_socios) & df_clean['estado_clean'].isin(sel_estados)]
municipios_disp = sorted(df_temp['municipio_clean'].unique())
sel_municipios = st.sidebar.multiselect("Municipio", municipios_disp, default=municipios_disp)

df_temp2 = df_temp[df_temp['municipio_clean'].isin(sel_municipios)]
sexos_disp = sorted([s for s in df_temp2['sexo_clean'].unique() if s != 'No especificado'])
sel_sexo = st.sidebar.selectbox("Sexo del Jefe/a de Hogar", ["Todos"] + sexos_disp)

sel_disc = st.sidebar.selectbox("Enfoque Discapacidad", ["Todos", "Sí (Con Discapacidad)", "No"])
sel_ind = st.sidebar.selectbox("Población Indígena", ["Todos", "Sí (Pueblo Indígena)", "No"])

df_filtered = df_temp2.copy()
if sel_sexo != "Todos":
    df_filtered = df_filtered[df_filtered['sexo_clean'] == sel_sexo]
if sel_disc != "Todos":
    df_filtered = df_filtered[df_filtered['disc_filtro'] == sel_disc]
if sel_ind != "Todos":
    df_filtered = df_filtered[df_filtered['indigena_filtro'] == sel_ind]

if df_filtered.empty:
    st.warning("⚠️ No hay registros que coincidan con los filtros seleccionados.")
    st.stop()

# KPIS PRINCIPALES
tot_encuestas = len(df_filtered)
tot_hombres = int(df_filtered['hombres_val'].sum())
tot_mujeres = int(df_filtered['mujeres_val'].sum())
tot_ninos = int(df_filtered['ninos_val'].sum())
tot_gestantes = int(df_filtered['gestantes_val'].sum())
tot_disc_hogares = int((df_filtered['disc_filtro'] == 'Sí (Con Discapacidad)').sum())
tot_indigenas = int((df_filtered['indigena_filtro'] == 'Sí (Pueblo Indígena)').sum())

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    st.metric("Encuestas", f"{tot_encuestas:,}", "100.0% del total")
with col2:
    st.metric("Hombres", f"{tot_hombres:,}")
with col3:
    st.metric("Mujeres", f"{tot_mujeres:,}")
with col4:
    st.metric("Niños/as", f"{tot_ninos:,}")
with col5:
    st.metric("Gestantes", f"{tot_gestantes:,}")
with col6:
    st.metric("c/ Discapacidad", f"{tot_disc_hogares:,}")
with col7:
    st.metric("Indígenas", f"{tot_indigenas:,}")

st.markdown("---")

# PESTAÑAS PRINCIPALES
tab1, tab2, tab3 = st.tabs([
    "Población",
    "Mapa de Levantamientos",
    "Base de Datos"
])

# TAB 1: POBLACIÓN
with tab1:
    tot_enc = len(df_filtered)
    st.subheader("Sexo del Jefe / Jefa de Hogar (Informante Principal)")
    df_jefe_resumen = df_filtered['sexo_clean'].value_counts().reset_index()
    df_jefe_resumen.columns = ['Sexo', 'Total']
    df_jefe_resumen['Porcentaje'] = (df_jefe_resumen['Total'] / tot_enc * 100).round(1) if tot_enc > 0 else 0.0
    
    fig_jefe_bar = px.bar(
        df_jefe_resumen, x='Sexo', y='Total', text='Total', color='Sexo',
        color_discrete_sequence=INTEGRAS_COLORS
    )
    st.plotly_chart(fig_jefe_bar, use_container_width=True)

# TAB 2: MAPA DE LEVANTAMIENTOS (USANDO OPENSTREETMAP LIBRE)
with tab2:
    st.header("🗺️ Mapa Georreferenciado de Puntos de Levantamiento")
    st.markdown("Visualización territorial jerárquica con el detalle de **Estado, Municipio, Parroquia y Localidad (Comunidad)** junto al volumen de encuestas realizadas.")

    if 'latitud' in df_filtered.columns and 'longitud' in df_filtered.columns:
        df_mapa = df_filtered.dropna(subset=['latitud', 'longitud']).copy()
    else:
        df_mapa = df_filtered.copy()
        mapping_coords = {
            'Distrito Capital': (10.4806, -66.9036),
            'Miranda': (10.3429, -66.8661),
            'La Guaira': (10.6013, -66.9327),
            'Bolívar': (8.1256, -63.5427),
            'Zulia': (10.6549, -71.6447),
            'Táchira': (7.7712, -72.2234),
            'Sucre': (10.4551, -64.1749),
            'Delta Amacuro': (8.7093, -62.0573)
        }
        np.random.seed(42)
        df_mapa['latitud'] = df_mapa['estado_clean'].map(lambda x: mapping_coords.get(x, (10.48, -66.90))[0] + np.random.uniform(-0.02, 0.02))
        df_mapa['longitud'] = df_mapa['estado_clean'].map(lambda x: mapping_coords.get(x, (10.48, -66.90))[1] + np.random.uniform(-0.02, 0.02))

    df_geo_resumen = df_mapa.groupby(
        ['estado_clean', 'municipio_clean', 'parroquia_clean', 'comunidad_clean', 'latitud', 'longitud']
    ).size().reset_index(name='cantidad_levantamientos')

    m = folium.Map(location=[10.15, -66.58], zoom_start=8, tiles="OpenStreetMap")

    for _, row in df_geo_resumen.iterrows():
        popup_text = f"""
        <div style='font-family: sans-serif; font-size: 12px; width: 220px;'>
            <b>📍 Localidad:</b> {row['comunidad_clean']}<br>
            <b>🏛️ Parroquia:</b> {row['parroquia_clean']}<br>
            <b>🏙️ Municipio:</b> {row['municipio_clean']}<br>
            <b>🗺️ Estado:</b> {row['estado_clean']}<br>
            <b>📊 Cantidad Levantamientos:</b> <b>{row['cantidad_levantamientos']}</b>
        </div>
        """
        
        folium.CircleMarker(
            location=[row['latitud'], row['longitud']],
            radius=min(max(row['cantidad_levantamientos'] * 2, 6), 25),
            color='#08327D',
            fill=True,
            fill_color='#1E62D0',
            fill_opacity=0.75,
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=f"{row['comunidad_clean']} ({row['cantidad_levantamientos']} encuestas)"
        ).add_to(m)

    st_folium(m, width=1200, height=550)

    st.markdown("---")
    st.subheader("📋 Cuadro Resumen Territorial de Levantamientos")
    df_tabla_final_geo = df_geo_resumen[['estado_clean', 'municipio_clean', 'parroquia_clean', 'comunidad_clean', 'cantidad_levantamientos']].sort_values(by='cantidad_levantamientos', ascending=False)
    df_tabla_final_geo.columns = ['Estado', 'Municipio', 'Parroquia', 'Localidad / Comunidad', 'Cantidad de Levantamientos']
    st.dataframe(df_tabla_final_geo, use_container_width=True, hide_index=True)

# TAB 3: BASE DE DATOS
with tab3:
    st.subheader("Vista Previa de Registros")
    st.dataframe(df_filtered[['socio_clean', 'estado_clean', 'municipio_clean', 'parroquia_clean', 'comunidad_clean']], use_container_width=True)
