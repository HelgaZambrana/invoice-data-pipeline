from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO
from app.services.validator import validate_required_columns, normalize_columns

router = APIRouter()

@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...)):
    # Validar extensión
    filename = file.filename
    if not filename.endswith((".csv", ".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Archivo no soportado. Debe ser .csv, .xls o .xlsx")

    try:
        # Leer el archivo en memoria como DataFrame
        contents = await file.read()
        file_like = BytesIO(contents)
        
        # Leer con Pandas según el tipo de archivo
        if filename.endswith(".csv"):
            df = pd.read_csv(file_like)
        else:  # Excel
            df = pd.read_excel(file_like)

        # Validar columnas requeridas
        missing = validate_required_columns(df)
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Faltan columnas requeridas: {', '.join(missing)}"
            )

        # Renombrar columnas normalizadas en el DataFrame
        df.columns = normalize_columns(df.columns.tolist())

        # Vista previa de los primeros 5 registros
        preview = df.head(5).to_dict(orient="records")

        return {
            "filename": file.filename,
            "preview": preview,
            "columns": df.columns.tolist()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar archivo: {str(e)}")