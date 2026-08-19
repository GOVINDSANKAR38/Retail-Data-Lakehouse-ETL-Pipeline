import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

import os

BUCKET = os.getenv("S3_BUCKET")

PROCESSED_PREFIX = os.getenv(
    "PROCESSED_PREFIX"
)
# =========================================================
# CONFIGURACIÓN DE LOGS
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# =========================================================
# CREAR SPARK SESSION
# =========================================================

spark = SparkSession.builder \
    .appName(
        "DataQualityChecks"
    ) \
    .getOrCreate()


# =========================================================
# FUNCIÓN PRINCIPAL
# =========================================================

def run_quality_checks() -> None:
    """
    Ejecuta validaciones de calidad sobre
    los datos procesados.
    """

    try:

        # -------------------------------------------------
        # LEER PARQUET PROCESADO
        # -------------------------------------------------

        logging.info(
            "Leyendo dataset procesado..."
        )

        df = spark.read.parquet(
            f"s3a://{BUCKET}/{PROCESSED_PREFIX}/"
        )
        # -------------------------------------------------
        # VALIDAR DATASET VACÍO
        # -------------------------------------------------

        total_rows = df.count()

        if total_rows == 0:

            raise ValueError(
                "El dataset procesado está vacío"
            )

        logging.info(
            f"Total registros: {total_rows}"
        )

        # -------------------------------------------------
        # VALIDAR VALORES NULOS
        # -------------------------------------------------

        null_count = df.filter(

            col("category").isNull() |
            col("avg_price").isNull()

        ).count()

        if null_count > 0:

            raise ValueError(
                f"Se encontraron {null_count} registros con valores nulos"
            )

        logging.info(
            "No se encontraron valores nulos"
        )

        # -------------------------------------------------
        # VALIDAR PRECIOS NEGATIVOS
        # -------------------------------------------------

        negative_prices = df.filter(
            col("avg_price") < 0
        ).count()

        if negative_prices > 0:

            raise ValueError(
                f"Se encontraron {negative_prices} precios negativos"
            )

        logging.info(
            "No se encontraron precios negativos"
        )

        # -------------------------------------------------
        # LOG ÉXITO
        # -------------------------------------------------

        logging.info(
            "Validaciones de calidad completadas correctamente"
        )

    # =====================================================
    # MANEJO DE ERRORES
    # =====================================================

    except Exception as e:

        logging.exception(
            f"Error en Data Quality: {str(e)}"
        )

        raise

    finally:

        spark.stop()


# =========================================================
# PUNTO DE ENTRADA
# =========================================================

if __name__ == "__main__":

    run_quality_checks()
