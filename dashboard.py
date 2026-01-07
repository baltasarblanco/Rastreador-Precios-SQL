import streamlit as st
import sqlite3
import pandas as pd

# 1 . CONFIGURACIÓN DE PÁGINA ( Para que se vea ancha )
st.set_page_config(page_title="Monitor de Precios", layout= "wide", page_icon="🦍")


st.title("🦍 CENTRO DE MANDO - PRECIOS 2026")
st.markdown("---")

# 2 . CONECTAR Y CARGAR DATOS
conn = sqlite3.connect("base_datos_tienda.db")
query = "SELECT * FROM productos"
df = pd.read_sql(query, conn)
conn.close()

# ---- BARRA LATERAL 🎯 SIDE BAR ----
st.sidebar.header ("🎛️ Filtros Avanzados")  
ver_todos = st.sidebar.checkbox("Mostrar todos los datos", value=True)

# . KPI (MÉTRICAS CLAVE) --- NUEVO !!!!
# Mostramos estadisticas rápidas arriba de todo
st.subheader("📊 Estadísticas Generales")
kpi1, kpi2, kpi3 = st.columns(3)

avg_price = df["precio"].mean()
max_price = df["precio"].max()
min_price = df["precio"].min()

kpi1.metric("Precio Promedio", f"${round(avg_price, 2)}", delta="Global")
kpi2.metric("Producto Más Caro", f"${max_price}", delta="-Riesgo", delta_color='inverse')
kpi3.metric("Producto Más Barato", f"${min_price}", delta="+Oportunidad")

st.markdown("----")


# 4 . FILTROS Y LÓGICA
max_p = int(df["precio"].max()) if not df.empty else 100
precio_filtro = st.sidebar.slider ("Tope de Precio ($)", 0, max_p, max_p)
texto_buscar = st.sidebar.text_input("🔍 Buscar producto")

df_filtrado = df.copy()

df_filtrado = df_filtrado[df_filtrado["precio"] <= precio_filtro]

# Filtramos por texto ( si existe)
if texto_buscar:
    df_filtrado = df_filtrado[df_filtrado["nombre"].str.contains(texto_buscar, case=False)]


# 5 . VISUALIZACIÓN PRO
col_grafico, col_tabla = st.columns([2, 1])

with col_grafico:
    st.subheader ("💰 Tendencias de Mercado")
    if not df_filtrado.empty:
        st.bar_chart(df_filtrado.set_index("nombre")["precio"], color="#00ff00") # COLOR VERDE HACKER !!
    else:
        st.warning("No hay datos para mostrar.")


with col_tabla:
    st.subheader("📋 Datos (Descargables)")

    # 6. BOTÓN DE DESCARGA (¡SUPER IMPORTANTE!)
    # Convertimos el DF a CSV (texto separado por comas)
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Descargar a Excel (CSV)",
        data=csv,
        file_name="reporte_precios_2026.csv",
        mime="text/csv",

    )

    # 7. TABLA CON COLORES (HEATMAP)
    # Resalta precios altos en un tono y bajos en otro

    st.dataframe(
        df_filtrado.style.highlight_max(axis=0, color='#ffcccb') # ROJO SUAVE PARA MAX
                    .highlight_min(axis=0, color='#90ee90'), # VERDE SUAVE PARA EL MIN
        height=400

    )
