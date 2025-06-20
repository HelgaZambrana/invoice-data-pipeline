import os
import pytest
from fastapi import UploadFile, HTTPException
from starlette.datastructures import UploadFile as StarletteUploadFile
from app.services.ingestion import read_file_to_dataframe

DATA_DIR = "data/samples"

def fake_upload_file_from_path(path: str) -> UploadFile:
    """
    Simula un UploadFile a partir de un archivo real.
    """
    assert os.path.exists(path), f"File not found: {path}"
    file_bytes = open(path, "rb")
    return StarletteUploadFile(filename=os.path.basename(path), file=file_bytes)


def test_read_csv_file_to_dataframe():
    """
    Verifica que un archivo .csv válido se lea correctamente.
    """
    path = f"{DATA_DIR}/invoice_demo.csv"
    upload_file = fake_upload_file_from_path(path)

    df = read_file_to_dataframe(upload_file)

    print("\n CSV content preview:")
    print(df.head())

    assert not df.empty, "CSV DataFrame is empty"
    assert df.shape[0] >= 1


def test_read_xlsx_file_to_dataframe():
    """
    Verifica que un archivo .xlsx válido se lea correctamente.
    """
    path = f"{DATA_DIR}/invoice_demo.xlsx"
    upload_file = fake_upload_file_from_path(path)

    df = read_file_to_dataframe(upload_file)

    print("\n XLSX content preview:")
    print(df.head())

    assert not df.empty, "XLSX DataFrame is empty"
    assert df.shape[0] >= 1


def test_invalid_file_type_raises_exception():
    """
    Verifica que un archivo con extensión no soportada (ej: .txt) genere error.
    """
    path = f"{DATA_DIR}/invalid_file.txt"
    upload_file = fake_upload_file_from_path(path)

    with pytest.raises(HTTPException) as excinfo:
        read_file_to_dataframe(upload_file)

    detail = str(excinfo.value.detail).lower()
    print("\n Invalid file error message:")
    print(detail)

    assert "unsupported" in detail or "not supported" in detail