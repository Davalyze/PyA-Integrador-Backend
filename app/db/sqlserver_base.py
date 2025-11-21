import os
import pyodbc
from dotenv import load_dotenv
from app.core.config import settings

class SQLServerBase:
    """
    Clase base para manejar conexiones a SQL Server.
    Permite ejecutar queries y leer archivos .sql sin duplicar código.
    """

    def __init__(self, database_name: str):
        load_dotenv()
        self.database_name = database_name
        self.connection = None

    def _connect(self):
        """
        Crea la conexión si no existe o está cerrada.
        """
        if self.connection is None:
            conn_str = (
                f"DRIVER={{{settings.MSSQL_DRIVER}}};"
                f"SERVER={settings.MSSQL_SERVER},{settings.MSSQL_PORT};"
                f"DATABASE={self.database_name};"
                f"UID={settings.MSSQL_USER};PWD={settings.MSSQL_PASSWORD};"
                f"Encrypt=no;TrustServerCertificate=yes;"
            )
            self.connection = pyodbc.connect(conn_str)

    def _read_sql(self, relative_path: str) -> str:
        """
        Lee un archivo .sql desde app/sql/.
        """
        base_path = os.path.join(os.path.dirname(__file__), "..", "sql")
        sql_path = os.path.join(base_path, relative_path)

        if not os.path.exists(sql_path):
            raise FileNotFoundError(f"No existe la consulta SQL: {sql_path}")

        with open(sql_path, "r", encoding="utf-8") as f:
            return f.read()

    def execute_query(self, sql: str, params: tuple | None = None):
        """
        Ejecuta un SELECT y devuelve los resultados como lista de dicts.
        """
        self._connect()
        cursor = self.connection.cursor()
        cursor.execute(sql, params or ())
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        return rows

    def execute_query_from_file(self, relative_path: str, params: tuple | None = None):
        """
        Ejecuta una consulta SQL leída desde un archivo.
        """
        sql = self._read_sql(relative_path)
        return self.execute_query(sql, params)

    def execute_non_query(self, sql: str, params: tuple | None = None):
        """
        Ejecuta INSERT, UPDATE o DELETE.
        """
        self._connect()
        cursor = self.connection.cursor()
        cursor.execute(sql, params or ())
        self.connection.commit()
        cursor.close()

    def close(self):
        """
        Cierra la conexión.
        """
        if self.connection:
            self.connection.close()
            self.connection = None

    def begin_transaction(self):
        self._connect()
        self.connection.autocommit = False

    def commit(self):
        if self.connection:
            self.connection.commit()
            self.connection.autocommit = True

    def rollback(self):
        if self.connection:
            self.connection.rollback()
            self.connection.autocommit = True
