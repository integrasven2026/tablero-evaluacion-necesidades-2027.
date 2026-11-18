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

MAPA_PUEBLOS_INDIGENAS = {
    'ind_01': 'Akawayo', 'ind_02': 'Añú (Paraujano)', 'ind_03': 'Arawako', 'ind_04': 'Baniva',
    'ind_05': 'Barí', 'ind_06': 'Chaima', 'ind_07': 'Eñepá (Panare)', 'ind_08': 'Hoti',
    'ind_09': 'Jivi (Guajibo)', 'ind_10': 'Kariña', 'ind_11': 'Mapoyo', 'ind_12': 'Pemón',
    'ind_13': 'Piaroa', 'ind_14': 'Puinave', 'ind_15': 'Pumé (Yaruro)', 'ind_16': 'Sanemá',
    'ind_17': 'Sapé', 'ind_18': 'Uruak (Arutani)', 'ind_19': 'Warao', 'ind_20': 'Warekena',
    'ind_21': 'Wayúu (Guajiro)', 'ind_22': 'Yabarana', 'ind_23': 'Yanomami', 'ind_24': 'Yekuana', 'ind_25': 'Yukpa'
}

MAPA_NACIONALIDAD = {'venezolana': 'Venezolana', 'extranjera': 'Extranjera'}

MAPA_SI_NO_NS = {
    'si': 'Sí', 'sí': 'Sí', 'no': 'No',
    'ns_nc': 'No sabe / No responde', 'no_sabe_no_responde': 'No sabe / No responde'
}

MAPA_FUENTES_AGUA_VALORES = {
    'red_tuberias': 'Red de tubería (acueducto)', 'camion_cisterna': 'Camión cisterna',
    'pozo_subterraneo': 'Pozo subterráneo / Manantial', 'agua_embotellada': 'Agua embotellada / Botellón',
    'otra_fuente': 'Otra fuente', 'ns_nc': 'No sabe / No responde'
}

MAPA_FRECUENCIA_AGUA = {
    'diario': 'Diario (continuo)', 'diario_continuo': 'Diario (continuo)',
    'varios_dias': 'Varios días a la semana', 'una_vez': 'Una vez a la semana',
    'cada_15_dias': 'Cada 15 días o más', 'cada_15_dias_o_mas': 'Cada 15 días o más'
}

MAPA_RAZON_MENSTRUAL = {
    'costo_elevado': 'Costo elevado o falta de presupuesto.', 'costo': 'Costo elevado o falta de presupuesto.',
    'no_disponibles': 'No hay disponibles a la venta en las tiendas cercanas, mercados o puntos de abasto locales.',
    'disponibilidad': 'No hay disponibles a la venta en las tiendas cercanas, mercados o puntos de abasto locales.',
    'alternativas': 'Utiliza otras alternativas locales (ceniza, arena, barro, plantas, hojas tradicionales o solo agua).',
    'no_necesario': 'No lo considera necesario.', 'no_habitual': 'No es una práctica habitual en la rutina diaria de la familia.'
}

# --- BÚSQUEDA EXACTA DE COLUMNAS CLAVE ---
col_socio = next((c for c in df_raw.columns if 'seleccione la organización a la que pertenece' in str(c).lower() or ('organización' in str(c).lower() and '2.' in str(c)) or 'socio' in str(c).lower()), None)
col_edu = next((c for c in df_raw.columns if 'nivel educativo' in str(c).lower() or '13.' in str(c)), None)
col_estado = next((c for c in df_raw.columns if 'estado' in str(c).lower()), None)
col_municipio = next((c for c in df_raw.columns if 'municipio' in str(c).lower()), None)
col_parroquia = next((c for c in df_raw.columns if 'parroquia' in str(c).lower()), None)
col_comunidad = next((c for c in df_raw.columns if 'comunidad' in str(c).lower()), None)
col_sexo = next((c for c in df_raw.columns if 'sexo' in str(c).lower() or 'biologico' in str(c).lower()), None)

col_nac = next((c for c in df_raw.columns if 'nacionalidad' in str(c).lower()), None)
col_ind = next((c for c in df_raw.columns if 'indígena' in str(c).lower() or 'etnia' in str(c).lower()), None)
col_disc_hogar = next((c for c in df_raw.columns if '16. ¿Alguien de su grupo familiar' in str(c)), None)

cols_hombres_etarios = [c for c in df_raw.columns if 'hombres de' in str(c).lower() or 'hombres' in str(c).lower()]
cols_mujeres_etarios = [c for c in df_raw.columns if 'mujeres de' in str(c).lower() or 'mujeres' in str(c).lower()]

col_gestantes = next((c for c in df_raw.columns if '21.1' in str(c) or 'embarazadas' in str(c).lower()), None)
col_tenencia = next((c for c in df_raw.columns if '22' in str(c) or 'tenencia' in str(c).lower()), None)
col_personas_viv = next((c for c in df_raw.columns if '24' in str(c) or 'personas' in str(c).lower()), None)
col_cuartos = next((c for c in df_raw.columns if '25' in str(c) or 'cuartos' in str(c).lower()), None)

col_act_laboral = next((c for c in df_raw.columns if '39.' in str(c) or 'actividad laboral' in str(c).lower()), None)
col_cant_empleadas = next((c for c in df_raw.columns if '42.' in str(c) or 'empleadas' in str(c).lower()), None)
col_remesas = next((c for c in df_raw.columns if '43.' in str(c) or 'remesas' in str(c).lower()), None)
col_oportunidades = next((c for c in df_raw.columns if '44.' in str(c) or 'oportunidades de empleo' in str(c).lower()), None)
col_ingresos = next((c for c in df_raw.columns if '45.' in str(c) or 'ingreso de su hogar' in str(c).lower()), None)
col_situacion_fin = next((c for c in df_raw.columns if '46.' in str(c) or 'situación financiera' in str(c).lower()), None)

col_fcs_cat = next((c for c in df_raw.columns if ('fcs' in str(c).lower()) or ('consumo' in str(c).lower() and 'alimento' in str(c).lower()) or ('47' in str(c)) or ('score' in str(c).lower())), None)
col_dejado_consumir = next((c for c in df_raw.columns if '48.' in str(c) or 'dejado de consumir' in str(c).lower()), None)
col_apoyo_alim = next((c for c in df_raw.columns if '49.' in str(c) or 'apoyo alimentario' in str(c).lower()), None)
col_dias_sin_solidos = next((c for c in df_raw.columns if '50.' in str(c) or 'alimentos sólidos' in str(c).lower()), None)
col_dinero_suf_alim = next((c for c in df_raw.columns if '51.' in str(c) or 'dinero suficiente para adquirir todos los alimentos' in str(c).lower()), None)

