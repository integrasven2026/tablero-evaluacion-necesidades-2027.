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
df_clean['indigena_filtro'] = df_raw[col_ind_hogar].apply(lambda x: 'Sí (Pueblo Indígena
