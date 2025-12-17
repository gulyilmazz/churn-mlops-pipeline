from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from src.data.preprocess import preprocess
import numpy as np
import os
import logging

# Environment değişkenleri
ENV = os.getenv("ENV", "development")
DEBUG = ENV != "production"

# Logging yapılandırması
if ENV == "production":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/api.log'),
            logging.StreamHandler()
        ]
    )
else:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Churn MLOps Pipeline API",
    debug=DEBUG
)

# Logs klasörünü oluştur (production için)
if ENV == "production":
    os.makedirs("logs", exist_ok=True)
    logger.info(f"🚀 API başlatıldı - Environment: {ENV}")
else:
    logger.debug(f"🔧 Development mode - Debug: {DEBUG}")

from fastapi.middleware.cors import CORSMiddleware

# CORS ayarları - environment'a göre
cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Production'da daha sıkı, development'ta daha açık
if ENV == "production":
    # Production'da sadece belirli origin'ler
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
else:
    # Development'ta daha açık
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Modeli bir kez yükle (startup'ta)
model = joblib.load("artifacts/churn_model.joblib")

# ---- UI Meta (demo için) ----
EXPECTED_COLS = []
DEFAULTS = {}
CATEGORICAL_OPTIONS = {}

def _build_expected_cols_from_pipeline(m):
    pre = m.named_steps["preprocess"]  # ColumnTransformer
    cols = []
    for name, transformer, col_list in pre.transformers_:
        if isinstance(col_list, list):
            cols.extend(col_list)
    # unique & stable order
    seen = set()
    out = []
    for c in cols:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out

def _compute_defaults_and_options():
    global EXPECTED_COLS, DEFAULTS, CATEGORICAL_OPTIONS

    df = pd.read_csv("data/raw/telco.csv")
    X, _, cat_cols, num_cols = preprocess(df)

    EXPECTED_COLS = _build_expected_cols_from_pipeline(model)

    # defaults: numeric -> median, categorical -> mode
    for c in num_cols:
        DEFAULTS[c] = float(pd.to_numeric(X[c], errors="coerce").median())

    for c in cat_cols:
        mode_val = X[c].mode(dropna=True)
        DEFAULTS[c] = str(mode_val.iloc[0]) if len(mode_val) else "Unknown"

        vals = sorted([str(v) for v in X[c].dropna().unique().tolist()])
        # çok uzunsa kısalt (demo için)
        CATEGORICAL_OPTIONS[c] = vals[:50]

    return X

# Uygulama açılırken meta hazırla
_X_CACHE = _compute_defaults_and_options()

class PredictRequest(BaseModel):
    # Bu input'u basit tutuyoruz: tüm feature'lar dict olarak gelecek
    features: dict


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: PredictRequest):
    from src.api.monitoring import log_prediction, update_probability_stats
    
    incoming = req.features or {}

    # Beklenen kolonları doldur + sırala
    row = {}
    for col in EXPECTED_COLS:
        val = incoming.get(col, None)
        if val is None or (isinstance(val, str) and val.strip() == ""):
            val = DEFAULTS.get(col)

        # sayısalsa float'a çevir
        if col in DEFAULTS and isinstance(DEFAULTS[col], float):
            try:
                val = float(val)
            except Exception:
                val = DEFAULTS[col]

        row[col] = val

    X = pd.DataFrame([row], columns=EXPECTED_COLS)

    pred_label = model.predict(X)[0]
    pred_proba_yes = float(model.predict_proba(X)[:, 1][0])

    response_data = {"pred_label": pred_label, "pred_proba_yes": pred_proba_yes}
    
    # Monitoring: Log prediction ve istatistikleri güncelle
    try:
        log_prediction({"features": incoming}, response_data)
        update_probability_stats(pred_proba_yes)
    except Exception as e:
        # Monitoring hatası ana işlevi etkilemesin
        logger.warning(f"Monitoring hatası: {e}")

    return response_data

@app.get("/meta")
def meta():
    return {
        "expected_cols": EXPECTED_COLS,
        "defaults": DEFAULTS,
        "categorical_options": CATEGORICAL_OPTIONS,
    }

@app.get("/sample")
def sample():
    # UI için: modelin beklediği kolonlarla örnek kayıt
    row = _X_CACHE.sample(1, random_state=42).iloc[0].to_dict()
    # numpy türlerini JSON'a uygun hale getir
    clean = {}
    for k, v in row.items():
        if pd.isna(v):
            clean[k] = DEFAULTS.get(k)
        elif isinstance(v, (np.integer, np.floating)):
            clean[k] = float(v)
        else:
            clean[k] = v
    return {"features": clean}

# Monitoring endpoints'i ekle
from src.api.monitoring_endpoints import router as monitoring_router
app.include_router(monitoring_router)
