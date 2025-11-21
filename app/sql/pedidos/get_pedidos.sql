select 
mov.n_numero_documento AS numero_documento,
mov.d_fecha_documento AS fecha,
ter.n_nit as nit,
ter.sc_nombre AS cliente,
mov.sv_observaciones as observaciones,
ter_v.sc_nombre AS vendedor,
sum(mov_items.n_cantidad ) as Cantidad
from movimientos mov
INNER JOIN fuentes as fue ON mov.ka_ni_fuente = fue.ka_ni_fuente
INNER JOIN terceros as ter  ON mov.ka_nl_tercero = ter.ka_nl_tercero
INNER JOIN movimientos_items AS mov_items ON mov.ka_nl_movimiento = mov_items.ka_nl_movimiento
left join terceros as ter_v on  ter_v.ka_nl_tercero = mov.ka_nl_tercero_vend 
left join documentos_relacionados dr on dr.n_numero_documento_ori = n_numero_documento
where mov.d_fecha_documento >= '2025-11-01'
AND mov.sc_anulado = 'N'
and fue.k_sc_codigo_fuente = 'PD'
and dr.ka_nl_movimiento is null
group by
mov.n_numero_documento,
mov.d_fecha_documento,
ter.n_nit,
ter.sc_nombre,
mov.sv_observaciones,
ter_v.sc_nombre
