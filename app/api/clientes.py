from fastapi import APIRouter, Query
from typing import Optional
from app.services import clientes as svc_clientes

router = APIRouter()

@router.get("/", summary="Lista los clientes ")
def listar_clientes(
):
    """
    Endpoint para obtener la lista de clientes.
    Parámetros:
        - nit (str, opcional): Filtro por NIT (LIKE).
        - nombre (str, opcional): Filtro por Nombre (LIKE).
    """
    return {"clientes": svc_clientes.listar_clientes()}