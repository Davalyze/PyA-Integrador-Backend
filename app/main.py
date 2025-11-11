from fastapi import FastAPI
from app.api import clientes,auth
from fastapi.middleware.cors import CORSMiddleware
import warnings

# Ignorar todos los warnings
warnings.filterwarnings("ignore")
app = FastAPI(title="PyA Integrador")
@app.get("/health")
def health():
    """
    Endpoint de salud de la API.
    """
    return {"status": "ok"}

app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(auth.router)