from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
 OTLPSpanExporter
)
from opentelemetry.sdk.trace.export import (
 BatchSpanProcessor, ConsoleSpanExporter
)
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import trace

tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)

console_exporter = ConsoleSpanExporter()
tracer_provider.add_span_processor(BatchSpanProcessor(console_exporter))

# Exportador OTLP a Jaeger/OTEL Collector
otlp_exporter = OTLPSpanExporter(
 endpoint="http://localhost:4317", insecure=True
)
tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# Obtener el tracer
tracer = trace.get_tracer("CCoinsUser", "1.0.0")
