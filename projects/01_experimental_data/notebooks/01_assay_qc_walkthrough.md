# Roteiro didático — Projeto 01

Este notebook espelha `python -m src.run_demo` com explicações passo a passo.

## Sequência

1. **Problema** — comparar potência a partir de leituras de placa.
2. **Fundamento** — controles, Z′, percent response, 4PL (`docs/theory.md`).
3. **Entrada** — CSVs em `data/example/`.
4. **Preparação** — QC e exclusões.
5. **Execução** — normalização e ajuste.
6. **Saída** — tabelas e figuras em `results/example/`.
7. **Interpretação** — o que a IC50 significa e o que não significa.
8. **Erros frequentes** — misturar unidades; tratar réplica técnica como biológica; omitir falhas de QC.
9. **Limitações** — ver `docs/limitations.md`.
10. **Exercício** — altere `min_zprime` em `configs/demo.yaml` e registre o efeito no relatório.

```python
# Executar a partir de projects/01_experimental_data
from src.run_demo import run
run()
```

Resposta comentada do exercício: elevar `min_zprime` pode marcar P02 como FAIL
mesmo após exclusão de bordas se a separação residual for insuficiente; isso não
apaga automaticamente as curvas, mas deve impedir uma conclusão confiante sem
revisão — o relatório deve tornar essa tensão visível.
