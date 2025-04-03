
# Balance de Masas: Molino - Hidrociclones

Aplicación interactiva desarrollada con **Streamlit** para simular el balance de masas en un circuito de molienda con clasificación por hidrociclones.

## Características

- Balance de masa y agua en estado estacionario
- Cálculo de carga circulante
- Cálculo de % de sólidos en cada corriente
- Simulación de eficiencia del ciclón en función del d50
- Gráficos dinámicos: eficiencia del ciclón y consumo energético del molino (modelo de Bond)

## Requisitos

```bash
pip install -r requirements.txt
```

## Cómo ejecutar

```bash
streamlit run balance_molino_hidrociclones_avanzado.py
```

## Despliegue en Streamlit Cloud

1. Sube los archivos a GitHub.
2. Ve a [https://streamlit.io/cloud](https://streamlit.io/cloud).
3. Selecciona tu repositorio y define `balance_molino_hidrociclones_avanzado.py` como archivo principal.
