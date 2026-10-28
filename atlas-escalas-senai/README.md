# Atlas de Escalas · SENAI

**Estudo e pesquisa exploratória** para estudantes de biologia e química.

Percorra, como um “mapa” de escalas, o caminho:

**organismo → órgão → tecido → célula → organela → molécula → átomo**

com painéis laterais de **bioinformática** e **quimioinformática**.

A vista celular inclui um HUD ilustrativo (ATS MATRIX · demonstração): métricas
sobre o “vidro”, rede dourada, mitocôndrias âmbar e ciclo de colorações. Os
números são **didáticos**, não um laudo de microscopia.

## Rodar local

```bash
cd atlas-escalas-senai
npm install
npm run dev
```

Abra o endereço indicado no terminal (em geral `http://localhost:5173`).

Build de produção:

```bash
npm run build
npm run preview
```

## O que há em cada modo

| Modo | Conteúdo |
|---|---|
| Contexto | Pergunta-guia, enquadramento SENAI e limites do estudo |
| Bioinformática | Genes, sequências-exemplo, mitocôndria, ligação ao portfólio |
| Quimioinformática | Fórmula, polaridade, SMILES e modelo 3D local (Three.js) |

## Relação com o repositório

Este módulo educacional complementa os workflows em `projects/`
(`drug-discovery-workflows`). Não substitui curadoria UniProt/ChEMBL/PDB nem
os demos científicos versionados.

## Limites

- Protótipo educacional / pesquisa exploratória.
- HUD celular ilustrativo.
- Modelo molecular esquemático (não docking / QSAR).
