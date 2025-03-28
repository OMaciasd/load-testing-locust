FROM jaegertracing/all-in-one:1.55.0

LABEL maintainer="omaciasd <omaciasnarvaez@gmail.com>" \
 description="Jaeger All-in-One con configuración personalizada"

USER root
RUN apk add --no-cache curl=8.5.0-r0

WORKDIR /etc/jaeger

COPY --chmod=644 ./jaeger-config.yaml jaeger-config.yaml
COPY --chmod=644 ./sampling.json sampling.json

USER jaeger

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=10s \
 CMD curl -fsS http://localhost:16686 || exit 1

EXPOSE 5775/udp 6831/udp 6832/udp 5778 16686 14250 14268 9411

ENTRYPOINT ["sh", "-c", "exec all-in-one-linux"]
