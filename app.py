import streamlit as st
import pandas as pd
import plotly.express as px
import requests

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
    .logo-box {
        background-color: white;
        color: #08327D;
        padding: 8px 15px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 0.9rem;
        text-align: center;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
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

# Encabezado institucional con contenedor de Logo e Identidad Consorcio ÍNTEGRAS
st.markdown("""
<div class="header-container">
    <div>
        <h1 class="titulo-principal">Tablero Dinámico de Evaluación de Necesidades - ECHO HIP 2027</h1>
        <div class="sub-titulo">Consorcio ÍNTEGRAS: COOPI, HIAS, FLM, PLAFAM, PALUZ | Monitoreo Multisectorial Post-Sismos y Crisis Estructural</div>
    </div>
    <div class="logo-box">
        LOGO ÍNTEGRAS<br><span style="font-size: 0.75rem; font-weight: normal; color: #4A5568;">(Espacio Oficial)</span>
    </div>
</div>
""", unsafe_allow_html=True)

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

MAPA_FUENTES_AGUA_VALORES = {
    'red_tuberias': 'Red de tubería (acueducto)',
    'camion_cisterna': 'Camión cisterna',
    'pozo_subterraneo': 'Pozo subterráneo / Manantial',
    'agua_embotellada': 'Agua embotellada / Botellón',
    'otra_fuente': 'Otra fuente',
    'ns_nc': 'No sabe / No responde'
}

MAPA_FRECUENCIA_AGUA = {
    'diario': 'Diario (continuo)', 'diario_continuo': 'Diario (continuo)',
    'varios_dias': 'Varios días a la semana',
    'una_vez': 'Una vez a la semana',
    'cada_15_dias': 'Cada 15 días o más', 'cada_15_dias_o_mas': 'Cada 15 días o más'
}

MAPA_SI_NO_NS = {
    'si': 'Sí', 'sí': 'Sí', 'no': 'No',
    'ns_nc': 'No sabe / No responde', 'no_sabe_no_responde': 'No sabe / No responde'
}

MAPA_TRATAMIENTO_AGUA = {
    'hervido': 'Hervido',
    'cloro': 'Cloro / Lavandina', 'cloro_lavandina': 'Cloro / Lavandina',
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
    'servicio_aseo': 'Es recogida por el servicio de aseo público',
    'calle': 'La deja en la calle',
    'entierra': 'La entierra',
    'quema': 'La quema',
    'recicla': 'La recicla',
    'rio': 'La tira en el rio, laguna, quebrada',
    'paga': 'Le paga a alguien para que se la lleve',
    'ns_nc': 'Ns/nc',
    'otra': 'Otra'
}

MAPA_TIPO_FILTRO = {
    'gravedad': 'Filtros por gravedad (Ej. Filtros de cerámica de 2 tanques/recipientes, velas filtrantes, etc.)',
    'sifon': 'Filtros de sifón (Ej. Sifón tipo Tulip u otros sistemas de succión/manguera)'
}

MAPA_RAZON_MENSTRUAL = {
    'costo_elevado': 'Costo elevado o falta de presupuesto.',
    'costo': 'Costo elevado o falta de presupuesto.',
    'no_disponibles': 'No hay disponibles a la venta en las tiendas cercanas, mercados o puntos de abasto locales.',
    'disponibilidad': 'No hay disponibles a la venta en las tiendas cercanas, mercados o puntos de abasto locales.',
    'alternativas': 'Utiliza otras alternativas locales (ceniza, arena, barro, plantas, hojas tradicionales o solo agua).',
    'no_necesario': 'No lo considera necesario.',
    'no_habitual': 'No es una práctica habitual en la rutina diaria de la familia.'
}

# --- FUNCIONES DE BÚSQUEDA ROBUSTA ---
def find_col(df, keywords):
    for col in df.columns:
        for kw in keywords:
            if kw.lower() in col.lower():
                return col
    return None

def find_col_flexible(df, keywords):
    for col in df.columns:
        col_lower = col.lower()
        for kw in keywords:
            if kw.lower() in col_lower:
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

col_hombres = find_col_flexible(df_raw, ['hombres', 'masculinos', 'num_hombres', '_hombres'])
col_mujeres = find_col_flexible(df_raw, ['mujeres', 'femeninos', 'num_mujeres', '_mujeres'])
col_ninos = find_col_flexible(df_raw, ['ninos', 'niños', 'menores', 'infantes', 'menores_18', 'ninos_nias', '0_17', 'edad_0_17'])

col_total_embarazadas = find_col_flexible(df_raw, ['21_1', '_21_1', 'embarazadas_hay', 'num_embarazadas', 'gestantes'])
col_emb_menores = find_col_flexible(df_raw, ['21_2', '_21_2', 'menores_de_edad', 'embarazadas_son_menores'])
col_emb_control = find_col_flexible(df_raw, ['21_3', '_21_3', 'control_prenatal', 'acuden'])

lgbti_col = find_col(df_raw, ['igtbiq', 'lgbti'])

col_tenencia = find_col(df_raw, ['22', 'tenencia', 'propiedad', 'habita', 'vivienda'])
col_personas_viv = find_col_flexible(df_raw, ['24', 'personas_vivienda', 'total_personas', 'habitan_la_vivienda', '_24'])
col_cuartos = find_col_flexible(df_raw, ['25', 'cuartos', 'habitaciones', 'dormir', '_25'])

col_agua_frec = None
for c in df_raw.columns:
    if df_raw[c].dropna().astype(str).str.lower().str.contains('diario|varios_dias|una_vez|cada_15', regex=True).any():
        col_agua_frec = c
        break
if not col_agua_frec:
    for c in df_raw.columns:
        c_l = c.lower()
        if ('27' in c_l or 'frecuencia' in c_l or 'abastec' in c_l) and ('agua' in c_l or c_l.endswith('_27') or c_l == '27'):
            col_agua_frec = c
            break

col_agua_beber = find_col_flexible(df_raw, ['28', 'beber', 'usa_esta_agua'])
col_agua_suf = find_col_flexible(df_raw, ['30', 'suficiente', 'suficiente_agua'])
col_agua_trat = find_col_flexible(df_raw, ['31', 'realiza_tratamiento', 'tratamiento_agua'])
col_almacena = find_col_flexible(df_raw, ['33', 'almacena', 'almacenas'])
col_acceso_jabon = find_col_flexible(df_raw, ['35', 'jabon', 'lavado_de_manos'])

# Búsqueda infalible para la pregunta 36 (Higiene Menstrual)
col_higiene_menstru = None
for c in df_raw.columns:
    c_l = c.lower()
    if any(k in c_l for k in ['36', 'menstrual', 'higiene', 'toallas']) and not 'jabon' in c_l and '36_1' not in c_l and '36.1' not in c_l:
        vals = df_raw[c].dropna().astype(str).str.lower().unique()
        if any('si' in v or 'sí' in v or 'no' in v for v in vals):
            col_higiene_menstru = c
            break
if not col_higiene_menstru:
    col_higiene_menstru = find_col_flexible(df_raw, ['36', 'menstrual', 'higiene'])

# Búsqueda infalible para la pregunta 36.1 (Razón por qué no tienen acceso)
col_razon_menstru = None
for c in df_raw.columns:
    c_l = c.lower()
    if any(k in c_l for k in ['36_1', '36.1', 'razon', 'por_que_razon', 'costo_elevado']):
        col_razon_menstru = c
        break

col_desecho_basura = find_col_flexible(df_raw, ['37', 'basura', 'desecha'])
col_filtro_agua = find_col_flexible(df_raw, ['38', 'filtro', 'filtro_de_agua'])
col_tipo_filtro = find_col_flexible(df_raw, ['38_1', '38.1', 'tipo_de_filtro'])

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
    if 'costo' in s or 'presupuesto' in s:
        return 'Costo elevado o falta de presupuesto.'
    elif 'disponible' in s or 'tienda' in s or 'mercado' in s:
        return 'No hay disponibles a la venta en las tiendas cercanas, mercados o puntos de abasto locales.'
    elif 'alternativa' in s or 'ceniza' in s or 'arena' in s:
        return 'Utiliza otras alternativas locales (ceniza, arena, barro, plantas, hojas tradicionales o solo agua).'
    elif 'necesario' in s:
        return 'No lo considera necesario.'
    elif 'habitual' in s:
        return 'No es una práctica habitual en la rutina diaria de la familia.'
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
df_clean['edu_clean'] = df_raw[col_edu].apply(lambda x: limpiar_codigo(x, MAPA_EDUCACION)) if col_edu else 'No especificado'

df_clean['nacionalidad_clean'] = df_raw[col_nac].apply(lambda x: limpiar_codigo(x, MAPA_NACIONALIDAD)) if col_nac else 'No especificado'
df_clean['pueblo_indigena_clean'] = df_raw[col_ind].apply(lambda x: limpiar_codigo(x, MAPA_PUEBLOS_INDIGENAS)) if col_ind else 'No especificado'
df_clean['discapacidad_clean'] = df_raw[col_disc].apply(lambda x: limpiar_codigo(x, MAPA_DISCAPACIDADES)) if col_disc else 'No especificado'
df_clean['gestantes_val'] = pd.to_numeric(df_raw[col_gestantes], errors='coerce').fillna(0) if col_gestantes else 0

df_clean['hombres_val'] = pd.to_numeric(df_raw[col_hombres], errors='coerce').fillna(0) if col_hombres in df_raw.columns else 0
df_clean['mujeres_val'] = pd.to_numeric(df_raw[col_mujeres], errors='coerce').fillna(0) if col_mujeres in df_raw.columns else 0

if col_ninos in df_raw.columns:
    df_clean['ninos_val'] = pd.to_numeric(df_raw[col_ninos], errors='coerce').fillna(0)
else:
    cols_infantes = [c for c in df_raw.columns if any(k in c.lower() for k in ['0_4', '5_17', '0 a 4', '5 a 17', 'menor'])]
    if cols_infantes:
        df_clean['ninos_val'] = df_raw[cols_infantes].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)
    else:
        df_clean['ninos_val'] = 0

