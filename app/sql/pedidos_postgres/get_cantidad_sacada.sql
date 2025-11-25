select 
p.origen,
p.numero_pedido as numero_documento,
p.codigo_producto as referencia,
p.cantidad_sacada,
p.cantidad_empacada,
t.blob_name,
p.observacion,
pe.observacion_sacador as observacion_documento,
pe.observacion_empacador as observacion_empacado,
p.numero_de_caja
from pedidos_det as p
LEFT JOIN pedidos_enc as pe on pe.numero_pedido = p.numero_pedido AND pe.origen = p.origen
left join producto_imagenes t on t.codigo_sis = p.codigo_producto
WHERE p.origen = %(origen)s 
AND p.numero_pedido = %(numero)s
and t.es_principal = True;