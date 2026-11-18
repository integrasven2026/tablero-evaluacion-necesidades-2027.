import pandas as pd
import streamlit as st

# ... (conexión, carga de datos y filtros principales previos) ...

# 1. FILTRADO DE LA BASE DE DATOS SEGÚN LOS FILTROS DEL SIDEBAR
# df_filtered es el dataframe resultante de aplicar los filtros de estado, municipio, parroquia, etc.

# 2. CÁLCULO DE MÉTRICAS CLAVE (ASEGURANDO LA SUMA CORRECTA POR HOGAR)
total_encuestas = len(df_filtered)

# Sumas exactas basadas en las columnas de composición del grupo familiar
total_hombres_hogares = int(df_filtered['calculate_grupofamiliar_hombres'].sum())
total_mujeres_hogares = int(df_filtered['calculate_grupofamiliar_mujeres'].sum())
total_lgbti_hogares = int(
    df_filtered['calculate_grupofamiliar_otro'].sum()
)  # O la columna correspondiente a la P12

# Total general de personas en los hogares bajo los filtros actuales
total_personas_hogares = (
    total_hombres_hogares + total_mujeres_hogares + total_lgbti_hogares
)

# Otras variables (Niños/as, Gestantes, Discapacidad, Indígenas)
total_ninos = int(df_filtered['ninos_niñas'].sum())  # Ajustar según tu columna
total_gestantes = int(df_filtered['gestantes'].sum())  # Ajustar según tu columna
total_discapacidad = int(
    df_filtered['con_discapacidad'].sum()
)  # Ajustar según tu columna
total_ indigenas = int(df_filtered['indigenas'].sum())  # Ajustar según tu columna

# 3. RENDERIZAR MÉTRICAS EN EL TABLERO (TARJETAS SUPERIORES)
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

with col1:
  st.metric(label="Encuestas", value=f"{total_encuestas:,}")
with col2:
  st.metric(label="Total Personas", value=f"{total_personas_hogares:,}")
with col3:
  st.metric(label="Hombres (Hogares)", value=f"{total_hombres_hogares:,}")
with col4:
  st.metric(label="Mujeres (Hogares)", value=f"{total_mujeres_hogares:,}")
with col5:
  st.metric(label="LGBTI+ (P.12)", value=f"{total_lgbti_hogares:,}")
with col6:
  st.metric(label="Niños/as", value=f"{total_ninos:,}")
with col7:
  st.metric(label="Gestantes", value=f"{total_gestantes:,}")
with col8:
  st.metric(label="c/ Discapacidad", value=f"{total_discapacidad:,}")

# 4. INCORPORACIÓN DEL FILTRO DE LA COMUNIDAD LGBTI+ (PREGUNTA 12) EN EL SIDEBAR
st.sidebar.subheader("Filtros Poblacionales y Enfoque Diferencial")

# Filtro por opciones de la Pregunta 12 / Identidad de Género / Diversidad
if 'pregunta_12' in df_filtered.columns:
  opciones_p12 = ['Todas'] + list(
      df_filtered['pregunta_12'].dropna().unique()
  )
  filtro_p12 = st.sidebar.selectbox(
      'Comunidad LGBTI+ (Pregunta 12)', opciones_p12
  )

  if filtro_p12 != 'Todas':
    df_filtered = df_filtered[df_filtered['pregunta_12'] == filtro_p12]
