import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from app.core.config import settings

class PostgresManager:
    def __init__(self):
        """
        Inicializa el gestor sin abrir conexión inmediata.
        """
        load_dotenv()
        self.connection = None

    def _connect(self):
        """
        Crea la conexión si no existe o está cerrada.
        Usa las credenciales de Postgres definidas en .env.docker
        """
        if self.connection is None or self.connection.closed:
            self.connection = psycopg2.connect(
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT,
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                dbname=settings.POSTGRES_DB,
                cursor_factory=RealDictCursor
            )

    def _read_sql(self, relative_path: str) -> str:
        """
        Lee un archivo .sql desde la carpeta app/sql/.
        """
        base_path = os.path.join(os.path.dirname(__file__), "..", "sql")
        sql_path = os.path.join(base_path, relative_path)

        if not os.path.exists(sql_path):
            raise FileNotFoundError(f"No existe la consulta SQL: {sql_path}")

        with open(sql_path, "r", encoding="utf-8") as f:
            return f.read()

    def execute_query(self, sql: str, params: dict | None = None):
        """
        Ejecuta un SELECT y retorna lista de diccionarios.
        """
        self._connect()
        with self.connection.cursor() as cur:
            cur.execute(sql, params or {})
            rows = cur.fetchall()
            return rows

    def execute_query_from_file(self, relative_path: str, params: dict | None = None):
        """
        Ejecuta un SELECT desde un archivo SQL.
        """
        sql = self._read_sql(relative_path)
        return self.execute_query(sql, params)

    def execute_non_query(self, sql: str, params: dict | None = None):
        """
        Ejecuta un INSERT, UPDATE o DELETE.
        """
        self._connect()
        with self.connection.cursor() as cur:
            cur.execute(sql, params or {})
            self.connection.commit()

    def execute_non_query_from_file(self, relative_path: str, params: dict | None = None):
        """
        Ejecuta un INSERT/UPDATE/DELETE desde un archivo SQL.
        """
        sql = self._read_sql(relative_path)
        self.execute_non_query(sql, params)

    def close(self):
        """
        Cierra la conexión activa.
        """
        if self.connection and not self.connection.closed:
            self.connection.close()
            self.connection = None
