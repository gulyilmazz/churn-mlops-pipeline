import pandas as pd
from src.data.preprocess import preprocess
import json

df = pd.read_csv("data/raw/telco.csv")
X, _, _, _ = preprocess(df)

sample = X.sample(1, random_state=42).iloc[0].to_dict()
print(json.dumps({"features": sample}, ensure_ascii=False, indent=2))
