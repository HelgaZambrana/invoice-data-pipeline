import os
import csv
from datetime import datetime

LOG_PATH = "data/logs/transformations_log.csv"
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def log_transformation(row_idx: int, column: str, original: str, transformed: str):
    """
    Guarda en archivo CSV una transformación aplicada a un valor.
    """
    with open(LOG_PATH, mode="a", newline="", encoding="utf-8") as log_file:
        writer = csv.writer(log_file)
        writer.writerow([
            datetime.now().isoformat(),
            row_idx,
            column,
            original,
            transformed
        ])