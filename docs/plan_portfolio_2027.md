# Portfólio científico em Drug Discovery — plano até 2027

**Hebert Felix | Proposta revisada em 6 de outubro de 2026**

Este documento define a construção do portfólio. Os projetos, ambientes e critérios descritos são entregas planejadas; sua implementação e validação deverão ser demonstradas em cada publicação.

## 1. Visão e posicionamento

Quero construir, até o final de 2027, um portfólio público no GitHub dedicado à descoberta de fármacos, integrando bioinformática, quimioinformática e físico-informática, com ênfase em biofísica e físico-química computacionais. Meu objetivo é desenvolver reconhecimento pela qualidade científica, pela utilidade dos recursos e pela capacidade de ensinar e documentar métodos reproduzíveis.

O eixo do portfólio será a conexão entre perguntas biológicas, dados experimentais, representações moleculares, modelos computacionais e interpretação estatística. Cada projeto deverá explicar qual problema resolve, quais evidências utiliza, como foi construído e quais conclusões seus resultados permitem sustentar.

Pretendo oferecer uma progressão de aprendizagem para iniciantes, intermediários e avançados, com exemplos executáveis, fundamentos acessíveis e aprofundamentos técnicos. Uma pessoa deverá conseguir compreender um resultado, reproduzi-lo e adaptá-lo a outra pergunta, identificando também suas limitações.

A proposta de valor será: **transformar dados biológicos, químicos e biofísicos em análises rastreáveis, visualizações interpretáveis e hipóteses que possam ser confrontadas com evidências experimentais.**

O reconhecimento em 2027 será uma ambição orientadora. As metas sob meu controle serão publicar projetos completos, obter reprodução por terceiros, incorporar revisões e demonstrar aplicações úteis.

## 2. Estratégia: profundidade com integração

O portfólio começará com seis projetos principais e um estudo integrador que reutilize suas etapas. As extensões mais exigentes serão incorporadas conforme os dados, a infraestrutura e a maturidade dos projetos permitirem.

Cada projeto deverá apresentar uma pergunta científica explícita. Exemplos: uma diferença de potência permanece após considerar variação entre placas? Um modelo consegue generalizar para séries químicas pouco semelhantes às de treinamento? Uma interação sugerida pelo docking aparece em simulações independentes?

O caso integrador deverá utilizar inicialmente um alvo com estruturas experimentais adequadas, ligantes de referência e dados de atividade suficientemente documentados. A seleção dependerá de uma auditoria dos dados; o tema terapêutico, sozinho, não será critério suficiente.

Para comunicação internacional, a área de físico-informática será apresentada também como **Computational Biophysics and Physical Chemistry**. O README principal terá versões em português e inglês. Os tutoriais didáticos poderão começar em português e ser traduzidos conforme amadurecerem.

Um pipeline representará uma sequência automatizada de transformações. O workflow registrará também dependências, parâmetros, alternativas e critérios de decisão. Sua complexidade deverá acompanhar o problema e a necessidade de reutilização.

## 3. Arquitetura proposta

Nome de trabalho: `drug-discovery-workflows`. Começar com um repositório modular facilita compartilhar convenções e recursos; separar projetos em outros repositórios quando houver necessidade real de manutenção ou distribuição independente.

| Caminho | Responsabilidade |
|---|---|
| `README.md` e `README.en.md` | Apresentação, público, mapa de aprendizagem, catálogo e acesso aos projetos executáveis. |
| `ROADMAP.md` | Escopo, prioridades, marcos e dependências. |
| `docs/foundations/` | Python científico, estatística, álgebra linear, química, biologia estrutural e termodinâmica necessárias. |
| `docs/methods/` | Convenções para curadoria, análise estatística, visualização e reprodução. |
| `docs/research_log/` | Perguntas, decisões, tentativas, resultados negativos e alterações justificadas. |
| `projects/01_experimental_data/` | Controle de qualidade e análise de dados de ensaios. |
| `projects/02_target_evidence/` | Evidências biológicas, sequências e estruturas dos alvos. |
| `projects/03_chemical_data/` | Curadoria de compostos, bioatividades e espaço químico. |
| `projects/04_predictive_models/` | Baselines, QSAR e avaliação de generalização. |
| `projects/05_validated_docking/` | Preparação molecular e avaliação de docking e triagem. |
| `projects/06_molecular_simulation/` | Análise de trajetórias e preparação de dinâmica molecular. |
| `case_studies/` | Estudos que conectem os módulos em uma pergunta científica comum. |
| `extensions/` | Propostas e protótipos de variantes, ômicas, energia livre e métodos avançados. |
| `templates/` | Modelos de documentação, relatórios, gráficos e registro de decisões. |
| `.github/workflows/` | Verificações automatizadas e execução dos exemplos pequenos. |
| `CITATION.cff`, `CONTRIBUTING.md` e `CHANGELOG.md` | Citação, colaboração e histórico de mudanças. |
| `LICENSE` e `DATA_SOURCES.md` | Termos do código e registro separado das condições de uso dos dados. |

