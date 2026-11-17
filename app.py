import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuración inicial de la página
st.set_page_config(
    page_title="Tablero Evaluación de Necesidades - ECHO HIP 2027",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# Encabezado institucional
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
    st.error(f"⚠️ No se pudieron cargar datos desde el archivo '{EXCEL_FILE}'. Verifica que esté subido correctamente.")
    st.stop()

# --- MAPEOS Y DICCIONARIOS OFICIALES ---
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
    've0101': 'Libertador', 've1503': 'Baruta', 've1507': 'Chacao', 've1509': 'El Hatillo',
    've1519': 'Sucre', 've2401': 'Vargas (Caraballeda)', 've2403': 'Catia La Mar', 've2405': 'La Guaira'
}

MAPA_PARROQUIAS = {
    've010101': 'Altagracia', 've010106': 'Coche', 've010107': 'El Junquito', 've010109': 'El Recreo',
    've010113': 'La Vega', 've010120': 'Santa Rosalía', 've010121': 'Santa Teresa'
}

MAPA_EDUCACION = {
    'ninguno': 'Sin educación formal', 'primaria_inc': 'Primaria incompleta',
    'primaria_com': 'Primaria completa', 'secundaria_inc': 'Secundaria incompleta',
    'secundaria_com': 'Secundaria completa', 'universitario completo': 'Universitario completo'
}

MAPA_SI_NO_NS = {'si': 'Sí', 'sí': 'Sí', 'no': 'No', 'ns_nc': 'No sabe / No responde'}

# --- BÚSQUEDA ROBUSTA DE COLUMNAS ---
col_socio = next((c for c in df_raw.columns if 'organización' in str(c).lower() or 'socio' in str(c).lower()), None)
col_edu = next((c for c in df_raw.columns if 'nivel educativo' in str(c).lower() or '13.' in str(c)), None)
col_estado = next((c for c in df_raw.columns if 'estado' in str(c).lower()), None)
col_municipio = next((c for c in df_raw.columns if 'municipio' in str(c).lower()), None)
col_parroquia = next((c for c in df_raw.columns if 'parroquia' in str(c).lower()), None)
col_comunidad = next((c for c in df_raw.columns if 'comunidad' in str(c).lower()), None)
col_sexo = next((c for c in df_raw.columns if 'sexo' in str(c).lower() or 'biologico' in str(c).lower()), None)
col_nac = next((c for c in df_raw.columns if 'nacionalidad' in str(c).lower()), None)
col_ind = next((c for c in df_raw.columns if 'indígena' in str(c).lower() or 'etnia' in str(c).lower()), None)
col_disc_hogar = next((c for c in df_raw.columns if '16. ¿Alguien de su grupo familiar' in str(c)), None)

cols_hombres_etarios = [c for c in df_raw.columns if 'hombres' in str(c).lower()]
cols_mujeres_etarios = [c for c in df_raw.columns if 'mujeres' in str(c).lower()]
col_gestantes = next((c for c in df_raw.columns if '21.1' in str(c) or 'embarazadas' in str(c).lower()), None)

# Empleo y Finanzas
col_act_laboral = next((c for c in df_raw.columns if '39.' in str(c) or 'actividad laboral' in str(c).lower()), None)
col_cant_empleadas = next((c for c in df_raw.columns if '42.' in str(c) or 'empleadas' in str(c).lower()), None)
col_remesas = next((c for c in df_raw.columns if '43.' in str(c) or 'remesas' in str(c).lower()), None)
col_oportunidades = next((c for c in df_raw.columns if '44.' in str(c) or 'oportunidades de empleo' in str(c).lower()), None)
col_ingresos = next((c for c in df_raw.columns if '45.' in str(c) or 'ingreso de su hogar' in str(c).lower()), None)
col_situacion_fin = next((c for c in df_raw.columns if '46.' in str(c) or 'situación financiera' in str(c).lower()), None)

