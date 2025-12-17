"""
Model registry'deki modelleri listele
"""
import os
import json
import glob

def list_models():
    """Artifacts klasöründeki tüm modelleri listele"""
    artifacts_dir = "artifacts"
    
    if not os.path.exists(artifacts_dir):
        print("❌ artifacts klasörü bulunamadı")
        return
    
    # Model dosyalarını bul
    model_files = glob.glob(f"{artifacts_dir}/churn_model_v*.joblib")
    
    if not model_files:
        print("📦 Hiç model bulunamadı")
        return
    
    print("\n" + "="*60)
    print("MODEL REGISTRY")
    print("="*60)
    
    models_info = []
    for model_file in sorted(model_files):
        version = model_file.split("_v")[1].replace(".joblib", "")
        metadata_file = f"{artifacts_dir}/churn_model_v{version}_metadata.json"
        
        info = {
            "version": version,
            "model_file": model_file,
            "metadata_file": metadata_file,
            "exists": os.path.exists(model_file),
            "has_metadata": os.path.exists(metadata_file)
        }
        
        if info["has_metadata"]:
            try:
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
                    info["metadata"] = metadata
            except Exception as e:
                info["metadata_error"] = str(e)
        
        models_info.append(info)
    
    # Modelleri göster
    for info in models_info:
        print(f"\n📦 Model v{info['version']}")
        print(f"   Dosya: {info['model_file']}")
        
        if info["has_metadata"] and "metadata" in info:
            meta = info["metadata"]
            print(f"   Eğitim Tarihi: {meta.get('training_date', 'N/A')}")
            if "metrics" in meta:
                m = meta["metrics"]
                print(f"   Accuracy: {m.get('accuracy', 0):.4f}")
                print(f"   F1 Score: {m.get('f1_score', 0):.4f}")
        else:
            print("   ⚠️ Metadata bulunamadı")
    
    print("\n" + "="*60)
    
    return models_info

if __name__ == "__main__":
    list_models()

