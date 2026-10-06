# Projeto 05 — Docking com validação do protocolo

**Pergunta:** o protocolo recupera poses plausíveis e produz uma priorização útil para o alvo estudado?

| Campo | Valor |
|---|---|
| Nível | Intermediário → avançado |
| Pré-requisitos | PDB/PDBQT, noção de RMSD; Vina + Open Babel no PATH |
| Dados | 1AQ1 cadeia A (CDK2–estaurosporina) + biblioteca minúscula active/decoy |
| Ambiente | Linux, AutoDock Vina 1.2.x, Open Babel 3.x, Python 3.11+ |
| Custo (demo) | ~1–3 min CPU (`exhaustiveness=4`) |
| Resultado esperado | Redocking RMSD, ranks, EF, relatório com limites |
| Maturidade | Exemplo executável |

## Dependências de sistema

```bash
# Debian/Ubuntu
sudo apt-get install -y autodock-vina openbabel
```

## Execução

```bash
cd projects/05_validated_docking
python -m venv .venv && source .venv/bin/activate
pip install -r envs/requirements.txt
python -m src.run_demo
pytest tests/ -q
# end-to-end (requires vina):
pytest tests/ -q -m integration
```

## Claims separados

| Tipo | Neste demo |
|---|---|
| Recuperação de pose (STU) | RMSD com matching húngaro |
| Ranqueamento | EF em set minúsculo com decoys **construídos** |
| Afinidade experimental | **Não afirmada** — score Vina é estimativa do modelo |

## English summary

Validates a Vina protocol on CDK2/1AQ1 by redocking STU and ranking a tiny
active/decoy set, with explicit separation of pose recovery vs ranking claims.
