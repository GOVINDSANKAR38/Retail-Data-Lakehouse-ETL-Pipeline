from pyspark.sql.functions import (
    avg,
    count
)


# =========================================================
# ANALYTICS POR CATEGORÍA
# =========================================================

def calculate_category_metrics(df):
    """
    Calcula métricas por categoría.
    """

    result = df.groupBy(
        "category"
    ).agg(

        count("*").alias(
            "total_products"
        ),

        avg("price").alias(
            "avg_price"
        )
    )

    return result
