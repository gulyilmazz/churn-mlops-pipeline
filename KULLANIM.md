# 🚀 Hızlı Başlangıç Kılavuzu

## Proje Şu Anda Çalışıyor!

### ✅ Durum
- **API**: http://127.0.0.1:8000 (Çalışıyor)
- **UI**: http://localhost:5173 (Çalışıyor)

### 📋 Kullanım Adımları

1. **Tarayıcınızı açın** (Chrome, Firefox, Edge, vb.)

2. **Adres çubuğuna yazın:**
   ```
   http://localhost:5173
   ```

3. **Sayfa açıldığında göreceksiniz:**
   - "Churn Predictor UI" başlığı
   - "API: Connected" (yeşil) veya "API: Not reachable" (kırmızı)
   - Sol tarafta JSON veri giriş alanı
   - Sağ tarafta sonuç alanı

4. **Tahmin yapmak için:**
   - Varsayılan JSON verisini kullanabilir veya değiştirebilirsiniz
   - "Predict" butonuna tıklayın
   - Sağ tarafta tahmin sonucunu göreceksiniz:
     - `pred_label`: "Yes" veya "No" (Müşteri kaybedecek mi?)
     - `pred_proba_yes`: 0.0 ile 1.0 arası olasılık değeri

### 🔍 Sorun Giderme

#### UI açılmıyorsa:

1. **Port kontrolü:**
   ```powershell
   netstat -ano | findstr ":5173"
   ```
   Eğer boşsa, UI çalışmıyor demektir.

2. **UI'yi yeniden başlatın:**
   ```powershell
   cd ui
   npm run dev
   ```

#### "API: Not reachable" görüyorsanız:

1. **API'nin çalıştığını kontrol edin:**
   ```powershell
   # Yeni terminal açın
   .\venv\Scripts\Activate.ps1
   uvicorn src.api.app:app --reload --port 8000
   ```

2. **Tarayıcıda API'yi test edin:**
   ```
   http://127.0.0.1:8000/health
   ```
   `{"status":"ok"}` görmelisiniz.

#### Tarayıcıda hata görüyorsanız:

1. **Konsolu açın:**
   - Chrome/Edge: F12 tuşuna basın
   - Console sekmesine gidin
   - Hataları kontrol edin

2. **Sayfayı yenileyin:**
   - Ctrl + R veya F5

### 📝 Örnek JSON Verisi

```json
{
  "features": {
    "Gender": "Female",
    "Age": 29,
    "Under 30": "No",
    "Senior Citizen": "No",
    "Married": "Yes",
    "Dependents": "No",
    "Number of Dependents": 0,
    "Referred a Friend": "No",
    "Number of Referrals": 0,
    "Tenure in Months": 3,
    "Offer": null,
    "Phone Service": "Yes",
    "Avg Monthly Long Distance Charges": 10.0,
    "Multiple Lines": "No",
    "Internet Service": "Yes",
    "Internet Type": "Fiber Optic",
    "Avg Monthly GB Download": 25,
    "Online Security": "No",
    "Online Backup": "Yes",
    "Device Protection Plan": "No",
    "Premium Tech Support": "No",
    "Streaming TV": "Yes",
    "Streaming Movies": "Yes",
    "Streaming Music": "No",
    "Unlimited Data": "Yes",
    "Contract": "Month-to-Month",
    "Paperless Billing": "Yes",
    "Payment Method": "Bank Withdrawal",
    "Monthly Charge": 95.0,
    "Total Charges": 280.0,
    "Total Refunds": 0.0,
    "Total Extra Data Charges": 0.0,
    "Total Long Distance Charges": 30.0,
    "Total Revenue": 310.0,
    "CLTV": 4000
  }
}
```

### 🔗 Yararlı Linkler

- **UI**: http://localhost:5173
- **API**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs
- **API Health**: http://127.0.0.1:8000/health
- **Sample Data**: http://127.0.0.1:8000/sample

