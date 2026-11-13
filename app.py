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

col_tenencia = find_col(df_raw, ['22', 'tenencia', 'propiedad', 'habita', 'vivienda'])
col_cuartos = find_col(df_raw, ['cuartos', 'habitaciones', 'dormir'])
col_personas_viv = find_col(df_raw, ['personas_vivienda', 'total_personas'])

# Búsqueda precisa de Pregunta 26 (Fuentes de Agua) y Pregunta 27 (Frecuencia de Agua)
col_agua_fuente = find_col(df_raw, ['26', 'fuentes_de_agua', 'principales_fuentes_de_agua', 'fuente_agua'])
col_agua_frec = find_col(df_raw, ['27', 'frecuencia', 'frecuencia_reciben_agua', 'frecuencia_servicio_agua'])

col_agua_suf = find_col(df_raw, ['suficiente_agua', 'agua_suficiente'])
col_agua_trat = find_col(df_raw, ['tratamiento_agua', 'trata_agua'])
col_tipo_trat = find_col(df_raw, ['tipo_tratamiento', 'metodo_tratamiento'])
col_almacena_agua = find_col(df_raw, ['almacena_agua', 'almacenamiento_agua'])
col_tipo_alm = find_col(df_raw, ['tipo_almacenamiento', 'recipiente_agua'])
col_filtro_agua = find_col(df_raw, ['filtro_agua', 'posee_filtro'])
col_tipo_filtro = find_col(df_raw, ['tipo_filtro'])
col_enfermedades = find_col(df_raw, ['enfermedades_hidricas', 'enfermedades'])
col_jabon = find_col(df_raw, ['acceso_jabon', 'jabon_manos'])
col_higiene_men = find_col(df_raw, ['higiene_menstrual', 'productos_menstruales'])
col_basura = find_col(df_raw, ['disposicion_basura', 'desecho_basura'])

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

def limpiar_tenencia(val):
    if pd.isna(val):
        return 'No especificado'
    v_str = str(val).strip().lower()
    if v_str in ['1', 'propia', 'prop']:
        return 'Propia'
    elif v_str in ['2', 'alquilada', 'alquiler', 'alquil']:
        return 'Alquilada'
    elif v_str in ['3', 'cedida', 'prestada', 'cedida / prestada', 'ced', 'prest']:
        return 'Cedida / Prestada'
    elif v_str in ['4', 'refugio', 'ocupacion', 'informal', 'refugio / ocupacion informal']:
        return 'Refugio / Ocupación informal'
    
    if 'prop' in v_str:
        return 'Propia'
    elif 'alquil' in v_str or 'alquiler' in v_str:
        return 'Alquilada'
    elif 'ced' in v_str or 'prest' in v_str:
        return 'Cedida / Prestada'
    elif 'refug' in v_str or 'ocup' in v_str or 'informal' in v_str:
        return 'Refugio / Ocupación informal'
    return 'No especificado'

df_clean['tenencia_clean'] = df_raw[col_tenencia].apply(limpiar_tenencia) if col_tenencia else 'No especificado'
df_clean['cuartos_dormir_val'] = pd.to_numeric(df_raw[col_cuartos], errors='coerce').fillna(1) if col_cuartos else 1
df_clean['cuartos_dormir_val'] = df_clean['cuartos_dormir_val'].apply(lambda x: 1 if x < 1 else x)

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

df_clean['total_personas_hogar'] = (
    df_clean['i1'] + df_clean['i2'] + df_clean['i3'] +
    df_clean['i12'] + df_clean['i13'] + df_clean['i14'] +
    df_clean['i23'] + df_clean['i24'] + df_clean['i25']
)
df_clean['total_personas_hogar'] = df_clean['total_personas_hogar'].apply(lambda x: 1 if x == 0 else x)

df_clean['indice_hacinamiento'] = df_clean['total_personas_hogar'] / df_clean['cuartos_dormir_val']
df_clean['hacinamiento_critico'] = df_clean['indice_hacinamiento'].apply(lambda x: 'Hacinamiento Crítico (>3 hab/cuarto)' if x > 3.0 else 'Sin Hacinamiento Crítico (<=3)')

# --- LIMPIEZA ROBUSTA PREGUNTA 26: FUENTES DE AGUA ---
def limpiar_fuente_agua(val):
    if pd.isna(val):
        return 'No especificado'
    v_str = str(val).strip().lower()
    if v_str in ['1', 'red', 'tubería', 'acueducto', 'red de tubería (acueducto)']:
        return 'Red de tubería (acueducto)'
    elif v_str in ['2', 'pozo', 'manantial', 'pozo subterráneo / manantial']:
        return 'Pozo subterráneo / Manantial'
    elif v_str in ['3', 'cisterna', 'camión', 'camión cisterna']:
        return 'Camión
