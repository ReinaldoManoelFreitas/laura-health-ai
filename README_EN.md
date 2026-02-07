# 💜 LAURA – Learning Analytics for Unified Risk Assessment

> *This project is a hug I could no longer give to my daughter Laura. It is the way I found to transform longing into care, so that other families may have the chances and the time we so deeply wished for.*

**LAURA** is an open-source project that uses explainable Artificial Intelligence to support the early identification of maternal and neonatal risks, based on public health data from the Brazilian SUS (SINASC and SIM systems).
Its purpose is to transform statistics into real care — helping health professionals to see, earlier, situations that deserve closer attention.

---

## 🌱 Why this project exists

Laura lived for only one day.
A silent infection crossed the pregnancy and reached her before there was enough time to react.
Among forms, exams, and protocols, something was missing — something able to connect the signals and clearly say:

> “There is risk here. Please look closer.”

This project does not bring perfect answers.
But it tries to build a bridge between data and lives, so that other Lauras may have a different outcome.

---

## 🎯 Goal

To support health teams in screening and monitoring pregnant women and newborns through:

* Estimation of **maternal-neonatal risk (0–1)**
* Clinical classification: **LOW | MODERATE | HIGH**
* Explanation of the main contributing factors
* Initial care recommendations

All in a transparent, auditable way, based on public data.

---

## 🧠 What the system provides

**Input:**
Basic data about pregnancy and birth.

**Output:**

* Risk score
* Triage level (🟢🟡🔴)
* Explanatory factors (Explainable AI – SHAP)
* Clinical summary in human language
* Suggested actions

Example:

```json
{
  "risk_score": 0.73,
  "risk_class": "MODERATE",
  "triage_level": "YELLOW",
  "main_factors": ["Prematurity", "Low birth weight"]
}
```
---

## How to obtain and prepare the data

Original SINASC and SIM files **must not be pushed to GitHub** due to file size, performance, and privacy best practices.  
This repository contains only the code required to fully reproduce the pipeline from public datasets.

### Reproduction steps

1. Download the official datasets from:
    
    - SINASC: [https://dados.gov.br](https://dados.gov.br/)
        
    - SIM: [https://dados.gov.br](https://dados.gov.br/)
        
2. Place the files in:
    

```
data/raw/sinasc
data/raw/sim
```

3. Run the pipeline:
    

```bash
python pipelines/ingest_csv.py
python pipelines/maternal_builder.py
python pipelines/risk_model.py
```

4. To generate explainability artifacts:
    

```bash
python pipelines/explain.py
```

### What is versioned

✅ Source code  
✅ Ingestion and training scripts  
✅ Synthetic examples  
❌ Real CSV/Parquet files  
❌ Raw DATASUS datasets

---

## 🚀 How to run

```bash
pip install -r requirements.txt
uvicorn app.api.main:app --reload
```

Access:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧩 Architecture

* FastAPI
* XGBoost
* SHAP (Explainable AI)
* Clean Architecture
* Auditable persistence layer

---

## ⚠️ Responsible use

* This project is **decision support** and does not replace medical evaluation.
* It must be used by qualified health professionals.
* Results are probabilistic and depend on data quality.
* Sensitive data must comply with privacy laws and ethical standards.

---

## 🤝 How to contribute

All help is welcome:

* clinical validation
* model improvement
* documentation
* integration with health systems

See: `docs/CONTRIBUTING.md`

---

## 🌻 Dedication

To Laura.
And to all the children who are yet to be born.

May technology serve to protect what is most fragile.

---

## 📄 License

MIT
