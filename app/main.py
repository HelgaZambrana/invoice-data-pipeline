from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Invoice Data Pipeline API",
    description="Subida y transformación inicial de archivos de facturas",
    version="0.1.0"
)

# Incluir rutas
app.include_router(router)