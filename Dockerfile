FROM python:3.12-slim

ARG DEBIAN_FRONTEND=noninteractive

# Crear usuario sin privilegios
RUN set -eux; \
  groupadd --system mygroup && \
  useradd --system --no-create-home --gid mygroup myuser

WORKDIR /mnt/locust

RUN set -eux; \
  apt-get update && apt-get install --yes --no-install-recommends \
  supervisor=4.2.5-1 \
  curl=7.68.0-1ubuntu2.18 \
  && rm -rf /var/lib/apt/lists/*

# Configurar variables de entorno
ENV PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PYTHONUNBUFFERED=1 \
  VIRTUAL_ENV="/opt/venv" \
  PATH="/opt/venv/bin:$PATH"

RUN set -eux; \
  python -m venv $VIRTUAL_ENV && \
  $VIRTUAL_ENV/bin/pip install --no-cache-dir --upgrade pip

COPY requirements.txt ./ \
  logrotate.conf /etc/logrotate.conf \
  supervisord.conf /etc/supervisor/supervisord.conf \
  ./scripts/ /mnt/locust/scripts/

RUN set -eux; \
  $VIRTUAL_ENV/bin/pip install --no-cache-dir -r requirements.txt

# Cambiar a usuario sin privilegios
USER myuser

EXPOSE 8089

# Healthcheck con reintentos
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8089 || exit 1

# Ejecutar supervisord con exec para manejar señales correctamente
CMD [ "exec", "supervisord", "-c", "/etc/supervisor/supervisord.conf" ]
