# 🚀 Projeyi Çalıştırma Kılavuzu

## Hızlı Başlangıç

### Yöntem 1: PowerShell Script'leri ile (Önerilen)

**1. API'yi başlatmak için:**
```powershell
.\start_api.ps1
```

**2. UI'yi başlatmak için (yeni bir terminal penceresi açın):**
```powershell
.\start_ui.ps1
```

### Yöntem 2: Manuel Çalıştırma

#### Adım 1: API'yi Başlat

Bir PowerShell/Command Prompt terminali açın ve şu komutları çalıştırın:

```powershell
# Virtual environment'ı aktif et
.\venv\Scripts\Activate.ps1

# API'yi başlat
uvicorn src.api.app:app --reload --port 8000
```

API başarıyla çalışıyorsa şu mesajı göreceksiniz:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

API dokümantasyonu: http://127.0.0.1:8000/docs

#### Adım 2: UI'yi Başlat

**Yeni bir terminal penceresi açın** ve şu komutları çalıştırın:

```powershell
cd ui
npm run dev
```

UI başarıyla çalışıyorsa şu mesajı göreceksiniz:
```
  VITE v7.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

#### Adım 3: Tarayıcıda Aç

1. Tarayıcınızda http://localhost:5173 adresine gidin
2. "API: Connected" yazısını görmelisiniz
3. JSON formatında veri girin veya varsayılan veriyi kullanın
4. "Predict" butonuna tıklayın

## Sorun Giderme

### API başlamıyorsa:

1. **Model dosyası kontrolü:**
   ```powershell
   Test-Path artifacts\churn_model.joblib
   ```
   Eğer `False` dönerse, önce modeli eğitin:
   ```powershell
   python src/models/train.py
   ```

2. **Bağımlılıkları kontrol edin:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Port 8000 kullanımda mı?**
   - Farklı bir port kullanmak için: `uvicorn src.api.app:app --reload --port 8001`
   - UI'deki API adresini de değiştirmeyi unutmayın

### UI başlamıyorsa:

1. **Node modules kontrolü:**
   ```powershell
   cd ui
   npm install
   ```

2. **Port 5173 kullanımda mı?**
   - Vite otomatik olarak başka bir port seçecektir
   - Terminal çıktısında gösterilen portu kullanın

### API'ye bağlanamıyorsa:

1. UI'deki API adresini kontrol edin (ui/src/App.jsx içinde `const API = "http://127.0.0.1:8000"`)
2. API'nin çalıştığından emin olun: http://127.0.0.1:8000/health
3. CORS ayarlarını kontrol edin (app.py içinde `allow_origins`)

## Geliştirme Notları

- API otomatik reload ile çalışır (kod değişikliklerinde yeniden başlar)
- UI hot module replacement (HMR) ile çalışır
- Her iki servisi de ayrı terminal pencerelerinde çalıştırmanız gerekir

