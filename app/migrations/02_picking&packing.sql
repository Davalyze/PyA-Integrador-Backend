DROP TABLE IF EXISTS pedidos_enc CASCADE;

CREATE TABLE IF NOT EXISTS pedidos_enc (
    id SERIAL PRIMARY KEY,
    origen VARCHAR(70),
    numero_pedido INTEGER NOT NULL,
    estado VARCHAR(20) NOT NULL,
    observacion_sacador TEXT,
    observacion_empacador TEXT,
    usuario VARCHAR(70),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);



DROP TABLE IF EXISTS pedidos_det CASCADE;

CREATE TABLE IF NOT EXISTS pedidos_det (
    id SERIAL PRIMARY KEY,
    origen VARCHAR(70),
    numero_pedido INTEGER NOT NULL,
    codigo_producto VARCHAR(70),
    cantidad_sacada INTEGER,
    cantidad_empacada INTEGER,
    numero_de_caja INTEGER,
    observacion TEXT,
    usuario VARCHAR(70),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
