
# balance_molino_hidrociclones_avanzado.py

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import math

st.set_page_config(page_title="Balance Molino-Hidrociclones", layout="wide")

st.image("logo.png", width=300)
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

ton_a_kg = 1000
m3_a_litros = 1000

def calc_porc_solidos(masa_seca_t, agua_m3):
    masa_seca_kg = masa_seca_t * ton_a_kg
    agua_litros = agua_m3 * m3_a_litros
    masa_agua_kg = agua_litros * densidad_agua
    return masa_seca_kg / (masa_seca_kg + masa_agua_kg) * 100

porc_solidos_molino = calc_porc_solidos(P, agua_adicional)
porc_solidos_uf = calc_porc_solidos(U, agua_underflow)
porc_solidos_of = calc_porc_solidos(O, agua_overflow)

E_d = 1 / (1 + math.exp(s * (d50 - d) / d50)) * 100

st.subheader("Resultados del balance")
st.markdown(f"- **Carga total al molino**: {P:.1f} t/h")
st.markdown(f"- **Overflow (producto final)**: {O:.1f} t/h")
st.markdown(f"- **Carga circulante**: {U / O:.2f}")

tabla_balance = pd.DataFrame({
    "Flujo / Corriente": ["Alimentación al Molino", "Underflow", "Overflow"],
    "Masa seca (t/h)": [P, U, O],
    "Agua (m³/h)": [agua_adicional, agua_underflow, agua_overflow],
    "% Sólidos": [porc_solidos_molino, porc_solidos_uf, porc_solidos_of],
    "Total (t/h aprox)": [
        P + agua_adicional * densidad_agua,
        U + agua_underflow * densidad_agua,
        O + agua_overflow * densidad_agua,
    ]
})

st.subheader("Tabla consolidada por flujo")
st.dataframe(tabla_balance.style.format({
    "Masa seca (t/h)": "{:.1f}",
    "Agua (m³/h)": "{:.1f}",
    "% Sólidos": "{:.1f}",
    "Total (t/h aprox)": "{:.1f}"
}))

# Subplots para los dos gráficos: eficiencia y consumo energético
st.subheader("Gráficos dinámicos del sistema")

# Datos para eficiencia del ciclón
d_values = np.linspace(10, 300, 100)
efficiency = 1 / (1 + np.exp(s * (d50 - d_values) / d50)) * 100

# Datos para energía del molino
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
