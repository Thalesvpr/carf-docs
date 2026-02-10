---
type: leaf
status: review
updated: 2026-02-08
---

# Tipos de Entidade

Interfaces TypeScript de entidades de dominio exportadas pelo modulo types do tscore, mapeadas 1:1 com o [schema PostgreSQL](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/INFRA/PERSISTENCE/02-database-schema.md). Cada interface espelha a tabela correspondente com tipos TypeScript equivalentes aos tipos PostgreSQL. Campos timestamptz mapeiam para string ISO 8601, geometry para objetos GeoJSON, uuid para string, decimal para number e jsonb para Record ou objeto tipado.

## Unit

Interface central representando unidade habitacional cadastrada em campo. Tipos de enum importados de [04-types-enums](./04-types-enums.md).

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID da unidade |
| tenantId | string | nao | UUID do tenant para isolamento RLS |
| communityId | string | nao | UUID da comunidade a que pertence |
| blockId | string | sim | UUID da quadra quando aplicavel |
| plotId | string | sim | UUID do lote quando existente |
| buildingId | string | sim | UUID da edificacao quando aplicavel |
| code | string | nao | Codigo unico no formato UNI-AAAA-NNNNN |
| status | UnitStatus | nao | Status do workflow de aprovacao |
| addressStreet | string | sim | Logradouro |
| addressNumber | string | sim | Numero |
| addressComplement | string | sim | Complemento |
| addressNeighborhood | string | sim | Bairro |
| addressCity | string | sim | Cidade |
| addressState | string | sim | UF com 2 caracteres |
| addressZipCode | string | sim | CEP sem formatacao, 9 caracteres |
| boundary | GeoJsonPolygon | sim | Perimetro da unidade em WGS84 EPSG:4326 |
| centroid | GeoJsonPoint | sim | Centroide calculado a partir do boundary |
| area | number | sim | Area calculada via ST_Area em metros quadrados |
| declaredArea | number | sim | Area declarada pelo titular |
| occupantType | OccupantType | sim | POSSUIDOR ou LOCATARIO |
| utilizationType | UtilizationType | sim | Finalidade de uso da unidade |
| unitCondition | UnitCondition | sim | Condicao fisica da unidade |
| attendanceStatus | AttendanceStatus | sim | Situacao de atendimento em campo |
| residenceTime | string | sim | Tempo de moradia declaratorio em texto livre |
| observation | string | sim | Observacoes do agente de campo |
| facadePhotoPath | string | sim | Caminho S3 da foto de fachada |
| customData | Record de string para unknown | sim | Dados especificos do tenant em JSON livre |
| createdAt | string | nao | ISO 8601 timestamp de criacao |
| updatedAt | string | nao | ISO 8601 timestamp de ultima atualizacao |
| createdBy | string | nao | UUID da conta que criou |
| updatedBy | string | nao | UUID da conta que atualizou por ultimo |
| deletedAt | string | sim | ISO 8601 timestamp de soft delete |
| version | number | nao | Controle de concorrencia otimista, incrementado a cada update |

## Holder

Interface representando titular ou posseiro pessoa fisica vinculado a unidades habitacionais.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID do titular |
| tenantId | string | nao | UUID do tenant |
| cpf | string | nao | CPF 11 digitos sem formatacao, validado mod-11 |
| cnpj | string | sim | CNPJ 14 digitos para pessoa juridica |
| fullName | string | nao | Nome completo com minimo 2 palavras |
| socialName | string | sim | Nome social quando diferente do registro |
| birthDate | string | nao | Data de nascimento ISO 8601 AAAA-MM-DD |
| gender | string | nao | MASCULINO, FEMININO, NAO_DECLARAR ou OUTROS |
| filiation | string | sim | Nomes de filiacao, campo unico |
| maritalStatus | string | nao | SOLTEIRO, CASADO, DIVORCIADO, VIUVO ou SEPARADO |
| stableUnion | string | sim | NAO, RECONHECIDA_CARTORIO ou NAO_RECONHECIDA |
| spouseName | string | sim | Nome do conjuge, obrigatorio se casado ou uniao estavel |
| spouseCpf | string | sim | CPF do conjuge, obrigatorio se casado ou uniao estavel |
| email | string | sim | Email de contato |
| phone | string | sim | Telefone com DDD |
| occupation | string | nao | Situacao profissional |
| profession | string | nao | Profissao conforme CBO simplificada |
| educationLevel | string | sim | Nivel de escolaridade |
| monthlyIncome | number | sim | Renda mensal declarada em reais |
| dependentsCount | number | sim | Numero de dependentes |
| nationality | string | nao | Nacionalidade, padrao BRASILEIRA |
| documentType | string | nao | RG, CNH, CIN, PASSAPORTE ou CTPS |
| documentNumber | string | nao | Numero do documento de identificacao |
| signaturePath | string | sim | Caminho S3 do PNG da assinatura criptografado AES-256 |
| signatureTimestamp | string | sim | ISO 8601 timestamp da captura da assinatura |
| signatureDeviceId | string | sim | Identificador do dispositivo usado para assinatura |
| createdAt | string | nao | ISO 8601 timestamp de criacao |
| updatedAt | string | nao | ISO 8601 timestamp de ultima atualizacao |
| createdBy | string | nao | UUID de quem cadastrou |
| updatedBy | string | nao | UUID de quem atualizou por ultimo |
| version | number | nao | Controle de concorrencia otimista |
| deletedAt | string | sim | ISO 8601 timestamp de soft delete |

