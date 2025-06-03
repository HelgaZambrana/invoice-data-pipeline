import pandas as pd
from io import BytesIO
from fastapi import UploadFile, HTTPException

def read_file_to_dataframe(file: UploadFile) -> pd.DataFrame:
    """
    Convierte un archivo recibido vía UploadFile en un DataFrame,
    detectando el formato automáticamente.
    """
    filename = file.filename
    try:
        contents = file.file.read()
        file_like = BytesIO(contents)

        if filename.endswith(".csv"):
            df = pd.read_csv(file_like)
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_like)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format.")
        
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")