---
type: leaf
status: review
updated: 2026-02-08
---

# Tipos TypeScript

Interfaces e enums de dominio CARF exportados pelo modulo @carf/tscore/types, garantindo type safety e autocomplete em todos os frontends do ecossistema. Os tipos sao a fundacao compartilhada entre REURBCAD, REURBWEB, ADMIN e as bibliotecas @carf/geoapi-client e @carf/ui-native.

## Mapeamento com Backend .NET e PostgreSQL

Cada interface TypeScript espelha a entidade correspondente no backend .NET que por sua vez mapeia para uma tabela no [schema PostgreSQL](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/INFRA/PERSISTENCE/02-database-schema.md). A correspondencia de tipos segue convencoes consistentes: uuid do PostgreSQL mapeia para string no TypeScript (por ser representado como texto nos JSONs da API), timestamptz mapeia para string ISO 8601, decimal mapeia para number, int mapeia para number, varchar mapeia para string, boolean mapeia para boolean, jsonb mapeia para Record de string para unknown ou interface tipada, e geometry PostGIS mapeia para objetos GeoJSON (GeoJsonPolygon, GeoJsonPoint). Campos nullable no PostgreSQL tornam-se propriedades opcionais com union type "T ou null" no TypeScript.

O processo de sincronizacao entre backend e frontend e manual: quando o backend modifica modelos .NET ou schema PostgreSQL, as interfaces TypeScript devem ser atualizadas correspondentemente. Documentos de API do TSCORE ([02-types-entities](../API/02-types-entities.md), [03-types-relationships](../API/03-types-relationships.md)) servem como referencia canonica para essa sincronizacao. No futuro, geracao automatica via NSwag (que le a especificacao OpenAPI do .NET e gera tipos TypeScript) podera automatizar esse processo.

## Organizacao dos Tipos

Os tipos estao organizados em tres categorias exportadas pelo modulo @carf/tscore/types. As [entidades](../API/02-types-entities.md) incluem as interfaces de dominio principal: Unit com mais de 30 propriedades tipadas, Holder com dados pessoais e documentais, Community, Team, Account, Tenant, Block, Plot, Building, Document, Annotation, Orthophoto, SyncLog e AuditLog. Os [relacionamentos](../API/03-types-relationships.md) cobrem interfaces de juncao (UnitHolder, TeamMember, CommunityAuthorization) e de legitimacao (LegitimationRequest, LegitimationResponse, LegitimationCertificate, Layer, LayerFeature, ApiKey). Os [enums](../API/04-types-enums.md) definem todos os conjuntos de valores aceitos: UnitStatus (6 valores), LegitimationStatus (11), Role (6), TeamRole (2), CommunityType (4), DocumentType (8), AnnotationType (4), Priority (4), SyncStatus (5), OccupantType (2), UtilizationType (5), UnitCondition (4), AttendanceStatus (4), RelationshipType (5), EntityType (5), Decision (2) e CertificateSituation (3). DTOs de API (Create*Request, Update*Request) sao gerados automaticamente pelo @carf/geoapi-client via orval e nao fazem parte do tscore. O tscore exporta apenas interfaces de response genericas como PaginatedResponse, ErrorResponse e tipos de sincronizacao.

## Versionamento de Tipos

Os tipos seguem o versionamento semantico do pacote @carf/tscore. Breaking changes em interfaces (remover propriedade, alterar tipo) incrementam a versao MAJOR. Adicionar propriedade opcional (backward-compatible) incrementa MINOR. Correcoes de documentacao incrementam PATCH. As entidades Unit e Holder possuem campo version (number) para concorrencia otimista, incrementado pelo servidor a cada update e verificado no PATCH para detectar conflitos de edicao concorrente. As demais entidades do schema que nao participam de sincronizacao mobile nao possuem campo version na tabela PostgreSQL.

## Uso nos Projetos

O REURBCAD importa types para tipar dados no WatermelonDB, garantindo que o schema local espelhe o PostgreSQL. O @carf/geoapi-client gera seus proprios tipos de request/response via orval a partir do swagger.json e usa os enums do tscore para logica de negocio. O @carf/ui-native consome os types em props de componentes de dominio como UnitCard e HolderCard. O REURBWEB e REURBMASTER usam os types em formularios e listagens. A fronteira e clara: tscore fornece modelos de dominio completos (para WatermelonDB, logica de campo, offline), enums com logica de negocio, auth e validacoes; geoapi-client fornece tipos de API (request/response) e hooks React Query.
