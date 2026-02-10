---
type: leaf
status: review
updated: 2026-02-08
---

# API de Tipos

Documentacao das interfaces e enums de dominio exportados pelo modulo types do tscore. Todos os tipos espelham modelos do backend .NET e o [schema PostgreSQL](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/INFRA/PERSISTENCE/02-database-schema.md) para consistencia entre frontend e API, cobrindo entidades, enums e DTOs utilizados pelos sistemas REURBCAD, GEOWEB, ADMIN e demais clientes do ecossistema CARF.

O modulo types exporta mais de vinte interfaces de entidade de dominio e dezessete enums de classificacao e status. DTOs de API (Create*Request, Update*Request) sao agora gerados automaticamente pelo @carf/geoapi-client via orval e nao fazem mais parte do tscore. A documentacao completa esta organizada nos seguintes sub-documentos.

A secao de [entidades](./02-types-entities.md) documenta as interfaces de dominio principal com tabela de propriedades completa para cada uma: Unit (32 propriedades), Holder (27 propriedades), Community, Team, Account, Tenant, Block, Plot, Building, Document, Annotation, Orthophoto, SyncLog e AuditLog. Inclui tambem os tipos GeoJSON auxiliares (GeoJsonPolygon, GeoJsonPoint, GeoJsonFeature, GeoJsonFeatureCollection).

A secao de [relacionamentos e infraestrutura](./03-types-relationships.md) cobre entidades de juncao (UnitHolder, TeamMember, CommunityAuthorization) com constraints e regras de negocio, entidades de legitimacao (LegitimationRequest, LegitimationResponse, LegitimationCertificate) com todos os campos do ciclo de vida, e entidades GIS (Layer, LayerFeature) e autenticacao (ApiKey).

A secao de [enums](./04-types-enums.md) documenta todos os dezessete enums com tabelas de valores, descricoes e correspondencia com CHECK constraints do schema PostgreSQL. Inclui enums de status (UnitStatus, LegitimationStatus, SyncStatus, AttendanceStatus, OccupantType, UtilizationType, UnitCondition), roles (Role, TeamRole), classificacao (CommunityType, DocumentType, AnnotationType, Decision, CertificateSituation, RelationshipType) e referencia (EntityType, Priority).

A secao de [DTOs e versionamento](./05-types-dtos.md) descreve interfaces de response (PaginatedResponse, ErrorResponse, SyncPullResponse, GeoJsonFeature) e a tabela de entidades com controle de versao para sincronizacao offline. DTOs de request (Create*Request, Update*Request) sao gerados automaticamente pelo @carf/geoapi-client via orval a partir do swagger.json da GEOAPI.
