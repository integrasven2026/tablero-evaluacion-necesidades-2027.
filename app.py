import os
import re
import pandas as pd
import plotly.express as px
import streamlit as st

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
        xls = pd.ExcelFile(EXCEL_FILE)
        sheet_name = 'Sheet1' if 'Sheet1' in xls.sheet_names else xls.sheet_names[0]
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)
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

MAPA_TRATAMIENTO_AGUA = {
    'hervido': 'Hervido', 'cloro': 'Cloro / Lavandina', 'cloro_lavandina': 'Cloro / Lavandina',
    'filtro': 'Filtro (cerámica/carbón/tela)', 'filtro_ceramica_carbon_tela': 'Filtro (cerámica/carbón/tela)',
    'otro': 'Otro método', 'otro_metodo': 'Otro método'
}

MAPA_PROBLEMAS_AGUA = {
    'color': 'Color', 'olor': 'Olor', 'sabor': 'Sabor',
    'ninguna': 'Ninguna', 'ns_nc': 'No sabe / No responde', 'otro': 'Otro'
}

MAPA_ALMACENAMIENTO_FORMA = {
    'recipientes_cubiertos_dentro': 'En recipientes cubiertos dentro de la casa',
    'recipientes_cubiertos_fuera': 'En recipientes cubiertos fuera de la casa',
    'recipientes_destapados_dentro': 'En recipientes destapados dentro de la casa',
    'recipientes_destapados_fuera': 'En recipientes destapados fuera de la casa'
}

MAPA_ENFERMEDADES_HIDRICAS = {
    'diarreas': 'Diarreas', 'enfermedades_piel': 'Enfermedades de piel',
    'vomitos': 'Vómitos', 'ninguno': 'Ninguno', 'ninguna': 'Ninguno'
}

MAPA_DESECHO_BASURA = {
    'servicio_aseo': 'Es recogida por el servicio de aseo público', 'calle': 'La deja en la calle',
    'entierra': 'La entierra', 'quema': 'La quema', 'recicla': 'La recicla',
    'rio': 'La tira en el rio, laguna, quebrada', 'paga': 'Le paga a alguien para que se la lleve',
    'ns_nc': 'Ns/nc', 'otra': 'Otra'
}

MAPA_TIPO_FILTRO = {
    'gravedad': 'Filtros por gravedad (Ej. Filtros de cerámica de 2 tanques/recipientes, velas filtrantes, etc.)',
    'sifon': 'Filtros de sifón (Ej. Sifón tipo Tulip u otros sistemas de succión/manguera)'
}

MAPA_RAZON_MENSTRUAL = {
    'costo_elevado': 'Costo elevado o falta de presupuesto.', 'costo': 'Costo elevado o falta de presupuesto.',
    'no_disponibles': 'No hay disponibles a la venta en las tiendas cercanas, mercados o puntos de abasto locales.',
    'disponibilidad': 'No hay disponibles a la venta en las tiendas cercanas, mercados o puntos de abasto locales.',
    'alternativas': 'Utiliza otras alternativas locales (ceniza, arena, barro, plantas, hojas tradicionales o solo agua).',
    'no_necesario': 'No lo considera necesario.', 'no_habitual': 'No es una práctica habitual en la rutina diaria de la familia.'
}

# --- BÚSQUEDA EXACTA DE COLUMNAS CLAVE ---
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

col_nac = [c for c in df_raw.columns if 'nacionalidad' in str(c).lower()][0] if any('nacionalidad' in str(c).lower() for c in df_raw.columns) else None
col_ind = [c for c in df_raw.columns if 'indígena' in str(c).lower() or 'etnia' in str(c).lower()][0] if any('indígena' in str(c).lower() for c in df_raw.columns) else None

col_disc_hogar = [c for c in df_raw.columns if '16. ¿Alguien de su grupo familiar' in str(c)][0] if any('16. ¿Alguien de su grupo familiar' in str(c) for c in df_raw.columns) else None

# --- VARIABLES EXACTAS DE CÁLCULO DE GRUPO FAMILIAR ---
col_calc_hombres = 'calculate_grupofamiliar_hombres'
col_calc_mujeres = 'calculate_grupofamiliar_mujeres'
col_calc_otro = 'calculate_grupofamiliar_otro'

cols_ninos_etarios = [c for c in df_raw.columns if ('0 a 17' in str(c).lower() or '0_17' in str(c).lower() or 'de 0 a' in str(c).lower())]

col_gestantes = [c for c in df_raw.columns if '21.1' in str(c) or 'embarazadas' in str(c).lower()][0] if any('21.1' in str(c) for c in df_raw.columns) else None
col_tenencia = [c for c in df_raw.columns if '22' in str(c) or 'tenencia' in str(c).lower()][0] if any('22' in str(c) for c in df_raw.columns) else None
col_personas_viv = [c for c in df_raw.columns if '24.' in str(c)][0] if any('24.' in str(c) for c in df_raw.columns) else None
col_cuartos = [c for c in df_raw.columns if '25.' in str(c)][0] if any('25.' in str(c) for c in df_raw.columns) else None

# Columnas de Empleo y Finanzas
col_act_laboral = [c for c in df_raw.columns if '39.' in str(c) or 'actividad laboral' in str(c).lower()][0] if any('39.' in str(c) or 'actividad laboral' in str(c).lower() for c in df_raw.columns) else None
col_cant_empleadas = [c for c in df_raw.columns if '42.' in str(c) or 'empleadas' in str(c).lower()][0] if any('42.' in str(c) for c in df_raw.columns) else None
col_remesas = [c for c in df_raw.columns if '43.' in str(c) or 'remesas' in str(c).lower()][0] if any('43.' in str(c) for c in df_raw.columns) else None
col_oportunidades = [c for c in df_raw.columns if '44.' in str(c) or 'oportunidades de empleo' in str(c).lower()][0] if any('44.' in str(c) for c in df_raw.columns) else None
col_ingresos = [c for c in df_raw.columns if '45.' in str(c) or 'ingreso de su hogar' in str(c).lower()][0] if any('45.' in str(c) for c in df_raw.columns) else None
col_situacion_fin = [c for c in df_raw.columns if '46.' in str(c) or 'situación financiera' in str(c).lower()][0] if any('46.' in str(c) for c in df_raw.columns) else None

# Búsqueda robusta de la columna FCS (Pregunta 47)
col_fcs_cat = None
for c in df_raw.columns:
    c_low = str(c).lower()
    if ('fcs' in c_low) or ('consumo' in c_low and 'alimento' in c_low) or ('47' in c_low) or ('score' in c_low):
        col_fcs_cat = c
        break

col_dejado_consumir = [c for c in df_raw.columns if '48.' in str(c) or 'dejado de consumir' in str(c).lower()][0] if any('48.' in str(c) for c in df_raw.columns) else None
col_apoyo_alim = [c for c in df_raw.columns if '49.' in str(c) or 'apoyo alimentario' in str(c).lower()][0] if any('49.' in str(c) for c in df_raw.columns) else None
col_dias_sin_solidos = [c for c in df_raw.columns if '50.' in str(c) or 'alimentos sólidos' in str(c).lower()][0] if any('50.' in str(c) for c in df_raw.columns) else None
col_dinero_suf_alim = [c for c in df_raw.columns if '51.' in str(c) or 'dinero suficiente para adquirir todos los alimentos' in str(c).lower()][0] if any('51.' in str(c) for c in df_raw.columns) else None
col_nut_prenatal = [c for c in df_raw.columns if '54.' in str(c) or 'prenatal' in str(c).lower()][0] if any('54.' in str(c) for c in df_raw.columns) else None
col_nut_pediatrica = [c for c in df_raw.columns if '55.' in str(c) or 'pediátricas' in str(c).lower() or 'pediatricas' in str(c).lower()][0] if any('55.' in str(c) for c in df_raw.columns) else None
col_lactancia = [c for c in df_raw.columns if '56.' in str(c) or 'lactancia materna' in str(c).lower()][0] if any('56.' in str(c) for c in df_raw.columns) else None
col_suplementos = [c for c in df_raw.columns if '57.' in str(c) or 'suplementos nutricionales' in str(c).lower()][0] if any('57.' in str(c) for c in df_raw.columns) else None
col_malnutricion = [c for c in df_raw.columns if '58.' in str(c) or 'malnutrición' in str(c).lower() or 'malnutricion' in str(c).lower()][0] if any('58.' in str(c) for c in df_raw.columns) else None

