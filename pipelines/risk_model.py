import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve
from xgboost import XGBClassifier
import joblib

DATA = Path("data/maternal/maternal_features.parquet")
MODEL_PATH = Path("models")
MODEL_PATH.mkdir(exist_ok=True)

FEATURES = [
    "IDADEMAE",
    "ESCMAE",
    "CONSPRENAT",
    "MESPRENAT",
    "SEMAGESTAC",
    "PESO",
]

TARGET = "APGAR_CRITICO"


def main():
    print("\n=== LAURA Risk Model v2 ===\n")

    df = pd.read_parquet(DATA)

    df = df[FEATURES + [TARGET]].dropna()

    X = df[FEATURES]
    y = df[TARGET].astype(int)

    print("Samples:", len(df))
    print("Positive rate:", y.mean())

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    scale = (len(y_train) - y_train.sum()) / y_train.sum()

    print("Scale pos weight:", scale)

    model = XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        scale_pos_weight=scale,
        tree_method="hist",
    )

    print("Training model...")
    model.fit(X_train, y_train)

    probs = model.predict_proba(X_test)[:, 1]

    # Auto threshold via F1
    precision, recall, thresholds = precision_recall_curve(y_test, probs)

    f1 = 2 * (precision * recall) / (precision + recall + 1e-8)
    best_idx = np.argmax(f1)
    best_threshold = thresholds[best_idx]

    print("\nBest threshold:", best_threshold)

    preds = (probs > best_threshold).astype(int)

    print("\nClassification report:\n")
    print(classification_report(y_test, preds))

    auc = roc_auc_score(y_test, probs)
    print("ROC AUC:", auc)

    # Persist model + threshold
    joblib.dump(
        {
            "model": model,
            "threshold": float(best_threshold),
            "features": FEATURES,
        },
        MODEL_PATH / "laura_risk_model.pkl",
    )

    print("\nModel + threshold saved:", MODEL_PATH / "laura_risk_model.pkl")


if __name__ == "__main__":
    main()
