import pandas as pd
from app.services.validator import normalize_columns
from app.core.logger import log_transformation

def standardize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza columnas y limpia datos para carga segura en base de datos.
    Aplica:
    - Renombrado de columnas
    - Limpieza de espacios en strings
    - Reemplazo de comas decimales por punto en precios
    - Conversión de tipos
    - Logging de transformaciones
    """

    # 1. Normalizar nombres de columnas
    df.columns = normalize_columns(df.columns.tolist())

    # 2. Limpiar columna 'product'
    if "product" in df.columns:
        for idx, val in df["product"].items():
            original = str(val)
            transformed = original.strip().lower()
            if original != transformed:
                log_transformation(idx, "product", original, transformed)
        df["product"] = df["product"].astype(str).str.strip().str.lower()

    # 3. Limpiar columna 'customer'
    if "customer" in df.columns:
        for idx, val in df["customer"].items():
            original = str(val)
            transformed = (
                original.strip()
                .replace("  ", " ")
                .title()
            )
            if original != transformed:
                log_transformation(idx, "customer", original, transformed)
        df["customer"] = (
            df["customer"]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.title()
        )

    # 4. Arreglar columna 'price' (comas → punto)
    if "price" in df.columns:
        for idx, val in df["price"].items():
            original = str(val)
            transformed = original.replace(",", ".")
            if original != transformed:
                log_transformation(idx, "price", original, transformed)
        df["price"] = df["price"].astype(str).str.replace(",", ".", regex=False).astype(float).round(2)

    # 5. Convertir 'quantity' a int
    if "quantity" in df.columns:
        df["quantity"] = df["quantity"].astype(int)

    # Log en consola para debug
    print("\n[Transformer] DataFrame after standardization:")
    print(df.dtypes)
    print(df.head())

    return df