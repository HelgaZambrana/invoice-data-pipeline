import os
import csv
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

SAMPLE_FILE = "data/samples/invoice_dirty_bulk.csv"
LOG_FILE = "data/logs/transformations_log.csv"


@pytest.fixture(scope="function", autouse=True)
def clean_log_before_test():
    """
    Limpia el log antes de cada test para asegurar trazabilidad limpia.
    """
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)


def test_upload_endpoint_with_dirty_file():
    """
    Testea el flujo completo:
    - Sube archivo sucio
    - Transforma columnas
    - Inserta en Supabase
    - Genera log
    """
    assert os.path.exists(SAMPLE_FILE), "Missing test sample file"

    with open(SAMPLE_FILE, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("invoice_dirty_bulk.csv", f, "text/csv")}
        )

    # Verificar respuesta del backend
    assert response.status_code == 200, f"Unexpected status: {response.status_code}"
    data = response.json()

    assert data["rows_inserted"] >= 1, "No rows inserted"
    assert "product" in data["columns"]
    assert isinstance(data["preview"], list)
    assert len(data["preview"]) >= 1


def test_transformation_log_created_and_populated():
    """
    Verifica que el archivo de log fue creado con encabezado y contenido.
    """
    assert os.path.exists(LOG_FILE), "Log file not created"

    with open(LOG_FILE, newline='', encoding="utf-8") as f:
        reader = list(csv.reader(f))

    assert len(reader) > 1, "Log file has no data rows"
    assert reader[0] == ["timestamp", "row_idx", "column", "original", "transformed"], "Log header incorrect"