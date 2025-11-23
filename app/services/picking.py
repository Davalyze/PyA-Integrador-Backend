from app.crud import picking as crud_picking
from app.services import a_transformer as transformer 
from app.db.azure_connection import AzureBlobService
azure = AzureBlobService()
def listar_pedidos():
    """
    Retorna:
      - pedidos por aprobar
      - pedidos aprobados o en estado 'SACAR'
    Maneja correctamente dataframes vacíos y evita errores.
    """

    # ============================
    # 🔹 PEDIDOS ERP
    # ============================
    rows_pedidos = crud_picking.get_pedidos_por_aprobar()
    df = transformer.sql_to_df(rows_pedidos)

    if df.empty:
        return [], []  # Nada de nada

    # Ordenar por fecha si existe
    if "fecha" in df.columns:
        df.sort_values(by=["fecha"], ascending=True, inplace=True)

    # ============================
    # 🔹 CARTERA
    # ============================
    rows_cartera = crud_picking.get_total_cartera()
    df_cartera = transformer.sql_to_df(rows_cartera)

    if not df_cartera.empty:
        df_cartera = (
            df_cartera.groupby("nit")[["total_saldo", "total_vencido"]]
            .sum()
            .reset_index()
        )
        df = df.merge(df_cartera, on="nit", how="left")
    else:
        df["total_saldo"] = 0
        df["total_vencido"] = 0

    # ============================
    # 🔹 ESTADOS
    # ============================
    rows_estados = crud_picking.get_pedidos_estados()
    df_estados = transformer.sql_to_df(rows_estados)

    if not df_estados.empty:
        df = df.merge(df_estados, on=["origen", "numero_documento"], how="left")
    else:
        df["estado"] = None

    # ============================
    # 🔹 Separar listas
    # ============================

    # Pedidos sin aprobar = sin estado
    df_sin_aprobar = df[df["estado"].isna()].copy()

    # Pedidos aprobados o sacando
    df_sacar = df[df["estado"].isin(["APROBADO", "SACAR"])].copy()
    print(df_sacar)
    print('pene')
    # ============================
    # 🔹 Convertir a listas
    # ============================
    rows_sin_aprobar = transformer.df_to_dict(df_sin_aprobar)
    rows_sacar = transformer.df_to_dict(df_sacar)

    return rows_sin_aprobar, rows_sacar



def pedido_details(numero_documento: int, origen: str):
    """
    Lógica de negocio para obtener los detalles de un pedido.
    """
    rows = crud_picking.get_detalle_pedido(numero_documento, origen)
    return rows

def listar_pedidos_por_gestionar():
    """
    Lógica de negocio para listar clientes.
    """
    rows = crud_picking.get_pedidos_por_gestionar()
    
    return rows



def cartera_by_cliente(cliente):
    """
    Lógica de negocio para obtener los detalles de un pedido.
    """
    rows = crud_picking.get_cartera_by_cliente(cliente)
    df= transformer.sql_to_df(rows)

    
    return rows

def aprobar_pedido(numero_pedido: int, origen: str, detalles):
    enc = crud_picking.insert_pedido_enc(numero_pedido, origen)

    for d in detalles:
        crud_picking.insert_pedido_det(
            origen=origen,
            numero_pedido=numero_pedido,
            codigo_producto=d.codigo_producto
        )

    return {"encabezado": enc, "total_detalles": len(detalles)}



def pedido_details_sacar(numero_documento: int, origen: str):
    """
    Lógica de negocio para obtener los detalles de un pedido.
    """
    rows_pedido= crud_picking.get_pedido_items_sacar(numero_documento, origen)
    df_pedido= transformer.sql_to_df(rows_pedido)
    rows_cantidad_sacada= crud_picking.get_cantidad_sacada(numero_documento, origen)
    df_cantidad_sacada= transformer.sql_to_df(rows_cantidad_sacada)
    df_pedido= df_pedido.merge( df_cantidad_sacada, on=['origen','numero_documento','referencia'], how='left')
    if 'blob_name' in df_pedido.columns:
        df_pedido['imagen_url'] = df_pedido['blob_name'].apply(
            lambda x: azure.build_blob_url(x) if x else None
        )
    else:
        df_pedido['imagen_url'] = None
    df_pedido['cantidad_sacada'] = df_pedido['cantidad_sacada'].fillna(0)
    rows = transformer.df_to_dict(df_pedido)
    return rows


def update_estado(numero_pedido: int, origen: str, nuevo_estado: str):
    """
    Lógica de negocio para actualizar el estado de un pedido.
    """
    return crud_picking.update_pedido_estado(numero_pedido, origen, nuevo_estado)




def actualizar_cantidad_sacada(
    numero_pedido: int,
    origen: str,
    referencia: str,
    cantidad_sacada: int,
    observacion: str | None = None,
):
    """
    Actualiza la cantidad sacada y la observación en pedidos_det.
    """
    crud_picking.update_cantidad_sacada(
        numero_pedido=numero_pedido,
        origen=origen,
        referencia=referencia,
        cantidad_sacada=cantidad_sacada,
        observacion=observacion,   # ⬅ se envía al CRUD
    )


