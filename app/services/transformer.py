import pandas as pd
from app.services.validator import normalize_columns

def standardize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza columnas y limpia datos para carga segura en base de datos.
    Aplica:
    - Renombrado de columnas
    - Limpieza de espacios en strings
    - Reemplazo de comas decimales por punto en precios
    - Conversión de tipos
    """

    # 1. Normalizar nombres de columnas
    df.columns = normalize_columns(df.columns.tolist())

    # 2. Limpiar columna 'product'
    if "product" in df.columns:
        df["product"] = df["product"].astype(str).str.strip().str.lower()

    # 3. Limpiar columna 'customer'
    if "customer" in df.columns:
        df["customer"] = (
            df["customer"]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.title()
        )

    # 4. Arreglar columna 'price' (comas → punto) y convertir a float
    if "price" in df.columns:
        df["price"] = (
            df["price"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .astype(float)
            .round(2)
        )

    # 5. Convertir 'quantity' a int
    if "quantity" in df.columns:
        df["quantity"] = df["quantity"].astype(int)

    # ✅ Log: mostrar preview y tipos
    print("\n[Transformer] DataFrame after standardization:")
    print(df.dtypes)
    print(df.head())

    return df