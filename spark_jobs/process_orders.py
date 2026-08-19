import logging

from pyspark.sql import SparkSession

from transformation import (
    calculate_category_metrics
)

from quality_checks import (
    validate_not_empty,
    validate_required_columns
)


# =========================================================
# CONFIGURACIÓN LOGS
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
        "RetailAnalyticsPipeline"
    ) \
    .getOrCreate()


try:

    # -----------------------------------------------------
    # INICIO ETL
    # -----------------------------------------------------

    logging.info(
        "Iniciando proceso ETL..."
    )

    # -----------------------------------------------------
    # LEER RAW DATA
    # -----------------------------------------------------

    logging.info(
        "Leyendo datos desde S3..."
    )

    df = spark.read \
        .option(
            "multiline",
            "true"
        ) \
        .json(
            "s3a://ecommerce-data-lake-airflow/raw/products/*.json"
        )

    # -----------------------------------------------------
    # MOSTRAR SCHEMA
    # -----------------------------------------------------

    logging.info(
        "Schema del DataFrame"
    )

    df.printSchema()

    # -----------------------------------------------------
    # DATA QUALITY
    # -----------------------------------------------------

    validate_not_empty(
        df
    )

    validate_required_columns(

        df,

        [
            "category",
            "price"
        ]
    )

    # -----------------------------------------------------
    # TRANSFORMACIONES
    # -----------------------------------------------------

    logging.info(
        "Calculando métricas..."
    )

    result = calculate_category_metrics(
        df
    )

    # -----------------------------------------------------
    # RESULTADO
    # -----------------------------------------------------

    result.show(
        truncate=False
    )

    # -----------------------------------------------------
    # ESCRITURA PARQUET
    # -----------------------------------------------------

    logging.info(
        "Guardando Parquet..."
    )

    result.write \
        .mode(
            "overwrite"
        ) \
        .parquet(
            "s3a://ecommerce-data-lake-airflow/processed/category_analytics/"
        )

    logging.info(
        "ETL completado correctamente"
    )

except Exception as e:

    logging.exception(
        f"Error durante ETL: {str(e)}"
    )

    raise

finally:

    logging.info(
        "Cerrando Spark Session..."
    )

    spark.stop()