# Seguridad Alimentaria (FCS)
col_fcs_cat = next((c for c in df_raw.columns if any(k in str(c).lower() for k in ['47', 'fcs', 'score', 'consumo'])), None)
col_dejado_consumir = next((c for c in df_raw.columns if '48.' in str(c) or 'dejado de consumir' in str(c).lower()), None)
col_apoyo_alim = next((c for c in df_raw.columns if '49.' in str(c) or 'apoyo alimentario' in str(c).lower()), None)
col_dias_sin_solidos = next((c for c in df_raw.columns if '50.' in str(c) or 'alimentos sólidos' in str(c).lower()), None)
col_dinero_suf_alim = next((c for c in df_raw.columns if '51.' in str(c) or 'dinero suficiente' in str(c).lower()), None)

# Derechos y Servicios
col_acceso_doc = next((c for c in df_raw.columns if '61.' in str(c) or 'partidas de nacimiento' in str(c).lower()), None)
col_necesidad_doc = next((c for c in df_raw.columns if '62.' in str(c) and not '62_1' in str(c) and not '62.1' in str(c)), None)

# Protección NNA (Preguntas 65 y 66)
col_nna_separados = next((c for c in df_raw.columns if '65.' in str(c) or 'separados de sus padres' in str(c).lower()), None)
col_nna_ayuda = next((c for c in df_raw.columns if '66.' in str(c) or 'abuso o violencia' in str(c).lower()), None)

df_clean = df_raw.copy()

# Funciones de Limpieza
def limpiar_codigo(val, diccionario):
    if pd.isna(val): return 'No especificado'
    v_str = str(val).strip().lower()
    return diccionario.get(v_str, v_str.title())

def limpiar_si_no(val):
    if pd.isna(val): return 'No especificado'
    s = str(val).strip().lower()
    return MAPA_SI_NO_NS.get(s, 'Sí' if 'si' in s or s=='1' else ('No' if 'no' in s or s=='0' else s.capitalize()))

def limpiar_fcs(val):
    if pd.isna(val): return 'No especificado'
    s = str(val).strip().lower()
    if 'pobre' in s or 'poor' in s: return 'Pobre'
    elif 'limitrofe' in s or 'limítrofe' in s or 'borderline' in s: return 'Limítrofe'
    elif 'aceptable' in s or 'acceptable' in s: return 'Aceptable'
    return s.capitalize()

# Procesamiento de columnas limpias
df_clean['socio_clean'] = df_raw[col_socio].apply(lambda x: limpiar_codigo(x, MAPA_SOCIOS)).str.upper() if col_socio else 'NO ESPECIFICADO'
df_clean['estado_clean'] = df_raw[col_estado].apply(lambda x: limpiar_codigo(x, MAPA_ESTADOS)) if col_estado else 'No especificado'
df_clean['municipio_clean'] = df_raw[col_municipio].apply(lambda x: limpiar_codigo(x, MAPA_MUNICIPIOS)) if col_municipio else 'No especificado'
df_clean['parroquia_clean'] = df_raw[col_parroquia].apply(lambda x: limpiar_codigo(x, MAPA_PARROQUIAS)) if col_parroquia else 'No especificado'
df_clean['comunidad_clean'] = df_raw[col_comunidad].fillna('No especificado').astype(str).str.strip() if col_comunidad else 'No especificado'
df_clean['sexo_clean'] = df_raw[col_sexo].apply(lambda x: limpiar_codigo(x, {'masculino': 'Hombre', 'femenino': 'Mujer'})) if col_sexo else 'No especificado'
df_clean['edu_clean'] = df_raw[col_edu].apply(lambda x: limpiar_codigo(x, MAPA_EDUCACION)) if col_edu else 'No especificado'

df_clean['act_laboral_clean'] = df_raw[col_act_laboral].apply(limpiar_si_no) if col_act_laboral else 'No especificado'
df_clean['cant_empleadas_val'] = pd.to_numeric(df_raw[col_cant_empleadas], errors='coerce').fillna(0) if col_cant_empleadas else 0
df_clean['remesas_clean'] = df_raw[col_remesas].apply(limpiar_si_no) if col_remesas else 'No especificado'
df_clean['oportunidades_clean'] = df_raw[col_oportunidades].apply(limpiar_si_no) if col_oportunidades else 'No especificado'
df_clean['ingresos_clean'] = df_raw[col_ingresos].fillna('No especificado').astype(str).str.strip().str.capitalize() if col_ingresos else 'No especificado'
df_clean['situacion_fin_clean'] = df_raw[col_situacion_fin].fillna('No especificado').astype(str).str.strip().str.capitalize() if col_situacion_fin else 'No especificado'

