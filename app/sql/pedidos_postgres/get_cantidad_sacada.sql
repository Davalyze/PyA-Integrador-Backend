select 
p.origen,
p.numero_pedido as numero_documento,
p.codigo_producto as referencia,
p.cantidad_sacada,
t.blob_name,
p.observacion
from pedidos_det as p
left join producto_imagenes t on t.codigo_sis = p.codigo_producto
WHERE origen = %(origen)s 
AND numero_pedido = %(numero)s
and t.es_principal = True;