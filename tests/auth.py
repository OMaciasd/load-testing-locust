import logging
import requests
from requests.exceptions import RequestException, Timeout

logger = logging.getLogger(__name__)


def get_token(client=None):
    """Obtiene un token de autenticación con manejo de errores mejorado"""
    try:
        response = requests.post(
            "$URL",
            json={"email": "$EMAIL", "password": "$PASSWORD"},
            timeout=10
        )

        # Verificar si la respuesta fue exitosa
        if response.status_code == 200:
            token = response.json().get("access_token")
            if token:
                logger.info("✅ Token obtenido con éxito")
                return token
            else:
                logger.error("❌ Token no encontrado en la respuesta JSON")
                try:
                    logger.debug(
                        f"Detalles completos: {response.json()}"
                    )
                except ValueError:
                    logger.debug(
                        f"Detalles de la respuesta no JSON: {response.text}"
                    )
        else:
            logger.error(
                f"❌ Error: {response.status_code} - {response.text}"
            )
            try:
                logger.debug(
                    f"Detalles completos de la respuesta: {response.json()}"
                )
            except ValueError:
                logger.debug(
                    f"Detalles de la respuesta no JSON: {response.text}"
                )

    except Timeout as e:
        logger.error(f"❌ Error de tiempo de espera: {e}")
    except RequestException as e:
        logger.error(f"❌ Error de conexión: {e}")

    return None
