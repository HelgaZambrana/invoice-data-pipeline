import os
import csv
from datetime import datetime

LOG_PATH = os.path.join("data", "logs", "transformations_log.csv")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def log_transformation(row_idx: int, column: str, original: str, transformed: str):
    """
    Guarda en archivo CSV una transformación aplicada a un valor.
    Crea encabezados si el archivo está vacío.
    """
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