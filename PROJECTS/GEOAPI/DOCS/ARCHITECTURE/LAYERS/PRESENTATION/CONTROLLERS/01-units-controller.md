---
type: leaf
status: active
updated: 2026-02-07
---

# Units Controller

O UnitsController e o controller REST principal para operacoes de unidades habitacionais. Anotado com ApiController e Authorize, exige autenticacao em todos os endpoints. Delega toda a logica ao MediatR, enviando commands para operacoes de escrita e queries para operacoes de leitura.

## Endpoints

| Metodo | Rota | Descricao | Sucesso | Erro |
|--------|------|-----------|---------|------|
| POST | /api/units | Criar unidade | 201 Created com UnitDto e header Location | 400 Bad Request com ProblemDetails |
| GET | /api/units/{id} | Obter por id | 200 OK com UnitDto | 404 Not Found |
| GET | /api/units | Listar com filtros e paginacao | 200 OK com PagedResult de UnitSummaryDto | - |
| PATCH | /api/units/{id} | Atualizar endereco e geometria | 200 OK com UnitDto | 400 ou 403 se unidade travada |
| POST | /api/units/{id}/submit | Submeter para analise | 200 OK | 400 com ProblemDetails |
| DELETE | /api/units/{id} | Excluir unidade rascunho | 204 No Content | 400 com ProblemDetails |

## Comportamento dos Endpoints

O endpoint de criacao monta um CreateUnitCommand com endereco, geometria, comunidade e fotos, e retorna CreatedAtAction apontando para GetById. O endpoint de consulta por id aceita query params opcionais includeHolders e includeCommunity para controlar eager loading de relacionamentos. A listagem recebe ListUnitsQueryParams que converte para query CQRS internamente. O endpoint de atualizacao trata o erro UNIT_LOCKED retornando 403 Forbid, diferenciando de erros genericos de validacao que retornam 400.
