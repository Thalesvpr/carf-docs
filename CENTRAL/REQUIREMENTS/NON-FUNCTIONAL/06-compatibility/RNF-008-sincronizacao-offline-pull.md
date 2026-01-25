---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-008: Sincronizacao Offline - Pull

## Descricao

Download inicial de comunidade com ate 5000 unidades em 30 segundos. Compressao gzip obrigatoria. Armazenamento local em SQLite. Download incremental em sincronizacoes subsequentes.

## Metricas

- Download inicial: <= 30s para 5000 unidades
- Compressao: gzip obrigatorio
- Armazenamento: SQLite local no dispositivo

## Criterios de Aceitacao

1. Barra de progresso com estimativa de tempo restante
2. Download incremental transfere apenas dados novos/modificados
3. Retomada de download interrompido sem reiniciar do zero
