# Projeto 03 — Curadoria de bioatividade e espaço químico

**Pergunta:** quais compostos e medidas podem ser comparados com coerência química e experimental?

| Campo | Valor |
|---|---|
| Nível | Intermediário |
| Pré-requisitos | SMILES, noção de IC50/Ki/Kd, Python |
| Origem dos dados | Estruturas públicas + **atividades SIMULADAS** |
| Ambiente testado | Python 3.11+, RDKit, Linux |
| Custo (demo) | < 1 min CPU |
| Resultado esperado | Dataset curado, exclusões, descritores, PCA |
| Maturidade | Exemplo executável |

## Políticas centrais

- Validar estruturas; registrar política de sais/fragmentos.
- Separar IC50, Ki, Kd, EC50 e qualificadores `<` / `>`.
- Converter unidades de forma explícita (100 nM → pIC50 = 7).
- Não fundir medidas incompatíveis.
- Lipinski/PAINS como contexto, não exclusão automática sem justificativa.

## Execução

```bash
cd projects/03_chemical_data
python -m venv .venv && source .venv/bin/activate
pip install -r envs/requirements.txt
python -m src.run_demo
pytest tests/ -q
```

## English summary

Curates a small CDK2-oriented table with planted pitfalls (salts, unit mix,
censored IC50, Ki/Kd separation, invalid SMILES) using RDKit parents,
descriptors and exploratory Morgan-fingerprint PCA.
