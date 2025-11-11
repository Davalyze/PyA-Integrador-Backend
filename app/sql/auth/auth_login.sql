SELECT 
    u.id,
    u.username,
    u.nombre,
    u.rol,
    u.empresa_id,
    e.nombre AS empresa_nombre,
    ARRAY_AGG(DISTINCT m.nombre) AS modulos
FROM usuarios u
JOIN empresas e ON u.empresa_id = e.id
LEFT JOIN permisos_usuario p ON p.usuario_id = u.id
LEFT JOIN modulos m ON m.id = p.modulo_id
WHERE u.username = %(username)s
  AND u.password_hash = crypt(%(password)s, u.password_hash)
  AND u.activo = TRUE
GROUP BY u.id, e.nombre;
