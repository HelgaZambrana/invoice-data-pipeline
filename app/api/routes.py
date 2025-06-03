from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd

from app.services.ingestion import read_file_to_dataframe
from app.services.transformer import standardize_dataframe
from app.services.validator import validate_required_columns
from app.services.loader import insert_invoices

router = APIRouter()

@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...)):
    try:
        # Ingestión: leer archivo a DataFrame
        df: pd.DataFrame = read_file_to_dataframe(file)

        # ✅ Transformación ANTES de validar
        df = standardize_dataframe(df)

        # Validación: verificar columnas requeridas
        missing = validate_required_columns(df)
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing)}"
            )

        # Carga: insertar datos en PostgreSQL/Supabase
        result = insert_invoices(df)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        # Respuesta
        preview = df.head(5).to_dict(orient="records")
        return {
            "filename": file.filename,
            "rows_inserted": result["rows"],
            "columns": df.columns.tolist(),
            "preview": preview
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")