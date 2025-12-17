# Churn Prediction API Dockerfile
# Multi-stage build için Python 3.10 slim image kullanıyoruz
FROM python:3.10-slim

# Working directory
WORKDIR /app

# Sistem bağımlılıkları (gerekirse)
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY src/ ./src/
COPY data/ ./data/
COPY artifacts/ ./artifacts/

# Port expose et
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Uvicorn ile API'yi başlat
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]

