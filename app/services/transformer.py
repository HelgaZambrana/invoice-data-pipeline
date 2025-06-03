import pandas as pd
from app.services.validator import normalize_columns

def standardize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica normalización de columnas y transformaciones necesarias:
    - Normaliza nombres de columnas
    - Limpia espacios en blanco y capitaliza texto
    - Convierte tipos de datos
    - Redondea precios
    """

    # Normalizar nombres de columnas
    df.columns = normalize_columns(df.columns.tolist())

    # Transformaciones básicas por columna
    df["product"] = df["product"].astype(str).str.strip().str.lower()
    df["customer"] = df["customer"].astype(str).str.strip().str.title()
    df["price"] = df["price"].astype(float).round(2)
    df["quantity"] = df["quantity"].astype(int)

    return df