import pytest

from pyspark.sql import SparkSession

from spark_jobs.quality_checks import (
    validate_not_empty,
    validate_required_columns
)


# =========================================================
# FIXTURE SPARK SESSION
# =========================================================

@pytest.fixture(scope="session")
def spark():
    """
    Crea una SparkSession para todos los tests.
    """

    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("pytest-quality") \
        .getOrCreate()

    yield spark

    spark.stop()


# =========================================================
# TEST DATAFRAME NO VACÍO
# =========================================================

def test_validate_not_empty_success(
    spark
):
    """
    Debe pasar cuando el DataFrame
    contiene registros.
    """

    # Crear DataFrame de prueba

    df = spark.createDataFrame(
        [
            ("Laptop",),
            ("Mouse",)
        ],
        ["product"]
    )

    # No debe lanzar excepción

    validate_not_empty(df)


# =========================================================
# TEST DATAFRAME VACÍO
# =========================================================

def test_validate_not_empty_failure(
    spark
):
    """
    Debe fallar cuando el DataFrame
    está vacío.
    """

    # Crear DataFrame vacío

    df = spark.createDataFrame(
        [],
        "product STRING"
    )

    # Esperar ValueError

    with pytest.raises(
        ValueError
    ):

        validate_not_empty(df)


# =========================================================
# TEST COLUMNAS CORRECTAS
# =========================================================

def test_required_columns_success(
    spark
):
    """
    Debe pasar cuando todas las
    columnas existen.
    """

    df = spark.createDataFrame(
        [
            ("electronics", 100)
        ],
        [
            "category",
            "price"
        ]
    )

    validate_required_columns(

        df,

        [
            "category",
            "price"
        ]
    )


# =========================================================
# TEST COLUMNA FALTANTE
# =========================================================

def test_required_columns_failure(
    spark
):
    """
    Debe fallar cuando falta una
    columna obligatoria.
    """

    df = spark.createDataFrame(
        [
            ("electronics",)
        ],
        [
            "category"
        ]
    )

    with pytest.raises(
        ValueError
    ):

        validate_required_columns(

            df,

            [
                "category",
                "price"
            ]
        )
