from pathlib import Path
import pandas as pd
from datetime import datetime, UTC

HISTORY = Path("data/inference/history.parquet")
HISTORY.parent.mkdir(parents=True, exist_ok=True)


def save_report(input_data: dict, report: dict):
    """Salva predição para auditoria e dashboard"""

    record = {
        "timestamp": datetime.now(UTC).isoformat(),
        "input": input_data,
        "output": report,
        "risk_score": report.get("risk_score"),
        "risk_class": report.get("risk_class"),
    }

    df_new = pd.DataFrame([record])

    if HISTORY.exists():
        df = pd.read_parquet(HISTORY)
        df = pd.concat([df, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_parquet(HISTORY, index=False)