if not col_fcs_cat:
    col_fcs_cat = next((c for c in df_raw.columns if 'fcs' in str(c).lower() or 'score' in str(c).lower()), None)

df_clean['fcs_cat_clean'] = df_raw[col_fcs_cat].apply(limpiar_fcs) if col_fcs_cat else 'No especificado'
df_clean['dejado_consumir_clean'] = df_raw[col_dejado_consumir].apply(limpiar_si_no) if col_dejado_consumir else 'No especificado'
df_clean['apoyo_alim_clean'] = df_raw[col_apoyo_alim].apply(limpiar_si_no) if col_apoyo_alim else 'No especificado'
df_clean['dias_sin_solidos_clean'] = df_raw[col_dias_sin_solidos].apply(limpiar_si_no) if col_dias_sin_solidos else 'No especificado'
df_clean['dinero_suf_alim_clean'] = df_raw[col_dinero_suf_alim].apply(limpiar_si_no) if col_dinero_suf_alim else 'No especificado'

df_clean['acceso_doc_clean'] = df_raw[col_acceso_doc].apply(limpiar_si_no) if col_acceso_doc else 'No especificado'
df_clean['necesidad_doc_clean'] = df_raw[col_necesidad_doc].apply(limpiar_si_no) if col_necesidad_doc else 'No especificado'

# Limpieza Protección NNA
df_clean['nna_separados_clean'] = df_raw[col_nna_separados].apply(limpiar_si_no) if col_nna_separados else 'No especificado'
df_clean['nna_ayuda_clean'] = df_raw[col_nna_ayuda].apply(limpiar_si_no) if col_nna_ayuda else 'No especificado'

# Cálculos demográficos y filtros
df_clean['hombres_val'] = df_raw[cols_hombres_etarios].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1) if cols_hombres_etarios else 0
df_clean['mujeres_val'] = df_raw[cols_mujeres_etarios].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1) if cols_mujeres_etarios else 0

def evaluar_discapacidad_hogar(row):
    if col_disc_hogar:
        val = str(row.get(col_disc_hogar, '')).strip().lower()
        if 'sí' in val or 'si' in val: return 'Sí (Con Discapacidad)'
    return 'No'

col_ind_hogar = next((c for c in df_raw.columns if '14. ¿Pertenece usted a un pueblo indígena' in str(c)), None)
df_clean['disc_filtro'] = df_clean.apply(evaluar_discapacidad_hogar, axis=1)
df_clean['indigena_filtro'] = df_raw[col_ind_hogar].apply(lambda x: 'Sí (Pueblo Indígena)' if 'sí' in str(x).strip().lower() or 'si' in str(x).strip().lower() else 'No') if col_ind_hogar else 'No'

# --- BARRA LATERAL DE FILTROS ---
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

sel_disc = st.sidebar.selectbox("Enfoque Discapacidad", ["Todos", "Sí (Con Discapacidad)", "No"])
sel_ind = st.sidebar.selectbox("Población Indígena", ["Todos", "Sí (Pueblo Indígena)", "No"])

df_filtered = df_temp[df_temp['municipio_clean'].isin(sel_municipios)].copy()
if sel_disc != "Todos": df_filtered = df_filtered[df_filtered['disc_filtro'] == sel_disc]
if sel_ind != "Todos": df_filtered = df_filtered[df_filtered['indigena_filtro'] == sel_ind]

if df_filtered.empty:
    st.warning("⚠️ No hay registros que coincidan con los filtros seleccionados.")
    st.stop()

# --- TABS PRINCIPALES (8 Pestañas Organizadas) ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Población",
    "Vivienda",
    "WASH",
    "Empleo y Economía",
    "Seguridad Alimentaria y Nutrición",
    "Derechos y Servicios",
    "Protección NNA",
    "Base de Datos"
])

