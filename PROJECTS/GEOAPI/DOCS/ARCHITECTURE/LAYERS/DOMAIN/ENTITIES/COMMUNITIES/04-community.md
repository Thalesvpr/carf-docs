---
type: leaf
status: approved
updated: 2026-02-07
---

# Community

Entidade aggregate root representando uma comunidade ou assentamento que agrupa unidades habitacionais em um contexto geografico e social especifico. Serve como unidade organizacional principal para processos de regularizacao fundiaria e como escopo de autorizacao de acesso para equipes de campo. Herda de BaseAggregateRoot suportando domain events.

## Papel no Dominio

A comunidade e o nivel organizacional mais alto abaixo do tenant. Toda unidade pertence obrigatoriamente a uma comunidade. Equipes de campo recebem autorizacao de acesso por comunidade via CommunityAuthorization. O download de pacotes para operacao offline no REURBCAD e filtrado por comunidades autorizadas para a equipe do usuario.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| TenantId | Guid | nao | Municipio. FK para Tenant. |
| Code | string | nao | Codigo unico por tenant. |
| Name | string | nao | Nome da comunidade. |
| CommunityType | string | nao | Tipo da comunidade. Valores: URBANA (area urbana com infraestrutura), RURAL (area rural ou periurbana), QUILOMBOLA (comunidade quilombola com legislacao especifica), RIBEIRINHA (comunidade ribeirinha com legislacao especifica). |
| Boundary | Polygon | sim | Perimetro da comunidade em WGS84 SRID 4326. Usado para validar que unidades estao dentro dos limites. |
| Area | decimal | sim | Area em metros quadrados calculada via PostGIS ST_Area. |
| Municipality | string | nao | Nome do municipio. |
| State | string | nao | UF com 2 caracteres. |
| District | string | sim | Distrito. |
| Neighborhood | string | sim | Bairro. |
| Reference | string | sim | Ponto de referencia para localizacao. |
| Status | string | nao | Status da comunidade. Default ACTIVE. |
| CreatedAt | DateTime | nao | Data de criacao. |
| UpdatedAt | DateTime | nao | Ultima atualizacao. |
| CreatedBy | Guid | nao | Quem criou. |
| UpdatedBy | Guid | nao | Quem atualizou. |
| DeletedAt | DateTime | sim | Soft delete. |

## Relacionamentos

Colecao de Units vinculadas via community_id. Hierarquia espacial opcional com Blocks subdividindo a comunidade em quadras. CommunityAuthorizations controlando quais Teams ou Accounts tem permissao de acesso.

## Invariantes de Negocio

Code deve ser unico por tenant. Boundary, quando preenchido, deve ser poligono valido conforme ST_IsValid. CommunityType determina legislacao aplicavel: QUILOMBOLA e RIBEIRINHA possuem marcos legais especificos alem da Lei 13.465/2017.

Comunidade nao pode ser excluida se possuir unidades ativas vinculadas.

## Domain Events

CommunityCreatedEvent emitido ao criar. CommunityUpdatedEvent emitido ao atualizar campos.