O catálogo deverá indicar, para cada projeto: pergunta, nível, pré-requisitos, origem dos dados, ambiente testado, custo computacional medido, resultado esperado e estágio de maturidade.

Os estados sugeridos são: **planejado, protótipo, exemplo executável e versão validada no escopo declarado**. Um protótipo deverá ser apresentado com seu estágio real de maturidade.

## 4. Progressão de aprendizagem

| Nível | Experiência oferecida | Evidência de aprendizagem |
|---|---|---|
| Iniciante | Dataset pequeno, roteiro guiado, conceitos explicados, saídas esperadas e exercícios comentados. | Executar, interpretar e explicar o significado de cada transformação. |
| Intermediário | Novos dados, parâmetros configuráveis, diagnóstico de problemas e comparação entre abordagens. | Adaptar o workflow e justificar escolhas metodológicas. |
| Avançado | Incerteza, vieses, validação independente, análise de sensibilidade e integração de evidências. | Avaliar limites, reproduzir um estudo e investigar uma pergunta original. |

A dificuldade será definida pelos conhecimentos exigidos e pela qualidade da inferência. Um iniciante pode explorar uma trajetória pronta; preparar e validar uma simulação proteína–ligante completa ficará na trilha avançada.

Cada tutorial seguirá uma sequência didática: problema, fundamento, entrada, preparação, execução, explicação do código, saída, interpretação, erros frequentes, limitações, exercício e resposta comentada. Funções e parâmetros deverão ser explicados no ponto em que forem utilizados.

## 5. Projetos principais

### Projeto 01 — Do arquivo de laboratório ao resultado estatístico

**Pergunta:** os dados de um ensaio sustentam uma comparação confiável entre compostos ou condições?

Entradas: tabelas CSV de leituras, mapa de placa, concentrações, controles, identificação de amostras, réplicas e lotes. Começar com dados simulados claramente identificados; incorporar dados públicos ou autorizados quando disponíveis.

O workflow deverá verificar unidades, identificadores, ausências e controles; registrar exclusões; analisar variação entre placas; normalizar sinais com justificativa; e ajustar curvas concentração–resposta quando o desenho do ensaio permitir. Documentar a definição de IC50 adotada e sinalizar estimativas fora da faixa experimental, sem atribuir precisão indevida. [1]

Entregas: relatório de qualidade, tabela de parâmetros, mapa de calor de placa, curvas com observações individuais, resíduos do ajuste e estimativas de incerteza.

Critério de conclusão: preservar a ligação entre cada resultado e os dados de origem; distinguir réplicas técnicas de experimentos independentes; demonstrar o comportamento do método diante de pelo menos uma falha de qualidade conhecida.

### Projeto 02 — Atlas de evidências de um alvo

**Pergunta:** quais evidências sustentam a escolha do alvo e a adequação de uma estrutura para determinado estudo?

Entradas: sequências e anotações do UniProt, estruturas experimentais do PDB e modelos preditos quando necessários, sempre com identificadores e datas de acesso.

O workflow deverá relacionar sequência, isoforma e estrutura; documentar resíduos ausentes, mutações, ligantes e cofatores; explorar alinhamentos e conservação; e avaliar cavidades em um aprofundamento intermediário.

Entregas: ficha do alvo, tabela de estruturas candidatas, mapa de conservação e visualização 3D anotada, acompanhados da justificativa da estrutura escolhida.

Critério de conclusão: distinguir observações experimentais, predições e hipóteses. Cavidade detectada não constitui, por si, evidência de função alostérica. Modelos do AlphaFold exigem interpretação de confiança local e das limitações do uso pretendido; o AlphaFold não é um validador geral de efeitos de mutações. [2]

### Projeto 03 — Curadoria de bioatividade e espaço químico

**Pergunta:** quais compostos e medidas podem ser comparados com coerência química e experimental?

