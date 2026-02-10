---
type: leaf
status: review
updated: 2026-02-07
---

# Holders API - Operacoes CRUD

O modulo holders do GeoApiClient expoe metodos para gerenciamento de posseiros e titulares de unidades habitacionais em processo de regularizacao fundiaria. Os metodos sao acessiveis via api.holders.

## Endpoints

| Metodo HTTP | Rota | Descricao |
|:------------|:-----|:----------|
| GET | /api/holders | Listar posseiros com filtros |
| GET | /api/holders/:id | Buscar posseiro por ID |
| POST | /api/holders | Criar novo posseiro |
| PATCH | /api/holders/:id | Atualizar posseiro |
| DELETE | /api/holders/:id | Deletar posseiro via soft delete |

## list

O metodo list aceita ListHoldersQueryDTO opcional e retorna Promise de PaginatedResponse de Holder.

| Parametro | Tipo | Obrigatorio | Descricao |
|:----------|:-----|:------------|:----------|
| page | number | nao | Pagina atual, padrao 1 |
| limit | number | nao | Itens por pagina, padrao 20, maximo 100 |
| communityId | string | nao | Filtrar por comunidade |
| search | string | nao | Busca em nome, CPF, CNPJ e email |
| sortBy | enum | nao | name, createdAt ou updatedAt |
| sortOrder | enum | nao | asc ou desc |
| include | array | nao | Aceita units para incluir unidades vinculadas |

## getById

O metodo getById aceita id string obrigatorio e opcoes com include opcional aceitando units. Retorna Promise de Holder completo.

## create

O metodo create aceita CreateHolderDTO e retorna Promise de Holder com ID gerado. Campos detalhados em 02b-holders-search-import-api.

## update

O metodo update aceita id string e UpdateHolderDTO com campos parciais. Retorna Promise de Holder atualizado.

## delete

O metodo delete aceita id string e retorna void. Executa soft delete. Posseiro vinculado a unidades nao pode ser deletado. E necessario desvincular de todas as unidades antes da remocao.