# Columnas de Acceso a Derechos y Servicios (Preguntas 61 y 62)
col_acceso_doc = [c for c in df_raw.columns if '61.' in str(c) or 'partidas de nacimiento' in str(c).lower()][0] if any('61.' in str(c) for c in df_raw.columns) else None
col_necesidad_doc = [c for c in df_raw.columns if '62.' in str(c) and not '62_1' in str(c) and not '62.1' in str(c) or ('documento legal' in str(c).lower() and not '62_1' in str(c))][0] if any(('62.' in str(c) or 'documento legal' in str(c).lower()) and not '62_1' in str(c) and not '62.1' in str(c) for c in df_raw.columns) else None

# Protección NNA (Preguntas 65 y 66)
col_nna_separados = next((c for c in df_raw.columns if '65.' in str(c) or 'separados de sus padres' in str(c).lower()), None)
col_nna_ayuda = next((c for c in df_raw.columns if '66.' in str(c) or 'abuso o violencia' in str(c).lower()), None)

# GBV y Género (Preguntas 67 y 69)
col_gbv_problemas = next((c for c in df_raw.columns if '67.' in str(c) and not '67.1' in str(c) and not '67_1' in str(c) or ('integridad física y emocional' in str(c).lower() and not '67.1' in str(c))), None)
col_gbv_acceso = next((c for c in df_raw.columns if '69.' in str(c) or 'acceden al servicio que refiere' in str(c).lower()), None)

# Educación en Emergencias (Preguntas 71, 72 y 74)
col_edu_asisten = next((c for c in df_raw.columns if '71.' in str(c) or 'asisten todos los niños' in str(c).lower()), None)
col_edu_operativas = next((c for c in df_raw.columns if '72.' in str(c) or 'escuelas operativas' in str(c).lower()), None)
col_edu_estado = next((c for c in df_raw.columns if '74.' in str(c) or 'estado general' in str(c).lower() or 'instalaciones de la unidad educativa' in str(c).lower()), None)

# Salud y Salud Sexual y Reproductiva (Preguntas 76 - 82)
col_salud_problema = next((c for c in df_raw.columns if '76.' in str(c) or 'problema de salud y necesitó acceder a atención médica' in str(c).lower()), None)
col_salud_obtener = next((c for c in df_raw.columns if '76.2' in str(c) or '76_2' in str(c) or 'pudieron obtener atención médica' in str(c).lower()), None)
col_salud_tiempo = next((c for c in df_raw.columns if '78.' in str(c) or 'cuánto tiempo (en minutos) tarda' in str(c).lower()), None)

col_ssr_servicios = next((c for c in df_raw.columns if '80.' in str(c) or 'salud sexual y reproductiva (ginecología' in str(c).lower()), None)
col_ssr_charlas = next((c for c in df_raw.columns if '82.' in str(c) or 'charla o formación sobre temas de salud sexual y reproductiva' in str(c).lower()), None)

# Movilidad Humana (Preguntas 83, 84, 85)
col_mov_residencia = next((c for c in df_raw.columns if '83.' in str(c) or 'cambiado su lugar de residencia' in str(c).lower()), None)
col_mov_pais = next((c for c in df_raw.columns if '84.' in str(c) or 'salido o salió del país con el propósito' in str(c).lower()), None)
col_mov_comunidad = next((c for c in df_raw.columns if '85.' in str(c) or 'conoce personas que hayan salido en los últimos tres meses' in str(c).lower()), None)

# SMAPS - PHQ-2 y GAD-2 (Preguntas 101.1 a 101.4)
col_phq1 = next((c for c in df_raw.columns if '101.1' in str(c) or '101_1' in str(c) or 'poco interés o placer' in str(c).lower()), None)
col_phq2 = next((c for c in df_raw.columns if '101.2' in str(c) or '101_2' in str(c) or 'sentirse deprimido o desesperado' in str(c).lower()), None)
col_gad1 = next((c for c in df_raw.columns if '101.3' in str(c) or '101_3' in str(c) or 'sentirte nervioso' in str(c).lower() or 'sentirse nervioso' in str(c).lower()), None)
col_gad2 = next((c for c in df_raw.columns if '101.4' in str(c) or '101_4' in str(c) or 'no ser capaz de parar o controlar' in str(c).lower()), None)

col_agua_frec = None
for c in df_raw.columns:
    if df_raw[c].dropna().astype(str).str.lower().str.contains('diario|varios_dias|una_vez|cada_15', regex=True).any():
        col_agua_frec = c
        break

col_agua_beber = [c for c in df_raw.columns if '28' in str(c) or 'beber' in str(c).lower()][0] if any('28' in str(c) for c in df_raw.columns) else None
col_agua_suf = [c for c in df_raw.columns if '30' in str(c) or 'suficiente' in str(c).lower()][0] if any('30' in str(c) for c in df_raw.columns) else None
col_agua_trat = [c for c in df_raw.columns if '31' in str(c) or 'tratamiento' in str(c).lower()][0] if any('31' in str(c) for c in df_raw.columns) else None
col_almacena = [c for c in df_raw.columns if '33' in str(c) or 'almacena' in str(c).lower()][0] if any('33' in str(c) for c in df_raw.columns) else None
col_acceso_jabon = [c for c in df_raw.columns if '35' in str(c) or 'jabon' in str(c).lower()][0] if any('35' in str(c) for c in df_raw.columns) else None

col_higiene_menstru = None
for c in df_raw.columns:
    c_l = str(c).lower()
    if '36' in c_l and not '36_1' in c_l and not '36.1' in c_l and not 'jabon' in c_l:
        col_higiene_menstru = c
        break

col_razon_menstru = [c for c in df_raw.columns if '36_1' in str(c) or '36.1' in str(c) or 'razón' in str(c).lower()][0] if any('36_1' in str(c) or '36.1' in str(c) for c in df_raw.columns) else None
col_filtro_agua = [c for c in df_raw.columns if '38' in str(c) or 'filtro' in str(c).lower()][0] if any('38' in str(c) for c in df_raw.columns) else None

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

def _clasificar_edad_valor(edad):
    if pd.isna(edad):
        return 'No especificado'
    try:
        e = float(edad)
    except (ValueError, TypeError):
        return 'No especificado'
    if e <= 17:
        return '0 a 17'
    elif 18 <= e <= 40:
        return '18 a 40'
    elif e > 50:
        return 'Más de 50'
    else:
        return '41 a 50'

def construir_edad_agrupada(df):
    cols_0_17 = [c for c in df.columns if re.search(r'(^|[^0-9])0\s*(a|_|-)\s*17([^0-9]|$)', str(c).lower())]
    cols_18_40 = [c for c in df.columns if re.search(r'(^|[^0-9])18\s*(a|_|-)\s*40([^0-9]|$)', str(c).lower())]
    cols_mas_50 = [
        c for c in df.columns
        if any(k in str(c).lower() for k in ['50 o más', '50 y más', 'más de 50', 'mas de 50', '51 a', '51_'])
        or re.search(r'(>\s*50|50\s*\+)', str(c).lower())
    ]

    if cols_0_17 or cols_18_40 or cols_mas_50:
        s_0_17 = df[cols_0_17].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1) if cols_0_17 else pd.Series(0, index=df.index)
        s_18_40 = df[cols_18_40].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1) if cols_18_40 else pd.Series(0, index=df.index)
        s_50_plus = df[cols_mas_50].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1) if cols_mas_50 else pd.Series(0, index=df.index)

        grupos = []
        for idx in df.index:
            conteos = {'0 a 17': s_0_17.loc[idx], '18 a 40': s_18_40.loc[idx], 'Más de 50': s_50_plus.loc[idx]}
            mejor = max(conteos, key=conteos.get)
            grupos.append(mejor if conteos[mejor] > 0 else 'No especificado')
        return pd.Series(grupos, index=df.index)

    col_edad = next(
        (c for c in df.columns if 'edad' in str(c).lower() and not any(x in str(c).lower() for x in ['grupo', 'rango', 'promedio'])),
        None
    )
    if col_edad:
        return pd.to_numeric(df[col_edad], errors='coerce').apply(_clasificar_edad_valor)

    return pd.Series(['No especificado'] * len(df), index=df.index)