Entradas: SMILES ou SDF, registros de bioatividade e metadados dos ensaios. O workflow deverá validar estruturas, registrar a política para sais, tautômeros e estereoquímica, detectar duplicatas e preservar a identidade do composto original.

Separar IC50, Ki, Kd e EC50, bem como organismo, alvo, tipo de ensaio e qualificadores como `<` e `>`. Uma transformação logarítmica exige unidades e condições interpretáveis: 100 nM correspondem a 10⁻⁷ M e, para uma IC50 pontual válida, a pIC50 = 7. Valores censurados deverão preservar essa condição.

Calcular descritores e fingerprints com RDKit e explorar distribuições, similaridade e diversidade. Regras de Lipinski/Veber e alertas PAINS serão informações contextuais; critérios de exclusão precisarão de justificativa. A biblioteca oferece recursos para descritores, fingerprints e filtros estruturais. [3]

Entregas: dataset curado, dicionário, registro de exclusões, visualizações de propriedades, PCA e exploração opcional por UMAP. Documentar parâmetros e evitar interpretar projeções como prova de mecanismos ou classes naturais.

Critério de conclusão: cada linha curada precisa ser rastreável à fonte e às transformações aplicadas; medidas incompatíveis não devem ser fundidas silenciosamente.

### Projeto 04 — QSAR com avaliação de generalização

**Pergunta:** o modelo prediz o endpoint escolhido em compostos suficientemente distintos daqueles usados no treinamento?

Usar os dados curados do Projeto 03. Começar com um preditor simples de referência e modelos convencionais antes de ampliar a complexidade. Comparar estratégias de divisão aleatória, por scaffold e, quando viável, temporal ou por séries químicas. O benchmark MoleculeNet evidencia que a escolha da divisão altera a avaliação de generalização. [4]

Inspecionar similaridade e sobreposição entre os conjuntos mesmo após separar scaffolds. Ajustar transformações e hiperparâmetros usando somente dados de treinamento nas etapas apropriadas. Reservar o teste final e documentar quando houver seleção de modelos repetida com base nele.

Entregas: comparação com baseline, predito versus observado, resíduos, MAE/RMSE e R² para regressão; métricas de classificação, calibração e desempenho por subgrupo quando aplicáveis; análise do domínio de aplicabilidade e das falhas.

Critério de conclusão: demonstrar o procedimento de validação, o comportamento fora das séries conhecidas e os limites do resultado. Um desempenho modesto devidamente explicado também é uma entrega válida.

O nome inicial será **QSAR com descritores e fingerprints**. A denominação 3D-QSAR será reservada a modelos que efetivamente utilizem representações tridimensionais apropriadas. Geração molecular será uma extensão separada.

### Projeto 05 — Docking com validação do protocolo

**Pergunta:** o protocolo recupera poses plausíveis e produz uma priorização útil para o alvo estudado?

Documentar preparação do receptor e dos ligantes, estados de protonação, águas e cofatores mantidos, configuração da busca e sementes. Utilizar uma ferramenta principal de docking e registrar as versões dos programas auxiliares.

Avaliar redocking com correspondência atômica adequada e tratamento de simetria. Complementar, quando houver dados, com avaliação de triagem usando ativos conhecidos e inativos medidos; se forem usados decoys, identificá-los como exemplos construídos, com possíveis vieses. A documentação do Vina recomenda avaliação específica para o alvo. [5]

Entregas: sobreposição de poses, RMSD, contatos intermoleculares, distribuição de scores e métricas de recuperação de ativos com incerteza apropriada ao conjunto.

Critério de conclusão: separar desempenho de pose de desempenho de ranqueamento. O score é uma estimativa produzida pelo modelo; não demonstra afinidade experimental, eficácia ou segurança. Redocking bem-sucedido não valida sozinho uma campanha de triagem.

### Projeto 06 — Dinâmica molecular e análise de trajetórias

**Pergunta:** quais comportamentos conformacionais e interações são observados de forma consistente nas condições simuladas?

A porta de entrada será a análise de trajetórias pequenas previamente produzidas e documentadas. A etapa avançada abrangerá preparação, parametrização, solvatação, minimização, equilibração e produção, com justificativa dos parâmetros.

Adotar inicialmente um motor, como OpenMM ou GROMACS, e ampliar a interoperabilidade quando houver necessidade. Planejar execuções independentes e avaliar amostragem e convergência para as grandezas de interesse. Duração fixa e estabilização visual de RMSD não bastam para demonstrar convergência global. [6]

