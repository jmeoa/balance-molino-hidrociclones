
# balance_molino_hidrociclones_avanzado.py

import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Balance Molino-Hidrociclones", layout="wide")

st.sidebar.image("logo.png", width=200)
st.title("Balance de Masas: Molino - Hidrociclones")

st.sidebar.header("Parámetros del sistema")

F = st.sidebar.number_input("Alimentación fresca (t/h)", min_value=0.0, value=100.0)
U = st.sidebar.number_input("Underflow (t/h)", min_value=0.0, value=200.0)
agua_adicional = st.sidebar.number_input("Agua adicional en cajón (m³/h)", min_value=0.0, value=50.0)
porc_agua_overflow = st.sidebar.slider("Porcentaje de agua al overflow (%)", 0, 100, 70)

densidad_solido = st.sidebar.number_input("Densidad del sólido (g/cm³)", min_value=1.0, value=2.7)
densidad_agua = 1.0

st.sidebar.header("Simulación eficiencia del ciclón")
d50 = st.sidebar.number_input("d50 (µm)", min_value=1.0, value=100.0)
d = st.sidebar.number_input("Tamaño de partícula simulada d (µm)", min_value=1.0, value=80.0)
s = 3.0

O = F
P = F + U

agua_overflow = agua_adicional * porc_agua_overflow / 100
agua_underflow = agua_adicional - agua_overflow

def calc_porc_solidos(masa_seca_t, agua_m3):
    masa_seca_kg = masa_seca_t * 1000
    agua_litros = agua_m3 * 1000
    masa_agua_kg = agua_litros * densidad_agua
    return masa_seca_kg / (masa_seca_kg + masa_agua_kg) * 100

porc_solidos_molino = calc_porc_solidos(P, agua_adicional)
porc_solidos_uf = calc_porc_solidos(U, agua_underflow)
porc_solidos_of = calc_porc_solidos(O, agua_overflow)

# Mostrar diagrama estático
st.subheader("🔁 Diagrama del sistema de molienda y clasificación")
st.image("diagrama_sistema.png", caption="Diagrama del sistema con información técnica", use_container_width=True)

# Tabla consolidada
st.subheader("📊 Tabla consolidada por flujo")

tabla_balance = pd.DataFrame({
    "Flujo / Corriente": [
        "Alimentación Fresca",
        "Adición de Agua",
        "Alimento al Molino",
        "Underflow",
        "Overflow (Producto Final)"
    ],
    "Masa seca (t/h)": [F, 0, P, U, O],
    "Agua (m³/h)": [0, agua_adicional, agua_adicional, agua_underflow, agua_overflow],
    "% Sólidos": [100, 0, porc_solidos_molino, porc_solidos_uf, porc_solidos_of],
    "Total (t/h aprox)": [
        F,
        agua_adicional,
        P + agua_adicional * densidad_agua,
        U + agua_underflow * densidad_agua,
        O + agua_overflow * densidad_agua
    ]
})

st.dataframe(tabla_balance.style.format({
    "Masa seca (t/h)": "{:.1f}",
    "Agua (m³/h)": "{:.1f}",
    "% Sólidos": "{:.1f}",
    "Total (t/h aprox)": "{:.1f}"
}))

# Gráficos dinámicos
st.subheader("📈 Gráficos de eficiencia del ciclón y consumo energético del molino")

d_values = np.linspace(10, 300, 100)
efficiency = 1 / (1 + np.exp(s * (d50 - d_values) / d50)) * 100
E_d = 1 / (1 + math.exp(s * (d50 - d) / d50)) * 100

f80 = 1000
wi = 12
p80_range = np.linspace(50, 500, 100)
energia = 10 * wi * (1 / np.sqrt(p80_range) - 1 / np.sqrt(f80))

fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Eficiencia del Hidrociclón", "Consumo Energético del Molino")
)

fig.add_trace(go.Scatter(x=d_values, y=efficiency, mode="lines", name="Eficiencia ciclón"),
              row=1, col=1)
fig.add_trace(go.Scatter(x=[d], y=[E_d], mode="markers+text", name="d simulado",
                         text=[f"{E_d:.1f}%"], textposition="top center"),
              row=1, col=1)

fig.add_trace(go.Scatter(x=p80_range, y=energia, mode="lines", name="Energía molino"),
              row=1, col=2)

fig.update_layout(height=500, template="plotly_white", showlegend=False)
fig.update_xaxes(title_text="Tamaño partícula (µm)", row=1, col=1)
fig.update_yaxes(title_text="Eficiencia (%)", row=1, col=1)
fig.update_xaxes(title_text="P80 (µm)", row=1, col=2)
fig.update_yaxes(title_text="kWh/t", row=1, col=2)

st.plotly_chart(fig, use_container_width=True)


# =============================================================
# MODELO DE DISTRIBUCIÓN GRANULOMÉTRICA - CICLÓN Y MOLINO
# =============================================================

st.subheader("🔬 Distribución granulométrica estimada para cada flujo")

# Definir rango de tamaños y log-normal base con F80
d_array = np.linspace(1, 1000, 100)
log_mean = np.log(F80)
sigma = 0.5  # dispersión asumida

# Distribución de alimentación fresca (densidad de probabilidad)
dist_fresca = (1 / (d_array * sigma * np.sqrt(2 * np.pi))) * np.exp(-((np.log(d_array) - log_mean) ** 2) / (2 * sigma ** 2))
dist_fresca /= dist_fresca.sum()

# Eficiencia del ciclón
eficiencia = 1 / (1 + np.exp(s * (d50 - d_array) / d50))

# Overflow = fresca * eficiencia
dist_overflow = dist_fresca * eficiencia
dist_overflow /= dist_overflow.sum()

# Underflow = fresca * (1 - eficiencia)
dist_underflow = dist_fresca * (1 - eficiencia)
dist_underflow /= dist_underflow.sum()

# Alimentación compuesta = combinación de fresca + underflow
peso_f = F
peso_u = U
dist_molino = (peso_f * dist_fresca + peso_u * dist_underflow) / (peso_f + peso_u)
dist_molino /= dist_molino.sum()

# Subplot de todas las curvas
fig3 = make_subplots(rows=1, cols=1)

fig3.add_trace(go.Scatter(x=d_array, y=dist_fresca, mode="lines", name="Alimentación Fresca"))
fig3.add_trace(go.Scatter(x=d_array, y=dist_molino, mode="lines", name="Alimentación al Molino"))
fig3.add_trace(go.Scatter(x=d_array, y=dist_underflow, mode="lines", name="Underflow"))
fig3.add_trace(go.Scatter(x=d_array, y=dist_overflow, mode="lines", name="Overflow (Producto)"))

fig3.update_layout(
    title="Distribuciones granulométricas estimadas",
    xaxis_title="Tamaño de partícula (µm)",
    yaxis_title="Fracción",
    template="plotly_white",
    height=500
)

st.plotly_chart(fig3, use_container_width=True)
