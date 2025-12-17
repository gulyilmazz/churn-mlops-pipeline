import os
import joblib
import json
from datetime import datetime

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, f1_score, precision_score, recall_score

from src.data.preprocess import preprocess


def train(version: str = "1"):
    """
    Model eğitimi ve versiyonlama
    
    Args:
        version: Model versiyonu (örn: "1", "2")
    """
    df = pd.read_csv("data/raw/telco.csv")

    X, y, cat_cols, num_cols = preprocess(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    numeric_transformer = Pipeline(steps=[
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, num_cols),
            ("cat", categorical_transformer, cat_cols)
        ]
    )

    model = Pipeline(steps=[
        ("preprocess", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000))
    ])

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # Metrikleri hesapla
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, pos_label="Yes", average="binary")
    precision = precision_score(y_test, y_pred, pos_label="Yes", average="binary", zero_division=0)
    recall = recall_score(y_test, y_pred, pos_label="Yes", average="binary", zero_division=0)

    print("\n" + "="*50)
    print(f"MODEL V{version} - EĞİTİM SONUÇLARI")
    print("="*50)
    print(classification_report(y_test, y_pred))
    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print("="*50 + "\n")

    # Model ve metadata kaydet
    os.makedirs("artifacts", exist_ok=True)
    
    model_filename = f"artifacts/churn_model_v{version}.joblib"
    metadata_filename = f"artifacts/churn_model_v{version}_metadata.json"
    
    # Model kaydet
    joblib.dump(model, model_filename)
    print(f"✅ Model kaydedildi: {model_filename}")
    
    # Metadata kaydet
    metadata = {
        "version": version,
        "training_date": datetime.now().isoformat(),
        "metrics": {
            "accuracy": float(accuracy),
            "f1_score": float(f1),
            "precision": float(precision),
            "recall": float(recall)
        },
        "model_type": "LogisticRegression",
        "preprocessor": {
            "numeric": "StandardScaler",
            "categorical": "OneHotEncoder"
        },
        "train_size": len(X_train),
        "test_size": len(X_test),
        "features_count": len(X.columns),
        "random_state": 42
    }
    
    with open(metadata_filename, "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Metadata kaydedildi: {metadata_filename}")
    
    # Backward compatibility için v1'i churn_model.joblib olarak da kaydet
    if version == "1":
        joblib.dump(model, "artifacts/churn_model.joblib")
        print("✅ Backward compatibility: artifacts/churn_model.joblib")
    
    return model, metadata


if __name__ == "__main__":
    import sys
    version = sys.argv[1] if len(sys.argv) > 1 else "1"
    train(version=version)