## Community

Interface representando comunidade ou assentamento que agrupa unidades habitacionais.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID da comunidade |
| tenantId | string | nao | UUID do tenant |
| code | string | nao | Codigo unico por tenant |
| name | string | nao | Nome da comunidade |
| communityType | CommunityType | nao | URBANA, RURAL, QUILOMBOLA ou RIBEIRINHA |
| boundary | GeoJsonPolygon | sim | Perimetro em WGS84 |
| area | number | sim | Area em metros quadrados |
| municipality | string | nao | Municipio |
| state | string | nao | UF com 2 caracteres |
| district | string | sim | Distrito |
| neighborhood | string | sim | Bairro |
| reference | string | sim | Ponto de referencia |
| status | string | nao | Status da comunidade, padrao ACTIVE |
| createdAt | string | nao | ISO 8601 timestamp |
| updatedAt | string | nao | ISO 8601 timestamp |
| createdBy | string | nao | UUID de quem criou |
| updatedBy | string | nao | UUID de quem atualizou |
| deletedAt | string | sim | ISO 8601 soft delete |

## Team

Interface representando equipe de campo que agrupa usuarios para atribuicao coletiva de acesso a comunidades.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID da equipe |
| tenantId | string | nao | UUID do tenant |
| name | string | nao | Nome da equipe |
| description | string | sim | Descricao opcional |
| createdAt | string | nao | ISO 8601 timestamp |
| updatedAt | string | nao | ISO 8601 timestamp |
| deletedAt | string | sim | ISO 8601 soft delete |

## Account

Interface representando conta de usuario do sistema, com dados vindos do Keycloak enriquecidos com informacoes locais.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID do usuario no Keycloak |
| email | string | nao | Email de login |
| name | string | nao | Nome completo |
| cpf | string | sim | CPF quando vinculado |
| role | Role | nao | Role hierarquico principal |
| tenantId | string | nao | UUID do tenant associado |
| isActive | boolean | nao | Conta ativa ou desativada |
| lastLoginAt | string | sim | ISO 8601 timestamp do ultimo login |

## Tenant

Interface representando organizacao inquilina (municipio) no sistema multi-tenant.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID do tenant |
| name | string | nao | Nome do municipio |
| slug | string | nao | Slug para URLs, unico |
| isActive | boolean | nao | Tenant ativo ou suspenso |
| settings | Record de string para unknown | sim | Configuracoes especificas do tenant |
| createdAt | string | nao | ISO 8601 timestamp |

## Block

Interface representando quadra urbana, subdivisao espacial de uma comunidade.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID da quadra |
| communityId | string | nao | UUID da comunidade pai |
| code | string | nao | Codigo unico dentro da comunidade |
| name | string | sim | Nome descritivo opcional |
| boundary | GeoJsonPolygon | sim | Perimetro da quadra em WGS84 |
| area | number | sim | Area em metros quadrados |
| createdAt | string | nao | ISO 8601 timestamp |
| updatedAt | string | nao | ISO 8601 timestamp |
| deletedAt | string | sim | ISO 8601 soft delete |

## Plot

Interface representando lote individual dentro de um bloco.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID do lote |
| blockId | string | nao | UUID da quadra pai |
| code | string | nao | Codigo unico dentro do bloco |
| boundary | GeoJsonPolygon | sim | Perimetro do lote em WGS84 |
| area | number | sim | Area em metros quadrados |
| createdAt | string | nao | ISO 8601 timestamp |
| updatedAt | string | nao | ISO 8601 timestamp |
| deletedAt | string | sim | ISO 8601 soft delete |

## Building

Interface representando edificacao dentro de um lote que pode conter multiplas unidades.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID da edificacao |
| plotId | string | sim | UUID do lote, nullable pois edificacao pode existir sem lote formal |
| unitCount | number | nao | Numero de unidades na edificacao |
| buildingType | string | nao | CASA, APARTAMENTO, COMERCIAL ou MISTO |
| floorsCount | number | sim | Numero de andares |
| createdAt | string | nao | ISO 8601 timestamp |
| updatedAt | string | nao | ISO 8601 timestamp |
| deletedAt | string | sim | ISO 8601 soft delete |

## Document

