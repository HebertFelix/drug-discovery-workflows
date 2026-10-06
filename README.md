# drug-discovery-workflows

**Hebert Felix** · Portfólio científico em descoberta de fármacos (2026–2027)

[English version](README.en.md)

Transformar dados biológicos, químicos e biofísicos em **análises rastreáveis**, **visualizações interpretáveis** e **hipóteses confrontáveis** com evidências experimentais.

Este repositório integra bioinformática, quimioinformática e físico-informática (*Computational Biophysics and Physical Chemistry*), com ênfase em métodos reproduzíveis e documentação didática.

## Estado atual

| Item | Status |
|---|---|
| Estrutura do portfólio | Exemplo executável |
| Projetos 01–04 | Exemplo executável |
| Projetos 05–06 | Planejado |
| Estudo integrador | Planejado |

Estados usados no catálogo: **planejado → protótipo → exemplo executável → versão validada no escopo declarado**.

## Início rápido (Projeto 01)

```bash
cd projects/01_experimental_data
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r envs/requirements.txt
python -m src.run_demo
pytest tests/ -q
```

Saídas de referência em `projects/01_experimental_data/results/example/`.

## Mapa de aprendizagem

| Nível | Experiência | Evidência |
|---|---|---|
| Iniciante | Dataset pequeno, roteiro guiado, saídas esperadas | Executar, interpretar e explicar cada transformação |
| Intermediário | Novos dados, parâmetros e comparação de abordagens | Adaptar o workflow e justificar escolhas |
| Avançado | Incerteza, vieses, validação independente | Avaliar limites e investigar uma pergunta original |

## Catálogo de projetos

| Projeto | Pergunta | Nível | Dados | Ambiente | Custo (demo) | Resultado esperado | Maturidade |
|---|---|---|---|---|---|---|---|
| [01 Experimental data](projects/01_experimental_data/) | Os dados do ensaio sustentam uma comparação confiável? | Iniciante → intermediário | Simulados | Python 3.11+ | < 1 min CPU | Relatório QC, IC50 com incerteza, figuras | Exemplo executável |
| [02 Target evidence](projects/02_target_evidence/) | Quais evidências sustentam o alvo e a estrutura? | Iniciante → intermediário | UniProt/PDB (snapshot) | Python 3.11+ | < 1 min CPU | Ficha, ranking, conservação, vista 3D | Exemplo executável |
| [03 Chemical data](projects/03_chemical_data/) | Quais compostos e medidas são comparáveis? | Intermediário | Estruturas públicas + atividades simuladas | Python 3.11+ / RDKit | < 1 min CPU | Dataset curado + PCA | Exemplo executável |
| [04 Predictive models](projects/04_predictive_models/) | O modelo generaliza para compostos distintos? | Intermediário → avançado | ChEMBL CDK2 snapshot | Python/RDKit/sklearn | ~1–2 min CPU | Baseline+RF, random vs scaffold | Exemplo executável |
| [05 Validated docking](projects/05_validated_docking/) | O protocolo recupera poses e prioriza bem? | Intermediário → avançado | — | — | — | Redocking + recuperação | Planejado |
| [06 Molecular simulation](projects/06_molecular_simulation/) | Quais comportamentos são consistentes nas simulações? | Intermediário → avançado | — | — | — | RMSD/RMSF com incerteza | Planejado |

## Arquitetura

```
docs/           fundamentos, métodos e diário de pesquisa
projects/       seis módulos principais
case_studies/   estudos que conectam módulos
extensions/     variantes avançadas (ômicas, energia livre, QM/MM, …)
templates/      modelos de documentação e relatórios
```

Detalhes em [`ROADMAP.md`](ROADMAP.md).

## Princípios

1. Cada projeto declara uma **pergunta científica** explícita.
2. Resultados preservam **proveniência** até os dados de origem.
3. Limitações e falhas conhecidas são documentadas, não ocultadas.
4. Demonstração (dados pequenos) e estudo completo são modos distintos.
5. Scores de métodos diferentes **não** são somados sem justificativa.

## Citação

Ver [`CITATION.cff`](CITATION.cff). Licença do código: [`LICENSE`](LICENSE) (MIT). Condições dos dados: [`DATA_SOURCES.md`](DATA_SOURCES.md).

## Cronograma indicativo

| Período | Foco |
|---|---|
| Out–Dez 2026 | Fundação + Projeto 01 |
| Jan–Mar 2027 | Projetos 02 e 03 |
| Abr–Jun 2027 | Projeto 04 e início do 05 |
| Jul–Set 2027 | Conclusão do 05 e Projeto 06 |
| Out–Dez 2027 | Estudo integrador e consolidação |