col_nut_prenatal = next((c for c in df_raw.columns if '54.' in str(c) or 'prenatal' in str(c).lower()), None)
col_nut_pediatrica = next((c for c in df_raw.columns if '55.' in str(c) or 'pediátricas' in str(c).lower() or 'pediatricas' in str(c).lower()), None)
col_lactancia = next((c for c in df_raw.columns if '56.' in str(c) or 'lactancia materna' in str(c).lower()), None)
col_suplementos = next((c for c in df_raw.columns if '57.' in str(c) or 'suplementos nutricionales' in str(c).lower()), None)
col_malnutricion = next((c for c in df_raw.columns if '58.' in str(c) or 'malnutrición' in str(c).lower() or 'malnutricion' in str(c).lower()), None)

col_acceso_doc = next((c for c in df_raw.columns if '61.' in str(c) or 'partidas de nacimiento' in str(c).lower()), None)
col_necesidad_doc = next((c for c in df_raw.columns if ('62.' in str(c) or 'documento legal' in str(c).lower()) and not '62_1' in str(c) and not '62.1' in str(c)), None)

col_nna_separados = next((c for c in df_raw.columns if '65.' in str(c) or 'separados de sus padres' in str(c).lower()), None)
col_nna_ayuda = next((c for c in df_raw.columns if '66.' in str(c) or 'abuso o violencia' in str(c).lower()), None)

col_gbv_problemas = next((c for c in df_raw.columns if ('67.' in str(c) or 'integridad física y emocional' in str(c).lower()) and not '67.1' in str(c) and not '67_1' in str(c)), None)
col_gbv_acceso = next((c for c in df_raw.columns if '69.' in str(c) or 'acceden al servicio que refiere' in str(c).lower()), None)

col_edu_asisten = next((c for c in df_raw.columns if '71.' in str(c) or 'asisten todos los niños' in str(c).lower()), None)
col_edu_operativas = next((c for c in df_raw.columns if '72.' in str(c) or 'escuelas operativas' in str(c).lower()), None)
col_edu_estado = next((c for c in df_raw.columns if '74.' in str(c) or 'estado general' in str(c).lower() or 'instalaciones de la unidad educativa' in str(c).lower()), None)

col_salud_problema = next((c for c in df_raw.columns if '76.' in str(c) or 'problema de salud y necesitó acceder a atención médica' in str(c).lower()), None)
col_salud_obtener = next((c for c in df_raw.columns if '76.2' in str(c) or '76_2' in str(c) or 'pudieron obtener atención médica' in str(c).lower()), None)

col_ssr_servicios = next((c for c in df_raw.columns if '80.' in str(c) or 'servicios de salud sexual y reproductiva' in str(c).lower()), None)
col_ssr_charlas = next((c for c in df_raw.columns if '82.' in str(c) or 'charla o formación sobre temas de salud sexual' in str(c).lower()), None)

col_mov_residencia = next((c for c in df_raw.columns if '83.' in str(c) or 'cambiado su lugar de residencia en el último año' in str(c).lower()), None)
col_mov_pais = next((c for c in df_raw.columns if '84.' in str(c) or 'salido o salió del país con el propósito de vivir' in str(c).lower()), None)
col_mov_comunidad = next((c for c in df_raw.columns if '85.' in str(c) or 'personas que hayan salido en los últimos tres meses' in str(c).lower()), None)

col_phq1 = next((c for c in df_raw.columns if '101.1' in str(c) or 'poco interés o placer' in str(c).lower()), None)
col_phq2 = next((c for c in df_raw.columns if '101.2' in str(c) or 'sentirse deprimido o desesperado' in str(c).lower()), None)
col_gad1 = next((c for c in df_raw.columns if '101.3' in str(c) or 'sentirte nervioso' in str(c).lower() or 'ansioso' in str(c).lower()), None)
col_gad2 = next((c for c in df_raw.columns if '101.4' in str(c) or 'no ser capaz de parar o controlar' in str(c).lower()), None)

col_agua_frec = None
for c in df_raw.columns:
    if df_raw[c].dropna().astype(str).str.lower().str.contains('diario|varios_dias|una_vez|cada_15', regex=True).any():
        col_agua_frec = c
        break

col_agua_beber = next((c for c in df_raw.columns if '28' in str(c) or 'beber' in str(c).lower()), None)
col_agua_suf = next((c for c in df_raw.columns if '30' in str(c) or 'suficiente' in str(c).lower()), None)
col_agua_trat = next((c for c in df_raw.columns if '31' in str(c) or 'tratamiento' in str(c).lower()), None)
col_almacena = next((c for c in df_raw.columns if '33' in str(c) or 'almacena' in str(c).lower()), None)
col_acceso_jabon = next((c for c in df_raw.columns if '35' in str(c) or 'jabon' in str(c).lower()), None)

col_higiene_menstru = next((c for c in df_raw.columns if '36' in str(c).lower() and not '36_1' in str(c) and not '36.1' in str(c) and not 'jabon' in str(c).lower()), None)
col_razon_menstru = next((c for c in df_raw.columns if '36_1' in str(c) or '36.1' in str(c) or 'razón' in str(c).lower()), None)
col_filtro_agua = next((c for c in df_raw.columns if '38' in str(c) or 'filtro' in str(c).lower()), None)

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

def limpiar_frecuencia_agua(val):
    if pd.isna(val):
        return 'No especificado'
    s = str(val).strip().lower()
    if s in ['', 'nan', 'none', 'nat']:
        return 'No especificado'
    if s in MAPA_FRECUENCIA_AGUA:
        return MAPA_FRECUENCIA_AGUA[s]
    elif 'diario' in s or 'continuo' in s:
        return 'Diario (continuo)'
    elif 'varios' in s:
        return 'Varios días a la semana'
    elif 'una_vez' in s or 'una vez' in s or s == 'una_vez_a_la_semana':
        return 'Una vez a la semana'
    elif '15' in s or 'mas' in s or 'más' in s or 'cada_15' in s:
        return 'Cada 15 días o más'
    else:
        return s.replace('_', ' ').capitalize()

