import os

import requests


# =========================================================
# CONFIGURACIÓN
# =========================================================

DISCORD_WEBHOOK_URL = os.getenv(
    "DISCORD_WEBHOOK_URL"
)


# =========================================================
# MENSAJE DE PRUEBA
# =========================================================

def send_test_message() -> None:
    """
    Envía un mensaje de prueba a Discord.
    """

    message = {

        "content":
        """
         Discord Webhook funcionando correctamente

        Proyecto:
        Retail Analytics Pipeline

        Estado:
        Conexión exitosa
        """
    }

    response = requests.post(

        DISCORD_WEBHOOK_URL,

        json=message,

        timeout=10
    )

    response.raise_for_status()

    print(
        "Mensaje enviado correctamente"
    )


# =========================================================
# PUNTO DE ENTRADA
# =========================================================

if __name__ == "__main__":

    send_test_message()
