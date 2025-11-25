from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, Query
from typing import Optional
from app.services import picking as svc_picking

router = APIRouter()

@router.get("/por_aprobar", summary="Pedidos por aprobar")
def list_pedidos_por_aprobar():
    """
    Lista los pedidos que están pendientes de aprobación.
    """
    rows,_ ,_= svc_picking.listar_pedidos()
    return {"data": rows}


@router.get("/aprobados", summary="Pedidos aprobados")
def list_pedidos_por_sacar():
    """
    Lista los pedidos que están pendientes de aprobación.
    """
    _,rows,_ = svc_picking.listar_pedidos()
    return {"data": rows}



@router.get("/empaque", summary="Pedidos aprobados")
def list_pedidos_por_empaque():
    """
    Lista los pedidos que están pendientes de aprobación.
    """
    _,_,rows = svc_picking.listar_pedidos()
    return {"data": rows}


@router.get("/detalle")
def detalle_pedido(numero: int, origen: str):
    rows = svc_picking.pedido_details(numero, origen)
    return {"data": rows}

@router.get("/detalle_sacar")
def detalle_pedido(numero: int, origen: str):
    rows = svc_picking.pedido_details_sacar(numero, origen)
    return {"data": rows}




@router.get("/por_gestionar")
def pedidos_por_gestionar():
    rows = svc_picking.listar_pedidos_por_gestionar()
    return {"data": rows}


@router.get("/cartera_cliente")
def cartera_cliente(cliente: str):
    rows = svc_picking.cartera_by_cliente(cliente)
    return {"data": rows}



class DetalleAprobar(BaseModel):
    codigo_producto: str

class PedidoAprobar(BaseModel):
    numero_pedido: int
    origen: str
    detalles: List[DetalleAprobar]


@router.post("/aprobar_pedido")
def aprobar_pedido(payload: PedidoAprobar):
    try:
        result = svc_picking.aprobar_pedido(
            numero_pedido=payload.numero_pedido,
            origen=payload.origen,
            detalles=payload.detalles
        )
        return {"success": True, "message": "Pedido aprobado correctamente", "data": result}
    except Exception as e:
        print("❌ Error aprobando pedido:", e)
        return {"success": False, "message": str(e)}




@router.get("/sacar_pedido")
def detalle_pedido_sacar(numero: int, origen: str):
    rows = svc_picking.pedido_details_sacar(numero, origen)
    print(rows)
    return {"data": rows}



@router.post("/cambiar_estado_sacar")
def cambiar_estado_sacar(data: dict):
    numero = data["numero_pedido"]
    origen = data["origen"]

    # Actualizamos pedidos_enc
    svc_picking.update_estado(numero, origen, "SACAR")

    return {"status": "ok", "estado": "SACAR"}


@router.post("/cambiar_estado_empaque")
def cambiar_estado_empaque(data: dict):
    numero = data["numero_pedido"]
    origen = data["origen"]

    # Actualizamos pedidos_enc
    svc_picking.update_estado(numero, origen, "EMPAQUE")

    return {"status": "ok", "estado": "EMPAQUE"}

@router.post("/cambiar_estado_en_empaque")
def cambiar_estado_empaque(data: dict):
    numero = data["numero_pedido"]
    origen = data["origen"]

    # Actualizamos pedidos_enc
    svc_picking.update_estado(numero, origen, "EN EMPAQUE")
    
    return {"status": "ok", "estado": "EN EMPAQUE"}


class ProductoSacado(BaseModel):
    codigo_producto: str
    cantidad_sacada: int
    observacion: str | None = None   # ← NUEVO CAMPO



class SacarItems(BaseModel):
    numero_pedido: int
    origen: str
    observacion_documento: str | None = None   # ← NUEVO CAMPO
    productos: List[ProductoSacado]
    


@router.post("/guardar_cantidad_sacada")
def guardar_cantidad_sacada(data: SacarItems):
    print("📦 Recibido:", data)

    try:
        # 🔹 1. Guardar la observación general del documento
        if data.observacion_documento is not None:
            svc_picking.actualizar_observacion_documento(
                numero_pedido=data.numero_pedido,
                origen=data.origen,
                observacion=data.observacion_documento
            )

        # 🔹 2. Guardar cantidades y observaciones por producto
        for prod in data.productos:
            svc_picking.actualizar_cantidad_sacada(
                numero_pedido=data.numero_pedido,
                origen=data.origen,
                referencia=prod.codigo_producto,
                cantidad_sacada=prod.cantidad_sacada,
                observacion=prod.observacion,
            )

        return {
            "ok": True,
            "message": "Datos guardados correctamente"
        }

    except Exception as e:
        return {"ok": False, "error": str(e)}




class ProductoEmpacado(BaseModel):
    codigo_producto: str
    cantidad_empacada: int
    observacion: Optional[str] = None
    numero_de_caja: Optional[int] = None   
  # observación del empacador por producto

class EmpaqueItems(BaseModel):
    numero_pedido: int
    origen: str
    observacion_empacador: Optional[str] = None
    productos: List[ProductoEmpacado]


@router.post("/guardar_empaque")
def guardar_empaque(data: EmpaqueItems):
    print("📦 Guardando empaque:", data)

    try:
        # 1️⃣ Guardar observación general del empacador EN encabezado
        if data.observacion_empacador is not None:
            svc_picking.actualizar_observacion_empacador(
                numero_pedido=data.numero_pedido,
                origen=data.origen,
                observacion=data.observacion_empacador
            )

        # 2️⃣ Guardar cantidades, observaciones y número de caja por producto
        for prod in data.productos:
            
            svc_picking.actualizar_cantidad_empacada(
                numero_pedido=data.numero_pedido,
                origen=data.origen,
                referencia=prod.codigo_producto,
                cantidad_empacada=prod.cantidad_empacada,
                observacion=prod.observacion,
                numero_de_caja=prod.numero_de_caja   
            )

        return {
            "ok": True,
            "message": "Empaque guardado correctamente"
        }

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {"ok": False, "error": str(e)}


