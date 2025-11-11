from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.postgres_manager import PostgresManager
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

# 🔐 Configuración de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 🔹 Modelo de entrada del login
class LoginRequest(BaseModel):
    username: str
    password: str


# 🔹 Función para crear token JWT
def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=settings.JWT_EXP_HOURS)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


# 🔹 Endpoint de login
@router.post("/login")
def login_user(req: LoginRequest):
    db = PostgresManager()

    try:
        # 🧩 Obtener usuario y empresa
        sql_user = """
            SELECT u.*, e.nombre AS empresa_nombre
            FROM usuarios u
            JOIN empresas e ON u.empresa_id = e.id
            WHERE u.username = %(username)s AND u.activo = TRUE
        """
        rows = db.execute_query(sql_user, {"username": req.username})
        if not rows:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        user = rows[0]

        # 🔑 Validar contraseña
        if not pwd_context.verify(req.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

        # 🧩 Obtener los módulos habilitados para el usuario
        sql_modulos = """
            SELECT m.nombre
            FROM permisos_usuario p
            JOIN modulos m ON p.modulo_id = m.id
            WHERE p.usuario_id = %(usuario_id)s
            AND p.empresa_id = %(empresa_id)s
            AND m.activo = TRUE
        """
        modulos_rows = db.execute_query(sql_modulos, {
            "usuario_id": user["id"],
            "empresa_id": user["empresa_id"]
        })
        modulos_lista = [m["nombre"] for m in modulos_rows]


        # 🔐 Crear token JWT
        token = create_token({
            "sub": user["username"],
            "rol": user["rol"],
            "empresa": user["empresa_nombre"]
        })

        # 📦 Respuesta
        return {
            "token": token,
            "username": user["username"],
            "nombre": user["nombre"],
            "rol": user["rol"],
            "empresa_nombre": user["empresa_nombre"],
            "modulos": modulos_lista
        }

    except HTTPException:
        raise

    except Exception as e:
        print("❌ Error en login_user:", e)
        raise HTTPException(status_code=500, detail="Error interno en el servidor")

    finally:
        db.close()
