import logging
import os

# Crear carpeta de logs si no existe
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Crear logger explícito (sin usar root logger)
logger = logging.getLogger("invoice_pipeline")
logger.setLevel(logging.INFO)

# Evitar múltiples handlers duplicados si se recarga el módulo
if not logger.hasHandlers():
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    # Archivo
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Consola
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
