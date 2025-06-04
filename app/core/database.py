import psycopg2
from app.core.config import settings


def get_postgres_connection():
    """
    Devuelve una conexión a PostgreSQL/Supabase usando las credenciales del entorno.
    """
    return psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )