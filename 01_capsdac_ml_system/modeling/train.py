import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from config import DATA_DIR, MODELS_DIR, TARGET_COLUMN, RANDOM_STATE

def load_split():
    train_df = pd.read_csv(DATA_DIR / "train_features.csv")
    test_df = pd.read_csv(DATA_DIR / "test_features.csv")

    X_train = train_df.drop(columns=[TARGET_COLUMN])
    y_train = train_df[TARGET_COLUMN]

    X_test = test_df.drop(columns=[TARGET_COLUMN])
    y_test = test_df[TARGET_COLUMN]
    return X_train, X_test, y_train, y_test

def evaluate(model, X_test, y_test, name: str) -> None:
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]

    print(f"\n{name}")
    print(f"Accuracy: {accuracy_score(y_test, preds):.4f}")
    print(f"ROC AUC:  {roc_auc_score(y_test, probs):.4f}")

def main() -> None:
    X_train, X_test, y_train, y_test = load_split()

    rf = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_leaf=5,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)
    evaluate(rf, X_test, y_test, "Random Forest")

    xgb = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        random_state=RANDOM_STATE,
    )
    xgb.fit(X_train, y_train)
    evaluate(xgb, X_test, y_test, "XGBoost")

    joblib.dump(rf, MODELS_DIR / "random_forest.joblib")
    joblib.dump(xgb, MODELS_DIR / "xgboost.joblib")
    joblib.dump(list(X_train.columns), MODELS_DIR / "feature_columns.joblib")

    print("Saved models and feature metadata.")

if __name__ == "__main__":
    main()