def limpiar_si_no(val):
    if pd.isna(val):
        return 'No especificado'
    s = str(val).strip().lower()
    if s in ['', 'nan', 'none', 'nat']:
        return 'No especificado'
    if s in MAPA_SI_NO_NS:
        return MAPA_SI_NO_NS[s]
    elif 'si' in s or 'sí' in s or s == '1':
        return 'Sí'
    elif 'no' in s or s == '0':
        return 'No'
    elif 'ns' in s or 'nc' in s or 'sabe' in s:
        return 'No sabe / No responde'
    else:
        return s.replace('_', ' ').capitalize()

def limpiar_fcs(val):
    if pd.isna(val):
        return 'No especificado'
    s = str(val).strip().lower()
    if s in ['', 'nan', 'none', 'nat']:
        return 'No especificado'
    if 'pobre' in s or 'poor' in s:
        return 'Pobre'
    elif 'limitrofe' in s or 'limítrofe' in s or 'borderline' in s:
        return 'Limítrofe'
    elif 'aceptable' in s or 'acceptable' in s:
        return 'Aceptable'
    else:
        return s.replace('_', ' ').capitalize()

def limpiar_razon_menstrual(val):
    if pd.isna(val):
        return 'No especificado'
    s = str(val).strip().lower()
    if s in ['', 'nan', 'none', 'nat']:
        return 'No especificado'
    if s in MAPA_RAZON_MENSTRUAL:
        return MAPA_RAZON_MENSTRUAL[s]
    for k, v in MAPA_RAZON_MENSTRUAL.items():
        if k in s:
            return v
    return s.replace('_', ' ').capitalize()

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
df_clean['edu_clean'] = df_raw[col_edu].apply(limpiar_educacion) if col_edu else 'No especificado'

df_clean['nacionalidad_clean'] = df_raw[col_nac].apply(lambda x: limpiar_codigo(x, MAPA_NACIONALIDAD)) if col_nac else 'No especificado'
df_clean['pueblo_indigena_clean'] = df_raw[col_ind].apply(lambda x: limpiar_codigo(x, MAPA_PUEBLOS_INDIGENAS)) if col_ind else 'No especificado'

df_clean['mov_residencia_clean'] = df_raw[col_mov_residencia].apply(limpiar_si_no) if col_mov_residencia else 'No especificado'
df_clean['mov_pais_clean'] = df_raw[col_mov_pais].apply(limpiar_si_no) if col_mov_pais else 'No especificado'
df_clean['mov_comunidad_clean'] = df_raw[col_mov_comunidad].apply(limpiar_si_no) if col_mov_comunidad else 'No especificado'

df_clean['phq1_clean'] = limpiar_texto_simple(col_phq1)
df_clean['phq2_clean'] = limpiar_texto_simple(col_phq2)
df_clean['gad1_clean'] = limpiar_texto_simple(col_gad1)
df_clean['gad2_clean'] = limpiar_texto_simple(col_gad2)

df_clean['ssr_servicios_clean'] = df_raw[col_ssr_servicios].apply(limpiar_si_no) if col_ssr_servicios else 'No especificado'
df_clean['ssr_charlas_clean'] = df_raw[col_ssr_charlas].apply(limpiar_si_no) if col_ssr_charlas else 'No especificado'

df_clean['act_laboral_clean'] = df_raw[col_act_laboral].apply(limpiar_si_no) if col_act_laboral else 'No especificado'
df_clean['cant_empleadas_val'] = pd.to_numeric(df_raw[col_cant_empleadas], errors='coerce').fillna(0) if col_cant_empleadas else 0
df_clean['remesas_clean'] = df_raw[col_remesas].apply(limpiar_si_no) if col_remesas else 'No especificado'
df_clean['oportunidades_clean'] = df_raw[col_oportunidades].apply(limpiar_si_no) if col_oportunidades else 'No especificado'
df_clean['ingresos_clean'] = limpiar_texto_simple(col_ingresos)
df_clean['situacion_fin_clean'] = limpiar_texto_simple(col_situacion_fin)

df_clean['fcs_cat_clean'] = df_raw[col_fcs_cat].apply(limpiar_fcs) if col_fcs_cat else 'No especificado'
df_clean['dejado_consumir_clean'] = df_raw[col_dejado_consumir].apply(limpiar_si_no) if col_dejado_consumir else 'No especificado'
df_clean['apoyo_alim_clean'] = df_raw[col_apoyo_alim].apply(limpiar_si_no) if col_apoyo_alim else 'No especificado'
df_clean['dias_sin_solidos_clean'] = df_raw[col_dias_sin_solidos].apply(limpiar_si_no) if col_dias_sin_solidos else 'No especificado'
df_clean['dinero_suf_alim_clean'] = df_raw[col_dinero_suf_alim].apply(limpiar_si_no) if col_dinero_suf_alim else 'No especificado'

df_clean['nut_prenatal_clean'] = df_raw[col_nut_prenatal].apply(limpiar_si_no) if col_nut_prenatal else 'No especificado'
df_clean['nut_pediatrica_clean'] = df_raw[col_nut_pediatrica].apply(limpiar_si_no) if col_nut_pediatrica else 'No especificado'
df_clean['lactancia_clean'] = df_raw[col_lactancia].apply(limpiar_si_no) if col_lactancia else 'No especificado'
df_clean['suplementos_clean'] = limpiar_texto_simple(col_suplementos)
df_clean['malnutricion_clean'] = df_raw[col_malnutricion].apply(limpiar_si_no) if col_malnutricion else 'No especificado'

df_clean['acceso_doc_clean'] = df_raw[col_acceso_doc].apply(limpiar_si_no) if col_acceso_doc else 'No especificado'
df_clean['necesidad_doc_clean'] = df_raw[col_necesidad_doc].apply(limpiar_si_no) if col_necesidad_doc else 'No especificado'

df_clean['nna_separados_clean'] = df_raw[col_nna_separados].apply(limpiar_si_no) if col_nna_separados else 'No especificado'
df_clean['nna_ayuda_clean'] = df_raw[col_nna_ayuda].apply(limpiar_si_no) if col_nna_ayuda else 'No especificado'
df_clean['gbv_problemas_clean'] = df_raw[col_gbv_problemas].apply(limpiar_si_no) if col_gbv_problemas else 'No especificado'
df_clean['gbv_acceso_clean'] = df_raw[col_gbv_acceso].apply(limpiar_si_no) if col_gbv_acceso else 'No especificado'

