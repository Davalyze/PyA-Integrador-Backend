-- ================================================
-- 🏢 EMPRESAS
-- ================================================


drop table if EXISTS empresas CASCADE;
drop table if EXISTS usuarios CASCADE;
drop table if EXISTS modulos CASCADE;
drop table if EXISTS permisos_usuario CASCADE;

CREATE TABLE IF NOT EXISTS empresas (
    id SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    nit TEXT,
    direccion TEXT,
    telefono TEXT,
    activa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ================================================
-- 👤 USUARIOS
-- ================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    nombre TEXT,
    rol TEXT DEFAULT 'usuario',  -- 'admin_global', 'admin_empresa', 'usuario'
    activo BOOLEAN DEFAULT TRUE,
    empresa_id INT REFERENCES empresas(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ================================================
-- 🧩 MÓDULOS
-- ================================================
CREATE TABLE IF NOT EXISTS modulos (
    id SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ================================================
-- 🔑 PERMISOS DE USUARIO (usuario ↔ módulo ↔ empresa)
-- ================================================
CREATE TABLE IF NOT EXISTS permisos_usuario (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
    modulo_id INT REFERENCES modulos(id) ON DELETE CASCADE,
    empresa_id INT REFERENCES empresas(id) ON DELETE CASCADE,
    UNIQUE (usuario_id, modulo_id, empresa_id)
);




-- ================================================
--  crear empresa
-- INSERT INTO empresas (nombre, nit, activa)
-- VALUES ('GIPAO', '900380734', TRUE);

-- ================================================
--  crear usuario 
-- INSERT INTO usuarios (username, password_hash, nombre, rol, activo, empresa_id)
-- VALUES (
--   'admin_gipao',
--   crypt('Sh6248597652', gen_salt('bf')),
--   'Davalyze',
--   'admin_global',
--   TRUE,
--   1 este depende del id de la empresa
-- );

-- ================================================
--  crear módulos
-- INSERT INTO modulos (nombre, descripcion, activo)
-- VALUES ('EXITO', 'Flujo de trabajo Éxito', TRUE);



-- ================================================
--  asignar permisos al usuario
-- INSERT INTO permisos_usuario (usuario_id, modulo_id, empresa_id)
-- VALUES (
--   (SELECT id FROM usuarios WHERE username = 'admin_gipao'),
--   (SELECT id FROM modulos WHERE nombre = 'EXITO'),
--   (SELECT id FROM empresas WHERE nombre = 'GIPAO')
-- );