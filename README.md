# 💜 LAURA – Laboratório de Apoio ao Risco Obstétrico com IA

> _Este projeto é um abraço que não pude mais dar na minha filha Laura. É a forma que encontrei de transformar a saudade em cuidado, para que outras famílias tenham as chances e o tempo que nós tanto desejamos._

O **LAURA** é um projeto open source que utiliza Inteligência Artificial explicável para apoiar a identificação precoce de riscos materno-neonatais, a partir de dados públicos do SUS (SINASC e SIM).  
Ele foi criado para transformar estatísticas em cuidado real — ajudando profissionais de saúde a enxergar, mais cedo, situações que merecem atenção.

---

## 🌱 Por que este projeto existe

Laura viveu apenas um dia.  
Uma infecção silenciosa atravessou a gestação e chegou até ela antes que houvesse tempo suficiente para reagir.  
Entre papéis, exames e protocolos, faltou algo que unisse os sinais e dissesse com clareza:

> “Aqui há risco. Olhem com mais cuidado.”

Este projeto não traz respostas perfeitas.  
Mas tenta construir uma ponte entre dados e vidas, para que outras Lauras possam ter um desfecho diferente.

---

## 🎯 Objetivo

Apoiar equipes de saúde na triagem e no acompanhamento de gestantes e recém-nascidos por meio de:

- Estimativa de **risco materno-neonatal (0–1)**
    
- Classificação clínica: **BAIXO | MODERADO | ALTO**
    
- Explicação dos principais fatores envolvidos
    
- Recomendações iniciais de cuidado
    

Tudo de forma transparente, auditável e baseada em dados públicos.

---

## 🧠 O que o sistema entrega

**Entrada:**  
Dados básicos da gestação e do nascimento.

**Saída:**

- Score de risco
    
- Nível de triagem (🟢🟡🔴)
    
- Fatores explicativos (Explainable AI – SHAP)
    
- Resumo clínico em linguagem humana
    
- Sugestões de conduta
    

Exemplo:

```json
{
  "risk_score": 0.73,
  "risk_class": "MODERADO",
  "triage_level": "YELLOW",
  "main_factors": ["Prematuridade", "Baixo peso ao nascer"]
}
```

---

## Como obter e preparar os dados

Os arquivos originais do SINASC e SIM **não devem ser enviados para o GitHub** por questões de tamanho, desempenho e boas práticas de privacidade.  
O repositório contém apenas o código necessário para reproduzir todo o pipeline a partir das bases públicas.

### Passos para reprodução

1. Baixe os dados oficiais em:
    
    - SINASC: [https://dados.gov.br](https://dados.gov.br/)
        
    - SIM: [https://dados.gov.br](https://dados.gov.br/)
        
2. Coloque os arquivos na pasta:
    

```
data/raw/sinasc
data/raw/sim
```

3. Execute o pipeline:
    

```bash
python pipelines/ingest_csv.py
python pipelines/maternal_builder.py
python pipelines/risk_model.py
```

4. Para gerar explicabilidade:
    

```bash
python pipelines/explain.py
```

### O que é versionado

✅ Código-fonte  
✅ Scripts de ingestão e treinamento  
✅ Exemplos sintéticos  
❌ CSV/Parquet reais  
❌ Bases brutas do DATASUS


---

## 🚀 Como executar

```bash
pip install -r requirements.txt
uvicorn app.api.main:app --reload
```

Acesse:  
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧩 Arquitetura

- FastAPI
    
- XGBoost
    
- SHAP (IA explicável)
    
- Clean Architecture
    
- Persistência auditável
    

---

## ⚠️ Uso responsável

- Este projeto é **apoio à decisão** e não substitui avaliação médica.
    
- Deve ser utilizado por profissionais de saúde.
    
- Resultados são probabilísticos e dependem da qualidade dos dados.
    
- Dados sensíveis devem respeitar LGPD e normas éticas.
    

---

## 🤝 Como contribuir

Toda ajuda é bem-vinda:

- validação clínica
    
- melhoria dos modelos
    
- documentação
    
- integração com sistemas de saúde
    

Veja: `docs/CONTRIBUTING.md`

---

## 🌻 A quem dedicamos

À Laura.  
E a todas as crianças que ainda vão nascer.

Que a tecnologia sirva para proteger o que há de mais frágil.

---

## 📄 Licença

MIT