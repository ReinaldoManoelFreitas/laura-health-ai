import pandas as pd
import joblib
import shap
from pathlib import Path

MODEL = Path("models/laura_risk_model.pkl")

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


class LauraModel:

    def __init__(self):

        bundle = joblib.load(MODEL)

        if isinstance(bundle, dict):
            self.model = bundle["model"]
            self.features = bundle["features"]
            self.threshold = bundle.get("threshold", 0.5)
        else:
            self.model = bundle
            self.features = FEATURES
            self.threshold = 0.5

        # SHAP explainer
        self.explainer = shap.TreeExplainer(self.model)

        print("Laura ML loaded")
        print("Features:", self.features)

    def predict(self, payload: dict):

        df = pd.DataFrame([payload])[self.features]

        prob = float(self.model.predict_proba(df)[0][1])

        return prob

    def explain(self, payload: dict, top_k=3):

        df = pd.DataFrame([payload])[self.features]

        shap_values = self.explainer(df)

        values = shap_values.values[0]
        names = self.features

        impacts = sorted(
            zip(names, values),
            key=lambda x: abs(x[1]),
            reverse=True
        )

        drivers = [f for f, _ in impacts[:top_k]]

        return drivers
