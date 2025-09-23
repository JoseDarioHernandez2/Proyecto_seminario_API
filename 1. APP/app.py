import streamlit as st
import requests

st.title("📊 APP de predicción modelo ML")
st.write("App de predicción modelo Random Forest.")

# ----------------------------------------------------------------
# Inputs acordes al modelo, pendiente definirlos con Alison ------
# ----------------------------------------------------------------
# Entradas de usuario
fuentes = st.number_input("Número de fuentes", value=1.0)
error_estandar = st.number_input("Error estándar", value=0.5)
cpi_rezago1 = st.number_input("CPI (rezago 1)", value=50.0)
cpi_rezago2 = st.number_input("CPI (rezago 2)", value=50.0)
delta1 = st.number_input("Delta 1", value=0.0)
flag_fuentes_imputadas = st.selectbox("¿Fuentes imputadas?", [0, 1])
flag_error_imputado = st.selectbox("¿Error imputado?", [0, 1])

if st.button("Predecir"):
    payload = {
        "Sources": fuentes,
        "Standard_error": error_estandar,
        "CPI_Score_lag1": cpi_rezago1,
        "CPI_Score_lag2": cpi_rezago2,
        "delta1": delta1,
        "flag_imputed_Sources": flag_fuentes_imputadas,
        "flag_imputed_SE": flag_error_imputado,
    }
    res = requests.post("http://127.0.0.1:8000/predict", json=payload)
    if res.status_code == 200:
     st.write(res.json())
    else:
        st.error("Error en la predicción")

# ejecutar en terminal:        
# cd "C:/Users/Acer/OneDrive/Escritorio/MINE009_Externado/Seminario_programacion/API_2025/Proyecto_seminario_API/1. APP" 
# streamlit run app.py
# ----------------------------------------------------------------
# Código FastAPI (no tocar) -------------------------------------   
