"""
Monitoring ve logging modülü
Prediction request'leri ve probability dağılımlarını kaydeder
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import pandas as pd
import numpy as np

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Monitoring dosya yolları
MONITORING_DIR = Path("monitoring")
PREDICTIONS_LOG = MONITORING_DIR / "predictions.log"
PROBABILITY_STATS = MONITORING_DIR / "probability_stats.json"

# Monitoring klasörünü oluştur
MONITORING_DIR.mkdir(exist_ok=True)


def log_prediction(request_data: Dict[str, Any], response_data: Dict[str, Any]):
    """
    Prediction request ve response'u logla
    
    Args:
        request_data: API'ye gelen request verisi
        response_data: API'den dönen response verisi
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "request": {
            "features_count": len(request_data.get("features", {})),
        },
        "response": {
            "pred_label": response_data.get("pred_label"),
            "pred_proba_yes": response_data.get("pred_proba_yes"),
        }
    }
    
    # JSON formatında log dosyasına yaz
    with open(PREDICTIONS_LOG, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    logger.info(f"Prediction logged: {response_data.get('pred_label')} (prob: {response_data.get('pred_proba_yes'):.4f})")


def update_probability_stats(probability: float):
    """
    Probability istatistiklerini güncelle
    
    Args:
        probability: Tahmin olasılığı (0-1 arası)
    """
    # Mevcut istatistikleri yükle
    if PROBABILITY_STATS.exists():
        try:
            with open(PROBABILITY_STATS, "r") as f:
                stats = json.load(f)
        except Exception:
            stats = {
                "count": 0,
                "sum": 0.0,
                "mean": 0.0,
                "min": 1.0,
                "max": 0.0,
                "updated_at": None
            }
    else:
        stats = {
            "count": 0,
            "sum": 0.0,
            "mean": 0.0,
            "min": 1.0,
            "max": 0.0,
            "updated_at": None
        }
    
    # İstatistikleri güncelle
    stats["count"] += 1
    stats["sum"] += probability
    stats["mean"] = stats["sum"] / stats["count"]
    stats["min"] = min(stats["min"], probability)
    stats["max"] = max(stats["max"], probability)
    stats["updated_at"] = datetime.now().isoformat()
    
    # Kaydet
    with open(PROBABILITY_STATS, "w") as f:
        json.dump(stats, f, indent=2)
    
    return stats


def check_drift(reference_mean: float = None, threshold: float = 0.1):
    """
    Basit drift kontrolü - ortalama değişti mi?
    
    Args:
        reference_mean: Referans ortalama (eğitim sırasındaki ortalama)
        threshold: Drift eşiği (default: 0.1 = %10)
    
    Returns:
        bool: Drift tespit edildi mi?
        dict: Drift bilgileri
    """
    if not PROBABILITY_STATS.exists():
        return False, {"error": "İstatistik bulunamadı"}
    
    with open(PROBABILITY_STATS, "r") as f:
        stats = json.load(f)
    
    current_mean = stats.get("mean", 0.0)
    
    # Referans mean yoksa drift kontrolü yapılamaz
    if reference_mean is None:
        return False, {
            "current_mean": current_mean,
            "note": "Referans ortalama belirtilmedi"
        }
    
    # Drift kontrolü
    drift_amount = abs(current_mean - reference_mean)
    is_drift = drift_amount > threshold
    
    drift_info = {
        "is_drift": is_drift,
        "reference_mean": reference_mean,
        "current_mean": current_mean,
        "drift_amount": drift_amount,
        "threshold": threshold,
        "count": stats.get("count", 0)
    }
    
    if is_drift:
        logger.warning(f"⚠️ DRIFT TESPİT EDİLDİ! Ortalama değişti: {reference_mean:.4f} -> {current_mean:.4f}")
    
    return is_drift, drift_info


def get_recent_predictions(n: int = 100) -> pd.DataFrame:
    """
    Son N prediction'ı pandas DataFrame olarak döndür
    
    Args:
        n: Kaç prediction alınacak
    
    Returns:
        pd.DataFrame: Prediction logları
    """
    if not PREDICTIONS_LOG.exists():
        return pd.DataFrame()
    
    # Log dosyasından son N satırı oku
    predictions = []
    try:
        with open(PREDICTIONS_LOG, "r") as f:
            lines = f.readlines()
            for line in lines[-n:]:
                try:
                    pred = json.loads(line.strip())
                    predictions.append(pred)
                except json.JSONDecodeError:
                    continue
        
        if predictions:
            df = pd.json_normalize(predictions)
            return df
    except Exception as e:
        logger.error(f"Error reading predictions log: {e}")
    
    return pd.DataFrame()