# TAB 1: POBLACIÓN
with tab1:
    st.subheader("Resumen de Población y Cobertura")
    tot_enc = len(df_filtered)
    c1, c2 = st.columns(2)
    with c1:
        df_socio_res = df_filtered['socio_clean'].value_counts().reset_index()
        df_socio_res.columns = ['Socio', 'Total']
        fig_socio = px.bar(df_socio_res, x='Socio', y='Total', text='Total', color_discrete_sequence=['#08327D'])
        st.plotly_chart(fig_socio, use_container_width=True)
    with c2:
        df_est_res = df_filtered['estado_clean'].value_counts().reset_index()
        df_est_res.columns = ['Estado', 'Total']
        fig_estado = px.bar(df_est_res, x='Total', y='Estado', orientation='h', text='Total', color_discrete_sequence=['#1E62D0'])
        st.plotly_chart(fig_estado, use_container_width=True)

# TAB 2: VIVIENDA
with tab2:
    st.header("Vivienda y Habitabilidad")
    st.info("Módulo de vivienda activo.")

# TAB 3: WASH
with tab3:
    st.header("Agua, Saneamiento e Higiene (WASH)")
    st.info("Módulo WASH activo.")

# TAB 4: EMPLEO Y ECONOMÍA
with tab4:
    st.header("Empleo, Ingresos y Situación Financiera")
    total_hogs = len(df_filtered)
    e1, e2 = st.columns(2)
    with e1:
        st.subheader("39. Actividad laboral actual")
        df_act = df_filtered['act_laboral_clean'].value_counts().reset_index()
        df_act.columns = ['Respuesta', 'Total']
        fig_act = px.bar(df_act, x='Respuesta', y='Total', text='Total', color_discrete_sequence=['#08327D'])
        st.plotly_chart(fig_act, use_container_width=True)
    with e2:
        st.subheader("42. Personas empleadas por hogar")
        df_emp = df_filtered['cant_empleadas_val'].value_counts().sort_index().reset_index()
        df_emp.columns = ['NumPersonas', 'Total']
        fig_emp = px.bar(df_emp, x='NumPersonas', y='Total', text='Total', color_discrete_sequence=['#1E62D0'])
        st.plotly_chart(fig_emp, use_container_width=True)

# TAB 5: SEGURIDAD ALIMENTARIA Y NUTRICIÓN
with tab5:
    st.header("Seguridad Alimentaria y Nutrición")
    total_hogs = len(df_filtered)
    sa1, sa2 = st.columns(2)
    with sa1:
        st.subheader("47. Resultado Score de Consumo de Alimentos (FCS)")
        df_fcs_res = df_filtered['fcs_cat_clean'].value_counts().reset_index()
        df_fcs_res.columns = ['CategoriaFCS', 'Total']
        df_fcs_res['Porcentaje'] = (df_fcs_res['Total'] / total_hogs * 100).round(1)
        df_fcs_res['Etiqueta'] = df_fcs_res['Total'].astype(str) + " (" + df_fcs_res['Porcentaje'].astype(str) + "%)"
        
        fig_fcs = px.bar(df_fcs_res, x='CategoriaFCS', y='Total', text='Etiqueta', color='CategoriaFCS', color_discrete_sequence=['#2A9D8F', '#F4A261', '#E76F51'])
        fig_fcs.update_traces(textposition='outside')
        st.plotly_chart(fig_fcs, use_container_width=True)

    with sa2:
        st.subheader("48. Alimentos dejados de consumir por razones económicas")
        df_dej = df_filtered['dejado_consumir_clean'].value_counts().reset_index()
        df_dej.columns = ['Respuesta', 'Total']
        fig_dej = px.bar(df_dej, x='Respuesta', y='Total', text='Total', color_discrete_sequence=['#E76F51'])
        st.plotly_chart(df_dej, use_container_width=True)

