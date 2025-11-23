import base64
from datetime import datetime, timedelta
from azure.storage.blob import (
    BlobServiceClient,
    BlobSasPermissions,
    generate_blob_sas
)
from app.core.config import settings


class AzureBlobService:
    """Manejo de Azure Blob Storage: conexión, carga y descarga."""

    def __init__(self):
        self.account_name = settings.AZURE_STORAGE_ACCOUNT_NAME
        self.account_key = settings.AZURE_STORAGE_ACCOUNT_KEY
        self.container = settings.AZURE_STORAGE_CONTAINER
        self.endpoint_suffix = settings.AZURE_STORAGE_ENDPOINT_SUFFIX

        self.connection_string = (
            f"DefaultEndpointsProtocol=https;"
            f"AccountName={self.account_name};"
            f"AccountKey={self.account_key};"
            f"EndpointSuffix={self.endpoint_suffix}"
        )

    # ======================================================
    # 🔌 Conexión
    # ======================================================
    def connect(self):
        return BlobServiceClient.from_connection_string(self.connection_string)

    # ======================================================
    # 🔗 URL directa a un blob (solo para contenedores públicos)
    # ======================================================
    def build_blob_url(self, blob_name: str) -> str:
        return (
            f"https://{self.account_name}.blob.{self.endpoint_suffix}/"
            f"{self.container}/{blob_name}"
        )

    # ======================================================
    # 📤 SUBIR IMAGEN desde ruta local
    # ======================================================
    def upload_image(self, local_path: str, blob_name: str) -> bool:
        try:
            blob_service = self.connect()
            container_client = blob_service.get_container_client(self.container)
            blob_client = container_client.get_blob_client(blob_name)

            with open(local_path, "rb") as f:
                blob_client.upload_blob(f, overwrite=True)

            print(f"✔ Imagen subida: {blob_name}")
            return True

        except Exception as e:
            print(f"❌ Error subiendo imagen: {e}")
            return False

    # ======================================================
    # 📥 DESCARGAR imagen de Azure → Base64
    # ======================================================
    def download_image_base64(self, blob_name: str) -> str | None:
        try:
            blob_service = self.connect()
            container_client = blob_service.get_container_client(self.container)
            blob_client = container_client.get_blob_client(blob_name)

            data = blob_client.download_blob().readall()
            return base64.b64encode(data).decode("utf-8")

        except Exception as e:
            print(f"❌ Error descargando imagen: {e}")
            return None

    # ======================================================
    # 🔗 Generar URL SAS temporal (para BD si fuera necesario)
    # ======================================================
    def generate_sas_url(self, blob_name: str, hours_valid: int = 12) -> str | None:
        try:
            sas_token = generate_blob_sas(
                account_name=self.account_name,
                container_name=self.container,
                blob_name=blob_name,
                account_key=self.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=hours_valid)
            )

            return (
                f"https://{self.account_name}.blob.{self.endpoint_suffix}/"
                f"{self.container}/{blob_name}?{sas_token}"
            )

        except Exception as e:
            print(f"❌ Error creando SAS URL: {e}")
            return None
