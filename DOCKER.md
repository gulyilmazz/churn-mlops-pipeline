# 🐳 Docker Kullanım Kılavuzu

## Hızlı Başlangıç

### Tüm Servisleri Başlat (API + UI)

```bash
docker-compose up --build
```

Bu komut:
- API container'ını oluşturur ve başlatır (port 8000)
- UI container'ını oluşturur ve başlatır (port 5173)
- Container'lar arası network kurar

### Arka Planda Çalıştır

```bash
docker-compose up -d
```

### Durum Kontrolü

```bash
docker-compose ps
```

### Logları Görüntüle

```bash
# Tüm servisler
docker-compose logs -f

# Sadece API
docker-compose logs -f api

# Sadece UI
docker-compose logs -f ui
```

### Durdur

```bash
docker-compose down
```

## Tek Başına API Container'ı

### Build

```bash
docker build -t churn-api .
```

### Run

```bash
docker run -p 8000:8000 \
  -v $(pwd)/artifacts:/app/artifacts:ro \
  -v $(pwd)/data:/app/data:ro \
  -e ENV=production \
  churn-api
```

Windows PowerShell için:
```powershell
docker run -p 8000:8000 `
  -v ${PWD}/artifacts:/app/artifacts:ro `
  -v ${PWD}/data:/app/data:ro `
  -e ENV=production `
  churn-api
```

## Docker Image Yapısı

### API Image
- **Base**: Python 3.10-slim
- **Port**: 8000
- **Health Check**: `/health` endpoint'i
- **Volume Mounts**: 
  - `artifacts/` (model dosyası - read-only)
  - `data/` (veri dosyaları - read-only)

### UI Image
- **Base**: Node 18-alpine
- **Port**: 5173
- **Environment**: `VITE_API_URL` (API adresi)

## Environment Variables

### API
- `ENV`: `development` veya `production` (default: `development`)
  - Production'da debug kapalı, CORS daha sıkı

### UI
- `VITE_API_URL`: API'nin erişilebilir adresi (default: `http://localhost:8000`)

## Troubleshooting

### Container başlamıyor
```bash
# Logları kontrol et
docker-compose logs api

# Container'ı yeniden build et
docker-compose build --no-cache api
```

### Port kullanımda
```bash
# Hangi process kullanıyor kontrol et
netstat -ano | findstr :8000

# docker-compose.yml'de portu değiştir
```

### Model dosyası bulunamıyor
```bash
# artifacts klasörünün varlığını kontrol et
ls artifacts/

# Model varsa, volume mount'un doğru olduğundan emin ol
docker-compose exec api ls /app/artifacts
```

## Production Deployment

Production'da kullanmak için:

1. **Environment variable ayarla:**
   ```yaml
   environment:
     - ENV=production
   ```

2. **Health check kullan:**
   Container'lar otomatik health check yapar.

3. **Volume yerine COPY kullan (opsiyonel):**
   Model dosyasını image içine kopyalamak için Dockerfile'ı güncelleyin.

## Neden Docker?

✅ **Reproducibility**: Her yerde aynı ortam  
✅ **Isolation**: Sistem bağımlılıklarından bağımsız  
✅ **Deployment Ready**: Container orchestration (Kubernetes, Docker Swarm) için hazır  
✅ **Version Control**: Her image versiyonu kaydedilebilir  
✅ **CI/CD**: Otomatik build ve test için uygun

