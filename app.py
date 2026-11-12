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

COLOR_AZUL_COOPI = '#0072CE'
COLOR_VERDE_COOPI = '#28A745'
PALETA_COOPI = [COLOR_AZUL_COOPI, COLOR_VERDE_COOPI, '#17C3B2', '#D89FE3', '#E5B130', '#08327D']

st.markdown("""
<style>
    .titulo-principal {
        color: #0072CE !important;
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
    've240103': 'Catia La Mar', 've240104': 'El Junco', 've240105
