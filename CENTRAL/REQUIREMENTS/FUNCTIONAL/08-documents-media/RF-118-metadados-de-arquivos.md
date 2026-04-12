---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-118: Metadados de Arquivos

## Descricao

Sistema deve armazenar metadados abrangentes para cada arquivo: nome original preservado, tamanho em bytes, tipo MIME real validado, data/hora de upload com timezone, e usuario responsavel. Campos atualizados automaticamente durante upload sem intervencao manual. Interface frontend exibe metadados claramente em detalhes ou listagens expandidas. Validacao e normalizacao durante ingestao com formatacao de tamanhos e datas. Metadados indexados para buscas eficientes por nome, tipo ou data.

## Criterios de Aceitacao

1. Nome original, tamanho, tipo MIME, timestamp, usuario
2. Atualizacao automatica no upload
3. Exibicao clara no frontend
4. Formatacao legivel (KB/MB, datas)
5. Indices para buscas eficientes

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-102, RF-108
