import streamlit as st
import requests

# ----------------------------
# tema oscuro, inputs y botón personalizado
# ----------------------------
st.markdown("""
    <style>
    /* Estilos para el entorno oscuro */
    .stApp {
        background-color: #1A1A1A;
        color: white;
        font-size: 1.1em; /* Aumenta el tamaño de la letra general */
    }
    
    /* Estilos para los títulos y texto */
    h1, h2, h3, h4, h5, h6 {
        color: #7CFC00; /* Verde manzana para los títulos */
    }
    
    /* Nombres de los inputs en blanco y negrilla, emojis más grandes */
    label, .st-ag, .st-bf { 
        color: white !important;
        font-weight: bold;
    }
    label .st-by {
        font-size: 1.5em; /* Aumenta el tamaño de los emojis */
    }

    /* Estilos para el botón de predicción (naranja oscuro) */
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
    
    /* Estilos para los campos de entrada de datos (inputs) */
    .stNumberInput input, .stSelectbox div[role="listbox"] {
        background-color: #262730; /* Color de fondo del input */
        color: #7CFC00; /* Color del texto dentro del input */
        border: 2px solid #7CFC00; /* Borde de color verde manzana */
        border-radius: 5px;
        padding: 5px;
    }

    /* Estilos para las opciones desplegables del selectbox */
    .stSelectbox div[role="listbox"] div[data-testid="stVirtualList"] {
        background-color: #262730 !important;
        border: 1px solid #7CFC00;
    }
    .stSelectbox div[role="listbox"] div[data-testid="stVirtualList"] div[role="option"] {
        color: #7CFC00 !important;
    }

    /* Estilos para la caja de resultados */
    .result-box {
        padding: 20px;
        border-radius: 10px;
        background-color: white; /* Fondo blanco */
        margin-top: 20px;
        font-size: 1.5em; /* Aumenta el tamaño de la letra de la salida */
        font-weight: bold; /* Texto en negrita */
        text-align: center;
        color: black; /* Letra negra */
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Título
# ----------------------------
st.title("📊 APP de Predicción — Random Forest")
st.write("Interfaz gráfica para realizar predicciones con el modelo de **Machine Learning**, elaboró Alison Gamba & Jose Dario Hernandez.")

# ----------------------------
# Entradas de usuario
# ----------------------------
fuentes = st.number_input("🔢 Número de fuentes", value=1.0)
error_estandar = st.number_input("📏 Error estándar", value=0.5)
cpi_rezago1 = st.number_input("📈 CPI (rezago 1)", value=50.0)
cpi_rezago2 = st.number_input("📉 CPI (rezago 2)", value=50.0)
delta1 = st.number_input("Δ Delta 1", value=0.0)
flag_fuentes_imputadas = st.selectbox("⚙️ ¿Fuentes imputadas?", [0, 1])
flag_error_imputado = st.selectbox("⚙️ ¿Error imputado?", [0, 1])

# ----------------------------
# Botón de predicción
# ----------------------------
if st.button("🔮 Predecir"):
    payload = {
        "Sources": fuentes,
        "Standard_error": error_estandar,
        "CPI_Score_lag1": cpi_rezago1,
        "CPI_Score_lag2": cpi_rezago2,
        "delta1": delta1,
        "flag_imputed_Sources": flag_fuentes_imputadas,
        "flag_imputed_SE": flag_error_imputado,
    }

    try:
        res = requests.post("http://127.0.0.1:8000/predict", json=payload)
        if res.status_code == 200:
            prediction = res.json().get("prediction", "Sin resultado")
            st.markdown(f"""
                <div class="result-box">
                    ✅ Predicción del modelo: <span>{prediction}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"❌ Error en la predicción ({res.status_code})")
    except Exception as e:
        st.error(f"⚠️ No se pudo conectar con la API: {e}")