Entregas: séries de RMSD, RMSF e raio de giração, ocupação de contatos, comparação entre réplicas e visualizações estruturais vinculadas a resultados quantitativos.

Critério de conclusão: definir alinhamento e seleção de átomos, justificar descarte de equilibração, avaliar autocorrelação e estimar incerteza respeitando a dependência temporal. Frames sucessivos não equivalem a experimentos independentes. Métodos de séries temporais, como os documentados no pymbar, ajudam a avaliar essa dependência. [7]

## 6. Estudo integrador e extensões

O estudo integrador deverá reunir evidência do alvo, curadoria química, avaliação experimental disponível, modelos preditivos, docking e análise de simulação quando pertinente. A pergunta será delimitada e os resultados deverão poder discordar entre métodos.

A entrega central será um relatório de priorização fundamentado: quais hipóteses são apoiadas, quais resultados são incertos, quais compostos merecem investigação adicional e que experimento seria capaz de distinguir explicações concorrentes. Scores de métodos diferentes não serão somados como se estivessem na mesma escala; qualquer regra de integração exigirá justificativa e análise de sensibilidade.

| Extensão | Pré-requisito | Evidência esperada |
|---|---|---|
| Expressão gênica e priorização de alvos | Desenho experimental, qualidade das amostras e fatores de confusão conhecidos. | Efeitos estimados, controle de múltiplas comparações e integração crítica com outras evidências. |
| Variantes e resistência | Mapeamento consistente entre variantes, sequências e estruturas; dados de referência. | Separação entre patogenicidade, estabilidade e alteração de resposta ao ligante. |
| MM/GBSA ou MM/PBSA | Trajetórias e preparação adequadas ao protocolo. | Análise de sensibilidade, incerteza, aproximações e termos incluídos ou omitidos. |
| Amostragem aprimorada | Estatística de simulações e variáveis coletivas justificadas. | Sobreposição/amostragem, convergência e perfil de energia livre com incerteza. |
| QM/MM | Pergunta sobre estrutura eletrônica ou reatividade e domínio de química quântica. | Justificativa da região QM, método, fronteiras e hipóteses físicas. |
| Geração molecular | Avaliador preditivo validado e política química explícita. | Validade, diversidade, novidade, plausibilidade e comparação com estratégias simples. |

MM/GBSA e MM/PBSA serão tratados como métodos aproximados e dependentes do protocolo; componentes energéticas e decomposições por resíduo exigem cautela interpretativa. Há avaliações empíricas mostrando sensibilidade ao tratamento da entropia. [8]

Umbrella sampling e metadinâmica são técnicas de amostragem; QM/MM é uma abordagem de modelagem do sistema. Esses temas terão objetivos e tutoriais distintos. Os tutoriais do PLUMED oferecem uma referência para reconstrução de perfis e avaliação de incerteza em amostragem enviesada. [9]

## 7. Estatística e visualização como competências centrais

Cada análise começará pela identificação da unidade experimental, estrutura de dependência, variável de interesse e pergunta a responder. Medidas de dispersão, incerteza de estimativas e erros de predição serão explicitamente diferenciados.

Média ± desvio padrão descreve dispersão; não representa automaticamente um intervalo de confiança. Testes de normalidade não serão uma etapa obrigatória universal. A escolha do método considerará o desenho, os resíduos quando pertinentes, o tamanho amostral e a robustez das conclusões.

Quando houver inferência, relatar magnitude do efeito, incerteza e pressupostos. Valores de p terão interpretação contextual, com ajuste para múltiplas comparações quando necessário. A orientação da ASA reforça que conclusões não devem depender apenas de um limiar de significância e que p não mede importância científica. [10]

| Situação | Visualização principal | Informação indispensável |
|---|---|---|
| Comparação experimental | Pontos individuais, pares quando existentes e estimativa do efeito. | Unidade experimental, n independente, dispersão e método de incerteza. |
| Concentração–resposta | Observações, curva ajustada e resíduos. | Concentração/unidade, controles, definição do parâmetro e limites do ajuste. |
| Espaço químico | Distribuições e projeções exploratórias. | Representação, escala, parâmetros, sementes e limitações da projeção. |
| Predição | Predito versus observado, resíduos e desempenho por grupo. | Conjunto avaliado, divisão dos dados, baseline e domínio de aplicação. |
| Docking | Poses, contatos e recuperação de ativos. | Configuração, método de score e referência usada na avaliação. |
| Dinâmica molecular | Séries e distribuições por réplica. | Tempo, seleção de átomos, equilibração e dependência temporal. |