df_clean['total_embarazadas_val'] = pd.to_numeric(df_raw[col_total_embarazadas], errors='coerce').fillna(0) if col_total_embarazadas in df_raw.columns else 0
df_clean['emb_menores_val'] = pd.to_numeric(df_raw[col_emb_menores], errors='coerce').fillna(0) if col_emb_menores in df_raw.columns else 0
if col_emb_control in df_raw.columns:
    df_clean['emb_control_val'] = df_raw[col_emb_control].apply(lambda x: 1 if str(x).strip().lower() in ['si', 'sí', '1', 'true', 'yes'] else 0)
else:
    df_clean['emb_control_val'] = 0

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

df_clean['lgbti_clean'] = df_raw[lgbti_col].apply(lambda x: 'Sí' if str(x).strip().lower() in ['si', 'sí', '1', 'true'] else 'No') if lgbti_col else 'No'
df_clean['indigena_filtro'] = df_clean['pueblo_indigena_clean'].apply(lambda x: 'Sí (Pueblo Indígena)' if x not in ['No Especificado', 'No especificado'] else 'No')
df_clean['disc_filtro'] = df_clean['discapacidad_clean'].apply(
    lambda x: 'Sí (Con Discapacidad)' if x not in ['No posee', 'Ns/Nc', 'No especificado', 'No Especificado'] else 'No'
)

