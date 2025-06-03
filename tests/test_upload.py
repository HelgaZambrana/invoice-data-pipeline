from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

def test_upload_csv():
    file_path = "data/samples/invoice_demo.csv"
    assert os.path.exists(file_path), "Sample file not found"

    with open(file_path, "rb") as f:
        response = client.post("/upload", files={"file": ("invoice_demo.csv", f, "text/csv")})

    assert response.status_code == 200
    json = response.json()
    assert "rows_inserted" in json
    assert json["rows_inserted"] > 0
    assert "columns" in json
    assert "preview" in json
