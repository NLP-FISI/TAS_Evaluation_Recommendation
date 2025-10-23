# Dockerfile para FastAPI con ML (scikit-learn)

# =============================================================================
# STAGE 1: Builder - Instala dependencias
# =============================================================================
FROM python:3.11-slim as builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Instala dependencias del sistema para compilar paquetes científicos
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia solo requirements.txt (para aprovechar cache de Docker)
COPY requirements.txt .

# Instala dependencias Python en /opt/venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# =============================================================================
# STAGE 2: Runtime - Imagen final optimizada
# =============================================================================
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"

# Instala solo las librerías runtime necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Crea usuario no-root para seguridad
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copia el entorno virtual desde el builder
COPY --from=builder /opt/venv /opt/venv

# Copia el código de la aplicación
COPY --chown=appuser:appuser ./app ./app

# Cambia al usuario no-root
USER appuser

# Expone el puerto
EXPOSE 8000

# Health check para Azure Container Apps
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/', timeout=2)"

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]