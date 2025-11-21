SELECT
	ter.n_nit as nit,
	ter.sc_nombre AS cliente,
	mov.n_numero_documento AS numero_documento,
    arti.k_sc_codigo_articulo AS referencia,
    arti.sc_detalle_articulo AS nombre_articulo,
    mov_items.n_cantidad AS cantidad_pedida
FROM movimientos mov
INNER JOIN fuentes AS fue ON mov.ka_ni_fuente = fue.ka_ni_fuente
INNER JOIN movimientos_items AS mov_items ON mov.ka_nl_movimiento = mov_items.ka_nl_movimiento
INNER JOIN articulos AS arti ON mov_items.ka_nl_articulo = arti.ka_nl_articulo
INNER JOIN terceros as ter  ON mov.ka_nl_tercero = ter.ka_nl_tercero
WHERE fue.k_sc_codigo_fuente = 'PD'
  AND mov.n_numero_documento = ?
  AND mov.sc_anulado = 'N'
ORDER BY arti.sc_detalle_articulo ASC;