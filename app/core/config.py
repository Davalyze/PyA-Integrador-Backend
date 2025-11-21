from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # SQL Server principal
    MSSQL_DRIVER: str = "ODBC Driver 18 for SQL Server"
    MSSQL_SERVER: str
    MSSQL_PORT: int = 1433
    MSSQL_DB: str
    MSSQL_USER: str
    MSSQL_PASSWORD: str

    # SQL Server remisiones
    MSSQL_DB_REM: str   # <-- la nueva base que agregaste

    # Postgres
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # JWT
    SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXP_HOURS: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
