# Projeto 02 — Atlas de evidências de um alvo

**Pergunta:** quais evidências sustentam a escolha do alvo e a adequação de uma estrutura para determinado estudo?

| Campo | Valor |
|---|---|
| Nível | Iniciante → intermediário |
| Pré-requisitos | Sequências FASTA, noção de PDB/UniProt |
| Origem dos dados | Instantâneos públicos (UniProt P24941, RCSB) com data de acesso |
| Ambiente testado | Python 3.11+, Linux |
| Custo computacional (demo) | < 1 min CPU |
| Resultado esperado | Ficha do alvo, ranking de estruturas, mapa de conservação, vista 3D |
| Maturidade | Exemplo executável |
| Alvo da demo | CDK2 / `P24941` |

## O que este projeto faz

1. Carrega identidade e anotações compactas do UniProt (snapshot).
2. Calcula conservação posicional contra ortólogos revisados.
3. Ranqueia estruturas PDB curadas para um **intent** declarado (`ligand_pose_reference`, etc.).
4. Audita resíduos observados/ausentes e HET groups no PDB demonstrativo.
5. Gera ficha Markdown, figuras e HTML 3D (NGL) com proveniência.

## Execução rápida

```bash
cd projects/02_target_evidence
python -m venv .venv && source .venv/bin/activate
pip install -r envs/requirements.txt
python -m src.run_demo
pytest tests/ -q
```

## Distinções obrigatórias

| Tipo | Exemplos neste demo |
|---|---|
| Observação experimental | Anotações UniProt revisadas; entradas PDB de raios X; coordenadas de 1AQ1 |
| Predição / método nosso | Fração de conservação por alinhamentos pairwise |
| Hipótese | Ranking de estrutura para um intent; leituras mecanísticas de ligantes |

Cavidade ou ligante co-cristalizado **não** prova mecanismo alostérico. Modelos AlphaFold estão fora deste demo e **não** validam efeitos de mutação de forma geral.

## Saídas

| Arquivo | Conteúdo |
|---|---|
| `target_brief.md` | Ficha do alvo e justificativa da estrutura |
| `structures_ranked.csv` | Catálogo pontuado |
| `structure_choice.json` | Escolha + caveats |
| `conservation_map.png` | Conservação ao longo da sequência |
| `structure_view.html` | Vista 3D anotada (coordenadas empacotadas de 1AQ1 cadeia A) |

## English summary

Evidence atlas for human CDK2: UniProt snapshot + ortholog conservation +
intent-aware PDB ranking + offline NGL view of a chain-A coordinate slice.
