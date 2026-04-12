---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-205: Relatorio de Progresso de Cadastramento

## Descricao

Sistema deve gerar relatorio analitico de acompanhamento da evolucao temporal do processo de cadastramento territorial, apresentando grafico de linha ilustrando progresso acumulado de unidades cadastradas ao longo do tempo com periodos configuraveis (dias, semanas, meses). Comparacao visual entre metas estabelecidas no plano de trabalho e realizado efetivamente pelas equipes permite identificacao de desvios de cronograma, atrasos ou superacao de expectativas. Filtros dinamicos segmentam analise por comunidade, equipe tecnica ou combinacao de criterios. Fundamental para gestao de projetos de regularizacao sob prazos contratuais, permitindo identificacao precoce de problemas e comunicacao transparente de progresso. Dados filtrados por tenant_id.

## Criterios de Aceitacao

1. Grafico de linha com evolucao temporal
2. Comparacao meta vs realizado
3. Filtros por comunidade e equipe
4. Periodos configuraveis (dia/semana/mes)
5. Segregacao por tenant_id

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-044, RF-017
