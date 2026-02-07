import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt
from pathlib import Path

DATA = Path("data/maternal/maternal_features.parquet")
MODEL = Path("models/laura_risk_model.pkl")
OUT = Path("models")

SAMPLE = 2000

FEATURES = [
    "IDADEMAE",
    "ESCMAE",
    "RACACOR",
    "CONSPRENAT",
    "MESPRENAT",
    "GESTACAO",
    "SEMAGESTAC",
    "PARTO",
    "PESO",
    "APGAR1",
    "APGAR5",
    "QTDFILVIVO",
    "QTDFILMORT"
]


def main():
    print("\n=== LAURA SHAP EXPLAINER ===\n")

    print("Loading data...")
    df = pd.read_parquet(DATA)

    print("Loading model...")
    print("Loading model...")
    bundle = joblib.load(MODEL)
    model = bundle["model"]

    features = bundle.get("features", FEATURES)

    print("Features:", features)

    X = df[features].astype("float32")

    # amostra pequena
    X_sample = X.sample(SAMPLE, random_state=42)

    print("Samples SHAP:", len(X_sample))

    print("Building SHAP explainer...")

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(X_sample)

    print("Saving plots...")

    # Summary plot
    shap.summary_plot(
        shap_values,
        X_sample,
        show=False
    )
    plt.tight_layout()
    plt.savefig(OUT / "shap_summary.png", dpi=200)
    plt.close()

    # Bar plot
    shap.summary_plot(
        shap_values,
        X_sample,
        plot_type="bar",
        show=False
    )
    plt.tight_layout()
    plt.savefig(OUT / "shap_bar.png", dpi=200)
    plt.close()

    print("\nSHAP saved:")
    print("→ models/shap_summary.png")
    print("→ models/shap_bar.png")


if __name__ == "__main__":
    main()
