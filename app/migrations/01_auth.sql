DROP TABLE IF EXISTS permisos_usuario CASCADE;
DROP TABLE IF EXISTS modulos CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS empresas CASCADE;


CREATE TABLE empresas (
    id SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    nit TEXT,
    direccion TEXT,
    telefono TEXT,
    activa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    nombre TEXT,
    rol TEXT DEFAULT 'usuario',
    activo BOOLEAN DEFAULT TRUE,
    empresa_id INT REFERENCES empresas(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE modulos (
    id SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE permisos_usuario (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
    modulo_id INT REFERENCES modulos(id) ON DELETE CASCADE,
    empresa_id INT REFERENCES empresas(id) ON DELETE CASCADE,
    UNIQUE (usuario_id, modulo_id, empresa_id)
);



-- INSERT INTO empresas (nombre, nit, activa)
-- VALUES ('Wg Importaciones', '1130612014', TRUE);



-- INSERT INTO usuarios (username, password_hash, nombre, rol, activo, empresa_id)
-- VALUES (
--   'admin_wg',
--   '$2b$12$hv6BbggZtXFbGk8/IBF99eS1uDTGSxDXqWc6/3U0CyJUYsF9/zEXq', -- HASH PASSLIB
--   'Davalyze',
--   'admin_global',
--   TRUE,
--   (SELECT id FROM empresas WHERE nombre = 'Wg Importaciones')
-- );


-- -- ================================================
-- -- 🧩 Crear módulo Picking & Packing
-- -- ================================================
-- INSERT INTO modulos (nombre, descripcion, activo)
-- VALUES ('Pickin & Packing', 'Flujo de trabajo del despacho de pedidos', TRUE);


-- -- ================================================
-- -- 🔑 Asignar permisos al usuario
-- -- ================================================
INSERT INTO permisos_usuario (usuario_id, modulo_id, empresa_id)
VALUES (
  (SELECT id FROM usuarios WHERE username = 'admin_wg'),
  (SELECT id FROM modulos WHERE nombre = 'Pickin & Packing'),
  (SELECT id FROM empresas WHERE nombre = 'Wg Importaciones')
);