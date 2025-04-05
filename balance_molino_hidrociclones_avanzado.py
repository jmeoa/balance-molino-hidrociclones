
# balance_molino_hidrociclones_avanzado.py

import streamlit as st
import pandas as pd
import numpy as np
import math
from PIL import Image
import plotly.graph_objects as go

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

st.subheader("🔁 Diagrama del sistema con valores superpuestos")

background_img = Image.open("diagrama_sistema.png")

fig = go.Figure()

fig.add_layout_image(
    dict(
        source=background_img,
        xref="paper", yref="paper",
        x=0, y=1,
        sizex=1, sizey=1,
        xanchor="left",
        yanchor="top",
        layer="below"
    )
)

# Anotaciones de valores principales
fig.add_annotation(x=0.06, y=0.5, text=f"{F:.1f} t/h", showarrow=False, font=dict(size=16, color="black"))
fig.add_annotation(x=0.24, y=0.45, text=f"{P:.1f} t/h\n{porc_solidos_molino:.1f}%\n{agua_adicional:.1f} m³/h", showarrow=False, font=dict(size=14, color="black"))
fig.add_annotation(x=0.65, y=0.28, text=f"{U:.1f} t/h\n{porc_solidos_uf:.1f}%\n{agua_underflow:.1f} m³/h", showarrow=False, font=dict(size=14, color="black"))
fig.add_annotation(x=0.85, y=0.72, text=f"{O:.1f} t/h\n{porc_solidos_of:.1f}%\n{agua_overflow:.1f} m³/h", showarrow=False, font=dict(size=14, color="black"))

fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_layout(
    margin=dict(l=10, r=10, t=10, b=10),
    height=600,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

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
