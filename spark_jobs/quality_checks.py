import logging


# =========================================================
# VALIDAR DATAFRAME VACÍO
# =========================================================

def validate_not_empty(df) -> None:
    """
    Verifica que el DataFrame tenga registros.
    """

    # count() devuelve el número de filas
    total_rows = df.count()

    # Si no hay registros
    if total_rows == 0:

        raise ValueError(
            "El DataFrame está vacío"
        )

    logging.info(
        f"Registros encontrados: {total_rows}"
    )


# =========================================================
# VALIDAR COLUMNAS REQUERIDAS
# =========================================================

def validate_required_columns(
    df,
    required_columns
) -> None:
    """
    Verifica que existan las columnas necesarias.
    """

    # Obtener columnas del DataFrame
    current_columns = df.columns

    # Recorrer columnas obligatorias
    for column in required_columns:

        # Si no existe
        if column not in current_columns:

            raise ValueError(
                f"Columna faltante: {column}"
            )

    logging.info(
        "Validación de columnas correcta"
    )
