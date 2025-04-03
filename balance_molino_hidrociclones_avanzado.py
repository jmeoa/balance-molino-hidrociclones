
# balance_molino_hidrociclones_avanzado.py

import streamlit as st
import plotly.graph_objects as go
import math

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
st.markdown(f"- **% de sólidos en:**")
st.markdown(f"   - Carga al molino: {porc_solidos_molino:.1f} %")
st.markdown(f"   - Underflow: {porc_solidos_uf:.1f} %")
st.markdown(f"   - Overflow: {porc_solidos_of:.1f} %")

st.subheader("Simulación eficiencia de corte del ciclón")
st.markdown(f"- d50: {d50:.1f} µm")
st.markdown(f"- Partícula simulada: {d:.1f} µm")
st.markdown(f"- **Eficiencia para d={d:.1f} µm**: {E_d:.1f} %")

st.subheader("Diagrama de flujo interactivo")

fig = go.Figure()

fig.add_trace(go.Scatter(x=[1], y=[2], mode="markers+text", text=["Molino"], marker=dict(size=40), textposition="top center"))
fig.add_trace(go.Scatter(x=[3], y=[2], mode="markers+text", text=["Hidrociclón"], marker=dict(size=40), textposition="top center"))

fig.add_annotation(x=1, y=2.5, text=f"F={F:.1f}", showarrow=True, arrowhead=1, ax=-50, ay=0)
fig.add_annotation(x=2, y=2, text=f"P={P:.1f}", showarrow=True, arrowhead=1)
fig.add_annotation(x=3, y=2.5, text=f"O={O:.1f}", showarrow=True, arrowhead=1, ax=50, ay=0)
fig.add_annotation(x=3, y=1.5, text=f"U={U:.1f}", showarrow=True, arrowhead=1, ax=50, ay=-30)

fig.update_layout(showlegend=False, xaxis=dict(visible=False), yaxis=dict(visible=False),
                  title="Diagrama de Flujo: Molino - Hidrociclones")

st.plotly_chart(fig)
