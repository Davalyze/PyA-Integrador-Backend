from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # SQL Server (ERP PyA)
    MSSQL_DRIVER: str = "ODBC Driver 18 for SQL Server"
    MSSQL_SERVER: str
    MSSQL_PORT: int = 1433
    MSSQL_DB: str
    MSSQL_USER: str
    MSSQL_PASSWORD: str

    # Postgres (base de datos del integrador)
    POSTGRES_HOST: str = "db"  # nombre del servicio en docker-compose
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # 🔐 Seguridad / JWT
    SECRET_KEY: str = "change_me_secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXP_HOURS: int = 12

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
