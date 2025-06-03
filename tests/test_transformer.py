import os
import pandas as pd
from app.services.transformer import standardize_dataframe

DATA_DIR = "data/samples"
DEBUG = os.getenv("DEBUG_TESTS", "false").lower() == "true"

def load_sample_dataframe(filename: str) -> pd.DataFrame:
    """
    Carga un archivo CSV o XLSX de la carpeta de ejemplos y devuelve un DataFrame.
    """
    path = os.path.join(DATA_DIR, filename)
    assert os.path.exists(path), f"File not found: {path}"

    if filename.endswith(".csv"):
        return pd.read_csv(path)
    elif filename.endswith((".xls", ".xlsx")):
        return pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file format: {filename}")


def test_standardize_dataframe_sample():
    """
    Verifica que los datos cargados desde el archivo sample sean transformados correctamente.
    Admite archivos .csv y .xlsx.
    """
    # CAMBIAR ACÁ para testear distintos formatos
    sample_file = "invoice_dirty_sample.csv"  # o "invoice_dirty_sample.xlsx"

    df = load_sample_dataframe(sample_file)

    if DEBUG:
        print("\nBefore cleaning:")
        print(df)

    df_transformed = standardize_dataframe(df)

    if DEBUG:
        print("\nAfter cleaning:")
        print(df_transformed)

    # Verificaciones
    assert "product" in df_transformed.columns
    assert "customer" in df_transformed.columns
    assert df_transformed["product"].str.contains(" ").sum() == 0, "Found unstripped spaces in 'product'"
    assert df_transformed["customer"].str.contains("  ").sum() == 0, "Customer names not properly stripped"
    assert pd.api.types.is_float_dtype(df_transformed["price"])
    assert pd.api.types.is_integer_dtype(df_transformed["quantity"])