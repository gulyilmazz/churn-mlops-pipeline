# Model Registry

Bu klasör eğitilmiş modelleri saklar.

## Model Versiyonlama

Model dosyaları şu formatta isimlendirilir:
- `churn_model_v{version}.joblib`
- Örnek: `churn_model_v1.joblib`, `churn_model_v2.joblib`

## Model Metadata

Her model için bir metadata dosyası tutulur:
- `churn_model_v{version}_metadata.json`

## Mevcut Modeller

### v1 (churn_model.joblib)
- **Eğitim Tarihi**: [Eğitim scripti çalıştırıldığında otomatik eklenir]
- **Accuracy**: [Train scripti output'undan]
- **Model Type**: Logistic Regression
- **Preprocessor**: StandardScaler + OneHotEncoder
- **Notlar**: İlk model versiyonu

