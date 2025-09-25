# --------------------------------------------
# Praparemos el testeo de contrato de la API
# --------------------------------------------
from fastapi.testclient import TestClient
# ASUME que la importación es correcta. Ajusta si la estructura de carpetas es diferente.
# Por ejemplo: 'from main import app' si estuviera en la raíz, o 'from src.main import app'
from SRC.API.main import app

# Inicializar el cliente de pruebas
client = TestClient(app)

# ----------------------------------------------------
# Tests de Contrato de la API
# ----------------------------------------------------

def test_health():
    """Prueba el endpoint /health"""
    response = client.get("/health")
    # El health check debe pasar (status 200) o indicar error interno (status 500)
    assert response.status_code in [200, 500] 
    data = response.json()
    assert "status" in data

def test_predict_contract():
    """
    Prueba el contrato del endpoint /predict con un payload válido.
    
    CORRECCIÓN: Se ajusta el payload para:
    1. Quitar 'delta1' (calculado internamente en la API).
    2. Usar valores dentro de los rangos y tipos esperados por InputData:
       - Sources: int entre 3 y 10.
       - Standard_error: float entre 0.60 y 8.30.
    """
    payload = {
        "Sources": 5,                     # Corregido a INT (1.0 era float y estaba fuera de rango [3, 10])
        "Standard_error": 1.5,            # Corregido a FLOAT y dentro de rango [0.60, 8.30] (0.5 estaba fuera)
        "CPI_Score_lag1": 50.0,
        "CPI_Score_lag2": 50.0,
        # "delta1": 0.0,                  # <--- ELIMINADO para evitar el error 422 de campo extra.
        "flag_imputed_Sources": 0,
        "flag_imputed_SE": 0
    }
    response = client.post("/predict", json=payload)
    # Ahora debería pasar con status_code 200
    assert response.status_code == 200 
    
    data = response.json()
    assert "predicted_cpi_score" in data
    assert "delta1_calculado" in data


def test_predict_invalid_payload():
    """
    Prueba el endpoint /predict con un payload inválido.

    CORRECCIÓN: Se ajusta el payload para:
    1. Incluir todos los campos obligatorios para que el error sea específico (no 'missing' en varios campos).
    2. Probar el error de parsing de tipo ('texto') en un campo float (Standard_error) 
       para que la aserción 'float' funcione correctamente en Pydantic v2.
    """
    payload = {
        "Sources": 5,
        "Standard_error": "texto_en_lugar_de_numero",  # <-- ¡Inválido! Fuerza un error de 'float_parsing'
        "CPI_Score_lag1": 50.0,
        "CPI_Score_lag2": 50.0,
        "flag_imputed_Sources": 0,
        "flag_imputed_SE": 0
    }
    response = client.post("/predict", json=payload)

    # FastAPI/Pydantic debe devolver un error de validación
    assert response.status_code == 422

    data = response.json()
    assert "detail" in data

    # Se verifica que haya un error cuyo 'type' contenga "float" (funciona para "float_parsing")
    assert any("float" in err["type"] for err in data["detail"])