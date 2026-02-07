from pathlib import Path
import pandas as pd
import numpy as np

SINASC_PATH = Path("data/parquet/sinasc")
SIM_PATH = Path("data/parquet/sim")
OUT_PATH = Path("data/maternal")

OUT_PATH.mkdir(parents=True, exist_ok=True)


# ===============================
# Utils
# ===============================

def load_folder(path: Path):
    dfs = []
    for f in path.glob("*.parquet"):
        print(f"Loading {f.name}")
        dfs.append(pd.read_parquet(f))
    return pd.concat(dfs, ignore_index=True)


def to_numeric(df, cols):
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


# ===============================
# Risk heuristic (v1)
# ===============================

def compute_risk(row):
    score = 0.0

    # Poucas consultas pré-natal
    if row.get("CONSPRENAT", 9) <= 3:
        score += 0.2

    # APGAR ruim
    if row.get("APGAR5", 10) < 7:
        score += 0.3

    # Baixo peso
    if row.get("PESO", 3000) < 2500:
        score += 0.2

    # Prematuridade
    if row.get("SEMAGESTAC", 40) < 37:
        score += 0.2

    # Pré-natal tardio
    if row.get("MESPRENAT", 1) > 4:
        score += 0.2

    # Escolaridade baixa
    if row.get("ESCMAE", 9) in [0, 1, 2]:
        score += 0.1

    return min(score, 1.0)


# ===============================
# Main pipeline
# ===============================

def main():
    print("\n=== LAURA Maternal Builder ===\n")

    print("Loading SINASC...")
    sinasc = load_folder(SINASC_PATH)

    print("Loading SIM...")
    sim = load_folder(SIM_PATH)

    # Normalizações principais SINASC
    sinasc = to_numeric(
        sinasc,
        [
            "IDADEMAE",
            "PESO",
            "APGAR1",
            "APGAR5",
            "SEMAGESTAC",
            "CONSPRENAT",
            "MESPRENAT",
            "ESCMAE",
        ],
    )

    # SIM
    sim = to_numeric(sim, ["IDADEMAE"])

    # Flag de óbito materno
    sim["OBITO_MATERNO"] = sim["CAUSABAS"].astype(str).str.startswith(("O", "A40", "A41"))

    sim_small = sim[
        [
            "CODMUNRES",
            "IDADEMAE",
            "SEMAGESTAC",
            "CAUSABAS",
            "OBITO_MATERNO",
        ]
    ]

    # Join probabilístico simples
    print("Joining SINASC + SIM...")

    maternal = sinasc.merge(
        sim_small,
        on=["CODMUNRES", "IDADEMAE", "SEMAGESTAC"],
        how="left",
        suffixes=("", "_SIM"),
    )

    maternal["OBITO_MATERNO"] = maternal["OBITO_MATERNO"].fillna(False)

    # Features principais
    features = [
        "CODMUNRES",
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
        "QTDFILMORT",
        "OBITO_MATERNO",
        "CAUSABAS",
    ]

    maternal = maternal[[c for c in features if c in maternal.columns]]

    # Score de risco
    print("Computing risk score...")
    maternal["RISCO_SCORE"] = maternal.apply(compute_risk, axis=1)

    # Labels úteis
    maternal["BAIXO_PESO"] = maternal["PESO"] < 2500
    maternal["PREMATURO"] = maternal["SEMAGESTAC"] < 37
    maternal["APGAR_CRITICO"] = maternal["APGAR5"] < 7

    out_file = OUT_PATH / "maternal_features.parquet"
    maternal.to_parquet(out_file, index=False)

    print("\n==============================")
    print("Dataset final gerado:")
    print(out_file)
    print(f"Total registros: {len(maternal)}")
    print("==============================\n")


if __name__ == "__main__":
    main()
