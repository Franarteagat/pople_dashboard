import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# 1. Configuración de la página
st.set_page_config(
    page_title="Pople - Dashboard de Gestión de Personas",
    page_icon="👥",
    layout="wide",
)

# Título del Dashboard
st.title("🚀 Pople - Gestión de Personas")
st.markdown(
    "Visualización estratégica de dotación, capacitaciones normativas, evaluaciones de desempeño y documentación laboral."
)
st.markdown("---")


# 2. Generación de datos simulados (reemplazar con la base de datos real de la PyME)
@st.cache_data
def cargar_datos():
    np.random.seed(42)
    n = 45  # Cantidad de trabajadores simulados

    departamentos = ["Operaciones", "Ventas", "Administración", "TI", "Logística"]
    estados_normativa = ["Completado", "En Curso", "Pendiente"]
    estados_doc = ["Al día", "Por Vencer", "Pendiente"]

    data = {
        "ID": range(101, 101 + n),
        "Trabajador": [f"Trabajador {i}" for i in range(1, n + 1)],
        "Departamento": np.random.choice(departamentos, size=n),
        "Capacitacion_Ley_Karin": np.random.choice(
            estados_normativa, size=n, p=[0.7, 0.2, 0.1]
        ),
        "Capacitacion_Prevencion": np.random.choice(
            estados_normativa, size=n, p=[0.6, 0.3, 0.1]
        ),
        "Evaluacion_Desempeno": np.random.uniform(2.5, 5.0, size=n).round(1),
        "Documentacion_Personal": np.random.choice(
            estados_doc, size=n, p=[0.8, 0.15, 0.05]
        ),
    }
    return pd.DataFrame(data)


df = cargar_datos()

# 3. Barra lateral con filtros
st.sidebar.header("🔍 Filtros de Búsqueda")
depto_seleccionado = st.sidebar.multiselect(
    "Seleccionar Departamento:",
    options=df["Departamento"].unique(),
    default=df["Departamento"].unique(),
)

# Filtrar DataFrame según selección
df_filtrado = df[df["Departamento"].isin(depto_seleccionado)]

# 4. Cálculo de Indicadores Clave (KPIs)
total_trabajadores = len(df_filtrado)

if total_trabajadores > 0:
    pct_karin = (
        df_filtrado["Capacitacion_Ley_Karin"] == "Completado"
    ).mean() * 100
    promedio_desempeno = df_filtrado["Evaluacion_Desempeno"].mean()
    pct_doc_al_dia = (
        df_filtrado["Documentacion_Personal"] == "Al día"
    ).mean() * 100
else:
    pct_karin, promedio_desempeno, pct_doc_al_dia = 0, 0, 0

# Visualización de KPIs en tarjetas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Trabajadores", value=f"{total_trabajadores}")

with col2:
    st.metric(
        label="Capacitación Ley Karin",
        value=f"{pct_karin:.1f}%",
        delta="Cumplimiento",
    )

with col3:
    st.metric(
        label="Evaluación Desempeño Promedio",
        value=f"{promedio_desempeno:.2f} / 5.0",
    )

with col4:
    st.metric(
        label="Documentos Personales Al Día",
        value=f"{pct_doc_al_dia:.1f}%",
        delta_color="normal" if pct_doc_al_dia > 80 else "inverse",
    )

st.markdown("---")

# 5. Gráficos Interactivos
g_col1, g_col2 = st.columns(2)

with g_col1:
    st.subheader("🎓 Capacitaciones Normativas (Ley Karin por Área)")
    fig_normativa = px.histogram(
        df_filtrado,
        x="Departamento",
        color="Capacitacion_Ley_Karin",
        barmode="group",
        color_discrete_map={
            "Completado": "#2ecc71",
            "En Curso": "#f1c40f",
            "Pendiente": "#e74c3c",
        },
        labels={"Capacitacion_Ley_Karin": "Estado Ley Karin"},
    )
    st.plotly_chart(fig_normativa, use_container_width=True)

with g_col2:
    st.subheader("📄 Estado de Documentación Personal (Contratos, Anexos, etc.)")
    fig_doc = px.pie(
        df_filtrado,
        names="Documentacion_Personal",
        color="Documentacion_Personal",
        color_discrete_map={
            "Al día": "#2ecc71",
            "Por Vencer": "#f39c12",
            "Pendiente": "#e74c3c",
        },
        hole=0.4,
    )
    st.plotly_chart(fig_doc, use_container_width=True)

g_col3, g_col4 = st.columns(2)

with g_col3:
    st.subheader("📊 Distribución de Evaluaciones de Desempeño")
    fig_desempeno = px.box(
        df_filtrado,
        x="Departamento",
        y="Evaluacion_Desempeno",
        points="all",
        color="Departamento",
        labels={"Evaluacion_Desempeno": "Nota Desempeño (1-5)"},
    )
    st.plotly_chart(fig_desempeno, use_container_width=True)

with g_col4:
    st.subheader("📋 Detalle de Registro de Trabajadores")
    st.dataframe(
        df_filtrado[
            [
                "Trabajador",
                "Departamento",
                "Capacitacion_Ley_Karin",
                "Evaluacion_Desempeno",
                "Documentacion_Personal",
            ]
        ],
        use_container_width=True,
        height=320,
    )