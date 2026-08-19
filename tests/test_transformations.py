import pytest

from pyspark.sql import SparkSession

from spark_jobs.transformation import (
    calculate_category_metrics
)


# =========================================================
# FIXTURE SPARK SESSION
# =========================================================

@pytest.fixture(scope="session")
def spark():
    """
    Crea una SparkSession compartida
    para todos los tests.
    """

    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("pytest-transformations") \
        .getOrCreate()

    yield spark

    spark.stop()


# =========================================================
# TEST ANALYTICS POR CATEGORÍA
# =========================================================

def test_calculate_category_metrics(
    spark
):
    """
    Verifica que el agrupamiento
    y agregaciones sean correctas.
    """

    # -----------------------------------------------------
    # DATAFRAME DE PRUEBA
    # -----------------------------------------------------

    df = spark.createDataFrame(

        [
            ("electronics", 100),
            ("electronics", 200),
            ("clothing", 50)
        ],

        [
            "category",
            "price"
        ]
    )

    # -----------------------------------------------------
    # EJECUTAR TRANSFORMACIÓN
    # -----------------------------------------------------

    result = calculate_category_metrics(
        df
    )

    # -----------------------------------------------------
    # CONVERTIR A PYTHON
    # -----------------------------------------------------

    rows = {

        row["category"]: row

        for row in result.collect()
    }

    # -----------------------------------------------------
    # VALIDAR ELECTRONICS
    # -----------------------------------------------------

    assert rows[
        "electronics"
    ]["total_products"] == 2

    assert rows[
        "electronics"
    ]["avg_price"] == 150

    # -----------------------------------------------------
    # VALIDAR CLOTHING
    # -----------------------------------------------------

    assert rows[
        "clothing"
    ]["total_products"] == 1

    assert rows[
        "clothing"
    ]["avg_price"] == 50
