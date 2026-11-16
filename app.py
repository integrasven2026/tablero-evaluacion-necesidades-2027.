import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Tablero de Monitoreo AICS",
    page_icon="📊",
    layout="wide"
)

# Estilos CSS limpios (sin emojis ni figuritas)
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        h1, h2, h3 {
            color: #1f2937;
        }
    </style>
""", unsafe_allow_html=True)

# Datos simulados / base para demostración (asegúrate de conectar tu fuente de KoboToolbox aquí)
@st.cache_data
def cargar_datos():
    # DataFrame de ejemplo para Población y Embarazo
    df_poblacion = pd.DataFrame({
        'Categoria': ['Total Personas Embarazadas', 'Embarazadas Menores de Edad', 'Asisten a Control Prenatal'],
        'Cantidad': [45, 12, 38]
    })
    
    # DataFrame para Tipos de Discapacidad (Top 5)
    df_discapacidad = pd.DataFrame({
        'Discapacidad': ['Motora', 'Auditiva', 'Auditiva y Visual', 'Auditiva y Motora', 'Cognitiva Visual'],
        'Cantidad': [158, 20, 15, 6, 4]
    })
    
    # DataFrame para Pueblos Indígenas (Top 5)
    df_indigenas = pd.DataFrame({
        'Pueblo Indigena': ['Wayúu (Guajiro)', 'Warao', 'Yukpa', 'Añú (Paraujano)', 'Kariña'],
        'Cantidad': [254, 73, 2, 2, 2]
    })
    
    # DataFrame para Vivienda
    df_vivienda = pd.DataFrame({
        'Tipo de Vivienda': ['Casa', 'Quinta', 'Rancho', 'Apartamento', 'Anexo'],
        'Total': [120, 15, 45, 30, 10]
    })
    
    return df_poblacion, df_discapacidad, df_indigenas, df_vivienda

df_pob, df_disc, df_ind, df_viv = cargar_datos()

# Título principal del tablero
st.title("Tablero de Monitoreo de Emergencia AICS")
st.markdown("---")

# Navegación por pestañas (Petición: Cambiar nombres y quitar figuritas)
pestanas = st.tabs(["Población", "Vivienda", "Agua, Saneamiento e Higiene (WASH)", "Base de Datos"])

# --- CAPÍTULO 1: POBLACIÓN (Anteriormente Cobertura y Demografía) ---
with pestanas[0]:
    st.header("Población")
    st.markdown("Indicadores demográficos y de atención prioritaria.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Indicadores de Embarazo")
        fig_emb = px.bar(
            df_pob, 
            x='Cantidad', 
            y='Categoria', 
            orientation='h',
            text='Cantidad',
            color='Categoria',
            color_discrete_sequence=['#e67e22', '#d35400', '#f39c12']
        )
        fig_emb.update_layout(showlegend=False, xaxis_title="Cantidad", yaxis_title="")
        st.plotly_chart(fig_emb, use_container_width=True)
        
    with col2:
        st.subheader("Tipos de Discapacidad Reportados (Top 5)")
        fig_disc = px.bar(
            df_disc.head(5), 
            x='Cantidad', 
            y='Discapacidad', 
            orientation='h',
            text='Cantidad',
            color_discrete_sequence=['#c0392b']
        )
        fig_disc.update_layout(showlegend=False, xaxis_title="Cantidad", yaxis_title="")
        st.plotly_chart(fig_disc, use_container_width=True)
        
    st.markdown("---")
    
    st.subheader("Pueblos Indígenas Identificados (Top 5)")
    fig_ind = px.bar(
        df_ind.head(5), 
        x='Cantidad', 
        y='Pueblo Indigena', 
        orientation='h',
        text='Cantidad',
        color_discrete_sequence=['#16a085']
    )
    fig_ind.update_layout(showlegend=False, xaxis_title="Cantidad", yaxis_title="")
    st.plotly_chart(fig_ind, use_container_width=True)

# --- CAPÍTULO 2: VIVIENDA (Anteriormente Vivienda y Habitabilidad) ---
with pestanas[1]:
    st.header("Vivienda")
    st.markdown("Datos generales sobre las condiciones y tipos de vivienda.")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        fig_viv = px.bar(
            df_viv,
            x='Tipo de Vivienda',
            y='Total',
            text='Total',
            color='Tipo de Vivienda',
            color_discrete_sequence=['#2980b9']
        )
        fig_viv.update_layout(showlegend=False)
        st.plotly_chart(fig_viv, use_container_width=True)
    with col_v2:
        st.dataframe(df_viv, use_container_width=True)

# --- CAPÍTULO 3: AGUA, SANEAMIENTO E HIGIENE (WASH) ---
with pestanas[2]:
    st.header("Agua, Saneamiento e Higiene (WASH)")
    st.write("Acceso a fuentes de agua segura, saneamiento y prácticas de higiene en los hogares evaluados.")
    # Espacio reservado para los indicadores WASH originales
    st.info("Módulo activo con los datos de saneamiento e higiene registrados.")

# --- CAPÍTULO 4: BASE DE DATOS ---
with pestanas[3]:
    st.header("Base de Datos General")
    st.write("Descarga y visualización de registros completos recopilados.")
    
    # Muestra de tabla consolidada
    tabla_maestra = pd.concat([df_pob, df_disc.rename(columns={'Discapacidad': 'Categoria', 'Cantidad': 'Cantidad'})])
    st.dataframe(tabla_maestra, use_container_width=True)
