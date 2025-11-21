SELECT 
    mov.ka_nl_movimiento AS ka_nl_movimiento,
    fuente.k_sc_codigo_fuente AS fuente,
    mov.n_numero_documento AS numero,
    mov.d_fecha_documento AS fecha,
    ter.sc_nombre AS cliente,
    arti.k_sc_codigo_articulo AS referencia,
    SUM(mov_items.n_cantidad) AS saldo,
    CASE 
        WHEN modx.ddt_fecha_autorizacion IS NULL 
            THEN 'Pendiente aprobacion'
        ELSE CONVERT(VARCHAR(20), CONVERT(DATE, modx.ddt_fecha_autorizacion))
    END AS fecha_autorizacion
FROM movimientos as mov WITH (NOLOCK)
INNER JOIN fuentes as fuente WITH (NOLOCK) ON mov.ka_ni_fuente = fuente.ka_ni_fuente
INNER JOIN movimientos_items as mov_items WITH (NOLOCK) ON mov.ka_nl_movimiento = mov_items.ka_nl_movimiento
INNER JOIN terceros as ter WITH (NOLOCK) ON mov.ka_nl_tercero = ter.ka_nl_tercero
INNER JOIN articulos as arti WITH (NOLOCK) ON mov_items.ka_nl_articulo = arti.ka_nl_articulo
INNER JOIN movimientos_facturas as mov_fac WITH (NOLOCK) ON mov.ka_nl_movimiento = mov_fac.ka_nl_movimiento
INNER JOIN saldos_pedidos as saldo WITH (NOLOCK) ON mov_items.ka_nl_movimiento_item = saldo.ka_nl_movimiento_item
LEFT JOIN movimientos_otros_datos as modx WITH (NOLOCK) ON modx.ka_nl_movimiento = mov.ka_nl_movimiento
WHERE fuente.k_sc_codigo_fuente = 'PD'   -- pedidos
   AND saldo.k_sc_periodo = (
        SELECT cal.k_sc_periodo
        FROM calendario cal WITH (NOLOCK)
        WHERE CONVERT(DATE, GETDATE()) BETWEEN cal.dd_fecha_ini AND cal.dd_fecha_fin
    )
    AND saldo.n_saldo_actual > 0       -- pedidos con saldo
    AND mov.sc_anulado = 'N'           -- solo no anulados
GROUP BY
    mov.ka_nl_movimiento,
    fuente.k_sc_codigo_fuente,
    mov.n_numero_documento,
    ter.sc_nombre,
    mov.d_fecha_documento,
    arti.k_sc_codigo_articulo,
    modx.ddt_fecha_autorizacion;
----------------------------------------------------------


select 
mov.ka_nl_movimiento,
mov.n_numero_documento AS numero,
mov.d_fecha_documento AS fecha,
ter.n_nit as nit,
ter.sc_nombre AS cliente,
arti.k_sc_codigo_articulo as referencia,
arti.sc_detalle_articulo as Nombre_Articulo,
mov_items.n_cantidad  as cantidad_pedida
from movimientos mov
INNER JOIN fuentes as fue ON mov.ka_ni_fuente = fue.ka_ni_fuente
INNER JOIN terceros as ter  ON mov.ka_nl_tercero = ter.ka_nl_tercero
INNER JOIN movimientos_items as mov_items ON mov.ka_nl_movimiento = mov_items.ka_nl_movimiento
INNER JOIN articulos as arti ON mov_items.ka_nl_articulo = arti.ka_nl_articulo
where mov.d_fecha_documento > '2025-11-01'
and fue.k_sc_codigo_fuente = 'PD' 
and mov.n_numero_documento = '3377'
AND mov.sc_anulado = 'N'
order by arti.sc_detalle_articulo  asc
--ORDER BY mov.d_fecha_documento DESC


