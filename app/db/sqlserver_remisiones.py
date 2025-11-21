from app.db.sqlserver_base import SQLServerBase
from app.core.config import settings

class SQLServerRemisiones(SQLServerBase):
    """
    Conexión a la base de datos de REMISIONES del ERP PyA.
    """
    def __init__(self):
        super().__init__(settings.MSSQL_DB_REM)
