---
type: leaf
status: approved
updated: 2026-02-07
---

# Unit

Entidade central do sistema representando uma unidade habitacional ou propriedade objeto de regularizacao fundiaria. Funciona como aggregate root coordenando relacionamentos com titulares, documentos, localizacao espacial e o workflow de regularizacao. Herda de BaseAggregateRoot ganhando suporte a domain events.

## Papel no Dominio

Cada unidade representa um imovel fisico dentro de uma comunidade. O cadastro de uma unidade e o ponto de partida de todo o processo de regularizacao: a partir dela, titulares sao vinculados, documentos sao anexados, e o processo de legitimacao fundiaria e iniciado. A unidade passa por uma maquina de estados formal (documentada em CENTRAL/DOMAIN-RULES/WORKFLOWS/04-unit-status-machine.md) desde DRAFT ate APPROVED ou REJECTED.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| TenantId | Guid | nao | Municipio ao qual pertence. FK para Tenant. Usado em RLS. |
| CommunityId | Guid | nao | Comunidade vinculada. FK para Community. |
| BlockId | Guid | sim | Quadra, desnormalizado para queries eficientes. FK para Block. |
| PlotId | Guid | sim | Lote formal quando existente. FK para Plot. |
| BuildingId | Guid | sim | Edificacao quando aplicavel. FK para Building. |
| Code | string | nao | Codigo unico por tenant no formato UNI-AAAA-NNNNN. Gerado pelo servidor. |
| Status | UnitStatus | nao | Status atual conforme state machine: DRAFT, PENDING_ANALYSIS, IN_REVIEW, APPROVED, REJECTED, REQUIRES_CHANGES. |
| AddressStreet | string | sim | Logradouro. |
| AddressNumber | string | sim | Numero. |
| AddressComplement | string | sim | Complemento. |
| AddressNeighborhood | string | sim | Bairro. |
| AddressCity | string | sim | Cidade. |
| AddressState | string | sim | UF com 2 caracteres. |
| AddressZipCode | string | sim | CEP sem formatacao. |
| Boundary | Polygon | sim | Perimetro da unidade em WGS84 SRID 4326. |
| Centroid | Point | sim | Centroide calculado a partir do boundary. |
| Area | decimal | sim | Area calculada via ST_Area em metros quadrados. |
| DeclaredArea | decimal | sim | Area declarada pelo titular quando diferente da calculada. |
| OccupantType | string | sim | POSSUIDOR ou LOCATARIO. |
| UtilizationType | string | sim | RESIDENCIAL, COMERCIAL, MISTO, TERRENO_VAZIO, NAO_HABITADO. |
| UnitCondition | string | sim | OCUPADA, VAZIA, EM_CONSTRUCAO, ABANDONADA. |
| AttendanceStatus | string | sim | AUSENTE, PRESENTE, NAO_QUIS, ASSINADO. |
| ResidenceTime | string | sim | Tempo de moradia declaratorio em texto livre. |
| Observation | string | sim | Observacoes do agente de campo. |
| FacadePhotoPath | string | sim | Caminho S3 da foto de fachada principal. |
| CustomData | JsonDocument | sim | Dados especificos do tenant em formato JSONB. |
| Version | int | nao | Controle de concorrencia otimista. Incrementado a cada update. |
| CreatedAt | DateTime | nao | Data de criacao. |
| UpdatedAt | DateTime | nao | Ultima atualizacao. |
| CreatedBy | Guid | nao | Account que criou. |
| UpdatedBy | Guid | nao | Account que atualizou por ultimo. |
| DeletedAt | DateTime | sim | Soft delete. Null indica registro ativo. |

## Relacionamentos

Relacionamento N:N com Holder via entidade de juncao UnitHolder, especificando tipo de vinculo (PROPRIETARIO, CONJUGE, MORADOR, PROCURADOR, HERDEIRO) e percentual de propriedade. Cada unidade deve ter ao menos um titular vinculado como PROPRIETARIO com is_primary true antes de ser submetida para analise.

Colecao de Documents vinculados via entity_type UNIT e entity_id igual ao ID da unidade, incluindo fotos de fachada, documentos de comprovacao e certidoes.

Vinculo opcional com Plot e Block suportando contextos urbanos formais com parcelamento definido e assentamentos informais sem organizacao espacial previa. Vinculo opcional com Building para unidades em edificacoes com multiplas unidades.

Pertence obrigatoriamente a uma Community que define o escopo geografico e de autorizacao de acesso.

## Invariantes de Negocio

Area calculada deve ser positiva quando preenchida. Valores menores que 10 metros quadrados ou maiores que 100.000 metros quadrados geram alerta AREA_EXCEEDED pois indicam possivel erro de georreferenciamento.

Boundary deve ser um poligono valido conforme PostGIS ST_IsValid: sem auto-intersecao, fechado (primeiro ponto igual ao ultimo) e com ao menos 4 pontos. Poligonos invalidos geram erro GEOMETRY_INVALID.

O centroide da unidade deve estar contido dentro do boundary da comunidade vinculada. Unidades fora dos limites geram erro OUTSIDE_BOUNDARY.

Para submissao (transicao DRAFT para PENDING_ANALYSIS), ao menos um titular deve estar vinculado com is_primary true e todos os campos obrigatorios de endereco devem estar preenchidos.

Sobreposicao com boundaries de outras unidades ativas no mesmo tenant gera alerta OVERLAP_DETECTED mas nao bloqueia a operacao.

Edicao so e permitida nos estados DRAFT e REQUIRES_CHANGES. Exclusao so e permitida em DRAFT.

## Domain Events

UnitCreatedEvent emitido ao criar a unidade. UnitUpdatedEvent emitido ao atualizar campos. UnitStatusChangedEvent emitido a cada transicao de status com oldStatus e newStatus. HolderLinkedEvent emitido ao vincular titular. HolderUnlinkedEvent emitido ao desvincular.