df_clean['tenencia_clean'] = limpiar_texto_simple(col_tenencia)
df_clean['agua_frec_clean'] = df_raw[col_agua_frec].apply(limpiar_frecuencia_agua) if col_agua_frec else 'No especificado'
df_clean['agua_beber_clean'] = df_raw[col_agua_beber].apply(limpiar_si_no) if col_agua_beber else 'No especificado'
df_clean['agua_suf_clean'] = df_raw[col_agua_suf].apply(limpiar_si_no) if col_agua_suf else 'No especificado'
df_clean['agua_trat_clean'] = df_raw[col_agua_trat].apply(limpiar_si_no) if col_agua_trat else 'No especificado'
df_clean['almacena_clean'] = df_raw[col_almacena].apply(limpiar_si_no) if col_almacena else 'No especificado'
df_clean['acceso_jabon_clean'] = df_raw[col_acceso_jabon].apply(limpiar_si_no) if col_acceso_jabon else 'No especificado'

# Asignación segura y directa para la higiene menstrual y su razón
col_higiene_real = None
for c in df_raw.columns:
    c_l = c.lower()
    if ('menstru' in c_l or 'higiene' in c_l) and 'jabon' not in c_l and '36_1' not in c_l and '36.1' not in c_l:
        col_higiene_real = c
        break

if col_higiene_real:
    df_clean['higiene_menstru_clean'] = df_raw[col_higiene_real].apply(limpiar_si_no)
else:
    df_clean['higiene_menstru_clean'] = 'No especificado'

if col_razon_menstru:
    df_clean['razon_menstru_clean'] = df_raw[col_razon_menstru].apply(limpiar_razon_menstrual)
else:
    df_clean['razon_menstru_clean'] = 'No especificado'

df_clean['filtro_agua_clean'] = df_raw[col_filtro_agua].apply(limpiar_si_no) if col_filtro_agua else 'No especificado'

# --- BARRA LATERAL DE FILTROS ---
st.sidebar.header("Filtros del Tablero")
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

df_filtered = df_temp[df_temp['municipio_clean'].isin(sel_municipios)].copy()
if sel_disc != "Todos":
    df_filtered = df_filtered[df_filtered['disc_filtro'] == sel_disc]
if sel_ind != "Todos":
    df_filtered = df_filtered[df_filtered['indigena_filtro'] == sel_ind]

if df_filtered.empty:
    st.warning("⚠️ No hay registros que coincidan con los filtros seleccionados.")
    st.stop()

# --- TARJETAS KPI PRINCIPALES ---
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    st.metric("Encuestas", f"{len(df_filtered):,}")
with col2:
    tot_h = int(df_filtered['h
