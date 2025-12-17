import pandas as pd

TARGET = "Churn Label"

DROP_COLUMNS = [
    "Customer ID",
    "Country", "State", "City", "Zip Code",
    "Latitude", "Longitude", "Population", "Quarter",
    "Customer Status", "Churn Score", "Churn Category",
    "Churn Reason", "Satisfaction Score"
]

def preprocess(df: pd.DataFrame):
    df = df.copy()

    y = df[TARGET]
    X = df.drop(columns=[TARGET] + DROP_COLUMNS)

    categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
    numerical_cols = X.select_dtypes(exclude=["object"]).columns.tolist()

    return X, y, categorical_cols, numerical_cols


if __name__ == "__main__":
    df = pd.read_csv("data/raw/telco.csv")
    X, y, cat_cols, num_cols = preprocess(df)

    print("Target distribution:\n", y.value_counts())
    print("\nCategorical columns:", cat_cols)
    print("\nNumerical columns:", num_cols)
