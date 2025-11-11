from app.db.connection import DatabaseManager

def get_clientes():
    """
    Ejecuta la consulta de clientes con filtros opcionales por NIT o Nombre.
    Retorna:
        list[dict]: Lista de clientes.
    """
    db = DatabaseManager()
    try:
        return db.execute_query_from_file(
            "clientes/get_v_clientes.sql"
        )
    finally:
        db.close()