import pandas as pd
import psycopg2
from app.core.config import settings
from app.core.logger import logger

def insert_invoices(df: pd.DataFrame):
    """
    Insertar DataFrame en la tabla 'invoices' de PostgreSQL.
    """

    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        cur = conn.cursor()

        # Insertar fila por fila (ver de optimizar con COPY o executemany)
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO invoices (product, price, quantity, customer)
                VALUES (%s, %s, %s, %s)
            """, (
                row["product"],
                row["price"],
                int(row["quantity"]),
                row["customer"]
            ))

        conn.commit()
        cur.close()
        conn.close()

        logger.info(f"{len(df)} invoices inserted into the database.")
        return {"message": "Invoices inserted successfully", "rows": len(df)}

    except Exception as e:
        return {"error": str(e)}