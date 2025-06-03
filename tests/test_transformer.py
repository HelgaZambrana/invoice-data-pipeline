import os
import pandas as pd
from app.services.transformer import standardize_dataframe

DATA_DIR = "data/samples"

def load_sample_dataframe(filename: str) -> pd.DataFrame:
    """
    Carga un archivo CSV de la carpeta de ejemplos y devuelve un DataFrame.
    """
    path = os.path.join(DATA_DIR, filename)
    assert os.path.exists(path), f"File not found: {path}"
    return pd.read_csv(path)


def test_standardize_dataframe_sample():
    """
    Verifica que los datos cargados desde el archivo sample sean transformados correctamente.
    """
    df = load_sample_dataframe("invoice_dirty_sample.csv")  # ← Este archivo lo podés crear con datos sucios
    df_transformed = standardize_dataframe(df)

    assert "product" in df_transformed.columns
    assert "customer" in df_transformed.columns
    assert df_transformed["product"].str.contains(" ").sum() == 0, "Found unstripped spaces in 'product'"
    assert df_transformed["customer"].str.contains("  ").sum() == 0, "Customer names not properly stripped"
    assert pd.api.types.is_float_dtype(df_transformed["price"])
    assert pd.api.types.is_integer_dtype(df_transformed["quantity"])