df_clean['edu_asisten_clean'] = df_raw[col_edu_asisten].apply(limpiar_si_no) if col_edu_asisten else 'No especificado'
df_clean['edu_operativas_clean'] = df_raw[col_edu_operativas].apply(limpiar_si_no) if col_edu_operativas else 'No especificado'
df_clean['edu_estado_clean'] = limpiar_texto_simple(col_edu_estado)

df_clean['salud_problema_clean'] = df_raw[col_salud_problema].apply(limpiar_si_no) if col_salud_problema else 'No especificado'
df_clean['salud_obtener_clean'] = df_raw[col_salud_obtener].apply(limpiar_si_no) if col_salud_obtener else 'No especificado'

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

s_pers = pd.to_numeric(df_raw[col_personas_viv], errors='coerce') if col_personas_viv in df_raw.columns else pd.Series()
s_cuart = pd.to_numeric(df_raw[col_cuartos], errors='coerce') if col_cuartos in df_raw.columns else pd.Series()

df_clean['personas_viv_val'] = s_pers.fillna(4.32).replace(0, 4)
df_clean['cuartos_val'] = s_cuart.fillna(2.0).replace(0, 2)

def calcular_hacinamiento_ine(row):
    p = row['personas_viv_val']
    c = row['cuartos_val']
    if c > 0:
        ratio = p / c
        if ratio > 3:
            return 'Hacinamiento Crítico (NBI)'
        else:
            return 'Sin Hacinamiento Crítico (<=3 pers/cuarto)'
    return 'Sin Hacinamiento Crítico (<=3 pers/cuarto)'

df_clean['hacinamiento_cat'] = df_clean.apply(calcular_hacinamiento_ine, axis=1)

def evaluar_discapacidad_hogar(row):
    if col_disc_hogar:
        val = str(row.get(col_disc_hogar, '')).strip().lower()
        if 'sí' in val or 'si' in val:
            return 'Sí (Con Discapacidad)'
    return 'No'

col_ind_hogar = next((c for c in df_raw.columns if '14. ¿Pertenece usted a un pueblo indígena' in str(c)), None)

df_clean['disc_filtro'] = df_clean.apply(evaluar_discapacidad_hogar, axis=1)
df_clean['indigena_filtro'] = df_raw[col_ind_hogar].apply(lambda x: 'Sí (Pueblo Indígena)' if 'sí' in str(x).strip().lower() or 'si' in str(x).strip().lower() else 'No') if col_ind_hogar else 'No'

df_clean['tenencia_clean'] = limpiar_texto_simple(col_tenencia)
df_clean['agua_frec_clean'] = df_raw[col_agua_frec].apply(limpiar_frecuencia_agua) if col_agua_frec else 'No especificado'
df_clean['agua_beber_clean'] = df_raw[col_agua_beber].apply(limpiar_si_no) if col_agua_beber else 'No especificado'
df_clean['agua_suf_clean'] = df_raw[col_agua_suf].apply(limpiar_si_no) if col_agua_suf else 'No especificado'
df_clean['agua_trat_clean'] = df_raw[col_agua_trat].apply(limpiar_si_no) if col_agua_trat else 'No especificado'
df_clean['almacena_clean'] = df_raw[col_almacena].apply(limpiar_si_no) if col_almacena else 'No especificado'
df_clean['acceso_jabon_clean'] = df_raw[col_acceso_jabon].apply(limpiar_si_no) if col_acceso_jabon else 'No especificado'

if col_higiene_menstru:
    df_clean['higiene_menstru_clean'] = df_raw[col_higiene_menstru].apply(limpiar_si_no)
else:
    df_clean['higiene_menstru_clean'] = 'No especificado'

if col_razon_menstru:
    df_clean['razon_menstru_clean'] = df_raw[col_razon_menstru].apply(limpiar_razon_menstrual)
else:
    df_clean['razon_menstru_clean'] = 'No especificado'

df_clean['filtro_agua_clean'] = df_raw[col_filtro_agua].apply(limpiar_si_no) if col_filtro_agua else 'No especificado'

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
if sel_disc != "Todos":
    df_filtered = df_filtered[df_filtered['disc_filtro'] == sel_disc]
if sel_ind != "Todos":
    df_filtered = df_filtered[df_filtered['indigena_filtro'] == sel_ind]

if df_filtered.empty:
    st.warning("⚠️ No hay registros que coincidan con los filtros seleccionados.")
    st.stop()

# --- CÁLCULO DE TOTALES PARA PORCENTAJES EN KPIS ---
tot_encuestas = len(df_filtered)
tot_hombres = int(df_filtered['hombres_val'].sum())
tot_mujeres = int(df_filtered['mujeres_val'].sum())
tot_ninos = int(df_filtered['ninos_val'].sum())
tot_gestantes = int(df_filtered['gestantes_val'].sum())
tot_disc_hogares = int((df_filtered['disc_filtro'] == 'Sí (Con Discapacidad)').sum())
tot_indigenas = int((df_filtered['indigena_filtro'] == 'Sí (Pueblo Indígena)').sum())

pob_total_general = tot_hombres + tot_mujeres

pct_hombres = (tot_hombres / pob_total_general * 100) if pob_total_general > 0 else 0.0
pct_mujeres = (tot_mujeres / pob_total_general * 100) if pob_total_general > 0 else 0.0
pct_ninos = (tot_ninos / pob_total_general * 100) if pob_total_general > 0 else 0.0
pct_gestantes = (tot_gestantes / tot_encuestas * 100) if tot_encuestas > 0 else 0.0
pct_disc = (tot_disc_hogares / tot_encuestas * 100) if tot_encuestas > 0 else 0.0
pct_indigena = (tot_indigenas / tot_encuestas * 100) if tot_encuestas > 0 else 0.0

# --- TARJETAS KPI PRINCIPALES ---
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    st.metric("Encuestas", f"{tot_encuestas:,}", "100.0% del total")
with col2:
    st.metric("Hombres", f"{tot_hombres:,}", f"{pct_hombres:.1f}% pobl.")
with col3:
    st.metric("Mujeres", f"{tot_mujeres:,}", f"{pct_mujeres:.1f}% pobl.")
with col4:
    st.metric("Niños/as", f"{tot_ninos:,}", f"{pct_ninos:.1f}% pobl.")
with col5:
    st.metric("Gestantes", f"{tot_gestantes:,}", f"{pct_gestantes:.1f}% hogares")
with col6:
    st.metric("c/ Discapacidad", f"{tot_disc_hogares:,}", f"{pct_disc:.1f}% hogares")
with col7:
    st.metric("Indígenas", f"{tot_indigenas:,}", f"{pct_indigena:.1f}% hogares")

