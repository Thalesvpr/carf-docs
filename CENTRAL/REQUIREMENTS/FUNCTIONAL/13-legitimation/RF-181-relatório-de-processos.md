---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-181: Relatorio de Processos

## Descricao

Sistema deve oferecer geracao de relatorio consolidado sobre processos de legitimacao fundiaria agregando informacoes cadastrais, estatisticas de tramitacao e indicadores de desempenho. Filtros configuraveis permitem segmentar processos por periodo, status atual, comunidade de origem e responsavel pela analise. Relatorio apresenta estatisticas agregadas como total de processos por status, tempo medio de tramitacao entre etapas do workflow, taxa de aprovacao versus indeferimento e distribuicao temporal de criacao de processos. Exportacao disponibilizada em multiplos formatos incluindo Excel com planilhas estruturadas e formulas para analises adicionais, e PDF com formatacao profissional para apresentacoes institucionais. Dados filtrados por tenant_id do usuario.

## Criterios de Aceitacao

1. Filtros por periodo, status, comunidade e responsavel
2. Estatisticas agregadas por status
3. Indicadores de tempo medio e taxa de aprovacao
4. Exportacao em Excel e PDF
5. Segregacao por tenant

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-172, RF-174, RF-175
