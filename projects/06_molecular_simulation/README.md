# Projeto 06 — Dinâmica molecular e análise de trajetórias

**Pergunta:** quais comportamentos conformacionais são consistentes nas condições simuladas?

| Campo | Valor |
|---|---|
| Nível | Intermediário → avançado |
| Pré-requisitos | Noções de MD; OpenMM + mdtraj |
| Sistema demo | Trp-cage (**1L2Y**), solvente implícito OBC2 |
| Ambiente | Python 3.11+, OpenMM, mdtraj, CPU |
| Custo (demo) | ~1–2 min CPU (2 × 10 ps) |
| Resultado esperado | RMSD/RMSF/Rg, H-bonds, τ_int, SE em blocos, 2 réplicas |
| Maturidade | Exemplo executável (porta de entrada) |

## Execução

```bash
cd projects/06_molecular_simulation
python -m venv .venv && source .venv/bin/activate
pip install -r envs/requirements.txt
python -m src.run_demo
pytest tests/ -q
pytest tests/ -q -m integration
```

## Disciplina de análise

- Alinhamento CA definido explicitamente
- Descarte de equilibração justificado no config (`equilibration_ps`)
- Frames sucessivos ≠ experimentos independentes
- Incerteza via SE em blocos + estimativa de autocorrelação

MD proteína–ligante completa permanece na trilha avançada.

## English summary

Entry-point MD module: short independent OpenMM replicas of Trp-cage (1L2Y)
in implicit solvent, with RMSD/RMSF/Rg, H-bond counts, autocorrelation and
block standard errors — emphasizing analysis discipline over long sampling.
