import pandas as pd
import joblib
from src.data.preprocess import preprocess

if __name__ == "__main__":
    # Load trained model
    model = joblib.load("artifacts/churn_model.joblib")

    # Load raw data
    df = pd.read_csv("data/raw/telco.csv")

    # Apply same preprocessing as training
    X, _, _, _ = preprocess(df)

    # Take a random sample
    sample = X.sample(10, random_state=42)

    # Run inference
    preds = model.predict(sample)
    proba = model.predict_proba(sample)[:, 1]

    # Show results
    out = sample.copy()
    out["pred_label"] = preds
    out["pred_proba_yes"] = proba

    print(out[["pred_label", "pred_proba_yes"]])
