
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

# Parámetros del sistema
st.sidebar.header("Parámetros del sistema")

F = st.sidebar.number_input("Alimentación fresca (t/h)", min_value=0.0, value=100.0)
U = st.sidebar.number_input("Underflow (t/h)", min_value=0.0, value=200.0)
agua_adicional = st.sidebar.number_input("Agua adicional en cajón (m³/h)", min_value=0.0, value=50.0)
porc_agua_overflow = st.sidebar.slider("Porcentaje de agua al overflow (%)", 0, 100, 70)
densidad_solido = st.sidebar.number_input("Densidad del sólido (g/cm³)", min_value=1.0, value=2.7)
densidad_agua = 1.0

# Parámetros del modelo de Bond y clasificación
st.sidebar.header("Parámetros Granulométricos")
F80 = st.sidebar.number_input("F80 (µm)", min_value=1.0, value=1000.0)
Wi = st.sidebar.number_input("Índice de Trabajo Wi (kWh/t)", min_value=1.0, value=12.0)
E = st.sidebar.number_input("Energía Específica E (kWh/t)", min_value=0.1, value=8.0)
d50 = st.sidebar.number_input("d50 ciclón (µm)", min_value=1.0, value=100.0)
d = st.sidebar.number_input("Tamaño de partícula simulada d (µm)", min_value=1.0, value=80.0)
s = 3.0

# Cálculo P80
try:
    P80 = 1 / (1 / np.sqrt(F80) - E / (10 * Wi)) ** 2
except ZeroDivisionError:
    P80 = 0

# Cálculos de balance
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

# Mostrar diagrama
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
    ],
    "F80 (µm)": [F80, "", F80, F80, ""],
    "P80 (µm)": ["", "", P80, "", P80]
})

st.dataframe(tabla_balance.style.format({
    "Masa seca (t/h)": "{:.1f}",
    "Agua (m³/h)": "{:.1f}",
    "% Sólidos": "{:.1f}",
    "Total (t/h aprox)": "{:.1f}",
    "F80 (µm)": "{:.0f}",
    "P80 (µm)": "{:.0f}"
}))

# Gráficos de eficiencia y energía
st.subheader("📈 Eficiencia del ciclón y energía del molino")

d_values = np.linspace(10, 300, 100)
efficiency = 1 / (1 + np.exp(s * (d50 - d_values) / d50)) * 100
E_d = 1 / (1 + math.exp(s * (d50 - d) / d50)) * 100
f80 = F80
p80_range = np.linspace(50, 500, 100)
energia = 10 * Wi * (1 / np.sqrt(p80_range) - 1 / np.sqrt(f80))

fig1 = make_subplots(rows=1, cols=2, subplot_titles=("Eficiencia del ciclón", "Consumo energético del molino"))
fig1.add_trace(go.Scatter(x=d_values, y=efficiency, mode="lines", name="Eficiencia"), row=1, col=1)
fig1.add_trace(go.Scatter(x=[d], y=[E_d], mode="markers+text", text=[f"{E_d:.1f}%"], textposition="top center"), row=1, col=1)
fig1.add_trace(go.Scatter(x=p80_range, y=energia, mode="lines", name="Energía molino"), row=1, col=2)

fig1.update_layout(height=500, showlegend=False, template="plotly_white")
fig1.update_xaxes(title_text="Tamaño partícula (µm)", row=1, col=1)
fig1.update_yaxes(title_text="Eficiencia (%)", row=1, col=1)
fig1.update_xaxes(title_text="P80 (µm)", row=1, col=2)
fig1.update_yaxes(title_text="kWh/t", row=1, col=2)

st.plotly_chart(fig1, use_container_width=True)

# Distribución granulométrica
st.subheader("🔬 Distribución granulométrica estimada para cada flujo")

d_array = np.linspace(1e-2, 1000, 100)
log_mean = np.log(F80)
sigma = 0.5
dist_fresca = (1 / (d_array * sigma * np.sqrt(2 * np.pi))) * np.exp(-((np.log(d_array) - log_mean) ** 2) / (2 * sigma ** 2))
dist_fresca /= dist_fresca.sum()

eficiencia = 1 / (1 + np.exp(s * (d50 - d_array) / d50))
dist_overflow = dist_fresca * eficiencia
dist_overflow /= dist_overflow.sum()
dist_underflow = dist_fresca * (1 - eficiencia)
dist_underflow /= dist_underflow.sum()
dist_molino = (F * dist_fresca + U * dist_underflow) / (F + U)
dist_molino /= dist_molino.sum()

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=d_array, y=dist_fresca, mode="lines", name="Alimentación Fresca"))
fig2.add_trace(go.Scatter(x=d_array, y=dist_molino, mode="lines", name="Alimentación al Molino"))
fig2.add_trace(go.Scatter(x=d_array, y=dist_underflow, mode="lines", name="Underflow"))
fig2.add_trace(go.Scatter(x=d_array, y=dist_overflow, mode="lines", name="Overflow"))

fig2.update_layout(
    title="Distribuciones granulométricas estimadas",
    xaxis_title="Tamaño de partícula (µm)",
    yaxis_title="Fracción",
    template="plotly_white",
    height=500
)

st.plotly_chart(fig2, use_container_width=True)
