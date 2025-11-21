from app.db.sqlserver_oficial import SQLServerOficial
from app.db.sqlserver_remisiones import SQLServerRemisiones

db_ofi = SQLServerOficial()
db_rem = SQLServerRemisiones()


def get_clientes():
    """
    Ejecuta la consulta de clientes con filtros opcionales por NIT o Nombre.
    Retorna:
        list[dict]: Lista de clientes.
    """
    
    db_ofi = SQLServerOficial()
    try:
        return db_ofi.execute_query_from_file("clientes/get_v_clientes.sql")
    finally:
        db_ofi.close()