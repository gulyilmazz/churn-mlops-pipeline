import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df

if __name__ == "__main__":
    data_path = "data/raw/telco.csv"
    df = load_data(data_path)
    print(df.head())
    print("\nShape:", df.shape)
    print("\nColumns:", list(df.columns))