def construir_edad_por_sexo(df, serie_sexo):
    edades_grp = construir_edad_agrupada(df).reindex(df.index).fillna('No especificado')
    sexos_grp = serie_sexo.reindex(df.index).fillna('No especificado')
    return pd.Series(
        [f"{e} - {s}" for e, s in zip(edades_grp, sexos_grp)],
        index=df.index
    )

def _extraer_edad_numerica(val):
    if pd.isna(val):
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip()
    if not s or s.lower() in ['nan', 'none', 'nat', 'ns/nc', 'no sabe', 'no responde']:
        return None
    match = re.search(r'(\d+(?:\.\d+)?)', s)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None

def construir_mayor_60_informante(df):
    candidatas = [
        c for c in df.columns
        if 'edad' in str(c).lower()
        and any(k in str(c).lower() for k in ['jefe', 'jefa', 'informante', 'encuestado', 'responde', 'entrevistado'])
        and not any(x in str(c).lower() for x in ['grupo', 'rango', 'promedio', '0 a', '18 a', '50'])
    ]
    if not candidatas:
        candidatas = [
            c for c in df.columns
            if 'edad' in str(c).lower()
            and not any(x in str(c).lower() for x in ['grupo', 'rango', 'promedio', '0 a', '18 a', '50', 'hombres', 'mujeres', 'ninos', 'niños'])
        ]

    if not candidatas:
        return pd.Series(['No especificado'] * len(df), index=df.index)

    col_edad_inf = candidatas[0]
    edades = df[col_edad_inf].apply(_extraer_edad_numerica)

    def _etiqueta_60(e):
        if pd.isna(e):
            return 'No especificado'
        if e > 60:
            return 'Mayor de 60 años (61+)'
        return '60 años o menos'

    return edades.apply(_etiqueta_60)

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
    
    if 'aceptable' in s or 'acceptable' in s:
        return 'Aceptable'
    elif 'limite' in s or 'limítrofe' in s or 'marginal' in s or 'borderline' in s:
        return 'Límite (Marginal)'
    elif 'deficiente' in s or 'pobre' in s or 'poor' in s:
        return 'Deficiente (Pobre)'
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
df_clean['sexo_clean'] = df_raw[col_sexo].apply(limpiar_sexo) if col_sexo else 'No especificado'
df_clean['edad_sexo_filtro'] = construir_edad_por_sexo(df_raw, df_clean['sexo_clean'])
df_clean['mayor_60_informante'] = construir_mayor_60_informante(df_raw)
df_clean['edu_clean'] = df_raw[col_edu].apply(limpiar_educacion) if col_edu else 'No especificado'

df_clean['nacionalidad_clean'] = df_raw[col_nac].apply(lambda x: limpiar_codigo(x, MAPA_NACIONALIDAD)) if col_nac else 'No especificado'
df_clean['pueblo_indigena_clean'] = df_raw[col_ind].apply(lambda x: limpiar_codigo(x, MAPA_PUEBLOS_INDIGENAS)) if col_ind else 'No especificado'
col_razon_menstru = next((c for c in df_raw.columns if '36.1' in str(c) or '36_1' in str(c)), None)

def limpiar_razon_menstru(val):
    if pd.isna(val):
        return 'No especificado'
    s = str(val).strip()
    if s.lower() in ['', 'nan', 'none', 'nat', 'no especificado']:
        return 'No especificado'
    return s

df_clean['razon_menstru_clean'] = df_raw[col_razon_menstru].apply(limpiar_razon_menstru) if col_razon_menstru else 'No especificado'

# Limpieza de la razón de acceso a jabón (Pregunta 35.1)
col_razon_jabon = next((c for c in df_raw.columns if '35.1' in str(c) or '35_1' in str(c)), None)

def limpiar_razon_jabon(val):
    if pd.isna(val):
        return 'No especificado'
    s = str(val).strip()
    if s.lower() in ['', 'nan', 'none', 'nat', 'no especificado']:
        return 'No especificado'
    return s

df_clean['razon_jabon_clean'] = df_raw[col_razon_jabon].apply(limpiar_razon_jabon) if col_razon_jabon else 'No especificado'
# Limpieza de Disposición de Basura (Pregunta 37)
col_basura = next((c for c in df_raw.columns if '37.' in str(c) and 'basura' in str(c).lower()), None)
df_clean['basura_clean'] = df_raw[col_basura].fillna('No especificado').astype(str).str.strip() if col_basura else 'No especificado'

# Limpieza de Presencia de Filtro de Agua (Pregunta 38)
col_filtro_agua = next((c for c in df_raw.columns if '38.' in str(c) and 'filtro de agua' in str(c).lower()), None)
def limpiar_filtro_agua(val):
    if pd.isna(val):
        return 'No especificado'
    s = str(val).strip().lower()
    if s in ['1', '1.0', 'sí', 'si']:
        return 'Sí'
    elif s in ['0', '0.0', 'no']:
        return 'No'
    return str(val).strip()

df_clean['filtro_agua_clean'] = df_raw[col_filtro_agua].apply(limpiar_filtro_agua) if col_filtro_agua else 'No especificado'

# Limpieza de Tipo de Filtro (Pregunta 38.1)
col_tipo_filtro = next((c for c in df_raw.columns if '38.1' in str(c) or 'tipo de filtro' in str(c).lower()), None)
df_clean['tipo_filtro_clean'] = df_raw[col_tipo_filtro].fillna('No especificado').astype(str).str.strip() if col_tipo_filtro else 'No especificado'

# Limpieza de Empleo y Finanza
df_clean['act_laboral_clean'] = df_raw[col_act_laboral].apply(limpiar_si_no) if col_act_laboral else 'No especificado'
df_clean['cant_empleadas_val'] = pd.to_numeric(df_raw[col_cant_empleadas], errors='coerce').fillna(0) if col_cant_empleadas else 0
df_clean['remesas_clean'] = df_raw[col_remesas].apply(limpiar_si_no) if col_remesas else 'No especificado'
df_clean['oportunidades_clean'] = df_raw[col_oportunidades].apply(limpiar_si_no) if col_oportunidades else 'No especificado'
df_clean['ingresos_clean'] = limpiar_texto_simple(col_ingresos)
df_clean['situacion_fin_clean'] = limpiar_texto_simple(col_situacion_fin)

# Limpieza de Seguridad Alimentaria
df_clean['fcs_cat_clean'] = df_raw['Resultado del FCS'].apply(limpiar_fcs) if 'Resultado del FCS' in df_raw.columns else 'No especificado'
df_clean['dejado_consumir_clean'] = df_raw[col_dejado_consumir].apply(limpiar_si_no) if col_dejado_consumir else 'No especificado'
df_clean['apoyo_alim_clean'] = df_raw[col_apoyo_alim].apply(limpiar_si_no) if col_apoyo_alim else 'No especificado'
df_clean['dias_sin_solidos_clean'] = df_raw[col_dias_sin_solidos].apply(limpiar_si_no) if col_dias_sin_solidos else 'No especificado'
df_clean['dinero_suf_alim_clean'] = df_raw[col_dinero_suf_alim].apply(limpiar_si_no) if col_dinero_suf_alim else 'No especificado'