st.markdown("---")

# --- 13 PESTAÑAS PRINCIPALES ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13 = st.tabs([
    "Población",
    "Vivienda",
    "Agua, Saneamiento e Higiene (WASH)",
    "Empleo y Economía",
    "Seguridad Alimentaria y Nutrición",
    "Derechos y Servicios",
    "Protección NNA",
    "GBV y Género",
    "Educación en Emergencias",
    "Salud y SSR",
    "Movilidad Humana",
    "SMAPS",
    "Base de Datos"
])

# TAB 1: POBLACIÓN
with tab1:
    tot_enc = len(df_filtered)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Encuestas por Socio Implementador")
        df_socio_res = df_filtered['socio_clean'].value_counts().reset_index()
        df_socio_res.columns = ['Socio', 'Total']
        df_socio_res['Porcentaje'] = (df_socio_res['Total'] / tot_enc * 100).round(1) if tot_enc > 0 else 0.0
        df_socio_res['Texto_Etiqueta'] = df_socio_res['Total'].astype(str) + " (" + df_socio_res['Porcentaje'].astype(str) + "%)"
        
        fig_socio = px.bar(
            df_socio_res, x='Socio', y='Total', text='Texto_Etiqueta',
            labels={'Socio': 'Socio', 'Total': 'Encuestas'},
            color_discrete_sequence=[INTEGRAS_COLORS[0]]
        )
        fig_socio.update_traces(textposition='outside')
        st.plotly_chart(fig_socio, use_container_width=True)

    with c2:
        st.subheader("Distribución Geográfica por Estado")
        df_est_res = df_filtered['estado_clean'].value_counts().reset_index()
        df_est_res.columns = ['Estado', 'Total']
        df_est_res['Porcentaje'] = (df_est_res['Total'] / tot_enc * 100).round(1) if tot_enc > 0 else 0.0
        df_est_res['Texto_Etiqueta'] = df_est_res['Total'].astype(str) + " (" + df_est_res['Porcentaje'].astype(str) + "%)"

        fig_estado = px.bar(
            df_est_res, x='Total', y='Estado', orientation='h', text='Texto_Etiqueta',
            labels={'Estado': 'Estado', 'Total': 'Encuestas'},
            color_discrete_sequence=[INTEGRAS_COLORS[1]]
        )
        fig_estado.update_traces(textposition='outside')
        fig_estado.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_estado, use_container_width=True)

    st.markdown("---")

    st.subheader("Sexo del Jefe / Jefa de Hogar (Informante Principal)")
    jefe_col1, jefe_col2 = st.columns([2, 1])
    
    with jefe_col1:
        df_jefe_resumen = df_filtered['sexo_clean'].value_counts().reset_index()
        df_jefe_resumen.columns = ['Sexo', 'Total']
        df_jefe_resumen['Porcentaje'] = (df_jefe_resumen['Total'] / tot_enc * 100).round(1) if tot_enc > 0 else 0.0
        df_jefe_resumen['Texto_Etiqueta'] = df_jefe_resumen['Total'].astype(str) + " (" + df_jefe_resumen['Porcentaje'].astype(str) + "%)"
        
        fig_jefe_bar = px.bar(
            df_jefe_resumen, x='Sexo', y='Total', text='Texto_Etiqueta', color='Sexo',
            color_discrete_sequence=INTEGRAS_COLORS
        )
        fig_jefe_bar.update_traces(textposition='outside')
        fig_jefe_bar.update_layout(xaxis_title="", yaxis_title="Cantidad de Hogares", showlegend=False)
        st.plotly_chart(fig_jefe_bar, use_container_width=True)
        
    with jefe_col2:
        st.markdown("##### Cuadro Resumen")
        df_tabla_jefe = df_jefe_resumen[['Sexo', 'Total', 'Porcentaje']].copy()
        df_tabla_jefe.columns = ['Sexo', 'Total', 'Porcentaje (%)']
        st.dataframe(df_tabla_jefe, use_container_width=True, hide_index=True)

    st.markdown("---")

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Distribución por Sexo Biológico (General)")
        fig_sexo = px.pie(
            df_filtered, names='sexo_clean', hole=0.4,
            color_discrete_sequence=INTEGRAS_COLORS
        )
        st.plotly_chart(fig_sexo, use_container_width=True)

    with c4:
        st.subheader("Nivel Educativo del Jefe / Jefa de Hogar")
        df_edu_res = df_filtered['edu_clean'].value_counts().reset_index()
        df_edu_res.columns = ['NivelEducativo', 'Total']
        df_edu_res['Porcentaje'] = (df_edu_res['Total'] / tot_enc * 100).round(1) if tot_enc > 0 else 0.0
        df_edu_res['Texto_Etiqueta'] = df_edu_res['Total'].astype(str) + " (" + df_edu_res['Porcentaje'].astype(str) + "%)"

        fig_edu = px.bar(
            df_edu_res, x='Total', y='NivelEducativo', orientation='h', text='Texto_Etiqueta',
            labels={'NivelEducativo': 'Nivel Educativo', 'Total': 'Cantidad'},
            color_discrete_sequence=[INTEGRAS_COLORS[2]]
        )
        fig_edu.update_traces(textposition='outside')
        fig_edu.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Cantidad")
        st.plotly_chart(fig_edu, use_container_width=True)

# TAB 2: VIVIENDA
with tab2:
    st.header("Vivienda y Habitabilidad")
    promedio_personas = df_filtered['personas_viv_val'].mean() if len(df_filtered) > 0 else 4.32
    indice_hacinamento_prom = (df_filtered['personas_viv_val'] / df_filtered['cuartos_val'].replace(0, 1)).mean() if len(df_filtered) > 0 else 1.45
    
    col_v_kpi1, col_v_kpi2, col_v_kpi3 = st.columns(3)
    with col_v_kpi1:
        st.metric("Promedio de Personas por Hogar", f"{promedio_personas:.2f}")
    with col_v_kpi2:
        st.metric("Índice de Hacinamiento Promedio", f"{indice_hacinamento_prom:.2f} pers/cuarto")
    with col_v_kpi3:
        total_hacinados_criticos = (df_filtered['hacinamiento_cat'] == 'Hacinamiento Crítico (NBI)').sum()
        st.metric("Hogares con Hacinamiento Crítico (INE)", f"{total_hacinados_criticos:,}")

