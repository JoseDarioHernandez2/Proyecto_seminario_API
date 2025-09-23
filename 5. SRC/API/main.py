from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os


app = FastAPI(title="Proyecto Final MINE IX API")


# Ruta al modelo (ajustar cuando se exporte)
MODEL_PATH = os.path.join("models", "rf_oob.pkl")


# Cargar modelo en startup
model = None
preprocess = None


@app.on_event("startup")
def load_model():
global model, preprocess
if os.path.exists(MODEL_PATH):
model = joblib.load(MODEL_PATH)
# Si el pipeline incluye preprocessing, se carga junto al modelo


class Features(BaseModel):
Sources: float
Standard_error: float
CPI_Score_lag1: float
CPI_Score_lag2: float
delta1: float
flag_imputed_Sources: int
flag_imputed_SE: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(features: Features):
    if model is None:
        return {"error": "Modelo no cargado"}

data = [[
features.Sources,
features.Standard_error,
features.CPI_Score_lag1,
features.CPI_Score_lag2,
features.delta1,
features.flag_imputed_Sources,
features.flag_imputed_SE,
]]
pred = model.predict(data)
proba = model.predict_proba(data).tolist()
return {"prediction": int(pred[0]), "probabilities": proba}