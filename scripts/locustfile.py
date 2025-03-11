from locust import HttpUser, task, between, events
from locust.env import Environment
from locust.stats import stats_history
from prometheus_client import start_http_server
import time
import logging
from locust.exception import StopUser

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@events.init.add_listener
def on_locust_init(environment: Environment, **_kwargs):
    logger.info("📡 Iniciando servidor Prometheus en puerto 8000")
    start_http_server(8000)


class CCoinsUser(HttpUser):
    """Usuario virtual de prueba para la app CCoins"""
    host = "https://app.ccoins.io"
    wait_time = between(1, 5)
    token = None

    def on_start(self):
        """Se ejecuta al inicio de cada usuario virtual"""
        logger.info("🚀 Iniciando usuario virtual")
        self.login()

    def login(self):
        """Obtiene un token de autenticación con reintentos"""
        for intento in range(5):
            try:
                response = self.client.post(
                    "/ms_users/internal/v1/users/tokens/generate",
                    json={"email": "apptest@gmail.com", "password": "1234567890"},
                    timeout=10
                )

                if response.status_code == 200:
                    self.token = response.json().get("access_token")
                    logger.info(f"✅ Token obtenido en intento {intento+1}")
                    return
                elif response.status_code == 503:
                    wait_time = 2 ** intento
                    logger.warning(f"⏳ Servicio no disponible, reintentando en {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"⚠️ Error {response.status_code} al obtener token: {response.text}")
                    break
            except Exception as e:
                logger.error(f"🚨 Error en la solicitud: {str(e)}")
                time.sleep(2 ** intento)

        logger.error("❌ No se pudo autenticar el usuario. Deteniendo ejecución.")
        raise StopUser("No se pudo autenticar el usuario.")

    @task
    def get_market_offers(self):
        """Obtiene ofertas del marketplace"""
        if not self.token:
            logger.error("🚫 No hay un token válido, deteniendo usuario.")
            raise StopUser("Token inválido.")

        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"page": 1, "per_page": 50, "operation": "buy"}

        response = self.client.get(
            "/ms_marketplace/internal/v1/market",
            headers=headers,
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            logger.info("✅ Ofertas obtenidas con éxito")
        elif response.status_code == 401:
            logger.warning("🔄 Token expirado, intentando renovar...")
            self.login()
        else:
            logger.error(f"⚠️ Error {response.status_code} al obtener ofertas: {response.text}")
