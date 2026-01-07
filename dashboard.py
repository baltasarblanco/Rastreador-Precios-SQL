import streamlit as st
import sqlite3
import pandas as pd

# 1 . CONFIGURACIÓN DE PÁGINA ( Para que se vea ancha )
st.set_page_config(page_title="Monitor de Precios", layout= "wide")

st.title("🦍 CENTRO DE MANDO - PRECIOS 2026")
st.markdown("---")

# 2 . CONECTAR Y CARGAR DATOS
conn = sqlite3.connect("base_datos_tienda.db")
query = "SELECT * FROM productos"
df = pd.read_sql(query, conn)
conn.close()

# ---- BARRA LATERAL 🎯 SIDE BAR ----
st.sidebar.header ("🎛️ Filtros")

# Filtro 1 : Checkbox para ver todo o solo lo nuevo
ver_solo_hoy = st.sidebar.checkbox("Ver solo datos de HOY")

# Filtro 2 : Slider de Precio ( Entre 0  y el máximo que encuentre)
precio_maximo_posible = int(df["precio"].max()) + 10 # Un poco mas del maximo real
precio_filtro = st.sidebar.slider(
    "Precio Máximo ($)",
    min_value=0,
    max_value=precio_maximo_posible,
    value=precio_maximo_posible # Valor por defecto (todo)
)

# Filtro 3: BUSCADOR DE TEXTO
texto_buscar = st.sidebar.text_input ("🔍 Buscar por nombre:")


# -----🧠 LOGICA DE FILTRADO (PANDAS) -----
# AQUI es donde ocurre la magia. Filtramos el DataFrame Original

df_filtrado = df.copy() # Trabajamos  sobre una copía para no romper el original

# Aplicar filtro de precio
df_filtrado = df_filtrado[df_filtrado["precio"] <= precio_filtro]

# Aplicar filtro de texto (si escribió algo0)
if texto_buscar:
    # str.cotains busca el texto, case=False ignora mayusculas
    df_filtrado = df_filtrado[df_filtrado["nombre"].str.contains(texto_buscar, case=False)]


# ----- 📊 MOSTRAR EL RESULTADO -----

# Dividimos la pantalla en 2 columnas (Gráfico y Tabla)

col_grafico, col_tabla = st.columns([2, 1]) # La columna 1 es el doble de ancha

with col_grafico:
    st.subheader("💰 Distribución de Precios")
    # Mostramos gráfico solo de lo filtrado
    st.bar_chart(df_filtrado.set_index("nombre")["precio"])

with col_tabla:
    st.subheader ("📋 Datos Detallados")
    st.write (f"Mostrando {len(df_filtrado)} productos")
    st.dataframe(df_filtrado, height=400)

# Métricas flotantes
st.markdown("---")
st.metric("Precio Promedio (Selección)", f"${round(df_filtrado['precio'].mean(), 2)}")
