from fastapi import FastAPI, HTTPException
from app.ml.inference import LauraModel
from app.domain.clinical import build_clinical_report
from app.persistence.repository import save_report
from app.schemas.maternal import MaternalInput

app = FastAPI(
    title="LAURA Health AI",
    description="Predição de risco materno-neonatal",
    version="1.0"
)

model = LauraModel()


@app.post("/predict")
def predict(data: MaternalInput):
    try:
        # 1. Inferência ML
        score = model.predict(data.dict())

        # 2. Camada clínica
        report = build_clinical_report(data.dict(), score)

        # 3. Persistência (audit trail)
        save_report(data.dict(), report)

        return report

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
