import os
import csv
from datetime import datetime

# Ruta del log
LOG_PATH = "data/logs/transformations_log.csv"

# Crear carpeta si no existe
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def log_transformation(row_idx: int, column: str, original: str, transformed: str):
    """
    Guarda en archivo CSV una transformación aplicada a un valor.
    Crea encabezados si el archivo está vacío.
    """
    try:
        # Verificar si hay que escribir encabezado
        write_header = not os.path.exists(LOG_PATH) or os.path.getsize(LOG_PATH) == 0

        with open(LOG_PATH, mode="a", newline="", encoding="utf-8") as log_file:
            writer = csv.writer(log_file)

            if write_header:
                writer.writerow(["timestamp", "row_idx", "column", "original", "transformed"])

            writer.writerow([
                datetime.now().isoformat(),
                row_idx,
                column,
                original,
                transformed
            ])
    except Exception as e:
        print(f"[LOGGER ERROR] Could not write transformation log: {e}")
