import streamlit as st
import pandas as pd
from pathlib import Path

DATA = Path("data/inference/history.parquet")

st.set_page_config(page_title="LAURA – Maternal Risk", layout="wide")

st.title("🧬 LAURA – Maternal Risk Dashboard")

# =====================
# Load data
# =====================

if not DATA.exists():
    st.error("Nenhuma inferência encontrada ainda.")
    st.stop()

df = pd.read_parquet(DATA)

# =====================
# Sidebar filters
# =====================

st.sidebar.header("Filtros")

risk_filter = st.sidebar.multiselect(
    "Classe de risco",
    df["risk_class"].unique(),
    default=df["risk_class"].unique()
)

df = df[df["risk_class"].isin(risk_filter)]

# =====================
# KPIs
# =====================

c1, c2, c3, c4 = st.columns(4)

c1.metric("Avaliações", len(df))
c2.metric("Alto risco", (df["risk_class"] == "ALTO").mean() * 100)
c3.metric("Moderado", (df["risk_class"] == "MODERADO").mean() * 100)
c4.metric("Baixo", (df["risk_class"] == "BAIXO").mean() * 100)

# =====================
# Charts
# =====================

st.subheader("Distribuição de risco")

st.bar_chart(df["risk_class"].value_counts())

st.subheader("Score")

st.line_chart(df["risk_score"])

# =====================
# Table
# =====================

st.subheader("Casos recentes")

cols = [
    "timestamp",
    "risk_score",
    "risk_class",
    "triage_level",
    "main_factors",
]

st.dataframe(df[cols].sort_values("timestamp", ascending=False).head(50))

# =====================
# Detail
# =====================

st.subheader("Resumo clínico")

idx = st.selectbox("Selecione um caso", df.index)

st.json(df.loc[idx].to_dict())
