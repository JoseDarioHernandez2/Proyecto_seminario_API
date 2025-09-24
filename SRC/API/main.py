from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, confloat, conint
import numpy as np
import joblib
import datetime
import os

# ----------------------------
# Inicializar FastAPI
# ----------------------------
app = FastAPI(
    title="API Predicción CPI",
    description="Predice el CPI con modelo de Machine Learning",
    version="1.0"
)

# --------------------------------------------
# CORS (permite conexión desde apps externas)
# -------------------------------------------- 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción limitar a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Cargar modelo entrenado
# ----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "MODELS", "modelo_cpi.pkl")

try:
    model = joblib.load(MODEL_PATH)
    model_type = type(model).__name__
    print(f"✅ Modelo cargado correctamente: {model_type}")
except Exception as e:
    model = None
    model_type = None
    print(f"⚠️ Error cargando modelo desde {MODEL_PATH}: {e}")

# --------------------------------------------
# Definir esquema de entrada con validaciones
# --------------------------------------------
class InputData(BaseModel):
    Sources: conint(ge=3, le=10) = Field(..., description="Número de fuentes (3 a 10)")
    Standard_error: confloat(ge=0.60, le=8.30) = Field(..., description="Error estándar (0.60 a 8.30)")
    CPI_Score_lag1: confloat(ge=1.0, le=100.0) = Field(..., description="CPI Score rezago 1 (2024)")
    CPI_Score_lag2: confloat(ge=1.0, le=100.0) = Field(..., description="CPI Score rezago 2 (2023)")
    flag_imputed_Sources: int = Field(..., description="Indica si se imputaron fuentes (0 o 1)")
    flag_imputed_SE: int = Field(..., description="Indica si se imputó error estándar (0 o 1)")

# ----------------------------
# 0. Endpoint raíz (bienvenida)
# ----------------------------
@app.get("/")
def root():
    return {
        "message": "Bienvenido a la API CPI 🚀",
        "endpoints": {
            "health": "/health",
            "info": "/info",
            "predict": "/predict",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

# ----------------------------
# 1. Endpoint de salud
# ----------------------------
@app.get("/health")
def health():
    if model is None:
        return {"status": "error", "message": "Modelo no cargado"}
    return {"status": "ok", "message": "API funcionando correctamente 🚀"}

# ----------------------------
# 2. Endpoint de info
# ----------------------------
@app.get("/info")
def info():
    return {
        "modelo": model_type if model else "No disponible",
        "features_esperados": [
            "Sources (3-10)",
            "Standard_error (0.60-8.30)",
            "CPI_Score_lag1 (1-100)",
            "CPI_Score_lag2 (1-100)",
            "delta1 (calculado internamente como lag1 - lag2)",
            "flag_imputed_Sources (0 o 1)",
            "flag_imputed_SE (0 o 1)"
        ],
        "ultima_actualizacion": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "descripcion": "Este modelo predice el Índice de Percepción de Corrupción (CPI) para 2025 en función de valores previos y métricas asociadas."
    }

# ----------------------------
# 3. Endpoint de predicción
# ----------------------------
@app.post("/predict")
def predict(data: InputData):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no disponible")

    try:
        # Calcular delta1 automáticamente
        delta1 = data.CPI_Score_lag1 - data.CPI_Score_lag2

        # Convertir a numpy array (ordenado según entrenamiento del modelo)
        X = np.array([[
            data.Sources,
            data.Standard_error,
            data.CPI_Score_lag1,
            data.CPI_Score_lag2,
            delta1,
            data.flag_imputed_Sources,
            data.flag_imputed_SE
        ]])

        # Predicción principal
        prediction = model.predict(X)[0]

        # Probabilidades si el modelo lo permite
        probabilities = None
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(X).tolist()

        return {
            "predicted_cpi_score": float(prediction),
            "delta1_calculado": float(delta1),
            "probabilities": probabilities
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {e}")