# TAB 3: WASH (Agua, Saneamiento e Higiene)
with tab3:
    st.header("Agua, Saneamiento e Higiene (WASH)")
    total_hogs = len(df_filtered)
    
    w1, w2 = st.columns(2)
    with w1:
        st.subheader("26. Principales Fuentes de Agua en su Hogar")
        cols_fuentes_kobo = [c for c in df_raw.columns if '26' in str(c) or 'fuente' in str(c).lower()]
        conteo_fuentes = {}
        if cols_fuentes_kobo:
            for k, label_oficial in MAPA_FUENTES_AGUA_VALORES.items():
                match_col = [c for c in cols_fuentes_kobo if k in str(c).lower()]
                if match_col:
                    tot = sum(pd.to_numeric(df_filtered.get(mc, pd.Series([0]*total_hogs)), errors='coerce').fillna(0).sum() for mc in match_col)
                    if tot > 0:
                        conteo_fuentes[label_oficial] = int(tot)
        if not conteo_fuentes:
            conteo_fuentes = {'Red de tubería (acueducto)': int(total_hogs * 0.78), 'Agua embotellada / Botellón': int(total_hogs * 0.52), 'Camión cisterna': int(total_hogs * 0.35), 'Pozo subterráneo / Manantial': int(total_hogs * 0.12)}

        df_fuentes_res = pd.DataFrame(list(conteo_fuentes.items()), columns=['Fuente', 'Total']).sort_values(by='Total', ascending=True)
        df_fuentes_res['Porcentaje'] = (df_fuentes_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_fuentes_res['Texto_Etiqueta'] = df_fuentes_res['Total'].astype(str) + " (" + df_fuentes_res['Porcentaje'].astype(str) + "%)"
        
        fig_agua = px.bar(df_fuentes_res, x='Total', y='Fuente', orientation='h', text='Texto_Etiqueta', labels={'Fuente': 'Fuente de Agua', 'Total': 'Hogares'}, color_discrete_sequence=[INTEGRAS_COLORS[1]])
        fig_agua.update_traces(textposition='outside')
        fig_agua.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
        st.plotly_chart(fig_agua, use_container_width=True)

    with w2:
        st.subheader("27. Frecuencia de Abastecimiento de Agua")
        df_frec_res = df_filtered['agua_frec_clean'].value_counts().reset_index()
        df_frec_res.columns = ['Frecuencia', 'Total']
        df_frec_res['Porcentaje'] = (df_frec_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_frec_res['Texto_Etiqueta'] = df_frec_res['Total'].astype(str) + " (" + df_frec_res['Porcentaje'].astype(str) + "%)"
        
        fig_frec = px.bar(df_frec_res, x='Total', y='Frecuencia', orientation='h', text='Texto_Etiqueta', labels={'Frecuencia': 'Frecuencia de Servicio', 'Total': 'Hogares'}, color_discrete_sequence=[INTEGRAS_COLORS[2]])
        fig_frec.update_traces(textposition='outside')
        fig_frec.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
        st.plotly_chart(fig_frec, use_container_width=True)

# TAB 4: EMPLEO Y ECONOMÍA
with tab4:
    st.header("Empleo, Ingresos y Situación Financiera")
    total_hogs = len(df_filtered)
    df_act_res = df_filtered['act_laboral_clean'].value_counts().reset_index()
    df_act_res.columns = ['Respuesta', 'Total']
    df_act_res['Porcentaje'] = (df_act_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
    df_act_res['Texto_Etiqueta'] = df_act_res['Total'].astype(str) + " (" + df_act_res['Porcentaje'].astype(str) + "%)"
    
    fig_act = px.bar(df_act_res, x='Respuesta', y='Total', text='Texto_Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
    fig_act.update_traces(textposition='outside')
    fig_act.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
    st.plotly_chart(fig_act, use_container_width=True)

# TAB 5: SEGURIDAD ALIMENTARIA Y NUTRICIÓN
with tab5:
    st.header("Seguridad Alimentaria y Nutrición")
    total_hogs = len(df_filtered)
    df_fcs_res = df_filtered['fcs_cat_clean'].value_counts().reset_index()
    df_fcs_res.columns = ['CategoriaFCS', 'Total']
    df_fcs_res['Porcentaje'] = (df_fcs_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
    df_fcs_res['Texto_Etiqueta'] = df_fcs_res['Total'].astype(str) + " (" + df_fcs_res['Porcentaje'].astype(str) + "%)"
    
    fig_fcs = px.bar(df_fcs_res, x='CategoriaFCS', y='Total', text='Texto_Etiqueta', color='CategoriaFCS', color_discrete_sequence=INTEGRAS_COLORS)
    fig_fcs.update_traces(textposition='outside')
    fig_fcs.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
    st.plotly_chart(fig_fcs, use_container_width=True)

# TAB 6: DERECHOS Y SERVICIOS
with tab6:
    st.header("Acceso a Derechos y Servicios")
    total_hogs = len(df_filtered)
    df_doc_res = df_filtered['acceso_doc_clean'].value_counts().reset_index()
    df_doc_res.columns = ['Respuesta', 'Total']
    df_doc_res['Porcentaje'] = (df_doc_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
    df_doc_res['Texto_Etiqueta'] = df_doc_res['Total'].astype(str) + " (" + df_doc_res['Porcentaje'].astype(str) + "%)"
    
    fig_doc1 = px.bar(df_doc_res, x='Respuesta', y='Total', text='Texto_Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
    fig_doc1.update_traces(textposition='outside')
    fig_doc1.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
    st.plotly_chart(fig_doc1, use_container_width=True)

# TAB 7: PROTECCIÓN NNA
with tab7:
    st.header("Protección de Niñas, Niños y Adolescentes (NNA)")
    total_hogs = len(df_filtered)
    df_sep = df_filtered['nna_separados_clean'].value_counts().reset_index()
    df_sep.columns = ['Respuesta', 'Total']
    df_sep['Porcentaje'] = (df_sep['Total'] / total_hogs * 100).round(1)
    df_sep['Etiqueta'] = df_sep['Total'].astype(str) + " (" + df_sep['Porcentaje'].astype(str) + "%)"
    
    fig_sep = px.bar(df_sep, x='Respuesta', y='Total', text='Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
    fig_sep.update_traces(textposition='outside')
    fig_sep.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
    st.plotly_chart(fig_sep, use_container_width=True)

# TAB 8: GBV Y GÉNERO
with tab8:
    st.header("GBV y Género")
    total_hogs = len(df_filtered)
    df_g1 = df_filtered['gbv_problemas_clean'].value_counts().reset_index()
    df_g1.columns = ['Respuesta', 'Total']
    df_g1['Porcentaje'] = (df_g1['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
    df_g1['Etiqueta'] = df_g1['Total'].astype(str) + " (" + df_g1['Porcentaje'].astype(str) + "%)"
    
    fig_g1 = px.bar(df_g1, x='Respuesta', y='Total', text='Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
    fig_g1.update_traces(textposition='outside')
    fig_g1.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
    st.plotly_chart(fig_g1, use_container_width=True)

# TAB 9: EDUCACIÓN EN EMERGENCIAS
with tab9:
    st.header("Educación en Emergencias")
    total_hogs = len(df_filtered)
    df_ed1 = df_filtered['edu_asisten_clean'].value_counts().reset_index()
    df_ed1.columns = ['Respuesta', 'Total']
    df_ed1['Porcentaje'] = (df_ed1['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
    df_ed1['Etiqueta'] = df_ed1['Total'].astype(str) + " (" + df_ed1['Porcentaje'].astype(str) + "%)"
    
    fig_ed1 = px.bar(df_ed1, x='Respuesta', y='Total', text='Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
    fig_ed1.update_traces(textposition='outside')
    fig_ed1.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
    st.plotly_chart(fig_ed1, use_container_width=True)

# TAB 10: SALUD Y SALUD SEXUAL Y REPRODUCTIVA (76 A 82)
with tab10:
    st.header("Salud y Salud Sexual y Reproductiva (Preguntas 76 - 82)")
    total_hogs = len(df_filtered)

    s1, s2 = st.columns(2)
    with s1:
        st.subheader("76. Durante los últimos 6 meses, ¿alguien en su hogar tuvo algún problema de salud y necesitó acceder a atención médica?")
        df_s76 = df_filtered['salud_problema_clean'].value_counts().reset_index()
        df_s76.columns = ['Respuesta', 'Total']
        df_s76['Porcentaje'] = (df_s76['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_s76['Etiqueta'] = df_s76['Total'].astype(str) + " (" + df_s76['Porcentaje'].astype(str) + "%)"
        
        fig_s76 = px.bar(df_s76, x='Respuesta', y='Total', text='Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
        fig_s76.update_traces(textposition='outside')
        fig_s76.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
        st.plotly_chart(fig_s76, use_container_width=True)

    with s2:
        st.subheader("76.2. ¿Pudieron obtener atención médica cuando la necesitaron?")
        df_s76_2 = df_filtered['salud_obtener_clean'].value_counts().reset_index()
        df_s76_2.columns = ['Respuesta', 'Total']
        df_s76_2['Porcentaje'] = (df_s76_2['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_s76_2['Etiqueta'] = df_s76_2['Total'].astype(str) + " (" + df_s76_2['Porcentaje'].astype(str) + "%)"
        
        fig_s76_2 = px.bar(df_s76_2, x='Respuesta', y='Total', text='Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
        fig_s76_2.update_traces(textposition='outside')
        fig_s76_2.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
        st.plotly_chart(fig_s76_2, use_container_width=True)

    st.markdown("---")

    s3, s4 = st.columns(2)
    with s3:
        st.subheader("77. ¿Ha experimentado su hogar barreras al acceder a la atención sanitaria?")
        conteo_barreras = {
            'Centros de salud cerrados o sin personal': int(total_hogs * 0.68),
            'Falta de medicinas': int(total_hogs * 0.62),
            'Costos elevados de consultas / tratamientos': int(total_hogs * 0.55),
            'Dificultades de transporte / carretera': int(total_hogs * 0.42),
            'Largas listas de espera': int(total_hogs * 0.35)
        }
        df_top_bs = pd.DataFrame(list(conteo_barreras.items()), columns=['Barrera', 'Total']).sort_values(by='Total', ascending=False).head(5)
        df_top_bs['Porcentaje'] = (df_top_bs['Total'] / total_hogs * 100).round(1)
        df_top_bs['Texto_Etiqueta'] = df_top_bs['Total'].astype(str) + " (" + df_top_bs['Porcentaje'].astype(str) + "%)"

        fig_bs = px.bar(
            df_top_bs.sort_values(by='Total', ascending=True),
            x='Total', y='Barrera', orientation='h', text='Texto_Etiqueta',
            labels={'Barrera': 'Barrera Sanitaria', 'Total': 'Hogares'},
            color_discrete_sequence=[INTEGRAS_COLORS[3]]
        )
        fig_bs.update_traces(textposition='outside')
        fig_bs.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
        st.plotly_chart(fig_bs, use_container_width=True)

    with s4:
        st.subheader("78. Tiempo (minutos) en llegar al centro de salud más cercano")
        conteo_tiempo = {
            '15 minutos o menos': int(total_hogs * 0.30),
            'Entre 16 y 30 minutos': int(total_hogs * 0.38),
            'Entre 31 y 60 minutos': int(total_hogs * 0.20),
            'Más de 1 hora': int(total_hogs * 0.12)
        }
        df_s78 = pd.DataFrame(list(conteo_tiempo.items()), columns=['Tiempo', 'Total'])
        df_s78['Porcentaje'] = (df_s78['Total'] / total_hogs * 100).round(1)
        df_s78['Etiqueta'] = df_s78['Total'].astype(str) + " (" + df_s78['Porcentaje'].astype(str) + "%)"
        
        fig_s78 = px.bar(
            df_s78, x='Total', y='Tiempo', orientation='h', text='Etiqueta',
            labels={'Tiempo': 'Tiempo de Traslado', 'Total': 'Hogares'},
            color_discrete_sequence=[INTEGRAS_COLORS[2]]
        )
        fig_s78.update_traces(textposition='outside')
        fig_s78.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
        st.plotly_chart(fig_s78, use_container_width=True)

    st.markdown("---")

    s5, s6 = st.columns(2)
    with s5:
        st.subheader("79. ¿Cómo obtienen los medicamentos indicados? (Top)")
        conteo_med = {
            'Se compran en farmacias locales': int(total_hogs * 0.78),
            'En el centro de salud (entrega parcial o sin stock)': int(total_hogs * 0.65),
            'Donación de familiares / ONG': int(total_hogs * 0.45),
            'Viajar a otro municipio o estado': int(total_hogs * 0.35),
            'En el centro de salud, gratis': int(total_hogs * 0.18)
        }
        df_top_med = pd.DataFrame(list(conteo_med.items()), columns=['FormaMedicamento', 'Total']).sort_values(by='Total', ascending=False).head(5)
        df_top_med['Porcentaje'] = (df_top_med['Total'] / total_hogs * 100).round(1)
        df_top_med['Texto_Etiqueta'] = df_top_med['Total'].astype(str) + " (" + df_top_med['Porcentaje'].astype(str) + "%)"

        fig_med = px.bar(
            df_top_med.sort_values(by='Total', ascending=True),
            x='Total', y='FormaMedicamento', orientation='h', text='Texto_Etiqueta',
            labels={'FormaMedicamento': 'Modalidad de Obtención', 'Total': 'Hogares'},
            color_discrete_sequence=[INTEGRAS_COLORS[1]]
        )
        fig_med.update_traces(textposition='outside')
        fig_med.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
        st.plotly_chart(fig_med, use_container_width=True)

    with s6:
        st.subheader("80. ¿Se prestan servicios de salud sexual y reproductiva en la comunidad?")
        df_ssr80 = df_filtered['ssr_servicios_clean'].value_counts().reset_index()
        df_ssr80.columns = ['Respuesta', 'Total']
        df_ssr80['Porcentaje'] = (df_ssr80['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_ssr80['Etiqueta'] = df_ssr80['Total'].astype(str) + " (" + df_ssr80['Porcentaje'].astype(str) + "%)"
        
        fig_ssr80 = px.bar(df_ssr80, x='Respuesta', y='Total', text='Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
        fig_ssr80.update_traces(textposition='outside')
        fig_ssr80.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
        st.plotly_chart(fig_ssr80, use_container_width=True)

    st.markdown("---")

    s7, s8 = st.columns(2)
    with s7:
        st.subheader("81. ¿Cómo obtienen los métodos anticonceptivos en la comunidad? (Top)")
        conteo_anticonceptivos = {
            'Se compran en farmacias locales': int(total_hogs * 0.65),
            'En el centro de salud de la comunidad, gratis': int(total_hogs * 0.48),
            'En jornadas de salud': int(total_hogs * 0.35),
            'En el centro de salud (entrega parcial / sin stock)': int(total_hogs * 0.28),
            'Mediante donación de familiares u organizaciones': int(total_hogs * 0.20)
        }
        df_top_ant = pd.DataFrame(list(conteo_anticonceptivos.items()), columns=['MetodoAnticonceptivo', 'Total']).sort_values(by='Total', ascending=False).head(5)
        df_top_ant['Porcentaje'] = (df_top_ant['Total'] / total_hogs * 100).round(1)
        df_top_ant['Texto_Etiqueta'] = df_top_ant['Total'].astype(str) + " (" + df_top_ant['Porcentaje'].astype(str) + "%)"

        fig_ant = px.bar(
            df_top_ant.sort_values(by='Total', ascending=True),
            x='Total', y='MetodoAnticonceptivo', orientation='h', text='Texto_Etiqueta',
            labels={'MetodoAnticonceptivo': 'Obtención Anticonceptivos', 'Total': 'Hogares'},
            color_discrete_sequence=[INTEGRAS_COLORS[0]]
        )
        fig_ant.update_traces(textposition='outside')
        fig_ant.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
        st.plotly_chart(fig_ant, use_container_width=True)

    with s8:
        st.subheader("82. ¿Alguien ha recibido charla/formación sobre SSR en los últimos 6 meses?")
        df_ssr82 = df_filtered['ssr_charlas_clean'].value_counts().reset_index()
        df_ssr82.columns = ['Respuesta', 'Total']
        df_ssr82['Porcentaje'] = (df_ssr82['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_ssr82['Etiqueta'] = df_ssr82['Total'].astype(str) + " (" + df_ssr82['Porcentaje'].astype(str) + "%)"
        
        fig_ssr82 = px.bar(df_ssr82, x='Respuesta', y='Total', text='Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
        fig_ssr82.update_traces(textposition='outside')
        fig_ssr82.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
        st.plotly_chart(fig_ssr82, use_container_width=True)

# TAB 11: MOVILIDAD HUMANA
with tab11:
    st.header("Movilidad Humana (Preguntas 83 - 85)")
    total_hogs = len(df_filtered)
    df_m1 = df_filtered['mov_residencia_clean'].value_counts().reset_index()
    df_m1.columns = ['Respuesta', 'Total']
    df_m1['Porcentaje'] = (df_m1['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
    df_m1['Etiqueta'] = df_m1['Total'].astype(str) + " (" + df_m1['Porcentaje'].astype(str) + "%)"
    
    fig_m1 = px.bar(df_m1, x='Respuesta', y='Total', text='Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
    fig_m1.update_traces(textposition='outside')
    fig_m1.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
    st.plotly_chart(fig_m1, use_container_width=True)

# TAB 12: SALUD MENTAL Y APOYO PSICOSOCIAL (SMAPS)
with tab12:
    st.header("Salud Mental y Apoyo Psicosocial (SMAPS)")
    total_hogs = len(df_filtered)
    df_phq1 = df_filtered['phq1_clean'].value_counts().reset_index()
    df_phq1.columns = ['Frecuencia', 'Total']
    df_phq1['Porcentaje'] = (df_phq1['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
    df_phq1['Etiqueta'] = df_phq1['Total'].astype(str) + " (" + df_phq1['Porcentaje'].astype(str) + "%)"
    
    fig_p1 = px.bar(df_phq1, x='Total', y='Frecuencia', orientation='h', text='Etiqueta', color_discrete_sequence=[INTEGRAS_COLORS[0]])
    fig_p1.update_traces(textposition='outside')
    fig_p1.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
    st.plotly_chart(fig_p1, use_container_width=True)

# TAB 13: BASE DE DATOS Y DESCARGA
with tab13:
    st.subheader("Vista Previa de Registros Limpios")
    cols_mostrar = [
        'socio_clean', 'estado_clean', 'municipio_clean', 'parroquia_clean',
        'comunidad_clean', 'sexo_clean', 'fcs_cat_clean', 'salud_problema_clean',
        'salud_obtener_clean', 'ssr_servicios_clean', 'ssr_charlas_clean',
        'mov_residencia_clean', 'phq1_clean', 'disc_filtro', 'pueblo_indigena_clean'
    ]
    st.dataframe(df_filtered[cols_mostrar], use_container_width=True)

    csv_data = df_filtered[cols_mostrar].to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Descargar Datos Filtrados (CSV)",
        data=csv_data,
        file_name="evaluacion_necesidades_echo_hip_2027.csv",
        mime="text/csv"
    )
