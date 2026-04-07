import pandas as pd
from sklearn.model_selection import train_test_split
from config import DATA_DIR, TARGET_COLUMN, RANDOM_STATE

CATEGORICAL_COLS = [
    "GenderCode",
    "PrimaryLanguageCode",
    "ProgramType",
]

NUMERIC_COLS = [
    "Age",
    "Capacity",
    "IEPIndicator",
    "CalWORKsIndicator",
]

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    for col in CATEGORICAL_COLS:
        df[col] = df[col].fillna("Unknown").astype(str)
    df[TARGET_COLUMN] = pd.to_numeric(df[TARGET_COLUMN], errors="coerce").fillna(0).astype(int)
    return df

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_data(df)
    X = pd.get_dummies(df[CATEGORICAL_COLS + NUMERIC_COLS], drop_first=False)
    y = df[TARGET_COLUMN]
    feature_df = X.copy()
    feature_df[TARGET_COLUMN] = y.values
    return feature_df

def main() -> None:
    raw_path = DATA_DIR / "raw_capsdac.csv"
    df = pd.read_csv(raw_path)
    feature_df = build_features(df)

    train_df, test_df = train_test_split(
        feature_df,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=feature_df[TARGET_COLUMN],
    )

    train_df.to_csv(DATA_DIR / "train_features.csv", index=False)
    test_df.to_csv(DATA_DIR / "test_features.csv", index=False)
    print("Saved train/test feature files.")

if __name__ == "__main__":
    main()
