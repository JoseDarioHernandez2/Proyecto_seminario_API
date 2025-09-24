import streamlit as st
import requests
import pandas as pd
import altair as alt

# ----------------------------
# Estilos (tema oscuro + customización)
# ----------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #1A1A1A;
        color: white;
        font-size: 1.1em;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #7CFC00;
    }
    label {
        color: white !important;
        font-weight: bold;
    }
    div.stButton > button:first-child {
        background-color: #CD5700;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #A34500;
        color: white;
        border: 1px solid white;
    }
    .stNumberInput input, .stSelectbox div[role="listbox"] {
        background-color: #262730;
        color: #7CFC00;
        border: 2px solid #7CFC00;
        border-radius: 5px;
        padding: 5px;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        margin-top: 20px;
        font-size: 1.5em;
        font-weight: bold;
        text-align: center;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# conectemos con la API 
# API_URL = "http://127.0.0.1:8000/predict"
# ----------------------------
API_URL = "http://127.0.0.1:8000/predict"


# ----------------------------
# Título
# ----------------------------
st.title("📊 APP Predicción 2025 - Índice de Percepción de la Corrupción")
st.write("Modelo de **Machine Learning** para predecir el índice de percepción de la corrupción, elaborado por Alison Gamba & Jose Dario Hernandez.")

# ----------------------------
# Inputs o entradas de usuario (más intuitivas)
# ----------------------------
st.subheader("📝 Datos de entrada")

fuentes = st.number_input("🔢 Número de fuentes", value=3, min_value=3, max_value=10, step=1)
error_estandar = st.number_input("📏 Error estándar", value=0.6, min_value=0.6, max_value=8.3, step=0.1)
cpi_2024 = st.number_input("📊 CPI Score 2024", value=50.0, min_value=1.0, max_value=100.0)
cpi_2023 = st.number_input("📊 CPI Score 2023", value=48.0, min_value=1.0, max_value=100.0)

# Cálculo automático de features técnicas
cpi_rezago1 = cpi_2024
cpi_rezago2 = cpi_2023
delta1 = cpi_2024 - cpi_2023
flag_fuentes_imputadas = 0
flag_error_imputado = 0

# ----------------------------
# Botón de predicción
# ----------------------------
if st.button("🔮 Predecir"):
    payload = {
        "Sources": fuentes,
        "Standard_error": error_estandar,
        "CPI_Score_lag1": cpi_rezago1,
        "CPI_Score_lag2": cpi_rezago2,
        "flag_imputed_Sources": flag_fuentes_imputadas,
        "flag_imputed_SE": flag_error_imputado,
    }
        # Llamada a la API
    try:
        res = requests.post("http://127.0.0.1:8000/predict", json=payload)
        if res.status_code == 200:
            data = res.json()
            prediction = data.get("predicted_cpi_score", "Sin resultado")

            # Mostrar resultado
            st.markdown(f"""
                <div class="result-box">
                    ✅ Predicción CPI 2025: <span>{prediction}</span>
                </div>
            """, unsafe_allow_html=True)

            # ----------------------------
            # Gráfico de probabilidades
            # ----------------------------
            if data.get("probabilities"):
                st.subheader("📊 Distribución de probabilidades")

                # Transformar a DataFrame
                probs = pd.DataFrame({
                    "Clase": [str(i) for i in range(len(data["probabilities"][0]))],
                    "Probabilidad": data["probabilities"][0]
                })

                # Gráfico de barras con Altair
                chart = (
                    alt.Chart(probs)
                    .mark_bar(color="#7CFC00")
                    .encode(
                        x=alt.X("Clase:N", title="Clase"),
                        y=alt.Y("Probabilidad:Q", title="Probabilidad", scale=alt.Scale(domain=[0,1])),
                        tooltip=["Clase", "Probabilidad"]
                    )
                    .properties(width=600, height=400)
                )

                st.altair_chart(chart, use_container_width=True)

        else:
            st.error(f"❌ Error en la predicción ({res.status_code})")
    except Exception as e:
        st.error(f"⚠️ No se pudo conectar con la API: {e}")
