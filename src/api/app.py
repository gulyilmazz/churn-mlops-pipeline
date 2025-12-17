from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import logging
import joblib
import pandas as pd
import numpy as np

from src.data.preprocess import preprocess


# -------------------------
# Environment & Logging
# -------------------------
ENV = os.getenv("ENV", "development")
DEBUG = ENV != "production"

# logs klasörü (production için)
if ENV == "production":
    os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO if ENV == "production" else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/api.log") if ENV == "production" else logging.StreamHandler(),
        logging.StreamHandler(),
    ] if ENV == "production" else None,
)

logger = logging.getLogger(__name__)


# -------------------------
# FastAPI App (TEK)
# -------------------------
app = FastAPI(
    title="Churn MLOps Pipeline API",
    debug=DEBUG
)

logger.info(f"API starting. ENV={ENV}, DEBUG={DEBUG}")


# -------------------------
# CORS
# -------------------------
cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

if ENV == "production":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# -------------------------
# Model + UI Meta Globals
# -------------------------
MODEL_PATH = os.getenv("MODEL_PATH", "artifacts/churn_model.joblib")
DATA_PATH = os.getenv("DATA_PATH", "data/raw/telco.csv")

model = None

EXPECTED_COLS = []
DEFAULTS = {}
CATEGORICAL_OPTIONS = {}
_X_CACHE = None


def _build_expected_cols_from_pipeline(m):
    pre = m.named_steps["preprocess"]  # ColumnTransformer
    cols = []
    for _, _, col_list in pre.transformers_:
        if isinstance(col_list, list):
            cols.extend(col_list)

    seen = set()
    out = []
    for c in cols:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def _compute_defaults_and_options(m):
    """
    Model + dataset varsa UI için meta üretir.
    Model/dataset yoksa boş döner (CI'da import kırılmasın).
    """
    global EXPECTED_COLS, DEFAULTS, CATEGORICAL_OPTIONS, _X_CACHE

    if m is None:
        logger.warning("Meta build skipped: model is not loaded.")
        return

    if not os.path.exists(DATA_PATH):
        logger.warning(f"Meta build skipped: dataset not found at {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    X, _, cat_cols, num_cols = preprocess(df)

    EXPECTED_COLS = _build_expected_cols_from_pipeline(m)

    # defaults: numeric -> median, categorical -> mode
    DEFAULTS = {}
    CATEGORICAL_OPTIONS = {}

    for c in num_cols:
        DEFAULTS[c] = float(pd.to_numeric(X[c], errors="coerce").median())

    for c in cat_cols:
        mode_val = X[c].mode(dropna=True)
        DEFAULTS[c] = str(mode_val.iloc[0]) if len(mode_val) else "Unknown"
        vals = sorted([str(v) for v in X[c].dropna().unique().tolist()])
        CATEGORICAL_OPTIONS[c] = vals[:50]

    _X_CACHE = X
    logger.info("Meta built successfully.")


@app.on_event("startup")
def startup():
    """
    CI'da import test sırasında artifact olmayabilir.
    Bu yüzden burada 'varsa yükle', yoksa servis ayakta kalsın.
    """
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        logger.info(f"Model loaded from: {MODEL_PATH}")
    else:
        model = None
        logger.warning(f"Model not found at: {MODEL_PATH}")

    # model + dataset varsa meta üret
    try:
        _compute_defaults_and_options(model)
    except Exception as e:
        logger.warning(f"Meta build failed (non-blocking): {e}")


class PredictRequest(BaseModel):
    features: dict


@app.get("/health")
def health():
    return {
        "status": "ok",
        "env": ENV,
        "model_loaded": model is not None,
        "meta_ready": bool(EXPECTED_COLS),
    }


@app.post("/predict")
def predict(req: PredictRequest):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail=f"Model artifact not loaded. Expected at {MODEL_PATH}. Train/build artifacts first.",
        )

    incoming = req.features or {}

    # Eğer meta hazır değilse minimum güvenli fallback:
    # (Normalde meta startup'ta doluyor)
    if not EXPECTED_COLS:
        raise HTTPException(
            status_code=503,
            detail="Meta not ready (EXPECTED_COLS empty). Ensure dataset exists and restart API.",
        )

    row = {}
    for col in EXPECTED_COLS:
        val = incoming.get(col, None)
        if val is None or (isinstance(val, str) and val.strip() == ""):
            val = DEFAULTS.get(col)

        # sayısal default varsa float'a çevir
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

    # Monitoring: hata olursa ana akış bozulmasın
    try:
        from src.api.monitoring import log_prediction, update_probability_stats
        log_prediction({"features": incoming}, response_data)
        update_probability_stats(pred_proba_yes)
    except Exception as e:
        logger.warning(f"Monitoring error (ignored): {e}")

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
    if _X_CACHE is None or not EXPECTED_COLS:
        raise HTTPException(status_code=503, detail="Sample not ready. Meta not built yet.")
    row = _X_CACHE.sample(1, random_state=42).iloc[0].to_dict()

    clean = {}
    for k, v in row.items():
        if pd.isna(v):
            clean[k] = DEFAULTS.get(k)
        elif isinstance(v, (np.integer, np.floating)):
            clean[k] = float(v)
        else:
            clean[k] = v

    return {"features": clean}


# Monitoring endpoints
from src.api.monitoring_endpoints import router as monitoring_router
app.include_router(monitoring_router)
