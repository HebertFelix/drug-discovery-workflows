# Projeto 04 — QSAR com descritores, fingerprints e generalização

**Pergunta:** o modelo prediz o endpoint em compostos suficientemente distintos dos de treinamento?

| Campo | Valor |
|---|---|
| Nível | Intermediário → avançado |
| Pré-requisitos | Projeto 03 (conceitos), RDKit, scikit-learn |
| Dados | Snapshot ChEMBL CDK2 (`CHEMBL301`) IC50 — 2026-10-06 |
| Ambiente | Python 3.11+, RDKit, scikit-learn |
| Custo (demo) | ~1–2 min CPU |
| Resultado esperado | Baseline vs modelos, random vs scaffold, AD por similaridade |
| Maturidade | Exemplo executável |
| Nome | **QSAR com descritores e fingerprints** (não é 3D-QSAR) |

## O que faz

1. Curadoria de IC50 não censurados → pais canônicos → mediana de pIC50 por InChIKey.
2. Modelos: média (baseline), Ridge em descritores, Random Forest em Morgan FP.
3. Divisões **aleatória** e por **scaffold** (Bemis–Murcko), com diagnóstico de vazamento.
4. Métricas MAE/RMSE/R²; resíduos; similaridade máxima ao treino (domínio de aplicabilidade simples).

## Execução

```bash
cd projects/04_predictive_models
python -m venv .venv && source .venv/bin/activate
pip install -r envs/requirements.txt
python -m src.run_demo
pytest tests/ -q
```

## English summary

Descriptor/fingerprint QSAR on a ChEMBL CDK2 IC50 snapshot, comparing random vs
scaffold splits and reporting a simple fingerprint applicability-domain slice.
