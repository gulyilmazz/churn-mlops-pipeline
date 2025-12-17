# 🔒 GitHub'da Görünmemesi Gerekenler

## ⚠️ ÖNEMLİ: GitHub'da Olmaması Gereken Dosyalar

### 1. 📊 Büyük Veri Dosyaları
**`data/raw/telco.csv`** - ~7MB+
- ✅ **ÇÖZÜM**: .gitignore'a ekle
- 💡 **Neden**: Büyük dosyalar repo'yu şişirir, clone/pull yavaşlar
- 📝 **Alternatif**: 
  - Veriyi external storage'a koy (S3, Google Drive)
  - veya README'de veri kaynağını belirt

### 2. 🤖 Model Dosyaları
**`artifacts/churn_model.joblib`** - Model dosyası
- ✅ **ÇÖZÜM**: .gitignore'a ekle (şu anda yorum satırında)
- 💡 **Neden**: Model dosyaları büyük, sık değişir
- 📝 **Alternatif**:
  - Model versioning için farklı bir sistem kullan
  - veya GitHub LFS (Large File Storage) kullan
  - veya model'i CI/CD ile build et

### 3. ✅ Zaten .gitignore'da Olanlar (İyi!)
- `venv/` - Virtual environment ✅
- `node_modules/` - Node packages ✅
- `*.log` - Log dosyaları ✅
- `monitoring/` - Monitoring logları ✅
- `.env` - Environment variables ✅

---

## 🔧 ÖNERİLEN .gitignore GÜNCELLEMESİ

```gitignore
# Büyük veri dosyaları
data/raw/*.csv
data/raw/*.xlsx
data/raw/*.parquet

# Model artifacts (büyük dosyalar)
artifacts/*.joblib
artifacts/*.pkl
artifacts/*.h5

# Ama README ve metadata dosyalarını tut
!artifacts/README.md
!artifacts/*_metadata.json
```

---

## 📋 KONTROL LİSTESİ

GitHub'a push etmeden önce kontrol edin:

- [ ] `data/raw/telco.csv` .gitignore'da mı?
- [ ] `artifacts/*.joblib` .gitignore'da mı?
- [ ] `.env` dosyası var mı? (varsa eklenmemeli)
- [ ] `venv/` klasörü eklenmemiş mi?
- [ ] `node_modules/` eklenmemiş mi?
- [ ] Log dosyaları (.log) eklenmemiş mi?
- [ ] Monitoring dosyaları eklenmemiş mi?

---

## 🚨 EĞER ZATEN EKLENDİYSE

Eğer bu dosyalar zaten commit edildiyse:

```bash
# Dosyayı git'ten kaldır ama yerel dosyayı koru
git rm --cached data/raw/telco.csv
git rm --cached artifacts/churn_model.joblib

# .gitignore'ı güncelle
# Sonra commit
git commit -m "Remove large files from git tracking"
git push
```

⚠️ **DİKKAT**: Eğer dosyalar zaten push edildiyse, geçmiş commit'lerden silmek için `git filter-branch` veya `git-filter-repo` gerekebilir.

