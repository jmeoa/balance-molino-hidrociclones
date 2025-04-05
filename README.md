
# Balance Molino - Hidrociclones | Hydrox Smart Metallurgy

Esta aplicación desarrollada con **Streamlit** permite simular el **balance de masas** y visualizar la **eficiencia de clasificación** en un circuito de molienda con hidrociclones, incorporando la adición de agua en el cajón de descarga del molino.

---

## 🔧 Funcionalidades

- Cálculo dinámico de:
  - Tonelajes en cada corriente
  - Porcentaje de sólidos (%)
  - Caudal de agua en m³/h
- Gráficos interactivos:
  - Eficiencia del ciclón según curva de clasificación
  - Consumo energético del molino usando el modelo de Bond
- Visualización integrada de:
  - Diagrama del sistema
  - Parámetros clave por corriente
  - Logo institucional en barra lateral

---

## 📂 Archivos incluidos

- `balance_molino_hidrociclones_avanzado.py`: código principal de la app.
- `logo.png`: logotipo de Hydrox.
- `diagrama_sistema.png`: diagrama del sistema de molienda + clasificación.
- `requirements.txt`: dependencias de la app.

---

## 🚀 Cómo ejecutar localmente

1. Crea un entorno virtual (opcional pero recomendado):

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instala dependencias:

```bash
pip install streamlit pandas numpy plotly
```

3. Ejecuta la aplicación:

```bash
streamlit run balance_molino_hidrociclones_avanzado.py
```

---

## 🌐 Despliegue en Streamlit Cloud

Sube los archivos a un repositorio público de GitHub y conéctalo a [Streamlit Cloud](https://streamlit.io/cloud) seleccionando como archivo principal:  
`balance_molino_hidrociclones_avanzado.py`

---

## 📧 Autor

**Hydrox Smart Metallurgy**  
Desarrollado por Jose M. Olguín Acevedo | [LinkedIn](https://linkedin.com/in/josemolguin)
