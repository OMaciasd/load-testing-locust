from prometheus_client import Counter, Histogram, Gauge, start_http_server
from river.anomaly import HalfSpaceTrees
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

# Configuración de Garbage Collector
gc.set_threshold(10000, 10, 10)

# Métricas de autenticación
TOKEN_RENEWAL_FAILURES = Counter("token_renewal_failures", "Total de fallos en la renovación del token")

# Métricas del sistema
PYTHON_GC_COLLECTED = Gauge("python_gc_collected_objects", "Número de objetos recolectados por el GC")
REQUEST_FAILURES = Counter("request_failures_total", "Cantidad de fallos en las solicitudes", ["endpoint"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Tiempo de respuesta por endpoint", ["endpoint", "status_code"])
HTTP_ERRORS = Counter("http_errors_total", "Total de errores HTTP", ["endpoint", "status_code"])
MEMORY_USAGE = Gauge("python_process_memory_mb", "Uso de memoria del proceso en MB")
CPU_USAGE = Gauge("python_process_cpu_percent", "Uso de CPU del proceso en %")
THREAD_COUNT = Gauge("python_process_thread_count", "Número de hilos activos")
UPTIME = Gauge("python_process_uptime_seconds", "Tiempo de ejecución del proceso")
ACTIVE_CONNECTIONS = Gauge("active_connections", "Número de conexiones activas")

# Modelo de detección de anomalías
hst = HalfSpaceTrees(window_size=200, n_trees=30, height=20)

def detect_anomaly(latency, endpoint, status_code):
    score = hst.score_one({"latency": latency})
    if score > 0.75:
        logger.warning(f"⚠️ Anomalía detectada en {endpoint} (Score: {score:.2f}, Código: {status_code}) con latencia de {latency:.2f}s")

def track_http_error(endpoint, status_code):
    if status_code >= 400:
        HTTP_ERRORS.labels(endpoint=endpoint, status_code=status_code).inc()

def measure_request(endpoint, status_code, func, *args, **kwargs):
    start_time = time.time()
    try:
        result = func(*args, **kwargs)
        latency = time.time() - start_time
        REQUEST_LATENCY.labels(endpoint=endpoint, status_code=status_code).observe(latency)
        detect_anomaly(latency, endpoint, status_code)
        return result
    except Exception as e:
        REQUEST_FAILURES.labels(endpoint=endpoint).inc()
        logger.error(f"❌ Error en {endpoint}: {str(e)}")
        raise

class AuthManager:
    def __init__(self):
        self.token = None

    def get_token(self):
        return "nuevo_token_generado"

    def renew_token(self, retries=3, delay=2):
        for attempt in range(retries):
            try:
                new_token = self.get_token()
                if new_token:
                    self.token = new_token
                    logger.info("✅ Token renovado correctamente")
                    return
                else:
                    logger.warning(f"🔄 Token no obtenido (Intento {attempt+1}/{retries})")
                    TOKEN_RENEWAL_FAILURES.inc()
            except Exception as e:
                TOKEN_RENEWAL_FAILURES.inc()
                logger.error(f"❌ Error al renovar token: {str(e)}")
            time.sleep(delay * (2 ** attempt))

def collect_gc_metrics():
    try:
        if gc.isenabled():
            gc.collect()
        collected = gc.get_stats()[0]["collected"] if hasattr(gc, "get_stats") else 0
        process = psutil.Process()
        memory_usage = process.memory_info().rss / (1024 * 1024)
        process.cpu_percent(interval=None)
        time.sleep(0.1)
        cpu_usage = process.cpu_percent(interval=None)
        thread_count = len(threading.enumerate())
        connections = len(process.connections())

        PYTHON_GC_COLLECTED.set(collected)
        MEMORY_USAGE.set(memory_usage)
        CPU_USAGE.set(cpu_usage)
        THREAD_COUNT.set(thread_count)
        ACTIVE_CONNECTIONS.set(connections)

        logger.info(f"📊 GC: {collected} objetos recolectados")
        logger.info(f"📊 Memoria: {memory_usage:.2f} MB, CPU: {cpu_usage:.2f}%, Hilos: {thread_count}, Conexiones: {connections}")
    except Exception as e:
        logger.error(f"❌ Error en métricas: {str(e)}")

def start_gc_metrics_collection():
    def run():
        while True:
            collect_gc_metrics()
            time.sleep(30)
    threading.Thread(target=run, daemon=True).start()

def update_uptime():
    start_time = time.time()
    while True:
        UPTIME.set(time.time() - start_time)
        time.sleep(10)

def start_metrics_server():
    logger.info(f"🚀 Iniciando servidor de métricas en puerto {METRICS_PORT}")
    start_http_server(METRICS_PORT)

if __name__ == "__main__":
    start_metrics_server()
    start_gc_metrics_collection()
    threading.Thread(target=update_uptime, daemon=True).start()
