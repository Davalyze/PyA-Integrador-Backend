# Imagen base
FROM python:3.10.11-slim

# Evitar caché de bytecode y forzar salida sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema y driver ODBC 18 descargando el paquete directo
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl ca-certificates gnupg \
      unixodbc unixodbc-dev \
 && curl -fSL -o /tmp/msodbcsql18.deb \
      https://packages.microsoft.com/repos/microsoft-debian-bullseye-prod/pool/main/m/msodbcsql18/msodbcsql18_18.3.2.1-1_amd64.deb \
 && ACCEPT_EULA=Y dpkg -i /tmp/msodbcsql18.deb || apt-get -f install -y \
 && rm -rf /var/lib/apt/lists/* /tmp/msodbcsql18.deb

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Exponer el puerto (opcional)
EXPOSE 8000

# Comando de arranque FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
