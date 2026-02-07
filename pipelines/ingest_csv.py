from pathlib import Path
import pandas as pd

SINASC = Path("data/raw/sinasc")
SIM = Path("data/raw/sim")

PARQUET_SINASC = Path("data/parquet/sinasc")
PARQUET_SIM = Path("data/parquet/sim")

PARQUET_SINASC.mkdir(parents=True, exist_ok=True)
PARQUET_SIM.mkdir(parents=True, exist_ok=True)


def ingest_folder(folder: Path, out_folder: Path):
    files = list(folder.glob("*.csv"))

    if not files:
        print(f"Nenhum CSV em {folder}")
        return

    for f in files:
        print("Ingesting", f.name)

        df = pd.read_csv(
            f,
            sep=";",
            encoding="latin1",
            low_memory=False
        )

        out = out_folder / f.with_suffix(".parquet").name
        df.to_parquet(out, index=False)

        print("→ salvo", out)


def main():
    print("\n=== INGEST CSV → PARQUET ===\n")

    ingest_folder(SINASC, PARQUET_SINASC)
    ingest_folder(SIM, PARQUET_SIM)

    print("\nFinalizado.")


if __name__ == "__main__":
    main()