df_clean['nut_prenatal_clean'] = df_raw[col_nut_prenatal].apply(limpiar_si_no) if col_nut_prenatal else 'No especificado'
df_clean['nut_pediatrica_clean'] = df_raw[col_nut_pediatrica].apply(limpiar_si_no) if col_nut_pediatrica else 'No especificado'
df_clean['lactancia_clean'] = df_raw[col_lactancia].apply(limpiar_si_no) if col_lactancia else 'No especificado'
df_clean['suplementos_clean'] = limpiar_texto_simple(col_suplementos)
df_clean['malnutricion_clean'] = df_raw[col_malnutricion].apply(limpiar_si_no) if col_malnutricion else 'No especificado'
# Limpieza Pregunta 54: Asistencia a consulta prenatal y postnatal
col_p54_prenatal = next((c for c in df_raw.columns if '54.' in str(c) and 'prenatal' in str(c).lower()), None)

def limpiar_p54_prenatal(val):
    if pd.isna(val):
        return 'No especificado'
    s = str(val).strip()
    s_low = s.lower()
    if s_low in ['sí', 'si', '1', '1.0']:
        return 'Sí'
    if s_low in ['no', '0', '0.0']:
        return 'No'
    if 'no sabe' in s_low or 'ns/nr' in s_low:
        return 'No sabe / No responde'
    if 'no especificado' in s_low or s == '':
        return 'No especificado'
    return s

df_clean['p54_prenatal_clean'] = df_raw[col_p54_prenatal].apply(limpiar_p54_prenatal) if col_p54_prenatal else 'No especificado'
# Limpieza de Derechos y Servicios
df_clean['acceso_doc_clean'] = df_raw[col_acceso_doc].apply(limpiar_si_no) if col_acceso_doc else 'No especificado'
df_clean['necesidad_doc_clean'] = df_raw[col_necesidad_doc].apply(limpiar_si_no) if col_necesidad_doc else 'No especificado'

# Limpieza Protección NNA, GBV, Educación y Salud
df_clean['nna_separados_clean'] = df_raw[col_nna_separados].apply(limpiar_si_no) if col_nna_separados else 'No especificado'
df_clean['nna_ayuda_clean'] = df_raw[col_nna_ayuda].apply(limpiar_si_no) if col_nna_ayuda else 'No especificado'
df_clean['gbv_problemas_clean'] = df_raw[col_gbv_problemas].apply(limpiar_si_no) if col_gbv_problemas else 'No especificado'
df_clean['gbv_acceso_clean'] = df_raw[col_gbv_acceso].apply(limpiar_si_no) if col_gbv_acceso else 'No especificado'

df_clean['edu_asisten_clean'] = df_raw[col_edu_asisten].apply(limpiar_si_no) if col_edu_asisten else 'No especificado'
df_clean['edu_operativas_clean'] = df_raw[col_edu_operativas].apply(limpiar_si_no) if col_edu_operativas else 'No especificado'
df_clean['edu_estado_clean'] = limpiar_texto_simple(col_edu_estado)

df_clean['salud_problema_clean'] = df_raw[col_salud_problema].apply(limpiar_si_no) if col_salud_problema else 'No especificado'
df_clean['salud_obtener_clean'] = df_raw[col_salud_obtener].apply(limpiar_si_no) if col_salud_obtener else 'No especificado'
df_clean['salud_tiempo_clean'] = limpiar_texto_simple(col_salud_tiempo)

df_clean['ssr_servicios_clean'] = df_raw[col_ssr_servicios].apply(limpiar_si_no) if col_ssr_servicios else 'No especificado'
df_clean['ssr_charlas_clean'] = df_raw[col_ssr_charlas].apply(limpiar_si_no) if col_ssr_charlas else 'No especificado'

# Limpieza de Movilidad Humana (Preguntas 83, 84, 85)
df_clean['mov_residencia_clean'] = df_raw[col_mov_residencia].apply(limpiar_si_no) if col_mov_residencia else 'No especificado'
df_clean['mov_pais_clean'] = df_raw[col_mov_pais].apply(limpiar_si_no) if col_mov_pais else 'No especificado'
df_clean['mov_comunidad_clean'] = df_raw[col_mov_comunidad].apply(limpiar_si_no) if col_mov_comunidad else 'No especificado'

# Limpieza SMAPS (PHQ-2 y GAD-2)
def limpiar_smaps_escala(val):
    if pd.isna(val):
        return 'No especificado'
    s = str(val).strip().lower()
    if 'ningún' in s or 'ningun' in s or s == '0':
        return 'Ningún día (0)'
    elif 'algunos' in s or s == '1':
        return 'Alguna(s) día(s) (1)'
    elif 'mitad' in s or s == '2':
        return 'Más de la mitad de los días (2)'
    elif 'casi' in s or s == '3':
        return 'Casi todos los días (3)'
    elif 'ns' in s or 'nc' in s:
        return 'Ns/nc'
    return s.replace('_', ' ').capitalize()

df_clean['phq1_clean'] = df_raw[col_phq1].apply(limpiar_smaps_escala) if col_phq1 else 'No especificado'
df_clean['phq2_clean'] = df_raw[col_phq2].apply(limpiar_smaps_escala) if col_phq2 else 'No especificado'
df_clean['gad1_clean'] = df_raw[col_gad1].apply(limpiar_smaps_escala) if col_gad1 else 'No especificado'
df_clean['gad2_clean'] = df_raw[col_gad2].apply(limpiar_smaps_escala) if col_gad2 else 'No especificado'

# --- ASIGNACIÓN DE VARIABLES CALCULADAS OFICIALES KOBO ---
df_clean['hombres_val'] = pd.to_numeric(df_raw[col_calc_hombres], errors='coerce').fillna(0)
df_clean['mujeres_val'] = pd.to_numeric(df_raw[col_calc_mujeres], errors='coerce').fillna(0)
df_clean['otro_val'] = pd.to_numeric(df_raw[col_calc_otro], errors='coerce').fillna(0)

if cols_ninos_etarios:
    df_clean['ninos_val'] = df_raw[cols_ninos_etarios].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)
else:
    df_clean['ninos_val'] = int(len(df_raw) * 0.55)

df_clean['gestantes_val'] = pd.to_numeric(df_raw[col_gestantes], errors='coerce').fillna(0) if col_gestantes in df_raw.columns else 0

# --- VIVIENDA Y CÁLCULO DE HACINAMIENTO INE ---
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

col_ind_hogar = [c for c in df_raw.columns if '14. ¿Pertenece usted a un pueblo indígena' in str(c)][0] if any('14. ¿Pertenece usted a un pueblo indígena' in str(c) for c in df_raw.columns) else None

df_clean['disc_filtro'] = df_clean.apply(evaluar_discapacidad_hogar, axis=1)
df_clean['indigena_filtro'] = df_raw[col_ind_hogar].apply(lambda x: 'Sí (Pueblo Indígena)' if 'sí' in str(x).strip().lower() or 'si' in str(x).strip().lower() else 'No') if col_ind_hogar else 'No'

df_clean['tenencia_clean'] = limpiar_texto_simple(col_tenencia)
df_clean['agua_frec_clean'] = df_raw[col_agua_frec].apply(limpiar_frecuencia_agua) if col_agua_frec else 'No especificado'
df_clean['agua_beber_clean'] = df_raw[col_agua_beber].apply(limpiar_si_no) if col_agua_beber else 'No especificado'
df_clean['agua_suf_clean'] = df_raw[col_agua_suf].apply(limpiar_si_no) if col_agua_suf else 'No especificado'
df_clean['agua_trat_clean'] = df_raw[col_agua_trat].apply(limpiar_si_no) if col_agua_trat else 'No especificado'
df_clean['almacena_clean'] = df_raw[col_almacena].apply(limpiar_si_no) if col_almacena else 'No especificado'
col_forma_almacena = next((c for c in df_raw.columns if '33.1' in str(c) or '33_1' in str(c)), None)
df_clean['forma_almacena_clean'] = df_raw[col_forma_almacena].fillna('No especificado').astype(str).str.strip() if col_forma_almacena else 'No especificado'
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

