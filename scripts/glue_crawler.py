import os
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
# CONFIGURACIÓN
# =========================================================

CRAWLER_NAME = os.getenv(
    "CRAWLER_NAME"
)


# =========================================================
# FUNCIÓN PRINCIPAL
# =========================================================

def run_glue_crawler() -> None:
    """
    Ejecuta un Glue Crawler existente
    para actualizar el Glue Catalog.
    """

    try:

        # -------------------------------------------------
        # CREAR CLIENTE GLUE
        # -------------------------------------------------

        glue = boto3.client(
            "glue"
        )

        # -------------------------------------------------
        # VALIDAR VARIABLE DE ENTORNO
        # -------------------------------------------------

        if not CRAWLER_NAME:

            raise ValueError(
                "CRAWLER_NAME no está definido"
            )

        # -------------------------------------------------
        # OBTENER ESTADO ACTUAL DEL CRAWLER
        # -------------------------------------------------

        response = glue.get_crawler(Name=CRAWLER_NAME)

        crawler_state = response["Crawler"]["State"]

        # -------------------------------------------------
        # LOG ESTADO
        # -------------------------------------------------

        logging.info(
            f"Crawler: {CRAWLER_NAME}"
        )

        logging.info(
            f"Estado actual: {crawler_state}"
        )

        # -------------------------------------------------
        # SI YA ESTÁ CORRIENDO
        # -------------------------------------------------

        if crawler_state == "RUNNING":

            logging.info(
                "Crawler ya se encuentra ejecutándose"
            )

            return

        # -------------------------------------------------
        # INICIAR CRAWLER
        # -------------------------------------------------

        logging.info(
            "Iniciando crawler..."
        )

        glue.start_crawler(
            Name=CRAWLER_NAME
        )

        # -------------------------------------------------
        # LOG ÉXITO
        # -------------------------------------------------

        logging.info(
            "Crawler iniciado correctamente"
        )

    # =====================================================
    # MANEJO DE ERRORES
    # =====================================================

    except Exception as e:

        logging.exception(
            f"Error ejecutando crawler: {str(e)}"
        )

        raise


# =========================================================
# PUNTO DE ENTRADA
# =========================================================

if __name__ == "__main__":

    run_glue_crawler()
