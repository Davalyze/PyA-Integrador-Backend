from app.db.sqlserver_oficial import SQLServerOficial
from app.db.sqlserver_remisiones import SQLServerRemisiones
from app.db.postgres_manager import PostgresManager

db_ofi = SQLServerOficial()
db_rem = SQLServerRemisiones()



def get_pedidos_por_aprobar():
    db_ofi = SQLServerOficial()
    db_rem = SQLServerRemisiones()

    try:
        # Ejecutar en ambas bases
        res_ofi = db_ofi.execute_query_from_file("pedidos/get_pedidos.sql")
        res_rem = db_rem.execute_query_from_file("pedidos/get_pedidos.sql")

        # Agregar el campo "origen"
        for r in res_ofi:
            r["origen"] = "FE"

        for r in res_rem:
            r["origen"] = "VARIEDADES"

        # Concatenar resultados
        combined = res_rem + res_ofi
        return combined

    finally:
        db_ofi.close()
        db_rem.close()

def get_total_cartera():
    db_ofi = SQLServerOficial()
    db_rem = SQLServerRemisiones()

    try:
        # Ejecutar en ambas bases
        res_ofi = db_ofi.execute_query_from_file("cartera/get_total_cartera.sql")
        res_rem = db_rem.execute_query_from_file("cartera/get_total_cartera.sql")
        combined = res_rem + res_ofi
        return combined

    finally:
        db_ofi.close()
        db_rem.close()
        
        
def get_detalle_pedido(numero_documento: int, origen: str):
    db = SQLServerOficial() if origen == "FE" else SQLServerRemisiones()

    try:
        return db.execute_query_from_file(
    "pedidos/get_pedidos_items.sql",(numero_documento,))   # ← DEBE SER UNA TUPL
    finally:
        db.close()


    
def get_pedidos_por_gestionar():
    db_ofi = SQLServerOficial()
    db_rem = SQLServerRemisiones()

    try:
        # Ejecutar en ambas bases
        res_ofi = db_ofi.execute_query_from_file("pedidos/get_pedidos_por_gestionar.sql")
        res_rem = db_rem.execute_query_from_file("pedidos/get_pedidos_por_gestionar.sql")

        # Agregar el campo "origen"
        for r in res_ofi:
            r["origen"] = "FE"

        for r in res_rem:
            r["origen"] = "VARIEDADES"

        # Concatenar resultados
        combined = res_rem + res_ofi
        return combined
    finally:
        db_ofi.close()
        db_rem.close()
    
    
def get_cartera_by_cliente(cliente):
    db_ofi = SQLServerOficial()
    db_rem = SQLServerRemisiones()

    try:
        # Ejecutar en ambas bases
        res_ofi = db_ofi.execute_query_from_file("cartera/get_cartera_by_cliente.sql",(cliente,))
        res_rem = db_rem.execute_query_from_file("cartera/get_cartera_by_cliente.sql",(cliente,))

        # Agregar el campo "origen"
        for r in res_ofi:
            r["origen"] = "FE"

        for r in res_rem:
            r["origen"] = "VARIEDADES"

        # Concatenar resultados
        combined = res_rem + res_ofi
        return combined

    finally:
        db_ofi.close()
        db_rem.close()
        
        
def insert_pedido_enc(numero_pedido: int, origen: str):
    pg = PostgresManager()
    try:
        sql = """
            INSERT INTO pedidos_enc (numero_pedido, origen, estado, updated_at)
            VALUES (%s, %s, 'APROBADO', NOW())
        """
        pg.execute_non_query(sql, (numero_pedido, origen))
        return {"numero_pedido": numero_pedido, "origen": origen, "estado": "APROBADO"}
    finally:
        pg.close()

def insert_pedido_det(
    origen: str,
    numero_pedido: int,
    codigo_producto: str,
    usuario: str | None = None,
    observacion: str | None = None,
    ):
    pg = PostgresManager()
    try:
        sql = """
            INSERT INTO pedidos_det (
                origen,
                numero_pedido,
                codigo_producto,
                cantidad_sacada,
                cantidad_empacada,
                numero_de_caja,
                observacion,
                usuario,
                updated_at
            )
            VALUES (%s, %s, %s, NULL, NULL, NULL, %s, %s, NOW());
        """
        pg.execute_non_query(
            sql,
            (origen, numero_pedido, codigo_producto, observacion, usuario)
        )
    finally:
        pg.close()



def get_pedidos_estados():
    pg = PostgresManager()
    try:
        rows = pg.execute_query_from_file("pedidos_postgres/get_pedidos_estados.sql")
        return rows
    finally:
        pg.close()





def get_pedido_items_sacar(numero_documento: int, origen: str):
    db = SQLServerOficial() if origen == "FE" else SQLServerRemisiones()

    try:
        rows = db.execute_query_from_file(
    "pedidos/get_pedidos_items_sacar.sql",(numero_documento,))   
        for r in rows:
            r["origen"] = origen

        return rows
    finally:
        db.close()


def get_cantidad_sacada(numero: int,origen: str ):
    pg = PostgresManager()
    try:
        rows = pg.execute_query_from_file(
            "pedidos_postgres/get_cantidad_sacada.sql",
            {"origen": origen, "numero": numero})
        return rows
    finally:
        pg.close()
        
        
def update_pedido_estado(numero_pedido, origen, nuevo_estado):
    pg = PostgresManager()
    try:
        sql = """
            UPDATE pedidos_enc
            SET estado = %s, updated_at = NOW()
            WHERE numero_pedido = %s AND origen = %s
        """
        pg.execute_non_query(sql, (nuevo_estado, numero_pedido, origen))
    finally:
        pg.close()



def update_cantidad_sacada(numero_pedido, origen, referencia, cantidad_sacada, observacion=None):
    pg = PostgresManager()
    try:
        sql = """
        UPDATE pedidos_det
        SET cantidad_sacada = %(cantidad_sacada)s,
            observacion = %(observacion)s,
            updated_at = NOW()
        WHERE numero_pedido = %(numero_pedido)s
        AND origen = %(origen)s
        AND codigo_producto = %(referencia)s;
        """
        params = {
            "cantidad_sacada": cantidad_sacada,
            "observacion": observacion,
            "numero_pedido": numero_pedido,
            "origen": origen,
            "referencia": referencia
        }
        pg.execute_non_query(sql, params)
    finally:
        pg.close()
