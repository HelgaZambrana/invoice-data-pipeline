from fastapi import APIRouter, UploadFile, File, HTTPException, Query
import pandas as pd

from app.services.ingestion import read_file_to_dataframe
from app.services.transformer import standardize_dataframe
from app.services.validator import validate_required_columns
from app.services.loader import insert_invoices
from app.services.loader import reset_invoices_table
from app.core.config import settings

router = APIRouter()

@router.post("/upload")
async def upload_invoice(
    file: UploadFile = File(...),
    dry_run: bool = Query(False, description="Simula el proceso sin insertar en la base de datos")
):
    try:
        # 1. Leer archivo
        df: pd.DataFrame = read_file_to_dataframe(file)

        # 2. Validar columnas requeridas
        missing = validate_required_columns(df)
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing)}"
            )

        # 3. Transformar
        df = standardize_dataframe(df)

        # 4. Si dry_run está activado, devolver preview sin insertar
        if dry_run:
            return {
                "filename": file.filename,
                "dry_run": True,
                "columns": df.columns.tolist(),
                "rows_detected": len(df),
                "preview": df.head(5).to_dict(orient="records")
            }

        # 5. Insertar en la base de datos
        result = insert_invoices(df)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        return {
            "filename": file.filename,
            "dry_run": False,
            "rows_inserted": result["rows"],
            "columns": df.columns.tolist(),
            "preview": df.head(5).to_dict(orient="records")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# ----------------------------------------------------------------------
# Endpoint extra solo disponible si ENABLE_DEV_ENDPOINTS=true en .env
# ----------------------------------------------------------------------
if settings.ENABLE_DEV_ENDPOINTS:
    @router.post("/reset")
    async def reset_table():
        try:
            reset_invoices_table()
            return {"message": "Tabla 'invoices' vaciada correctamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al resetear tabla: {str(e)}")
