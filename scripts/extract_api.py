# =========================================================
# FLUJO DEL SCRIPT
# =========================================================
        # Consume una API
        # Convierte JSON → Python
        # Genera timestamp
        # Crea archivo dinámico
        # Guarda JSON localmente
        # Retorna la ruta del archivo

import json
import logging
import traceback
from pathlib import Path
from datetime import datetime

import requests


# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

# URL de la API pública
API_URL = "https://fakestoreapi.com/products"

# Carpeta donde se guardarán los archivos JSON
OUTPUT_DIR = Path("/tmp/products")

# Tiempo máximo de espera para la petición HTTP
TIMEOUT = 30


# =========================================================
# CONFIGURACIÓN DE LOGGING
# =========================================================

# Configuración básica del sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# =========================================================
# FUNCIÓN PRINCIPAL DE EXTRACCIÓN
# =========================================================

def extract_data() -> str:
    """
    Extrae datos desde una API y los guarda
    en un archivo JSON local.

    Returns:
        str: Ruta completa del archivo generado.
    """

    try:

        # -------------------------------------------------
        # Crear carpeta si no existe
        # -------------------------------------------------

        # parents=True:
        # crea carpetas intermedias si faltan

        # exist_ok=True:
        # evita error si la carpeta ya existe

        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        # -------------------------------------------------
        # Iniciar extracción
        # -------------------------------------------------

        logging.info("Iniciando extracción de datos desde API...")

        # -------------------------------------------------
        # Realizar petición GET
        # -------------------------------------------------

        response = requests.get(
            API_URL,
            timeout=TIMEOUT
        )

        # -------------------------------------------------
        # Validar errores HTTP
        # -------------------------------------------------

        # Si la API responde:
        # 404
        # 500
        # 403
        # etc.
        #
        # lanzará excepción automáticamente

        response.raise_for_status()

        # -------------------------------------------------
        # Convertir JSON → objeto Python
        # -------------------------------------------------


        data = response.json()

        # -------------------------------------------------
        # Generar timestamp dinámico
        # -------------------------------------------------

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        # -------------------------------------------------
        # Construir nombre del archivo
        # -------------------------------------------------

        filename = OUTPUT_DIR / f"products_{timestamp}.json"

        # -------------------------------------------------
        # Guardar archivo JSON
        # -------------------------------------------------

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                # JSON legible/formateado
                indent=4,
                # Permite caracteres UTF-8 reales
                ensure_ascii=False
            )
        # -------------------------------------------------
        # Log éxito
        # -------------------------------------------------
        logging.info(
            f"Archivo guardado correctamente: {filename}"
        )
        logging.info(f"Productos recibidos: {len(data)}")
        # PROTEGER DE ERROR IndexError si API regresa []
        if data:
            logging.info(
                f"Primer producto: {data[0]}"
            )
        # -------------------------------------------------
        # Retornar ruta del archivo generado
        # -------------------------------------------------

        return str(filename)

    # =====================================================
    # ERRORES HTTP / RED
    # =====================================================

    except requests.exceptions.RequestException as e:

        logging.error(
            f"Error en petición HTTP: {str(e)}"
        )

        # -------------------------------------------------
        # Mostrar traceback completo
        # -------------------------------------------------

        logging.error(
            traceback.format_exc()
        )

        raise

    # =====================================================
    # ERRORES GENERALES
    # =====================================================

    except Exception as e:

        logging.error(
            f"Error inesperado: {str(e)}"
        )

        # -------------------------------------------------
        # Mostrar traceback completo
        # -------------------------------------------------

        logging.error(
            traceback.format_exc()
        )

        raise


# =========================================================
# PUNTO DE ENTRADA PRINCIPAL
# =========================================================

# Solo ejecuta la función si el archivo
# se corre directamente:
#
# python extract_api.py
#
# Si se importa desde otro archivo:
#
# from extract_api import extract_data
#
# NO se ejecutará automáticamente

if __name__ == "__main__":

    extract_data()
