import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

def insert_invoices(df: pd.DataFrame):
    """
    Insertar DataFrame en la tabla 'invoices' de PostgreSQL.
    """

    try:
        # Conectar a PostgreSQL (Supabase)
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
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

        return {"message": "Invoices inserted successfully", "rows": len(df)}

    except Exception as e:
        return {"error": str(e)}