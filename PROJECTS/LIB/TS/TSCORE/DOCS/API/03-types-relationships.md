---
type: leaf
status: review
updated: 2026-02-08
---

# Tipos de Relacionamento e Infraestrutura

Interfaces de juncao, legitimacao, GIS e autenticacao exportadas pelo modulo types do tscore. Cada interface espelha a tabela correspondente no [schema PostgreSQL](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/INFRA/PERSISTENCE/02-database-schema.md) com tipos derivados dos enums documentados em [04-types-enums](./04-types-enums.md).

## UnitHolder

Interface de juncao N:N entre unidades e titulares, correspondendo a tabela unit_holders. Cada registro representa o vinculo de um titular com uma unidade, especificando o tipo de relacionamento e o percentual de propriedade quando aplicavel. Constraint UNIQUE em (unitId, holderId) impede vinculo duplicado. Trigger garante que a soma de ownershipPercentage por unidade nao excede 100 e que exatamente um isPrimary true existe por unidade.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID do vinculo |
| unitId | string | nao | UUID da unidade, ON DELETE CASCADE |
| holderId | string | nao | UUID do titular, ON DELETE RESTRICT |
| relationshipType | RelationshipType | nao | PROPRIETARIO, CONJUGE, MORADOR, PROCURADOR ou HERDEIRO |
| ownershipPercentage | number | sim | Percentual de 0 a 100, obrigatorio para PROPRIETARIO |
| isPrimary | boolean | nao | Titular principal responsavel legal pela unidade |
| createdAt | string | nao | ISO 8601 timestamp de criacao do vinculo |
| createdBy | string | nao | UUID de quem criou o vinculo |

## TeamMember

Interface vinculando conta de usuario a equipe de campo, correspondendo a tabela team_members. O papel (role) define as permissoes do membro dentro do app mobile REURBCAD. Constraint UNIQUE em (teamId, accountId) impede membro duplicado.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID do registro |
| teamId | string | nao | UUID da equipe |
| accountId | string | nao | UUID do usuario no Keycloak |
| role | TeamRole | nao | COORDINATOR ou CADASTRATOR |
| joinedAt | string | nao | ISO 8601 timestamp de entrada na equipe |
| leftAt | string | sim | ISO 8601 timestamp de saida, null indica membro ativo |

## CommunityAuthorization

Interface de controle de acesso granular por comunidade, correspondendo a tabela community_authorizations. Pode ser atribuida a uma equipe inteira ou a um usuario individual, com constraint CHECK garantindo que exatamente um entre teamId e accountId esta preenchido (XOR). Quando atribuida a uma equipe, todos os membros ativos herdam a autorizacao.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID da autorizacao |
| communityId | string | nao | UUID da comunidade |
| teamId | string | sim | UUID da equipe, mutuamente exclusivo com accountId |
| accountId | string | sim | UUID do usuario, mutuamente exclusivo com teamId |
| permissionLevel | string | nao | READ, WRITE ou ADMIN |
| grantedAt | string | nao | ISO 8601 timestamp de concessao |
| grantedBy | string | nao | UUID de quem concedeu |

## LegitimationRequest

Interface representando processo de legitimacao fundiaria conforme Lei 13.465/2017, correspondendo a tabela legitimation_requests. Cada registro acompanha o ciclo de vida completo desde a submissao ate o registro em cartorio. Constraint UNIQUE parcial em unitId impede dois processos ativos para a mesma unidade.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID do processo |
| tenantId | string | nao | UUID do tenant |
| unitId | string | nao | UUID da unidade objeto da legitimacao |
| status | LegitimationStatus | nao | Status atual conforme enum de 11 valores |
| requestedAt | string | nao | ISO 8601 timestamp de protocolo |
| requestedBy | string | nao | UUID de quem iniciou o processo |
| analystId | string | sim | UUID do analista responsavel |
| managerId | string | sim | UUID do manager responsavel pela decisao |
| decision | Decision | sim | APPROVED ou REJECTED |
| decisionReason | string | sim | Justificativa da decisao |
| decisionAt | string | sim | ISO 8601 timestamp da decisao |
| deadline | string | sim | Data ISO 8601 para prazo de decisao (120 dias apos contestacao) |
| contestationDeadline | string | sim | Data ISO 8601 para prazo de contestacoes (30 dias apos publicacao) |
| createdAt | string | nao | ISO 8601 timestamp |
| updatedAt | string | nao | ISO 8601 timestamp |
| deletedAt | string | sim | ISO 8601 soft delete |

## LegitimationResponse

Interface representando respostas e pareceres vinculados a um processo de legitimacao, correspondendo a tabela legitimation_responses. Inclui pareceres tecnicos de analistas, decisoes de managers e contestacoes de terceiros.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID da resposta |
| requestId | string | nao | UUID do processo de legitimacao |
| responderId | string | nao | UUID do responsavel pela resposta |
| responseType | string | nao | PARECER_TECNICO, DECISAO, CONTESTACAO ou CORRECAO |
| content | string | nao | Texto completo da resposta |
| respondedAt | string | nao | ISO 8601 timestamp da resposta |

## LegitimationCertificate

Interface representando certidao de legitimacao fundiaria emitida apos aprovacao, correspondendo a tabela legitimation_certificates. Numero unico sequencial no formato CERT-AAAA-NNNNN com constraint UNIQUE global.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID da certidao |
| requestId | string | nao | UUID do processo de legitimacao |
| certificateNumber | string | nao | Numero unico CERT-AAAA-NNNNN |
| situation | CertificateSituation | nao | COVERED, CONFRONTING ou BOTH |
| issuedAt | string | nao | ISO 8601 timestamp de emissao |
| issuedBy | string | nao | UUID de quem emitiu |
| pdfPath | string | nao | Caminho S3 do PDF da certidao |

## Layer

Interface representando camada GIS customizavel por tenant, correspondendo a tabela layers.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID da camada |
| tenantId | string | nao | UUID do tenant |
| name | string | nao | Nome da camada |
| layerType | string | nao | POINT, LINESTRING ou POLYGON |
| sourceUrl | string | sim | URL de origem se importada |
| visible | boolean | nao | Visivel por padrao |
| opacity | number | nao | Opacidade de 0 a 1 |
| zIndex | number | nao | Ordem de empilhamento |
| createdAt | string | nao | ISO 8601 timestamp |
| updatedAt | string | nao | ISO 8601 timestamp |
| deletedAt | string | sim | ISO 8601 soft delete |

## LayerFeature

Interface representando feature individual de uma camada com geometria propria, correspondendo a tabela layer_features.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID da feature |
| layerId | string | nao | UUID da camada pai |
| geometry | GeoJsonGeometry | nao | Geometria PostGIS, tipo deve corresponder ao layerType |
| properties | Record de string para unknown | sim | Atributos descritivos em formato livre |
| createdAt | string | nao | ISO 8601 timestamp |
| updatedAt | string | nao | ISO 8601 timestamp |
| deletedAt | string | sim | ISO 8601 soft delete |

## ApiKey

Interface representando chave de API para integracao server-to-server, baseada nos endpoints de auth-keys da [API Reference](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/00-api-reference.md).

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID da chave |
| name | string | nao | Nome descritivo da chave |
| key | string | sim | UUID v4 da chave, retornado apenas na criacao |
| expiresAt | string | nao | ISO 8601 timestamp de expiracao (30 dias) |
| createdAt | string | nao | ISO 8601 timestamp de criacao |
| lastUsedAt | string | sim | ISO 8601 timestamp do ultimo uso |
