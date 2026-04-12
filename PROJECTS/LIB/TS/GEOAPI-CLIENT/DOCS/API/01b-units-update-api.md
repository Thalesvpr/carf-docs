---
type: leaf
status: review
updated: 2026-02-08
---

# Units API - Criacao, Atualizacao e Remocao

Detalhamento dos campos do CreateUnitDTO conforme [API Reference](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/00-api-reference.md) e metodos update e delete do modulo api.units. Tipos TypeScript importados de @carf/tscore/types conforme [02-types-entities](../../TSCORE/DOCS/API/02-types-entities.md).

## Endpoints

| Metodo HTTP | Rota | Descricao | Sucesso | Erros | Roles |
|:------------|:-----|:----------|:--------|:------|:------|
| POST | /api/units | Criar unidade | 201 | 400 VALIDATION_ERROR, 401, 403 | todos autenticados |
| PATCH | /api/units/{id} | Atualizar unidade | 200 | 403 UNIT_LOCKED, 404, 409 VERSION_CONFLICT | todos autenticados |
| DELETE | /api/units/{id} | Excluir unidade em rascunho | 204 | 400 NOT_DRAFT, 404 | todos autenticados |

## Campos do CreateUnitDTO

O campo code nao e enviado na criacao pois e gerado automaticamente pelo servidor no formato UNI-AAAA-NNNNN. O campo communityId e obrigatorio para vincular a unidade a uma comunidade existente.

| Campo | Tipo TS | Obrigatorio | Descricao |
|:------|:--------|:------------|:----------|
| communityId | string | sim | UUID da comunidade destino |
| street | string | sim | Logradouro, maximo 200 caracteres |
| number | string | sim | Numero do endereco, maximo 20 caracteres |
| complement | string | nao | Complemento, maximo 100 caracteres |
| neighborhood | string | sim | Bairro, maximo 100 caracteres |
| city | string | sim | Cidade, maximo 100 caracteres |
| state | string | sim | UF com exatamente 2 letras |
| zipCode | string | sim | CEP sem formatacao, 9 caracteres |
| geometry | GeoJsonPolygon | nao | Objeto GeoJSON com type Polygon e coordinates WGS84 |
| photos | array de string | nao | UUIDs de documentos previamente uploaded |
| blockId | string | nao | UUID da quadra |
| plotId | string | nao | UUID do lote |
| buildingId | string | nao | UUID da edificacao |
| occupantType | OccupantType | nao | POSSUIDOR ou LOCATARIO |
| utilizationType | UtilizationType | nao | RESIDENCIAL, COMERCIAL, MISTO, TERRENO_VAZIO ou NAO_HABITADO |
| unitCondition | UnitCondition | nao | OCUPADA, VAZIA, EM_CONSTRUCAO ou ABANDONADA |
| attendanceStatus | AttendanceStatus | nao | AUSENTE, PRESENTE, NAO_QUIS ou ASSINADO |
| residenceTime | string | nao | Tempo de moradia declaratorio em texto livre |
| observation | string | nao | Observacoes do agente de campo |
| customData | Record de string para unknown | nao | Dados especificos do tenant |

A response retorna UnitDto completo com id gerado, code automatico, status DRAFT, timestamps createdAt e updatedAt, e version 1.

## update (PATCH)

O metodo update aceita id string e UpdateUnitDTO, retornando Promise de Unit atualizado. O UpdateUnitDTO contem os mesmos campos do CreateUnitDTO todos opcionais, acrescido do campo obrigatorio version (number) para concorrencia otimista. O servidor compara a version enviada com a armazenada e retorna ConflictError 409 com code VERSION_CONFLICT se divergirem, indicando que outro usuario editou a unidade desde a ultima leitura. O client deve re-buscar a unidade e re-aplicar as mudancas. Unidades com status APPROVED ou REJECTED lancam ForbiddenError 403 com code UNIT_LOCKED.

## delete

O metodo delete aceita id string e retorna void (204 No Content). Executa soft delete preenchendo o campo deletedAt. Apenas unidades em status DRAFT podem ser deletadas; unidades em qualquer outro status lancam ValidationError 400 com code NOT_DRAFT. A unidade nao aparece mais em listagens apos a remocao. Lanca NotFoundError 404 se a unidade nao existir ou ja estiver deletada.
