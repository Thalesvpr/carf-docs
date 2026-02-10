---
type: leaf
status: review
updated: 2026-02-08
---

# Holders Controller

O HoldersController gerencia operacoes REST sobre titulares de unidades habitacionais. Anotado com ApiController e Authorize, exige autenticacao JWT em todos os endpoints. A rota base e /api/holders. Toda logica e delegada ao MediatR via commands e queries, mantendo o controller como camada fina de traducao HTTP.

## Endpoints

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| POST | /api/holders | Criar titular | 201 | 400 CPF_INVALID, 409 CPF_EXISTS | todos autenticados |
| GET | /api/holders/{id} | Obter titular | 200 | 404 | todos autenticados |
| GET | /api/holders | Listar com paginacao | 200 | - | todos autenticados |
| PATCH | /api/holders/{id} | Atualizar titular | 200 | 404 | todos autenticados |
| DELETE | /api/holders/{id} | Excluir titular sem unidades | 204 | 400 HAS_UNITS | todos autenticados |
| GET | /api/holders/search?cpf= | Buscar por CPF | 200 | 404 | todos autenticados |
| POST | /api/holders/import | Importar planilha | 200 | 400 VALIDATION_ERROR | analyst+ |
| POST | /api/units/{unitId}/holders/{holderId}/link | Vincular titular a unidade | 200 | 404 UNIT_NOT_FOUND, 404 HOLDER_NOT_FOUND, 409 ALREADY_LINKED | todos autenticados |
| DELETE | /api/units/{unitId}/holders/{holderId}/unlink | Desvincular titular de unidade | 204 | 404 LINK_NOT_FOUND | todos autenticados |

> **Nota de organizacao**: Os endpoints link/unlink usam rotas sob `/api/units/{unitId}/holders/` seguindo convencoes REST (recurso subordinado), porem os action methods estao no HoldersController por decisao de agrupamento de responsabilidade sobre titulares. Isso nao e um bug — e uma escolha de organizacao de codigo.

## Comportamento

O endpoint de criacao monta CreateHolderCommand com CPF, nome completo, data de nascimento, genero, estado civil e dados de documentacao, retornando CreatedAtAction apontando para GetById com HolderDto no body. A validacao de CPF via Mod-11 ocorre no validator antes do handler. O endpoint de busca por CPF recebe query param cpf como string de 11 digitos e despacha GetHolderByCpfQuery, retornando HolderDto ou 404. O endpoint de importacao aceita multipart/form-data com arquivo XLSX ou CSV, requer role analyst ou superior e retorna relatorio com totais de linhas processadas, importadas e erros detalhados por linha. O endpoint de exclusao verifica vinculos ativos em unit_holders antes de executar soft delete, retornando 400 HAS_UNITS quando existem unidades vinculadas.

## Autorizacao

Todos os endpoints de CRUD basico sao acessiveis por qualquer usuario autenticado do tenant. O endpoint de importacao requer role analyst, manager, admin ou super-admin. O isolamento por tenant e garantido via RLS, filtrando automaticamente titulares por tenant_id do JWT.