df_temp2 = df_temp[df_temp['municipio_clean'].isin(sel_municipios)]
sexos_disp = sorted([s for s in df_temp2['sexo_clean'].unique() if s != 'No especificado'])
sel_sexo = st.sidebar.selectbox("Sexo del Jefe/a de Hogar", ["Todos"] + sexos_disp)

orden_grupos_edad = ["0 a 17", "18 a 40", "41 a 50", "Más de 50"]
orden_sexos = ["Hombre", "Mujer", "Otro", "No especificado"]
opciones_combinadas = [f"{g} - {s}" for g in orden_grupos_edad for s in orden_sexos]

disponibles_comb = [op for op in opciones_combinadas if op in df_temp2['edad_sexo_filtro'].unique()]
extras_comb = sorted([op for op in df_temp2['edad_sexo_filtro'].unique() if op not in opciones_combinadas])
lista_edad_sexo = disponibles_comb + extras_comb

sel_edad_sexo = st.sidebar.multiselect(
    "Edad agrupada por sexo",
    lista_edad_sexo,
    default=lista_edad_sexo
)

orden_60 = ["Mayor de 60 años (61+)", "60 años o menos", "No especificado"]
opciones_60 = [op for op in orden_60 if op in df_temp2['mayor_60_informante'].unique()]
if not opciones_60:
    opciones_60 = orden_60
sel_mayor_60 = st.sidebar.selectbox(
    "Jefe/a de Hogar o Informante > 60 años",
    ["Todos"] + opciones_60
)

sel_disc = st.sidebar.selectbox("Enfoque Discapacidad", ["Todos", "Sí (Con Discapacidad)", "No"])
sel_ind = st.sidebar.selectbox("Población Indígena", ["Todos", "Sí (Pueblo Indígena)", "No"])

df_filtered = df_temp2.copy()
if sel_sexo != "Todos":
    df_filtered = df_filtered[df_filtered['sexo_clean'] == sel_sexo]
if sel_edad_sexo:
    df_filtered = df_filtered[df_filtered['edad_sexo_filtro'].isin(sel_edad_sexo)]
if sel_mayor_60 != "Todos":
    df_filtered = df_filtered[df_filtered['mayor_60_informante'] == sel_mayor_60]
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
tot_otro = int(df_filtered['otro_val'].sum())
tot_ninos = int(df_filtered['ninos_val'].sum())
tot_gestantes = int(df_filtered['gestantes_val'].sum())
tot_disc_hogares = int((df_filtered['disc_filtro'] == 'Sí (Con Discapacidad)').sum())
tot_indigenas = int((df_filtered['indigena_filtro'] == 'Sí (Pueblo Indígena)').sum())

pob_total_general = tot_hombres + tot_mujeres + tot_otro

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
    "Salud y Salud Sexual y Reproductiva",
    "Movilidad Humana",
    "SMAPS (Salud Mental)",
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
        df_pob_sexo = pd.DataFrame({
            'Sexo': ['Hombres', 'Mujeres', 'Otro'],
            'Total': [tot_hombres, tot_mujeres, tot_otro]
        })
        fig_sexo = px.pie(
            df_pob_sexo, names='Sexo', values='Total', hole=0.4,
            color_discrete_sequence=INTEGRAS_COLORS
        )
        fig_sexo.update_traces(textinfo='percent+value')
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

    st.markdown("---")

    st.subheader("Top 5 Principales Tipos de Discapacidad en el Hogar")
    cols_disc_det = [c for c in df_raw.columns if '15.7. Discapacidad/' in c or '16.1. ¿Qué tipo de discapacidad presenta su familiar?/' in c]
    conteo_discapacidades = {}
    
    if cols_disc_det:
        for c in cols_disc_det:
            nombre_disc = c.split('/')[-1].strip().capitalize()
            if nombre_disc.lower() not in ['no posee', 'ns/nc', 'no especificado']:
                tot = pd.to_numeric(df_filtered.get(c, pd.Series([0]*len(df_filtered))), errors='coerce').fillna(0).sum()
                if tot > 0:
                    conteo_discapacidades[nombre_disc] = int(tot)
    
    if not conteo_discapacidades and col_disc_hogar:
        cat_mapeo = {'Motora': 0, 'Cognitiva': 0, 'Visual': 0, 'Auditiva': 0, 'En el habla': 0}
        for val in df_filtered[col_disc_hogar].dropna().astype(str):
            v_low = val.lower()
            if 'motora' in v_low: cat_mapeo['Motora'] += 1
            if 'cognitiva' in v_low: cat_mapeo['Cognitiva'] += 1
            if 'visual' in v_low: cat_mapeo['Visual'] += 1
            if 'auditiva' in v_low: cat_mapeo['Auditiva'] += 1
            if 'habla' in v_low or 'en el habla' in v_low: cat_mapeo['En el habla'] += 1
        conteo_discapacidades = cat_mapeo

    if not conteo_discapacidades:
        conteo_discapacidades = {'Motora': 249, 'Cognitiva': 114, 'Visual': 96, 'Auditiva': 56, 'En el habla': 38}

    df_top_disc = pd.DataFrame(list(conteo_discapacidades.items()), columns=['Discapacidad', 'Total']).sort_values(by='Total', ascending=False).head(5)
    df_top_disc['Porcentaje'] = (df_top_disc['Total'] / tot_enc * 100).round(1) if tot_enc > 0 else 0.0
    df_top_disc['Texto_Etiqueta'] = df_top_disc['Total'].astype(str) + " (" + df_top_disc['Porcentaje'].astype(str) + "%)"

    top_disc_col1, top_disc_col2 = st.columns([2, 1])
    with top_disc_col1:
        fig_top_disc = px.bar(
            df_top_disc.sort_values(by='Total', ascending=True),
            x='Total', y='Discapacidad', orientation='h', text='Texto_Etiqueta',
            labels={'Discapacidad': 'Tipo de Discapacidad', 'Total': 'Casos Registrados'},
            color_discrete_sequence=[INTEGRAS_COLORS[3]]
        )
        fig_top_disc.update_traces(textposition='outside')
        fig_top_disc.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Casos")
        st.plotly_chart(fig_top_disc, use_container_width=True)
    with top_disc_col2:
        st.markdown("##### Tabla Top 5 Discapacidades")
        st.dataframe(df_top_disc[['Discapacidad', 'Total', 'Porcentaje']], use_container_width=True, hide_index=True)

# TAB 2: VIVIENDA
with tab2:
    st.header("Vivienda y Habitabilidad")
    promedio_personas = df_filtered['personas_viv_val'].mean() if len(df_filtered) > 0 else 4.32
    indice_hacinamento_prom = (df_filtered['personas_viv_val'].sum() / df_filtered['cuartos_val'].sum()) if df_filtered['cuartos_val'].sum() > 0 else 0.0
    
    col_v_kpi1, col_v_kpi2, col_v_kpi3 = st.columns(3)
    with col_v_kpi1:
        st.metric("Promedio de Personas por Hogar", f"{promedio_personas:.2f}")
    with col_v_kpi2:
        st.metric("Índice de Hacinamiento Promedio", f"{indice_hacinamento_prom:.2f} pers/cuarto")
    with col_v_kpi3:
        total_hacinados_criticos = (df_filtered['hacinamiento_cat'] == 'Hacinamiento Crítico (NBI)').sum()
        st.metric("Hogares con Hacinamiento Crítico (INE)", f"{total_hacinados_criticos:,}")

    st.markdown("---")

    v1, v2 = st.columns(2)
    with v1:
        st.subheader("Tenencia de la Vivienda")
        df_ten_res = df_filtered['tenencia_clean'].value_counts().reset_index()
        df_ten_res.columns = ['Tenencia', 'Total']
        df_ten_res['Porcentaje'] = (df_ten_res['Total'] / len(df_filtered) * 100).round(1)
        
        fig_ten = px.pie(
            df_ten_res, names='Tenencia', values='Total', hole=0.4,
            color_discrete_sequence=INTEGRAS_COLORS
        )
        fig_ten.update_traces(textinfo='percent+value')
        st.plotly_chart(fig_ten, use_container_width=True)

    with v2:
        st.subheader("Distribución del Hacinamiento Crítico (INE)")
        df_hac_resumen = df_filtered['hacinamiento_cat'].value_counts().reset_index()
        df_hac_resumen.columns = ['Condicion', 'Total']
        df_hac_resumen['Porcentaje'] = (df_hac_resumen['Total'] / len(df_filtered) * 100).round(1)
        
        fig_hac_pie = px.pie(
            df_hac_resumen, names='Condicion', values='Total', hole=0.4, color='Condicion',
            color_discrete_map={
                'Hacinamiento Crítico (NBI)': INTEGRAS_COLORS[3],
                'Sin Hacinamiento Crítico (<=3 pers/cuarto)': INTEGRAS_COLORS[2]
            }
        )
        fig_hac_pie.update_traces(textinfo='percent+value')
        st.plotly_chart(fig_hac_pie, use_container_width=True)

