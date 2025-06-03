# tests/conftest.py
import os
import pytest

LOG_FILE = "data/logs/transformations_log.csv"

@pytest.fixture(autouse=True)
def clear_log_file_before_tests():
    """
    Borra el contenido del archivo de log antes de cada test.
    """
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.truncate(0)