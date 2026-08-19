# =========================================================
# IMPORTS
# =========================================================

import json

from pathlib import Path

from unittest.mock import Mock
from unittest.mock import patch

from scripts.extract_api import extract_data


# =========================================================
# TEST PRINCIPAL
# =========================================================

def test_extract_data_success():

    # -----------------------------------------------------
    # RESPUESTA FALSA DE LA API
    # -----------------------------------------------------
    # Simula:
    #
    # requests.get(...)
    #
    # sin consumir Internet
    # y sin depender de FakeStoreAPI

    fake_response = Mock()

    # -----------------------------------------------------
    # JSON FALSO
    # -----------------------------------------------------

    fake_response.json.return_value = [
        {
            "id": 1,
            "title": "Test Product",
            "price": 10.5
        }
    ]

    # -----------------------------------------------------
    # SIMULAR HTTP 200 OK
    # -----------------------------------------------------

    fake_response.raise_for_status.return_value = None

    # -----------------------------------------------------
    # REEMPLAZAR requests.get()
    # -----------------------------------------------------
    # Mientras corre este bloque:
    #
    # requests.get(...)
    #
    # regresará fake_response

    with patch(
        "scripts.extract_api.requests.get",
        return_value=fake_response
    ):

        # -------------------------------------------------
        # EJECUTAR FUNCIÓN
        # -------------------------------------------------

        file_path = extract_data()

        # -------------------------------------------------
        # VALIDAR ARCHIVO CREADO
        # -------------------------------------------------

        assert Path(file_path).exists()

        # -------------------------------------------------
        # ABRIR ARCHIVO GENERADO
        # -------------------------------------------------

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        # -------------------------------------------------
        # VALIDAR CONTENIDO
        # -------------------------------------------------

        assert len(data) == 1

        assert data[0]["id"] == 1

        assert data[0]["title"] == "Test Product"
