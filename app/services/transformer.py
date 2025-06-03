import pandas as pd
from app.services.validator import normalize_columns

def standardize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica normalización de columnas y transformaciones necesarias:
    - Normaliza nombres de columnas
    - Limpia espacios en blanco y capitaliza texto
    - Convierte tipos de datos robustamente
    """

    # Normalizar nombres de columnas
    df.columns = normalize_columns(df.columns.tolist())

    # Limpiar texto
    df["product"] = df["product"].astype(str).str.strip().str.lower()
    df["customer"] = (
        df["customer"]
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.title()
    )

    # Corregir coma decimal en precio y convertir a float
    df["price"] = df["price"].astype(str).str.replace(",", ".", regex=False).astype(float).round(2)


    # Convertir cantidad a entero de forma segura
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)

    return df