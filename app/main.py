from fastapi import FastAPI
from app.api import clientes, auth,picking
from fastapi.middleware.cors import CORSMiddleware
import warnings

# Ignorar todos los warnings
warnings.filterwarnings("ignore")

app = FastAPI(title="PyA Integrador")

# 🟢 AGREGAR ESTO AQUÍ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Puedes restringirlo luego
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(picking.router, prefix="/picking", tags=["Picking & Packing"])

app.include_router(auth.router)
