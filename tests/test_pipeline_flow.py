import os
import csv
import psycopg2
import pytest
from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv

client = TestClient(app)

SAMPLE_FILE = "data/samples/invoice_dirty_bulk.csv"
LOG_FILE = "data/logs/transformations_log.csv"
EXPECTED_ROWS = 100  # Ajustar según archivo

load_dotenv()

@pytest.fixture(autouse=True)
def clean_log_before_test():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

@pytest.mark.parametrize("dry_run", [True, False])
def test_pipeline_flow(dry_run):
    """
    Testea todo el pipeline con dry_run on/off:
    - Transforma datos sucios
    - Muestra preview y log
    - Inserta o no en DB según bandera
    """
    assert os.path.exists(SAMPLE_FILE), "Missing sample file"

    with open(SAMPLE_FILE, "rb") as f:
        response = client.post(
            f"/upload?dry_run={str(dry_run).lower()}",
            files={"file": ("invoice_dirty_bulk.csv", f, "text/csv")}
        )

    assert response.status_code == 200
    data = response.json()

    # Validaciones comunes
    assert data["rows_inserted"] == EXPECTED_ROWS
    assert "product" in data["columns"]
    assert isinstance(data["preview"], list)
    assert len(data["preview"]) >= 1

    # Validación del log
    assert os.path.exists(LOG_FILE), "Log file not created"
    with open(LOG_FILE, newline='', encoding="utf-8") as f:
        rows = list(csv.reader(f))
        assert len(rows) > 1, "Log has no data"
        assert rows[0] == ["timestamp", "row_idx", "column", "original", "transformed"]

    # Validación de inserción real solo si dry_run=False
    if not dry_run:
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

        assert count == EXPECTED_ROWS, f"Expected {EXPECTED_ROWS}, found {count} in DB"