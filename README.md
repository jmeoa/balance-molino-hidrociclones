
# Balance de Masas: Molino - Hidrociclones

Aplicación interactiva desarrollada con **Streamlit** para simular el balance de masas en un circuito de molienda con clasificación por hidrociclones.

## Características

- Balance de masa y agua en estado estacionario
- Cálculo de carga circulante
- Cálculo de % de sólidos en cada corriente
- Simulación de eficiencia del ciclón en función del d50
- Diagrama de flujo interactivo con Plotly
- Gráficos dinámicos: eficiencia del ciclón y consumo energético del molino (modelo de Bond)

## Requisitos

Instala las dependencias ejecutando:

```bash
pip install -r requirements.txt
```

## Cómo ejecutar la app localmente

```bash
streamlit run balance_molino_hidrociclones_avanzado.py
```

## Cómo desplegar en Streamlit Cloud

1. Sube los archivos a un repositorio en GitHub.
2. Ve a [https://streamlit.io/cloud](https://streamlit.io/cloud).
3. Conecta tu cuenta de GitHub y selecciona este repositorio.
4. Define `balance_molino_hidrociclones_avanzado.py` como script principal.
5. ¡Listo! Tu app estará en línea.

---

Desarrollado por un ingeniero metalurgista usando ❤️ y Python.
