---
type: leaf
status: review
updated: 2026-02-08
---

# Community Commands

Os commands de comunidades representam operacoes de escrita sobre o agregado Community. Cada command e um record imutavel implementando IRequest do MediatR. Os handlers coordenam validacao espacial via PostGIS e persistencia com controle de unicidade por tenant.

---

## CreateCommunityCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| Code | string | sim | Codigo unico por tenant |
| Name | string | sim | Nome da comunidade |
| CommunityType | string | sim | URBANA, RURAL, QUILOMBOLA, RIBEIRINHA |
| Boundary | GeometryDto | nao | Poligono GeoJSON do perimetro |
| Municipality | string | sim | Municipio |
| State | string | sim | UF com 2 letras |
| District | string | nao | Distrito |
| Neighborhood | string | nao | Bairro |
| Reference | string | nao | Ponto de referencia |

O handler primeiro verifica unicidade do codigo por tenant usando constraint UNIQUE em (tenant_id, code). Segundo, quando boundary e informado, valida o poligono via PostGIS ST_IsValid garantindo que e valido, fechado e sem auto-interseccao. Terceiro, cria a entidade Community com status ACTIVE e calcula area via ST_Area quando boundary esta presente. Quarto, persiste via repositorio e retorna CommunityDto.

Emite CommunityCreatedEvent com Id, Code e TenantId. Erros possiveis: VALIDATION_ERROR para codigo duplicado ou boundary invalido.

---

## UpdateCommunityCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| Id | Guid | sim | Identificador da comunidade |
| Name | string | nao | Nome atualizado |
| Boundary | GeometryDto | nao | Novo perimetro |
| District | string | nao | Distrito atualizado |
| Neighborhood | string | nao | Bairro atualizado |
| Reference | string | nao | Referencia atualizada |

O handler carrega a comunidade pelo Id e aplica atualizacoes parciais. Quando o boundary e alterado, revalida via ST_IsValid e recalcula area via ST_Area. O codigo e o tipo da comunidade nao podem ser alterados apos criacao.

Emite CommunityBoundaryChangedEvent quando o boundary e alterado, contendo Id e novo boundary em GeoJSON.
