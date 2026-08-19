import os
import logging

import requests


# =========================================================
# CONFIGURACIÓN DE LOGS
# =========================================================

# Configura el formato que aparecerá en los logs
# de Airflow y de la consola.

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# =========================================================
# CONFIGURACIÓN
# =========================================================

# Obtiene la URL del webhook desde el archivo .env
#
# Ejemplo:
#
# DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
#

DISCORD_WEBHOOK_URL = os.getenv(
    "DISCORD_WEBHOOK_URL"
)


# =========================================================
# FUNCIÓN PRINCIPAL
# =========================================================

def notify_failure(context) -> None:
    """
    Envía una alerta a Discord cuando una
    tarea de Airflow falla.

    Parameters
    ----------
    context : dict
        Diccionario enviado automáticamente
        por Airflow con información de la
        ejecución actual.
    """

    try:

        # -------------------------------------------------
        # OBTENER INFORMACIÓN DEL DAG
        # -------------------------------------------------

        # Nombre del DAG

        dag_id = context["dag"].dag_id

        # -------------------------------------------------
        # OBTENER INFORMACIÓN DE LA TASK
        # -------------------------------------------------

        # Nombre de la tarea que falló

        task_id = context[
            "task_instance"
        ].task_id

        # -------------------------------------------------
        # OBTENER FECHA DE EJECUCIÓN
        # -------------------------------------------------

        execution_date = context.get(
            "execution_date"
        )

        # -------------------------------------------------
        # CONSTRUIR MENSAJE
        # -------------------------------------------------

        # Discord recibe un JSON con la clave "content"

        message = {

            "content":

                        f"""
            Airflow Task Failed

            DAG:
            {dag_id}

            Task:
            {task_id}

            Execution Date:
            {execution_date}
        """
        }

        # -------------------------------------------------
        # ENVIAR MENSAJE A DISCORD
        # -------------------------------------------------

        requests.post(

            # URL del webhook
            DISCORD_WEBHOOK_URL,

            # Payload JSON
            json=message,

            # Tiempo máximo espera
            timeout=10
        )

        # -------------------------------------------------
        # LOG ÉXITO
        # -------------------------------------------------

        logging.info(
            "Alerta enviada correctamente"
        )

    # =====================================================
    # MANEJO DE ERRORES
    # =====================================================

    except Exception as e:

        logging.exception(
            f"Error enviando alerta: {str(e)}"
        )