Gráficos deverão conter unidades consistentes e convencionais para a área, legenda explicativa, paleta acessível e identificação da origem dos dados. Salvar tabelas usadas nas figuras e o código que as produz. Preferir SVG/PDF para elementos vetoriais e resolução adequada ao destino para imagens raster; 300 DPI isoladamente não garante qualidade científica.

## 8. Padrão de documentação por projeto

| Arquivo ou diretório | Conteúdo mínimo |
|---|---|
| `README.md` | Problema, público, requisitos, execução rápida, saídas, status e limites. |
| `docs/theory.md` | Conceitos, equações necessárias, pressupostos e referências. |
| `docs/protocol.md` | Procedimento, decisões, alternativas e critérios de exclusão. |
| `docs/statistics.md` | Unidade de análise, dependências, métricas, incerteza e validação. |
| `docs/limitations.md` | Vieses, falhas conhecidas e contextos em que o método não foi avaliado. |
| `data/manifest.tsv` | Fonte, identificador, versão/data, licença, origem experimental ou simulada e checksum quando aplicável. |
| `data/example/` | Entradas pequenas adequadas à demonstração e aos testes. |
| `configs/` | Parâmetros e perfis de execução. |
| `notebooks/` | Exploração explicada, com ordem de execução verificável. |
| `src/` | Funções reutilizáveis e interface de execução do projeto. |
| `workflow/` | Automação quando houver múltiplas etapas ou necessidade de retomada. |
| `tests/` | Verificações de transformações e resultados críticos. |
| `results/example/` | Saídas esperadas pequenas e relatório de referência. |
| `envs/` | Ambiente específico e dependências fixadas para a plataforma declarada. |

O registro de exploração deverá responder: o que foi perguntado, o que se tentou, por que se escolheu o método, que resultado apareceu, quais limitações surgiram e qual decisão foi tomada. Resultados negativos deverão ser preservados quando informativos.

Os notebooks servirão para ensino e exploração. O processamento reutilizável deverá ficar em funções e scripts, permitindo automatização e comparação de execuções.

## 9. Reprodutibilidade verificável e manutenção

Criar ambientes por módulo ou etapa quando necessário. Registrar versões, configurações, sementes, snapshots dos dados e plataforma. Containers e arquivos de ambiente ajudam a controlar dependências; sua presença, isoladamente, não garante reprodução. A documentação do Snakemake descreve implantação com ambientes e containers, inclusive fixação de versões. [11]

Oferecer dois modos: **demonstração**, com dados pequenos e saídas de referência, e **estudo completo**, com requisitos e custo computacional medidos. Trajetórias e conjuntos volumosos terão instruções de obtenção e verificação, conforme suas condições de acesso.

Para Windows com VS Code, documentar os módulos testados nativamente. Quando o ecossistema exigir Linux, fornecer uma rota específica por WSL2 ou ambiente equivalente e verificar essa rota antes de anunciá-la como suportada.

Os testes deverão proteger decisões e transformações científicas relevantes: unidades, identificadores, correspondência entre dados e amostras, isolamento entre treinamento e teste, cálculo de métricas e interpretação de falhas. Os exemplos rápidos serão executados automaticamente; simulações caras terão registros de execução próprios.

Nos cálculos estocásticos e sensíveis à plataforma, definir tolerâncias e critérios científicos de comparação. Reprodutibilidade numérica bit a bit e consistência estatística são objetivos distintos e deverão ser declarados conforme o caso.

## 10. Cronograma indicativo

Planejamento para outubro de 2026 a dezembro de 2027, condicionado à disponibilidade semanal, aos dados e à infraestrutura. Os tempos serão revistos após a primeira entrega completa.

| Período | Prioridade | Marco verificável |
|---|---|---|
| Outubro–dezembro de 2026 | Fundação, padrão documental e Projeto 01. | Primeiro ciclo de dados a relatório reproduzido por outra pessoa. |
| Janeiro–março de 2027 | Projetos 02 e 03. | Alvo justificado e conjunto químico curado com proveniência. |
| Abril–junho de 2027 | Projeto 04 e início do Projeto 05. | Benchmark de predição e protocolo inicial de docking avaliados. |
| Julho–setembro de 2027 | Conclusão do Projeto 05 e Projeto 06. | Validação de docking e análise de trajetórias com incerteza. |
| Outubro–dezembro de 2027 | Estudo integrador, revisão externa e consolidação. | Versão pública documentada e relato de reprodução independente. |

