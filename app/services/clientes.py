from app.crud import clientes as crud_clientes
from app.services import a_transformer as transformer 
def listar_clientes():
    """
    Lógica de negocio para listar clientes.
    """
    rows = crud_clientes.get_pedidos_por_aprobar()
    return rows