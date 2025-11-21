select 
origen,
numero_pedido as numero_documento,
codigo_producto as referencia,
cantidad_sacada,
observacion
from pedidos_det
WHERE origen = %(origen)s 
AND numero_pedido = %(numero)s
