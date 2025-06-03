import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_dry_run_only_transforms_and_returns_preview():
    """
    Simula una carga de archivo completa sin insertar en DB (dry_run).
    """
    file_path = "data/samples/invoice_dirty_bulk.csv"
    assert os.path.exists(file_path), "Sample file not found."

    with open(file_path, "rb") as f:
        response = client.post(
            "/upload?dry_run=true",
            files={"file": ("invoice_dirty_bulk.csv", f, "text/csv")}
        )

    assert response.status_code == 200
    data = response.json()

    assert data["dry_run"] is True
    assert "rows_detected" in data
    assert "columns" in data
    assert "preview" in data
    assert data["rows_detected"] == 100