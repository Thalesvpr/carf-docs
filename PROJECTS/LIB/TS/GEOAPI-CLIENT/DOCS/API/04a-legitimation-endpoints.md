---
type: leaf
status: review
updated: 2026-02-07
---

# Legitimation API - Endpoints e Consultas

## Visao Geral

A Legitimation API fornece operacoes para gerenciamento de processos de legitimacao fundiaria, permitindo controlar o fluxo de aprovacao de titulos de propriedade. O acesso ocorre via o namespace api.legitimation no GeoApiClient.

## Endpoints

| Metodo HTTP | Rota | Descricao |
|:------------|:-----|:----------|
| GET | /api/legitimation | Listar processos |
| GET | /api/legitimation/:id | Buscar por ID |
| POST | /api/legitimation | Criar processo |
| POST | /api/legitimation/:id/actions | Executar acao de workflow |
| GET | /api/legitimation/:id/history | Historico de acoes |
| GET | /api/legitimation/:id/documents | Documentos do processo |
| POST | /api/legitimation/:id/documents | Anexar documento |
| GET | /api/legitimation/:id/certificate | Download certificado |

## Metodo list

Lista processos de legitimacao com filtros. Recebe um objeto opcional de consulta e retorna PaginatedResponse de Legitimation.

### Parametros de Consulta

| Campo | Tipo | Obrigatorio | Descricao |
|:------|:-----|:------------|:----------|
| page | number | Nao | Pagina atual |
| limit | number | Nao | Itens por pagina |
| communityId | string | Nao | Filtrar por comunidade |
| unitId | string | Nao | Filtrar por unidade |
| holderId | string | Nao | Filtrar por posseiro |
| status | LegitimationStatus | Nao | Filtrar por status |
| assignedTo | string | Nao | Usuario responsavel |
| createdAfter | Date | Nao | Data inicio |
| createdBefore | Date | Nao | Data fim |
| sortBy | string | Nao | Ordenar por createdAt, updatedAt ou status |
| sortOrder | string | Nao | Direcao asc ou desc |

Para listar processos pendentes atribuidos ao usuario corrente, informe status como PENDING_ANALYSIS e assignedTo com o ID do usuario. Para filtrar por unidade, informe unitId.

## Metodo getById

Busca processo por ID. Recebe o ID como string e um objeto opcional com campo include, que aceita um array contendo unit, holder, documents ou history. Retorna o objeto Legitimation com as relacoes solicitadas carregadas.
