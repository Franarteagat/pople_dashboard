import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuración de página
st.set_page_config(
    page_title="Pople | Tablero de Gestión de Personas",
    page_icon="👥",
    layout="wide"
)

# Estilos CSS personalizados (Paleta Pople: Rosa Coral, Azul Marino y Gris Claro)
st.markdown("""
    <style>
    .main {
        background-color: #FAFAFA;
    }
    .stMetric {
        background-color: #FFFFFF;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        border-left: 5px solid #E63946;
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
    }
    div[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal
st.title("👥 Pople — Tablero de Control B2B")
st.markdown("**Plataforma de Inteligencia en Gestión de Personas, Cumplimiento Normativo y Desarrollo Organizacional para PyMEs.**")
st.markdown("---")

# Carga de datos de prueba
@st.cache_data
def cargar_datos():
    np.random.seed(42)
    n = 50
    departamentos = ["Operaciones", "Ventas", "Tecnología", "Finanzas", "Logística"]
    estados_normativa = ["Completado", "En Curso", "Pendiente"]
    estados_doc = ["Al día", "Por Vencer", "Pendiente"]
    
    data = {
        "ID": range(101, 101 + n),
        "Trabajador": [f"Colaborador {i}" for i in range(1, n + 1)],
        "Departamento": np.random.choice(departamentos, size=n),
        "Capacitacion_Ley_Karin": np.random.choice(estados_normativa, size=n, p=[0.75, 0.18, 0.07]),
        "Capacitacion_Prevencion": np.random.choice(estados_normativa, size=n, p=[0.65, 0.25, 0.10]),
        "Evaluacion_Desempeno": np.random.uniform(3.0, 5.0, size=n).round(1),
        "Documentacion_Personal": np.random.choice(estados_doc, size=n, p=[0.82, 0.12, 0.06])
    }
    return pd.DataFrame(data)

df = cargar_datos()

# Filtros en la barra lateral
st.sidebar.image("https://img.icons8.com/color/96/group-task.png", width=70)
st.sidebar.title("Filtros Pople")
depto_seleccionado = st.sidebar.multiselect(
    "Filtrar por Área / Departamento:",
    options=df["Departamento"].unique(),
    default=df["Departamento"].unique()
)

df_filtrado = df[df["Departamento"].isin(depto_seleccionado)]

# Métricas KPI Principales
col1, col2, col3, col4 = st.columns(4)

total_colab = len(df_filtrado)
pct_karin = (df_filtrado['Capacitacion_Ley_Karin'] == 'Completado').mean() * 100 if total_colab > 0 else 0
prom_desempeno = df_filtrado['Evaluacion_Desempeno'].mean() if total_colab > 0 else 0
pct_carpetas = (df_filtrado['Documentacion_Personal'] == 'Al día').mean() * 100 if total_colab > 0 else 0

col1.metric("Dotación Total", f"{total_colab} Colaboradores")
col2.metric("Cumplimiento Ley Karin", f"{pct_karin:.1f}%")
col3.metric("Promedio Desempeño", f"{prom_desempeno:.2f} / 5.0")
col4.metric("Carpetas Auditadas Al Día", f"{pct_carpetas:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

# Gráficos Visuales
g_col1, g_col2 = st.columns(2)

with g_col1:
    st.subheader("📊 Cumplimiento Ley Karin por Departamento")
    fig_karin = px.histogram(
        df_filtrado, 
        x="Departamento", 
        color="Capacitacion_Ley_Karin", 
        barmode="group",
        color_discrete_map={"Completado": "#1D3557", "En Curso": "#457B9D", "Pendiente": "#E63946"},
        labels={"Capacitacion_Ley_Karin": "Estado Capacitación"}
    )
    fig_karin.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_karin, use_container_width=True)

with g_col2:
    st.subheader("🎯 Distribución de Evaluaciones de Desempeño")
    fig_desempeno = px.box(
        df_filtrado, 
        x="Departamento", 
        y="Evaluacion_Desempeno",
        color="Departamento",
        color_discrete_sequence=["#E63946", "#1D3557", "#457B9D", "#A8DADC", "#F1FAEE"]
    )
    fig_desempeno.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
    st.plotly_chart(fig_desempeno, use_container_width=True)

# Tabla de detalles
st.markdown("---")
st.subheader("📋 Registro Detallado de Colaboradores")
st.dataframe(
    df_filtrado[["ID", "Trabajador", "Departamento", "Capacitacion_Ley_Karin", "Documentacion_Personal", "Evaluacion_Desempeno"]],
    use_container_width=True
)
