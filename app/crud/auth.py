from app.db.postgres_manager import PostgresManager

pg = PostgresManager()

import pandas as pd
def login_user(username: str, password: str):
    db = PostgresManager()
    query = db.read_sql_file("auth_login.sql")
    result = db.fetch_one(query, {"username": username, "password": password})
    return result
