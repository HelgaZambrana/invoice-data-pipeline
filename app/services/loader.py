import pandas as pd
from app.core.config import settings
from app.core.logger import logger  # Logger global
from app.core.database import get_postgres_connection


def insert_invoices(df: pd.DataFrame):
    """
    Inserta un DataFrame en la tabla 'invoices' de PostgreSQL.
    """
    try:
        conn = get_postgres_connection()
        cur = conn.cursor()

        for _, row in df.iterrows():
            cur.execute(
                """
                INSERT INTO invoices (product, price, quantity, customer)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    row["product"],
                    row["price"],
                    int(row["quantity"]),
                    row["customer"]
                )
            )

        conn.commit()
        cur.close()
        conn.close()

        logger.info(f"{len(df)} invoices inserted into the database.")
        return {"message": "Invoices inserted successfully", "rows": len(df)}

    except Exception as e:
        logger.error(f"Error inserting invoices: {str(e)}")
        return {"error": str(e)}


def reset_invoices_table():
    """
    Vacia la tabla 'invoices' y reinicia el contador de ID.
    Solo debe usarse en entorno de desarrollo/test.
    """
    try:
        conn = get_postgres_connection()
        cur = conn.cursor()

        cur.execute("TRUNCATE TABLE invoices RESTART IDENTITY")
        conn.commit()
        cur.close()
        conn.close()

        logger.info("Tabla 'invoices' vaciada con éxito.")

    except Exception as e:
        logger.error(f"Error al vaciar la tabla 'invoices': {str(e)}")
        raise