
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

# Diagrama interactivo
st.subheader("🔁 Diagrama interactivo con parámetros del flujo")

fig = go.Figure()

fig.add_layout_image(
    dict(
        source="diagrama_sistema.jpeg",
        xref="paper", yref="paper",
        x=0, y=1,
        sizex=1, sizey=1,
        xanchor="left",
        yanchor="top",
        layer="below"
    )
)

# Anotaciones con coordenadas aproximadas (pueden ajustarse luego)
fig.add_annotation(x=0.06, y=0.5, text=f"{F:.1f} t/h", showarrow=False, font=dict(size=12, color="black"))
fig.add_annotation(x=0.24, y=0.45, text=f"{P:.1f} t/h<br>{porc_solidos_molino:.1f}% sólidos<br>{agua_adicional:.1f} m³/h", showarrow=False)
fig.add_annotation(x=0.65, y=0.28, text=f"{U:.1f} t/h<br>{porc_solidos_uf:.1f}%<br>{agua_underflow:.1f} m³/h", showarrow=False)
fig.add_annotation(x=0.85, y=0.72, text=f"{O:.1f} t/h<br>{porc_solidos_of:.1f}%<br>{agua_overflow:.1f} m³/h", showarrow=False)

fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_layout(
    margin=dict(l=10, r=10, t=10, b=10),
    height=600,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)
