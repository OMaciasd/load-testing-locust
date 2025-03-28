import os
import yaml
import logging
import gc
from prometheus_client import Counter, Histogram
from river.anomaly import HalfSpaceTrees
from dotenv import load_dotenv
from locust import HttpUser, task, between


def load_config():
    load_dotenv()
    try:
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


config = load_config()

LOG_FILE = os.getenv("LOG_FILE", config.get("log_file", "app.log"))
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_env_variable(var_name, default=None, required=False, cast=str):
    value = os.getenv(var_name, config.get(var_name, default))
    if required and value is None:
        raise ValueError(f"⚠️ The variable '{var_name}' is required.")
    try:
        return cast(value)
    except ValueError:
        logger.warning(f"⚠️ Invalid value for {var_name}, using {default}")
        return default


MAX_DELAY = get_env_variable("MAX_DELAY", required=True, cast=int)
METRICS_PORT = get_env_variable("METRICS_PORT", required=True, cast=int)
WINDOW_SIZE = get_env_variable("HST_WINDOW_SIZE", required=True, cast=int)
N_TREES = get_env_variable("HST_N_TREES", required=True, cast=int)
HEIGHT = get_env_variable("HST_HEIGHT", required=True, cast=int)
ANOMALY_THRESHOLD = config.get("anomaly", {}).get("threshold", 0.5)

gc.set_threshold(
    get_env_variable("GC_THRESHOLD_0", 700, cast=int),
    get_env_variable("GC_THRESHOLD_1", 10, cast=int),
    get_env_variable("GC_THRESHOLD_2", 10, cast=int),
)

hst = HalfSpaceTrees(window_size=WINDOW_SIZE, n_trees=N_TREES, height=HEIGHT)

METRICS = {
    "request_failures": Counter(
        "request_failures_total", "Total request failures", ["endpoint"]
    ),
    "request_latency": Histogram(
        "http_request_duration_seconds",
        "Response time", ["endpoint", "status_code"]
    ),
    "anomalies_detected": Counter(
        "anomalies_detected", "Detected anomalies"
    ),
}


class LoadTestUser(HttpUser):
    wait_time = between(1, MAX_DELAY)

    @task
    def test_endpoint(self):
        endpoint = "/api/data"
        with self.client.get(endpoint, catch_response=True) as response:
            latency = response.elapsed.total_seconds()
            METRICS[
                "request_latency"
            ].labels(
                endpoint=endpoint, status_code=response.status_code
            ).observe(latency)

            score = hst.score_one({"latency": latency})
            if score > ANOMALY_THRESHOLD:
                METRICS["anomalies_detected"].inc()
                logger.warning(
                    f"⚠️ Anomaly detected in {endpoint}:"
                    "{score:.3f} (latency: {latency}s)"
                )

            if response.status_code != 200:
                METRICS["request_failures"].labels(endpoint=endpoint).inc()
                response.failure(
                    f"Failure in {endpoint}: {response.status_code}"
                )


if __name__ == "__main__":
    import locust
    locust.run_single_user(LoadTestUser)