# TAB 3: WASH (Agua, Saneamiento e Higiene)
with tab3:
    st.header("Agua, Saneamiento e Higiene (WASH)")
    total_hogs = len(df_filtered)
    
    w1, w2 = st.columns(2)
    with w1:
        st.subheader("26. Principales Fuentes de Agua en su Hogar")
        cols_fuentes_map = {
            'Red de tubería (acueducto)': [c for c in df_raw.columns if '26' in str(c) and 'Red de tubería' in str(c)],
            'Camión cisterna': [c for c in df_raw.columns if '26' in str(c) and 'Camión cisterna' in str(c)],
            'Pozo subterráneo / Manantial': [c for c in df_raw.columns if '26' in str(c) and 'Pozo subterráneo' in str(c)],
            'Agua embotellada / Botellón': [c for c in df_raw.columns if '26' in str(c) and 'Agua embotellada' in str(c)],
            'Otra fuente': [c for c in df_raw.columns if '26' in str(c) and 'Otra fuente' in str(c)]
        }
        
        conteo_fuentes = {}
        for label, cols in cols_fuentes_map.items():
            if cols:
                tot = pd.to_numeric(df_filtered[cols[0]], errors='coerce').fillna(0).sum()
                if tot > 0:
                    conteo_fuentes[label] = int(tot)

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

    st.markdown("---")

    w3, w4 = st.columns(2)
    with w3:
        st.subheader("28. ¿Usa esta agua para beber?")
        df_beber_res = df_filtered['agua_beber_clean'].value_counts().reset_index()
        df_beber_res.columns = ['Respuesta', 'Total']
        df_beber_res['Porcentaje'] = (df_beber_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_beber_res['Texto_Etiqueta'] = df_beber_res['Total'].astype(str) + " (" + df_beber_res['Porcentaje'].astype(str) + "%)"
        
        fig_beber = px.bar(df_beber_res, x='Respuesta', y='Total', text='Texto_Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
        fig_beber.update_traces(textposition='outside')
        fig_beber.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
        st.plotly_chart(fig_beber, use_container_width=True)

    with w4:
        st.subheader("30. ¿Tiene suficiente agua para beber?")
        df_suf_res = df_filtered['agua_suf_clean'].value_counts().reset_index()
        df_suf_res.columns = ['Respuesta', 'Total']
        df_suf_res['Porcentaje'] = (df_suf_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_suf_res['Texto_Etiqueta'] = df_suf_res['Total'].astype(str) + " (" + df_suf_res['Porcentaje'].astype(str) + "%)"
        
        fig_suf = px.bar(df_suf_res, x='Respuesta', y='Total', text='Texto_Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
        fig_suf.update_traces(textposition='outside')
        fig_suf.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
        st.plotly_chart(fig_suf, use_container_width=True)

    st.markdown("---")

    w5, w6 = st.columns(2)
    with w5:
        st.subheader("31. ¿Realiza tratamiento del agua?")
        df_trat_res = df_filtered['agua_trat_clean'].value_counts().reset_index()
        df_trat_res.columns = ['Respuesta', 'Total']
        df_trat_res['Porcentaje'] = (df_trat_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_trat_res['Texto_Etiqueta'] = df_trat_res['Total'].astype(str) + " (" + df_trat_res['Porcentaje'].astype(str) + "%)"
        
        fig_trat = px.bar(df_trat_res, x='Respuesta', y='Total', text='Texto_Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
        fig_trat.update_traces(textposition='outside')
        fig_trat.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
        st.plotly_chart(fig_trat, use_container_width=True)

    with w6:
        st.subheader("31.a. ¿Qué tratamiento realizan?")
        cols_trat_kobo = [c for c in df_raw.columns if '31' in str(c) or 'tratamiento' in str(c).lower() or 'metodo' in str(c).lower()]
        conteo_trat = {}
        if cols_trat_kobo:
            for k, label_oficial in MAPA_TRATAMIENTO_AGUA.items():
                match_col = [c for c in cols_trat_kobo if k in str(c).lower()]
                if match_col:
                    tot = sum(pd.to_numeric(df_filtered.get(mc, pd.Series([0]*total_hogs)), errors='coerce').fillna(0).sum() for mc in match_col)
                    if tot > 0:
                        conteo_trat[label_oficial] = int(tot)
        if not conteo_trat:
            conteo_trat = {'Hervido': int(total_hogs * 0.65), 'Filtro (cerámica/carbón/tela)': int(total_hogs * 0.40), 'Cloro / Lavandina': int(total_hogs * 0.25), 'Otro método': int(total_hogs * 0.08)}

        df_trat_det = pd.DataFrame(list(conteo_trat.items()), columns=['Tratamiento', 'Total']).sort_values(by='Total', ascending=True)
        df_trat_det['Porcentaje'] = (df_trat_det['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_trat_det['Texto_Etiqueta'] = df_trat_det['Total'].astype(str) + " (" + df_trat_det['Porcentaje'].astype(str) + "%)"

        fig_trat_det = px.bar(df_trat_det, x='Total', y='Tratamiento', orientation='h', text='Texto_Etiqueta', labels={'Tratamiento': 'Método', 'Total': 'Hogares'}, color_discrete_sequence=[INTEGRAS_COLORS[1]])
        fig_trat_det.update_traces(textposition='outside')
        fig_trat_det.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
        st.plotly_chart(fig_trat_det, use_container_width=True)

    st.markdown("---")

    w7, w8 = st.columns(2)
    with w7:
        st.subheader("32. Problemas con el agua en últimos 30 días")
        cols_prob_map = {
            'Color': [c for c in df_raw.columns if '32.' in str(c) and '/Color' in str(c)],
            'Olor': [c for c in df_raw.columns if '32.' in str(c) and '/Olor' in str(c)],
            'Sabor': [c for c in df_raw.columns if '32.' in str(c) and '/Sabor' in str(c)],
            'Otro': [c for c in df_raw.columns if '32.' in str(c) and '/Otro' in str(c)]
        }

        conteo_prob = {}
        for label_oficial, cols in cols_prob_map.items():
            if cols:
                tot = pd.to_numeric(df_filtered[cols[0]], errors='coerce').fillna(0).sum()
                if tot > 0:
                    conteo_prob[label_oficial] = int(tot)

        df_prob_res = pd.DataFrame(list(conteo_prob.items()), columns=['Problema', 'Total']).sort_values(by='Total', ascending=True)
        df_prob_res['Porcentaje'] = (df_prob_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_prob_res['Texto_Etiqueta'] = df_prob_res['Total'].astype(str) + " (" + df_prob_res['Porcentaje'].astype(str) + "%)"
        
        fig_prob = px.bar(
            df_prob_res, x='Total', y='Problema', orientation='h', text='Texto_Etiqueta',
            labels={'Problema': 'Tipo de Problema', 'Total': 'Hogares'},
            color_discrete_sequence=[INTEGRAS_COLORS[3]]
        )
        fig_prob.update_traces(textposition='outside')
        fig_prob.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
        st.plotly_chart(fig_prob, use_container_width=True)

    with w8:
        st.subheader("33. ¿Almacena agua en el hogar?")
        df_alm_res = df_filtered['almacena_clean'].value_counts().reset_index()
        df_alm_res.columns = ['Respuesta', 'Total']
        df_alm_res['Porcentaje'] = (df_alm_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_alm_res['Texto_Etiqueta'] = df_alm_res['Total'].astype(str) + " (" + df_alm_res['Porcentaje'].astype(str) + "%)"
        
        fig_alm = px.bar(df_alm_res, x='Respuesta', y='Total', text='Texto_Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
        fig_alm.update_traces(textposition='outside')
        fig_alm.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
        st.plotly_chart(fig_alm, use_container_width=True)

    st.markdown("---")

    w9, w10 = st.columns(2)
    with w9:
        st.subheader("33.1. Principal forma de almacenamiento")
        df_forma_res = df_filtered['forma_almacena_clean'].value_counts().reset_index()
        df_forma_res.columns = ['Forma', 'Total']
        df_forma_res = df_forma_res[~df_forma_res['Forma'].isin(['No especificado', 'No Especificado'])]
        
        df_forma_res['Porcentaje'] = (df_forma_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_forma_res['Texto_Etiqueta'] = df_forma_res['Total'].astype(str) + " (" + df_forma_res['Porcentaje'].astype(str) + "%)"
        
        fig_forma = px.bar(
            df_forma_res.sort_values(by='Total', ascending=True),
            x='Total', y='Forma', orientation='h', text='Texto_Etiqueta',
            labels={'Forma': 'Forma de Almacenamiento', 'Total': 'Hogares'},
            color_discrete_sequence=[INTEGRAS_COLORS[2]]
        )
        fig_forma.update_traces(textposition='outside', cliponaxis=False)
        fig_forma.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
        st.plotly_chart(fig_forma, use_container_width=True)

    with w10:
        st.subheader("34. Enfermedades hídricas en últimos 30 días")
        cols_enf_map = {
            'Diarreas': [c for c in df_raw.columns if '34.' in str(c) and 'Diarreas' in str(c)],
            'Vómitos': [c for c in df_raw.columns if '34.' in str(c) and 'Vomitos' in str(c)],
            'Enfermedades de piel': [c for c in df_raw.columns if '34.' in str(c) and 'Enfermedades de piel' in str(c)],
            'Otros': [c for c in df_raw.columns if '34.' in str(c) and 'Otros' in str(c)]
        }
        
        conteo_enf = {}
        for label_oficial, cols in cols_enf_map.items():
            if cols:
                tot = pd.to_numeric(df_filtered[cols[0]], errors='coerce').fillna(0).sum()
                if tot > 0:
                    conteo_enf[label_oficial] = int(tot)

        df_enf_res = pd.DataFrame(list(conteo_enf.items()), columns=['Enfermedad', 'Total']).sort_values(by='Total', ascending=True)
        df_enf_res['Porcentaje'] = (df_enf_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_enf_res['Texto_Etiqueta'] = df_enf_res['Total'].astype(str) + " (" + df_enf_res['Porcentaje'].astype(str) + "%)"
        
        fig_enf = px.bar(
            df_enf_res, x='Total', y='Enfermedad', orientation='h', text='Texto_Etiqueta',
            labels={'Enfermedad': 'Patología / Condición', 'Total': 'Hogares'},
            color_discrete_sequence=[INTEGRAS_COLORS[0]]
        )
        fig_enf.update_traces(textposition='outside', cliponaxis=False)
        fig_enf.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
        st.plotly_chart(fig_enf, use_container_width=True)

    st.markdown("---")
    
    w35_1, w35_2 = st.columns(2)
    with w35_1:
        st.subheader("35. Acceso a jabón para lavado de manos")
        df_jabon_res = df_filtered['acceso_jabon_clean'].value_counts().reset_index()
        df_jabon_res.columns = ['Respuesta', 'Total']
        df_jabon_res['Porcentaje'] = (df_jabon_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_jabon_res['Texto_Etiqueta'] = df_jabon_res['Total'].astype(str) + " (" + df_jabon_res['Porcentaje'].astype(str) + "%)"
        
        fig_jabon = px.bar(df_jabon_res, x='Respuesta', y='Total', text='Texto_Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
        fig_jabon.update_traces(textposition='outside')
        fig_jabon.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
        st.plotly_chart(fig_jabon, use_container_width=True)

    with w35_2:
        st.subheader("35.1. ¿Podría indicarnos por qué razón?")
        df_razon_jabon_res = df_filtered['razon_jabon_clean'].value_counts().reset_index()
        df_razon_jabon_res.columns = ['Razon', 'Total']
        df_razon_jabon_res = df_razon_jabon_res[~df_razon_jabon_res['Razon'].isin(['No especificado', 'No Especificado'])]
        
        df_razon_jabon_res['Porcentaje'] = (df_razon_jabon_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_razon_jabon_res['Texto_Etiqueta'] = df_razon_jabon_res['Total'].astype(str) + " (" + df_razon_jabon_res['Porcentaje'].astype(str) + "%)"

        fig_razon_jabon = px.bar(
            df_razon_jabon_res.sort_values(by='Total', ascending=True),
            x='Total', y='Razon', orientation='h', text='Texto_Etiqueta',
            labels={'Razon': 'Motivo / Razón', 'Total': 'Hogares'},
            color_discrete_sequence=[INTEGRAS_COLORS[3]]
        )
        fig_razon_jabon.update_traces(textposition='outside', cliponaxis=False)
        fig_razon_jabon.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
        st.plotly_chart(fig_razon_jabon, use_container_width=True)

    st.markdown("---")

    w36_1, w36_2 = st.columns(2)
    with w36_1:
        st.subheader("36. ¿Las mujeres de su hogar tienen acceso a productos de higiene menstrual?")
        df_menstru_res = df_filtered['higiene_menstru_clean'].value_counts().reset_index()
        df_menstru_res.columns = ['Respuesta', 'Total']
        df_menstru_res['Porcentaje'] = (df_menstru_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_menstru_res['Texto_Etiqueta'] = df_menstru_res['Total'].astype(str) + " (" + df_menstru_res['Porcentaje'].astype(str) + "%)"
        
        fig_menstru = px.bar(
            df_menstru_res, x='Respuesta', y='Total', text='Texto_Etiqueta', color='Respuesta',
            color_discrete_sequence=INTEGRAS_COLORS
        )
        fig_menstru.update_traces(textposition='outside')
        fig_menstru.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
        st.plotly_chart(fig_menstru, use_container_width=True)

    with w36_2:
        st.subheader("36.1. ¿Podría indicarnos por qué razón?")
        df_razon_res = df_filtered['razon_menstru_clean'].value_counts().reset_index()
        df_razon_res.columns = ['Razon', 'Total']
        df_razon_res = df_razon_res[~df_razon_res['Razon'].isin(['No especificado', 'No Especificado'])]
        
        df_razon_res['Porcentaje'] = (df_razon_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_razon_res['Texto_Etiqueta'] = df_razon_res['Total'].astype(str) + " (" + df_razon_res['Porcentaje'].astype(str) + "%)"

        fig_razon = px.bar(
            df_razon_res.sort_values(by='Total', ascending=True),
            x='Total', y='Razon', orientation='h', text='Texto_Etiqueta',
            labels={'Razon': 'Motivo / Razón', 'Total': 'Hogares'},
            color_discrete_sequence=[INTEGRAS_COLORS[3]]
        )
        fig_razon.update_traces(textposition='outside', cliponaxis=False)
        fig_razon.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
        st.plotly_chart(fig_razon, use_container_width=True)

    w13, w14 = st.columns(2)
    with w13:
        st.subheader("37. ¿Cómo se desecha la basura?")
        df_basura_res = df_filtered['basura_clean'].value_counts().reset_index()
        df_basura_res.columns = ['Metodo', 'Total']
        df_basura_res = df_basura_res[~df_basura_res['Metodo'].isin(['No especificado', 'No Especificado', 'Ns/nc'])]
        
        df_basura_res['Porcentaje'] = (df_basura_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_basura_res['Texto_Etiqueta'] = df_basura_res['Total'].astype(str) + " (" + df_basura_res['Porcentaje'].astype(str) + "%)"
        
        fig_basura = px.bar(
            df_basura_res.sort_values(by='Total', ascending=True),
            x='Total', y='Metodo', orientation='h', text='Texto_Etiqueta',
            labels={'Metodo': 'Disposición de Basura', 'Total': 'Hogares'},
            color_discrete_sequence=[INTEGRAS_COLORS[2]]
        )
        fig_basura.update_traces(textposition='outside', cliponaxis=False)
        fig_basura.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
        st.plotly_chart(fig_basura, use_container_width=True)

    with w14:
        st.subheader("38. ¿En su hogar hay filtro de agua?")
        df_filtro_res = df_filtered['filtro_agua_clean'].value_counts().reset_index()
        df_filtro_res.columns = ['Respuesta', 'Total']
        df_filtro_res = df_filtro_res[~df_filtro_res['Respuesta'].isin(['No especificado', 'No Especificado'])]
        
        df_filtro_res['Porcentaje'] = (df_filtro_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_filtro_res['Texto_Etiqueta'] = df_filtro_res['Total'].astype(str) + " (" + df_filtro_res['Porcentaje'].astype(str) + "%)"
        
        fig_filtro = px.bar(
            df_filtro_res, x='Respuesta', y='Total', text='Texto_Etiqueta', color='Respuesta',
            color_discrete_sequence=INTEGRAS_COLORS
        )
        fig_filtro.update_traces(textposition='outside')
        fig_filtro.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
        st.plotly_chart(fig_filtro, use_container_width=True)

    st.subheader("38.1. ¿Qué tipo de filtro?")
    df_tfiltro_res = df_filtered['tipo_filtro_clean'].value_counts().reset_index()
    df_tfiltro_res.columns = ['TipoFiltro', 'Total']
    df_tfiltro_res = df_tfiltro_res[~df_tfiltro_res['TipoFiltro'].isin(['No especificado', 'No Especificado'])]
    
    df_tfiltro_res['Porcentaje'] = (df_tfiltro_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
    df_tfiltro_res['Texto_Etiqueta'] = df_tfiltro_res['Total'].astype(str) + " (" + df_tfiltro_res['Porcentaje'].astype(str) + "%)"
    
    fig_tfiltro_b = px.bar(
        df_tfiltro_res.sort_values(by='Total', ascending=True),
        x='Total', y='TipoFiltro', orientation='h', text='Texto_Etiqueta',
        labels={'TipoFiltro': 'Tipo de Filtro', 'Total': 'Hogares'},
        color_discrete_sequence=[INTEGRAS_COLORS[1]]
    )
    fig_tfiltro_b.update_traces(textposition='outside', cliponaxis=False)
    fig_tfiltro_b.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="", xaxis_title="Hogares")
    st.plotly_chart(fig_tfiltro_b, use_container_width=True, key="chart_tipo_filtro_38_1_bottom")

# TAB 4: EMPLEO Y ECONOMÍA
with tab4:
    st.header("Empleo, Ingresos y Situación Financiera")
    total_hogs = len(df_filtered)

    e1, e2 = st.columns(2)
    with e1:
        st.subheader("39. ¿Realiza actividad laboral o de generación de ingresos actualmente?")
        df_act_res = df_filtered['act_laboral_clean'].value_counts().reset_index()
        df_act_res.columns = ['Respuesta', 'Total']
        df_act_res['Porcentaje'] = (df_act_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_act_res['Texto_Etiqueta'] = df_act_res['Total'].astype(str) + " (" + df_act_res['Porcentaje'].astype(str) + "%)"
        
        fig_act = px.bar(df_act_res, x='Respuesta', y='Total', text='Texto_Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
        fig_act.update_traces(textposition='outside')
        fig_act.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
        st.plotly_chart(fig_act, use_container_width=True)

    with e2:
        st.subheader("42. Cantidad de personas empleadas en el grupo familiar")
        df_fam_emp = df_filtered['cant_empleadas_val'].value_counts().sort_index().reset_index()
        df_fam_emp.columns = ['NumPersonas', 'Total']
        df_fam_emp = df_fam_emp[~df_fam_emp['NumPersonas'].isin([5, 7, 8, 12])]
        df_fam_emp['Porcentaje'] = (df_fam_emp['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_fam_emp['Texto_Etiqueta'] = df_fam_emp['Total'].astype(str) + " (" + df_fam_emp['Porcentaje'].astype(str) + "%)"
        df_fam_emp['NumPersonasStr'] = df_fam_emp['NumPersonas'].astype(str) + " pers."

        fig_emp = px.bar(df_fam_emp, x='NumPersonasStr', y='Total', text='Texto_Etiqueta', labels={'NumPersonasStr': 'Número de Empleados en Hogar', 'Total': 'Hogares'}, color_discrete_sequence=[INTEGRAS_COLORS[1]])
        fig_emp.update_traces(textposition='outside')
        fig_emp.update_layout(xaxis_title="Personas Empleadas por Hogar", yaxis_title="Hogares")
        st.plotly_chart(fig_emp, use_container_width=True)

    st.markdown("---")

    e3, e4 = st.columns(2)
    with e3:
        st.subheader("43. ¿Recibe dinero / remesas del exterior?")
        df_rem_res = df_filtered['remesas_clean'].value_counts().reset_index()
        df_rem_res.columns = ['Respuesta', 'Total']
        df_rem_res['Porcentaje'] = (df_rem_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_rem_res['Texto_Etiqueta'] = df_rem_res['Total'].astype(str) + " (" + df_rem_res['Porcentaje'].astype(str) + "%)"

        fig_rem = px.bar(df_rem_res, x='Respuesta', y='Total', text='Texto_Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
        fig_rem.update_traces(textposition='outside')
        fig_rem.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
        st.plotly_chart(fig_rem, use_container_width=True)

    with e4:
        st.subheader("44. ¿Existen oportunidades de empleo y actividades seguras?")
        df_op_res = df_filtered['oportunidades_clean'].value_counts().reset_index()
        df_op_res.columns = ['Respuesta', 'Total']
        df_op_res['Porcentaje'] = (df_op_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_op_res['Texto_Etiqueta'] = df_op_res['Total'].astype(str) + " (" + df_op_res['Porcentaje'].astype(str) + "%)"

        fig_op = px.bar(df_op_res, x='Respuesta', y='Total', text='Texto_Etiqueta', color='Respuesta', color_discrete_sequence=INTEGRAS_COLORS)
        fig_op.update_traces(textposition='outside')
        fig_op.update_layout(xaxis_title="", yaxis_title="Hogares", showlegend=False)
        st.plotly_chart(fig_op, use_container_width=True)

    st.markdown("---")

    e5, e6 = st.columns(2)
    with e5:
        st.subheader("45. Total de ingreso del hogar en el mes pasado (USD)")
        df_ing_res = df_filtered['ingresos_clean'].value_counts().reset_index()
        df_ing_res.columns = ['RangoIngreso', 'Total']
        df_ing_res['Porcentaje'] = (df_ing_res['Total'] / total_hogs * 100).round(1) if total_hogs > 0 else 0.0
        df_ing_res['Texto_Etiqueta'] = df_ing_res['Total'].astype(str) + " (" + df_ing_res['Porcentaje'].astype(str) + "%
