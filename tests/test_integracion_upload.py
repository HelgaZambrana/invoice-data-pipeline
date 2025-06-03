import os
import csv
import psycopg2
import pytest
from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv
from datetime import datetime

# Inicializa variables y cliente
load_dotenv()
client = TestClient(app)

SAMPLE_FILE = "data/samples/invoice_dirty_bulk.csv"
LOG_FILE = "data/logs/transformations_log.csv"
APP_LOG_FILE = "logs/app.log"
EXPECTED_ROWS = 100  # Comprobar que el archivo de test tenga esta cantidad de rows

@pytest.fixture(scope="function", autouse=True)
def clean_logs_before_test():
    """
    Elimina logs antes de cada test.
    """
    for path in [LOG_FILE, APP_LOG_FILE]:
        if os.path.exists(path):
            os.remove(path)


def test_upload_and_integration_flow():
    """
    Test de integración completo:
    - Carga archivo
    - Verifica respuesta
    - Verifica log de transformaciones
    - Verifica inserción en base de datos
    - Verifica log general
    """
    assert os.path.exists(SAMPLE_FILE), "Missing test sample file"

    # --- 1. Subir archivo
    with open(SAMPLE_FILE, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": (os.path.basename(SAMPLE_FILE), f, "text/csv")}
        )

    assert response.status_code == 200, f"Unexpected status: {response.status_code}"
    data = response.json()

    assert data["rows_inserted"] == EXPECTED_ROWS
    assert "product" in data["columns"]
    assert isinstance(data["preview"], list)
    assert len(data["preview"]) > 0

    # --- 2. Verificar log de transformaciones
    assert os.path.exists(LOG_FILE), "Transformation log not found"

    with open(LOG_FILE, newline='', encoding="utf-8") as f:
        reader = list(csv.reader(f))
        assert reader[0] == ["timestamp", "row_idx", "column", "original", "transformed"]
        assert len(reader) > 1, "Transformation log has no data"

    # --- 3. Verificar que se insertaron en Supabase/PostgreSQL
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM invoices")
    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    assert count == EXPECTED_ROWS, f"Expected {EXPECTED_ROWS} rows in DB, found {count}"

    # --- 4. Verificar log general
    assert os.path.exists(APP_LOG_FILE), "Application log not found"

    with open(APP_LOG_FILE, "r", encoding="utf-8") as log_file:
        logs = log_file.read()
        assert "invoices inserted into the database" in logs
        assert str(EXPECTED_ROWS) in logs