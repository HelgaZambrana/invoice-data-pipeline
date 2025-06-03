import pandas as pd
from app.services.validator import normalize_columns

def standardize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica normalización de columnas y cualquier transformación de negocio.
    """
    df.columns = normalize_columns(df.columns.tolist())

    # Agregar transformaciones necesarias, como: convertir tipos de datos, valores nulos, limpiar texto, etc.

    return df
