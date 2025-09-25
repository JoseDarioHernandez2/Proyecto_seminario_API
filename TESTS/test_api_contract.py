from fastapi.testclient import TestClient
from src.api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
assert response.status_code == 200
assert response.json() == {"status": "ok"}


def test_predict_contract():
    payload = {
"Sources": 1.0,
"Standard_error": 0.5,
"CPI_Score_lag1": 50.0,
"CPI_Score_lag2": 50.0,
"delta1": 0.0,
"flag_imputed_Sources": 0,
"flag_imputed_SE": 0
}
response = client.post("/predict", json=payload)
assert response.status_code == 200
assert "prediction" in response.json()

# --------------------------------------------
# Levantar la API con Uvicorn
# poetry run uvicorn SRC.API.main:app --reload --host 127.0.0.1 --port 8000
# --------------------------------------------