Interface representando documento ou foto vinculado a qualquer entidade via relacionamento polimorfico.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID do documento |
| tenantId | string | nao | UUID do tenant |
| entityType | EntityType | nao | Tipo da entidade pai: UNIT, HOLDER ou COMMUNITY |
| entityId | string | nao | UUID da entidade pai |
| documentType | DocumentType | nao | Tipo do documento conforme enum |
| filePath | string | nao | Caminho completo no S3 |
| fileName | string | nao | Nome original do arquivo |
| fileSize | number | nao | Tamanho em bytes |
| mimeType | string | nao | Tipo MIME: image/jpeg, image/png, image/webp ou application/pdf |
| checksum | string | nao | Hash SHA-256 do conteudo |
| uploadedAt | string | nao | ISO 8601 timestamp do upload |
| uploadedBy | string | nao | UUID de quem fez upload |
| deletedAt | string | sim | ISO 8601 soft delete |

## Annotation

Interface representando anotacao vinculada a qualquer entidade via relacionamento polimorfico.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID da anotacao |
| tenantId | string | nao | UUID do tenant |
| entityType | EntityType | nao | Tipo da entidade anotada |
| entityId | string | nao | UUID da entidade |
| annotationType | AnnotationType | nao | NOTE, WARNING, ISSUE ou REMINDER |
| content | string | nao | Texto da anotacao |
| priority | Priority | sim | Obrigatorio para ISSUE e REMINDER |
| createdAt | string | nao | ISO 8601 timestamp |
| createdBy | string | nao | UUID de quem criou |
| deletedAt | string | sim | ISO 8601 soft delete |

## Orthophoto

Interface representando ortofoto de drone vinculada a uma comunidade.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID da ortofoto |
| tenantId | string | nao | UUID do tenant |
| communityId | string | sim | UUID da comunidade, nullable se cobre area sem comunidade |
| originalPath | string | nao | Caminho S3 do GeoTIFF original |
| optimizedPath | string | sim | Caminho S3 da versao JPEG otimizada |
| tilesPath | string | sim | Caminho base S3 dos tiles XYZ |
| fileSize | number | nao | Tamanho do original em bytes |
| width | number | sim | Largura em pixels |
| height | number | sim | Altura em pixels |
| srid | number | sim | Sistema de referencia espacial |
| boundsGeojson | GeoJsonPolygon | sim | Limites geograficos em GeoJSON |
| captureDate | string | sim | Data do voo ISO 8601 |
| processingStatus | string | nao | PENDING, PROCESSING, COMPLETED ou FAILED |
| processingError | string | sim | Mensagem de erro quando FAILED |
| uploadedAt | string | nao | ISO 8601 timestamp do upload |
| uploadedBy | string | nao | UUID de quem fez upload |
| processedAt | string | sim | ISO 8601 timestamp de conclusao do processamento |

## SyncLog

Interface representando registro de operacao de sincronizacao entre REURBCAD mobile e servidor.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID do registro |
| tenantId | string | nao | UUID do tenant |
| userId | string | nao | UUID do usuario que sincronizou |
| entityType | string | nao | Tipo da entidade: UNIT, HOLDER, DOCUMENT |
| entityId | string | nao | UUID da entidade sincronizada |
| operation | string | nao | CREATE, UPDATE ou DELETE |
| payload | Record de string para unknown | nao | Dados completos da operacao em JSON |
| syncedAt | string | nao | ISO 8601 timestamp do processamento no servidor |
| clientTimestamp | string | nao | ISO 8601 timestamp do client na operacao local |
| serverTimestamp | string | nao | ISO 8601 timestamp do servidor |
| conflictResolved | boolean | nao | Se houve conflito e foi resolvido |

## AuditLog

Interface representando registro de auditoria imutavel. Append-only com retencao minima de 7 anos conforme LGPD.

| Propriedade | Tipo TS | Nullable | Descricao |
|:------------|:--------|:---------|:----------|
| id | string | nao | UUID do registro |
| tenantId | string | nao | UUID do tenant |
| userId | string | sim | UUID do usuario, null se operacao automatica |
| action | string | nao | CREATE, UPDATE, DELETE, LOGIN, LOGOUT ou STATUS_CHANGE |
| entityType | string | nao | Tipo da entidade afetada |
| entityId | string | nao | UUID da entidade afetada |
| oldValues | Record de string para unknown | sim | Valores anteriores, null em CREATE |
| newValues | Record de string para unknown | sim | Novos valores, null em DELETE |
| ipAddress | string | sim | IP de origem IPv4 ou IPv6 |
| userAgent | string | sim | User-Agent do cliente HTTP |
| timestamp | string | nao | ISO 8601 timestamp da operacao |

## Tipos GeoJSON Auxiliares

GeoJsonPolygon representa poligono GeoJSON com type "Polygon" e coordinates como array tridimensional de numeros representando aneis de coordenadas em formato longitude, latitude conforme WGS84. GeoJsonPoint representa ponto GeoJSON com type "Point" e coordinates como par longitude, latitude. GeoJsonFeature encapsula geometria com properties tipadas como Record de string para unknown. GeoJsonFeatureCollection agrupa multiplos GeoJsonFeature em colecao com type "FeatureCollection".
