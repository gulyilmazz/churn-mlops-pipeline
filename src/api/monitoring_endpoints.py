"""
Monitoring için API endpoints
"""
from fastapi import APIRouter
from src.api.monitoring import get_recent_predictions, check_drift, PROBABILITY_STATS
import json
from pathlib import Path

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/stats")
def get_stats():
    """Probability istatistiklerini döndür"""
    if not PROBABILITY_STATS.exists():
        return {"error": "İstatistik bulunamadı", "count": 0}
    
    with open(PROBABILITY_STATS, "r") as f:
        stats = json.load(f)
    
    return stats


@router.get("/drift")
def check_drift_endpoint(reference_mean: float = None, threshold: float = 0.1):
    """Drift kontrolü yap"""
    is_drift, drift_info = check_drift(reference_mean=reference_mean, threshold=threshold)
    return drift_info


@router.get("/predictions")
def get_predictions(limit: int = 100):
    """Son prediction'ları döndür"""
    df = get_recent_predictions(n=limit)
    
    if df.empty:
        return {"predictions": [], "count": 0}
    
    # DataFrame'i JSON'a çevir
    predictions = df.to_dict(orient="records")
    
    return {
        "predictions": predictions,
        "count": len(predictions)
    }