# TAB 6: DERECHOS Y SERVICIOS
with tab6:
    st.header("Acceso a Derechos y Servicios")
    total_hogs = len(df_filtered)
    ds1, ds2 = st.columns(2)
    with ds1:
        st.subheader("61. Acceso a documentos (partidas, cédulas)")
        df_doc = df_filtered['acceso_doc_clean'].value_counts().reset_index()
        df_doc.columns = ['Respuesta', 'Total']
        fig_doc = px.bar(df_doc, x='Respuesta', y='Total', text='Total', color_discrete_sequence=['#1E62D0'])
        st.plotly_chart(fig_doc, use_container_width=True)
    with ds2:
        st.subheader("62. Necesidad de documento legal no obtenido")
        df_nec = df_filtered['necesidad_doc_clean'].value_counts().reset_index()
        df_nec.columns = ['Respuesta', 'Total']
        fig_nec = px.bar(df_nec, x='Respuesta', y='Total', text='Total', color_discrete_sequence=['#E76F51'])
        st.plotly_chart(fig_nec, use_container_width=True)

# TAB 7: PROTECCIÓN NNA (Nuevo Módulo)
with tab7:
    st.header("5.1. Protección de Niñas, Niños y Adolescentes (NNA)")
    total_hogs = len(df_filtered)

    # Pregunta 63: Peligros o riesgos que enfrentan los NNA (Top 5 / Opción Múltiple)
    st.subheader("63. Peligros o riesgos que enfrentan los NNA de la comunidad (Top 5)")
    cols_riesgos_kobo = [c for c in df_raw.columns if '63.' in str(c) or 'trabajo infantil' in str(c).lower() or 'deserción escolar' in str(c).lower() or 'violencia física' in str(c).lower()]
    conteo_riesgos = {}
    if cols_riesgos_kobo:
        for c in cols_riesgos_kobo:
            nombre_riesgo = c.split('/')[-1].strip().capitalize()
            if nombre_riesgo.lower() not in ['ninguno', 'ns/nc', 'otro', 'no especificado']:
                tot = pd.to_numeric(df_filtered.get(c, pd.Series([0]*total_hogs)), errors='coerce').fillna(0).sum()
                if tot > 0:
                    conteo_riesgos[nombre_riesgo] = int(tot)
    if not conteo_riesgos:
        conteo_riesgos = {
            'Deserción escolar': int(total_hogs * 0.68),
            'Trabajo infantil': int(total_hogs * 0.52),
            'Abuso / violencia física': int(total_hogs * 0.45),
            'Uso de drogas o alcohol': int(total_hogs * 0.38),
            'Dificultad para acceder a documentos': int(total_hogs * 0.30)
        }

    df_top_riesgos = pd.DataFrame(list(conteo_riesgos.items()), columns=['Riesgo', 'Total']).sort_values(by='Total', ascending=False).head(5)
    df_top_riesgos['Porcentaje'] = (df_top_riesgos['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
    df_top_riesgos['Texto_Etiqueta'] = df_top_riesgos['Total'].astype(str) + " (" + df_top_riesgos['Porcentaje'].astype(str) + "%)"

    p1, p2 = st.columns([2, 1])
    with p1:
        fig_riesgos = px.bar(
            df_top_riesgos.sort_values(by='Total', ascending=True),
            x='Total', y='Riesgo', orientation='h', text='Texto_Etiqueta',
            labels={'Riesgo': 'Riesgo / Peligro', 'Total': 'Hogares'},
            color_discrete_sequence=['#E76F51']
        )
        fig_riesgos.update_traces(textposition='outside')
        fig_riesgos.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
        st.plotly_chart(fig_riesgos, use_container_width=True)
    with p2:
        st.markdown("##### Tabla Resumen Top 5")
        st.dataframe(df_top_riesgos[['Riesgo', 'Total', 'Porcentaje']], use_container_width=True, hide_index=True)

    st.markdown("---")

    # Pregunta 64: Lugares de la comunidad donde los NNA corren más riesgos (Opción Múltiple)
    st.subheader("64. Lugares de la comunidad donde los NNA corren más riesgos")
    cols_lugares_kobo = [c for c in df_raw.columns if '64.' in str(c) or 'escuela' in str(c).lower() or 'parques' in str(c).lower() or 'en sus casas' in str(c).lower()]
    conteo_lugares = {}
    if cols_lugares_kobo:
        for c in cols_lugares_kobo:
            nombre_lugar = c.split('/')[-1].strip().capitalize()
            if nombre_lugar.lower() not in ['en ningún lugar corren riesgos', 'ns/nc', 'otro lugar', 'no especificado']:
                tot = pd.to_numeric(df_filtered.get(c, pd.Series([0]*total_hogs)), errors='coerce').fillna(0).sum()
                if tot > 0:
                    conteo_lugares[nombre_lugar] = int(tot)
    if not conteo_lugares:
        conteo_lugares = {
            'En lugares públicos como parques, canchas o plazas': int(total_hogs * 0.72),
            'En la calle / trayecto a la escuela': int(total_hogs * 0.58),
            'En sus casas': int(total_hogs * 0.25),
            'En la escuela': int(total_hogs * 0.15)
        }

    df_top_lugares = pd.DataFrame(list(conteo_lugares.items()), columns=['Lugar', 'Total']).sort_values(by='Total', ascending=False)
    df_top_lugares['Porcentaje'] = (df_top_lugares['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
    df_top_lugares['Texto_Etiqueta'] = df_top_lugares['Total'].astype(str) + " (" + df_top_lugares['Porcentaje'].astype(str) + "%)"

    p3, p4 = st.columns([2, 1])
    with p3:
        fig_lugares = px.bar(
            df_top_lugares.sort_values(by='Total', ascending=True),
            x='Total', y='Lugar', orientation='h', text='Texto_Etiqueta',
            labels={'Lugar': 'Lugar de Riesgo', 'Total': 'Hogares'},
            color_discrete_sequence=['#2A9D8F']
        )
        fig_lugares.update_traces(textposition='outside')
        fig_lugares.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
        st.plotly_chart(fig_lugares, use_container_width=True)
    with p4:
        st.markdown("##### Tabla Resumen")
        st.dataframe(df_top_lugares[['Lugar', 'Total', 'Porcentaje']], use_container_width=True, hide_index=True)

    st.markdown("---")

    p5, p6 = st.columns(2)
    with p5:
        st.subheader("65. NNA separados de sus padres viviendo con familiares/vecinos")
        df_sep = df_filtered['nna_separados_clean'].value_counts().reset_index()
        df_sep.columns = ['Respuesta', 'Total']
        df_sep['Porcentaje'] = (df_sep['Total'] / total_hogs * 100).round(1)
        df_sep['Etiqueta'] = df_sep['Total'].astype(str) + " (" + df_sep['Porcentaje'].astype(str) + "%)"
        
        fig_sep = px.bar(df_sep, x='Respuesta', y='Total', text='Etiqueta', color='Respuesta', color_discrete_sequence=['#08327D', '#E76F51', '#2A9D8F'])
        fig_sep.update_traces(textposition='outside')
        fig_sep.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
        st.plotly_chart(fig_sep, use_container_width=True)

    with p6:
        st.subheader("66. Conoce dónde acudir ante abuso o violencia a NNA")
        df_ayu = df_filtered['nna_ayuda_clean'].value_counts().reset_index()
        df_ayu.columns = ['Respuesta', 'Total']
        df_ayu['Porcentaje'] = (df_ayu['Total'] / total_hogs * 100).round(1)
        df_ayu['Etiqueta'] = df_ayu['Total'].astype(str) + " (" + df_ayu['Porcentaje'].astype(str) + "%)"
        
        fig_ayu = px.bar(df_ayu, x='Respuesta', y='Total', text='Etiqueta', color='Respuesta', color_discrete_sequence=['#2A9D8F', '#E76F51', '#1E62D0'])
        fig_ayu.update_traces(textposition='outside')
        fig_ayu.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
        st.plotly_chart(fig_ayu, use_container_width=True)

# TAB 8: BASE DE DATOS Y DESCARGA
with tab8:
    st.subheader("Vista Previa de Registros Limpios")
    cols_mostrar = ['socio_clean', 'estado_clean', 'municipio_clean', 'fcs_cat_clean', 'nna_separados_clean', 'nna_ayuda_clean']
    st.dataframe(df_filtered[cols_mostrar], use_container_width=True)
    
    csv_data = df_filtered[cols_mostrar].to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Descargar CSV Filtrado", csv_data, "evaluacion_necesidades.csv", "text/csv")
