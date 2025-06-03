from typing import List, Set
import pandas as pd

# Definimos las columnas requeridas (ya normalizadas)
REQUIRED_COLUMNS = {"producto", "precio", "cantidad", "cliente"}

def normalize_columns(columns: List[str]) -> List[str]:
    """
    Limpia los nombres de columnas para hacerlos comparables:
    - minúsculas
    - sin espacios extra
    - sin tildes ni símbolos especiales
    """
    return [col.strip().lower().replace(" ", "_") for col in columns]

def validate_required_columns(df: pd.DataFrame) -> Set[str]:
    """
    Verifica que las columnas requeridas estén presentes en el DataFrame.
    Devuelve un set de columnas que faltan (si hay).
    """
    normalized_cols = set(normalize_columns(df.columns.tolist()))
    missing = REQUIRED_COLUMNS - normalized_cols
    return missing