Extensões avançadas dependerão da conclusão e qualidade dos módulos necessários. Uma extensão poderá substituir outra no planejamento se responder melhor à pergunta científica central.

## 11. Critérios para uma entrega publicável

Um projeto estará pronto quando tiver pergunta delimitada; dados rastreáveis; execução documentada; resultado de referência; avaliação coerente; interpretação das figuras; limitações explícitas; custo computacional registrado; e evidência de execução em ambiente declarado.

As metas iniciais serão seis módulos úteis, um estudo integrador e pelo menos uma reprodução independente documentada. Indicadores complementares serão reutilização, contribuições, relatos de aplicação, problemas corrigidos e qualidade das explicações. Estrelas e visitas serão indicadores de alcance, sem substituir evidência de utilidade.

A inovação deverá ser demonstrada por uma pergunta relevante, comparação com uma referência e benefício observável: melhor rastreabilidade, análise de incerteza, adaptação a dados de laboratório, menor custo ou diagnóstico de uma limitação negligenciada. O uso de uma técnica avançada, sozinho, não define originalidade.

## 12. Primeiro ciclo de trabalho

1. Selecionar um problema de análise experimental pequeno e definir sua pergunta, entradas e resultado esperado.
2. Montar a estrutura mínima do repositório e preencher os modelos de documentação para esse projeto.
3. Desenvolver um exemplo completo com dados simulados identificados e pelo menos um cenário de falha conhecido.
4. Produzir figuras, relatório e explicação das decisões; registrar as versões usadas.
5. Solicitar que outra pessoa execute o roteiro, corrigir os obstáculos observados e registrar a primeira versão.

O primeiro marco será um workflow pequeno que produza um resultado compreensível e reproduzível. A partir dele, o portfólio poderá crescer preservando o mesmo padrão de qualidade.

## Referências técnicas

Fontes consultadas em 6 de outubro de 2026. As recomendações de arquitetura, escopo e cronograma são decisões propostas para este portfólio.

1. Assay Guidance Manual. [Assay Operations for SAR Support](https://ncbi.nlm.nih.gov/sites/books/NBK91994/) e [Data Standardization for Results Management](https://www.ncbi.nlm.nih.gov/books/NBK91993/?report=classic). Referências para interpretação e documentação de resultados de ensaios.
2. EMBL-EBI / AlphaFold Protein Structure Database. [Frequently Asked Questions](https://www.alphafold.ebi.ac.uk/faq). Confiança dos modelos, aplicações e limitações.
3. RDKit. [Getting Started with the RDKit in Python](https://www.rdkit.org/docs/GettingStartedInPython.html). Descritores, fingerprints e recursos de análise química.
4. Wu et al. [MoleculeNet: a benchmark for molecular machine learning](https://doi.org/10.1039/C7SC02664A). Chemical Science, 2018. Benchmarks e estratégias de avaliação.
5. AutoDock Vina. [Frequently Asked Questions](https://autodock-vina.readthedocs.io/en/stable/faq.html). Validação específica para o alvo e limitações do modelo.
6. Communications Biology. [Reliability and reproducibility checklist for molecular dynamics simulations](https://www.nature.com/articles/s42003-023-04653-0), 2023. Amostragem, análise e descrição das simulações.
7. pymbar. [The timeseries module](https://pymbar.readthedocs.io/en/stable/timeseries.html). Autocorrelação e análise de amostras temporalmente dependentes.
8. [Assessing the performance of MM/PBSA and MM/GBSA methods. 7. Entropy effects on the performance of end-point binding free energy calculation approaches](https://pubmed.ncbi.nlm.nih.gov/29785435/), 2018. Avaliação empírica de aproximações de energia livre.
9. PLUMED. [Masterclass 21.3: Umbrella sampling](https://www.plumed.org/doc-v2.9/user-doc/html/masterclass-21-3.html). Reconstrução de perfis e avaliação de erros.
10. American Statistical Association. [Statement on Statistical Significance and P-Values — comunicado oficial](https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf), 2016. Princípios para interpretação de significância estatística.
11. Snakemake. [Distribution and Reproducibility](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html). Ambientes e implantação reproduzível de workflows.
