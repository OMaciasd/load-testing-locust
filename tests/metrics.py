from prometheus_client import Counter, Histogram, Gauge, start_http_server
import logging
import gc
import psutil
import threading
import time
import os

METRICS_PORT = int(os.getenv("METRICS_PORT", 8088))

# Configuración de logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

gc.set_threshold(10000, 10, 10)

# Métricas de autenticación
TOKEN_RENEWAL_FAILURES = Counter(
    "token_renewal_failures", "Total de fallos en la renovación del token"
)

# Definir métricas del sistema
PYTHON_GC_COLLECTED = Gauge(
    "python_gc_collected_objects", "Número de objetos recolectados por el GC"
)
REQUEST_FAILURES = Counter(
    "request_failures_total",
    "Cantidad de fallos en las solicitudes", ["endpoint"]
)
REQUEST_LATENCY = Histogram(
    "locust_request_latency_seconds",
    "Tiempo de respuesta",
    buckets=[0.1, 0.3, 0.5, 1, 2, 3, 5, 10],
)
MEMORY_USAGE = Gauge(
    "python_process_memory_mb", "Uso de memoria del proceso en MB"
)
CPU_USAGE = Gauge("python_process_cpu_percent", "Uso de CPU del proceso en %")
THREAD_COUNT = Gauge("python_process_thread_count", "Número de hilos activos")
UPTIME = Gauge(
    "python_process_uptime_seconds", "Tiempo de ejecución del proceso"
)


class AuthManager:
    def __init__(self, client):
        self.client = client
        self.token = None

    def get_token(self):
        """Servicio de autenticación."""
        return "nuevo_token_generado"

    def renew_token(self, retries=3, delay=2):
        for attempt in range(retries):
            try:
                new_token = self.get_token()
                if new_token:
                    self.token = new_token
                    logger.info("authentication_success: token_renewed")
                    return
                else:
                    logger.warning(
                        f"token_not_obtained (Intento {attempt+1}/{retries})"
                    )
                    TOKEN_RENEWAL_FAILURES.inc()
            except Exception as e:
                TOKEN_RENEWAL_FAILURES.inc()
                logger.error(
                    f"token_error: {str(e)} (Intento {attempt+1}/{retries})"
                )
            time.sleep(delay * (2 ** attempt))  # Exponential backoff


last_gc_collected = 0
last_memory_usage = 0


def collect_gc_metrics():
    global last_gc_collected, last_memory_usage

    try:
        if gc.isenabled():
            gc.collect()

        gc_stats = gc.get_stats() if hasattr(gc, "get_stats") else []
        collected = gc_stats[0]["collected"] if gc_stats else 0

        process = psutil.Process()
        memory_usage = process.memory_info().rss / (1024 * 1024)
        process.cpu_percent(interval=None)
        time.sleep(0.1)
        cpu_usage = process.cpu_percent(interval=None)
        thread_count = len(threading.enumerate())

        if abs(
            collected - last_gc_collected
        ) > 50 or abs(memory_usage - last_memory_usage) > 0.5:
            PYTHON_GC_COLLECTED.set(collected)
            MEMORY_USAGE.set(memory_usage)
            CPU_USAGE.set(cpu_usage)
            THREAD_COUNT.set(thread_count)

            logger.info(f"📊 GC: {collected} objetos recolectados")
            logger.info(
                f"📊 Memoria: {memory_usage:.2f} MB,"
                f"CPU: {cpu_usage:.2f}%, Hilos: {thread_count}"
            )

            last_gc_collected = collected
            last_memory_usage = memory_usage

    except Exception as e:
        logger.error(f"❌ Error en métricas: {str(e)}")


METRICS_COLLECTION_INTERVAL = 30


def start_gc_metrics_collection():
    """Ejecuta la recolección de métricas en un hilo de ejecución continuo."""
    def run():
        while True:
            try:
                collect_gc_metrics()
            except Exception as e:
                logger.error(f"❌ Error en el hilo de métricas: {str(e)}")
            time.sleep(METRICS_COLLECTION_INTERVAL)

    gc_thread = threading.Thread(target=run, daemon=True)
    gc_thread.start()


def update_uptime():
    """Actualiza la métrica de tiempo de ejecución."""
    start_time = time.time()
    while True:
        UPTIME.set(time.time() - start_time)
        time.sleep(10)


def start_metrics_server():
    """Inicia el servidor de métricas en el puerto configurado."""
    logger.info(f"🚀 Iniciando Cliente Prometheus en puerto {METRICS_PORT}")
    start_http_server(METRICS_PORT)


if __name__ == "__main__":
    start_metrics_server()
    start_gc_metrics_collection()
    threading.Thread(target=update_uptime, daemon=True).start()
