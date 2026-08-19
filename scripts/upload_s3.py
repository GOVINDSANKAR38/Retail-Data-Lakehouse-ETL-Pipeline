import logging

import boto3


# =========================================================
# CONFIGURACIÓN DE LOGS
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# =========================================================
# CLIENTE AWS S3
# =========================================================

# Crear cliente para conectarse a S3
s3 = boto3.client("s3")


# =========================================================
# CONFIGURACIÓN BUCKET
# =========================================================

# Nombre del bucket S3 desde el arcjivo.env
import os

BUCKET = os.getenv(
    "S3_BUCKET",
    "ecommerce-data-lake-airflow"
)

# =========================================================
# FUNCIÓN PRINCIPAL
# =========================================================

def upload_to_s3(file_path: str) -> None:
    """
    Sube un archivo local hacia AWS S3.

    Args:
        file_path (str):
            Ruta local del archivo a subir.
    """

    try:

        # -------------------------------------------------
        # Obtener nombre archivo
        # -------------------------------------------------

        # Ejemplo:
        #
        # /tmp/products/file.json
        #
        # Resultado:
        #
        # file.json

        file_name = file_path.split("/")[-1]

        # -------------------------------------------------
        # Construir path destino en S3
        # -------------------------------------------------

        s3_key = f"raw/products/{file_name}"

        # -------------------------------------------------
        # Log inicio subida
        # -------------------------------------------------

        logging.info(
            f"Subiendo archivo a S3: {s3_key}"
        )

        # -------------------------------------------------
        # Subir archivo a S3
        # -------------------------------------------------

        s3.upload_file(
            file_path,
            BUCKET,
            s3_key
        )

        # -------------------------------------------------
        # Log éxito
        # -------------------------------------------------

        logging.info(
            "Archivo subido correctamente"
        )

    # =====================================================
    # MANEJO DE ERRORES
    # =====================================================

    except Exception as e:


        # Muestra:
        # - mensaje error
        # - traceback completo
        # - línea exacta
        # - tipo excepción

        logging.exception(
            f"Error subiendo archivo a S3: {str(e)}"
        )

        # -------------------------------------------------
        # Relanzar excepción
        # -------------------------------------------------
        # permite que Airflow marque: Task = FAILED

        raise
