# Projeto 01 — Do arquivo de laboratório ao resultado estatístico

**Pergunta:** os dados de um ensaio sustentam uma comparação confiável entre compostos ou condições?

| Campo | Valor |
|---|---|
| Nível | Iniciante → intermediário |
| Pré-requisitos | Python básico, leitura de CSV, noção de concentração–resposta |
| Origem dos dados | Simulados (explicitamente rotulados) |
| Ambiente testado | Python 3.11+, Linux |
| Custo computacional (demo) | < 1 minuto de CPU |
| Resultado esperado | Relatório QC, parâmetros IC50 com incerteza, figuras |
| Maturidade | Exemplo executável |

[English summary](#english-summary) · Theory: [`docs/theory.md`](docs/theory.md) · Protocol: [`docs/protocol.md`](docs/protocol.md)

## O que este projeto faz

1. Lê leituras de placa, mapa de poços e metadados de amostras.
2. Verifica unidades, identificadores, ausências e controles.
3. Registra exclusões e analisa variação entre placas.
4. Normaliza o sinal para percentual de resposta (justificativa no protocolo).
5. Ajusta curvas concentração–resposta (logística de 4 parâmetros) e estima IC50.
6. Sinaliza estimativas fora da faixa experimental.
7. Produz figuras e um relatório Markdown rastreável às linhas de origem.

## Execução rápida

```bash
cd projects/01_experimental_data
python -m venv .venv && source .venv/bin/activate
pip install -r envs/requirements.txt
python -m src.run_demo
pytest tests/ -q
```

Saídas em `results/example/`:

| Arquivo | Conteúdo |
|---|---|
| `qc_report.md` | Qualidade, exclusões, Z′ por placa |
| `fit_parameters.csv` | Top, bottom, hill, IC50, IC50_CI, flags |
| `plate_heatmap.png` | Mapa de calor das leituras brutas |
| `dose_response_curves.png` | Observações + curvas ajustadas |
| `fit_residuals.png` | Resíduos do ajuste |
| `normalized_readings.csv` | Tabela intermediária rastreável |
| `run_manifest.json` | Versões, semente, timestamps |

## Cenário de falha plantado

A placa `P02` contém um **efeito de borda** artificial nas colunas 1 e 12 (sinal inflado nos controles negativos de borda). O workflow deve:

- detectar Z′ degradado nessa placa;
- excluir poços de controle de borda comprometidos conforme a regra do protocolo;
- documentar a exclusão no relatório.

## Limites (resumo)

- Dados são **simulados**; não representam um ensaio biológico real.
- IC50 é definida como a concentração na meia-resposta do modelo ajustado (ver `docs/theory.md`).
- Estimativas fora da faixa de concentração testada são sinalizadas, sem precisão indevida.
- Réplicas na mesma placa são **técnicas**; placas distintas são tratadas como lotes.

Detalhes em [`docs/limitations.md`](docs/limitations.md).

## Estrutura

```
data/example/     entradas pequenas da demonstração
configs/          parâmetros (YAML)
src/              funções e interface de execução
tests/            proteções científicas
results/example/  saídas de referência
docs/             teoria, protocolo, estatística, limitações
notebooks/        roteiro didático
```

---

## English summary

**Question:** do assay readings support a reliable comparison between compounds?

This module runs QC → plate-effect checks → signal normalization → 4-parameter
logistic fits → figures and a provenance-aware report on a **simulated** 96-well
dataset that includes a planted edge-effect failure on plate `P02`.
