from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO

from app.services.validator import validate_required_columns, normalize_columns
from app.services.loader import insert_invoices

router = APIRouter()

@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...)):
    # Validar extensión
    filename = file.filename
    
    if not filename.endswith((".csv", ".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Unsupported file format. Must be .csv, .xls, or .xlsx")

    try:
        # Leer el archivo en memoria como DataFrame
        contents = await file.read()
        file_like = BytesIO(contents)
        
        # Leer con Pandas según el tipo de archivo
        if filename.endswith(".csv"):
            df = pd.read_csv(file_like)
        else:  # Excel
            df = pd.read_excel(file_like)

        # Normalizar y validar columnas
        df.columns = normalize_columns(df.columns.tolist())
        missing = validate_required_columns(df)
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing)}"
            )

        # Insertar en PostgreSQL/Supabase
        result = insert_invoices(df)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        # Vista previa de los primeros 5 registros
        preview = df.head(5).to_dict(orient="records")
        return {
            "filename": filename,
            "rows_inserted": result["rows"],
            "columns": df.columns.tolist(),
            "preview": preview
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")