---
type: leaf
status: review
updated: 2026-02-08
---

# Holder Queries

As queries de titulares implementam o lado de leitura do CQRS para a entidade Holder. Todas sao records imutaveis retornando DTOs otimizados para cada cenario de uso.

## GetHolderByIdQuery

Recebe Id do titular como Guid. O handler projeta diretamente para HolderDto via Select, incluindo CPF mascarado e idade calculada. Retorna Result contendo HolderDto ou 404 se nao encontrado.

## ListHoldersQuery

| Parametro | Tipo | Padrao | Descricao |
|-----------|------|--------|-----------|
| Page | int | 1 | Pagina atual |
| Limit | int | 20 | Registros por pagina (maximo 100) |
| Search | string | nulo | Busca por nome ou CPF |
| SortBy | string | full_name | Campo de ordenacao |
| SortDir | string | asc | Direcao da ordenacao |

O handler aplica filtros Where para search (busca textual em full_name e cpf), ordenacao dinamica e paginacao via Skip/Take. Retorna PaginatedResult de HolderListItemDto contendo id, cpf mascarado, full_name, birth_date e total de unidades vinculadas.

## GetHolderByCpfQuery

Recebe cpf como string de 11 digitos. O handler consulta pelo par (tenant_id, cpf) usando o indice UNIQUE. Retorna HolderDto se encontrado ou 404 se nao existe no tenant.

## GetHolderStatisticsQuery

Recebe filtro opcional por CommunityId. O handler calcula agregacoes como total de titulares no tenant, contagem por genero e distribuicao por estado civil. Retorna HolderStatisticsDto.
