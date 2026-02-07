from datetime import datetime, UTC


CLINICAL_MAP = {
    "PESO": "Baixo peso ao nascer",
    "SEMAGESTAC": "Prematuridade",
    "CONSPRENAT": "Pré-natal insuficiente",
    "APGAR5": "Baixa vitalidade neonatal",
    "IDADEMAE": "Idade materna de risco"
}


def classify(score):

    if score >= 0.8:
        return "ALTO", "RED"

    if score >= 0.5:
        return "MODERADO", "YELLOW"

    return "BAIXO", "GREEN"


def extract_drivers(payload):

    drivers = []

    if payload.get("PESO", 9999) < 2500:
        drivers.append("Baixo peso ao nascer")

    if payload.get("SEMAGESTAC", 99) < 37:
        drivers.append("Prematuridade")

    if payload.get("CONSPRENAT", 99) < 6:
        drivers.append("Pré-natal insuficiente")

    return drivers


def recommend(drivers):

    recs = []

    if "Baixo peso ao nascer" in drivers:
        recs.append("Monitorar ganho ponderal e manter aquecimento neonatal.")

    if "Prematuridade" in drivers:
        recs.append("Avaliar necessidade de UTI neonatal e vigilância respiratória.")

    if "Pré-natal insuficiente" in drivers:
        recs.append("Encaminhar mãe para acompanhamento pós-parto imediato.")

    return recs or ["Seguimento ambulatorial padrão."]


def build_clinical_report(payload, score):

    risk_class, triage = classify(score)
    drivers = extract_drivers(payload)
    recommendations = recommend(drivers)

    summary = (
        f"Avaliação perinatal indica risco {risk_class.lower()} ({round(score*100,1)}%). "
        f"Gestante com idade {payload.get('IDADEMAE')} anos, "
        f"parto com {payload.get('SEMAGESTAC')} semanas "
        f"e recém-nascido com peso {payload.get('PESO')}g. "
        f"Principais fatores associados: {', '.join(drivers)}."
    )

    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "risk_score": round(score, 2),
        "risk_class": risk_class,
        "triage_level": triage,
        "clinical_summary": summary,
        "main_factors": drivers,
        "recommendations": recommendations
    }
