import os
import pandas as pd
from app.services.validator import validate_required_columns, normalize_columns, REQUIRED_COLUMNS

DATA_DIR = "data/samples"


def load_csv_as_dataframe(path: str) -> pd.DataFrame:
    """Carga un archivo CSV y normaliza sus columnas."""
    assert os.path.exists(path), f"File not found: {path}"
    df = pd.read_csv(path)
    df.columns = normalize_columns(df.columns.tolist())
    return df


def test_valid_invoice_file():
    """
    Verifica que el archivo válido no tenga columnas faltantes.
    """
    df = load_csv_as_dataframe(f"{DATA_DIR}/invoice_demo.csv")

    missing = validate_required_columns(df)

    print("\n test_valid_invoice_file")
    print(f"Columns found: {set(df.columns)}")
    print(f"Missing columns: {missing}")

    assert missing == set(), f"Expected no missing columns, but got: {missing}"


def test_invalid_invoice_file():
    """
    Verifica que un archivo con columnas faltantes sea detectado correctamente.
    """
    df = load_csv_as_dataframe(f"{DATA_DIR}/invoice_invalid.csv")

    missing = validate_required_columns(df)

    present_columns = set(df.columns)
    expected_missing = REQUIRED_COLUMNS - present_columns

    print("\n test_invalid_invoice_file")
    print(f"Columns present: {present_columns}")
    print(f"Missing columns detected: {missing}")
    print(f"Expected missing columns: {expected_missing}")

    assert missing == expected_missing, f"Expected missing: {expected_missing}, got: {missing}"