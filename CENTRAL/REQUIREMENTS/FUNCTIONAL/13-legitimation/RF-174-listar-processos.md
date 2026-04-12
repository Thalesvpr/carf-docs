---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-174: Listar Processos

## Descricao

Sistema deve fornecer interface de listagem de processos de legitimacao fundiaria com filtros avancados permitindo segmentacao por status (Em Analise, Documentacao Pendente, Aprovado, Concluido, Indeferido), comunidade de origem e periodo de criacao ou atualizacao. Implementacao utiliza paginacao eficiente carregando registros em lotes configuraveis para otimizar desempenho em bases com milhares de processos. Busca textual permite localizar processos por numero de protocolo, nome do titular ou endereco da unidade utilizando indexacao full-text. Listagem apresenta colunas configuraveis com numero, titular, unidade vinculada, status e data de criacao, permitindo ordenacao por qualquer coluna. Dados filtrados automaticamente por tenant_id do usuario autenticado.

## Criterios de Aceitacao

1. Filtros por status, comunidade e periodo
2. Paginacao com lotes configuraveis
3. Busca textual por protocolo, titular ou endereco
4. Ordenacao por qualquer coluna
5. Segregacao automatica por tenant

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-172
