---
type: leaf
status: approved
updated: 2026-02-07
---

# ER Diagram

Descricao do modelo Entity-Relationship do banco de dados CARF com PostgreSQL e PostGIS para dados geoespaciais.

## Relacionamentos

| Tabela Pai | Tabela Filha | Cardinalidade | Relacao |
|------------|-------------|---------------|---------|
| tenants | units | 1:N | Tenant contem unidades |
| tenants | holders | 1:N | Tenant contem titulares |
| tenants | communities | 1:N | Tenant contem comunidades |
| tenants | legitimations | 1:N | Tenant contem legitimacoes |
| communities | units | 1:N | Comunidade contem unidades |
| units | unit_photos | 1:N | Unidade tem fotos |
| units | unit_holders | 1:N | Unidade vinculada a titulares |
| units | unit_documents | 1:N | Unidade tem documentos |
| holders | unit_holders | 1:N | Titular vinculado a unidades |
| holders | holder_documents | 1:N | Titular tem documentos |
| legitimations | units | 1:1 | Legitimacao referencia unidade |
| legitimations | legitimation_holders | 1:N | Legitimacao inclui titulares |
| legitimations | legitimation_documents | 1:N | Legitimacao requer documentos |
| legitimations | legitimation_history | 1:N | Legitimacao rastreia historico |
| holders | legitimation_holders | 1:N | Titular participa de legitimacoes |

## Tabela tenants

| Coluna | Tipo | Constraint |
|--------|------|-----------|
| id | uuid | PK |
| name | string | - |
| slug | string | UK |
| settings | jsonb | - |
| created_at | timestamp | - |

## Tabela communities

| Coluna | Tipo | Constraint |
|--------|------|-----------|
| id | uuid | PK |
| tenant_id | uuid | FK |
| code | string | UK |
| name | string | - |
| description | text | - |
| boundary | geometry | - |
| area_m2 | decimal | - |
| reurb_modality | string | - |
| created_at | timestamp | - |

## Tabela units

| Coluna | Tipo | Constraint |
|--------|------|-----------|
| id | uuid | PK |
| tenant_id | uuid | FK |
| community_id | uuid | FK |
| code | string | UK |
| status | string | - |
| address | jsonb | - |
| boundary | geometry | - |
| area_m2 | decimal | - |
| centroid | point | - |
| created_at | timestamp | - |
| updated_at | timestamp | - |

## Tabela holders

| Coluna | Tipo | Constraint |
|--------|------|-----------|
| id | uuid | PK |
| tenant_id | uuid | FK |
| code | string | UK |
| name | string | - |
| cpf_encrypted | string | - |
| cpf_hash | string | UK |
| birth_date | date | - |
| gender | string | - |
| marital_status | string | - |
| contact | jsonb | - |
| income | jsonb | - |
| created_at | timestamp | - |

## Tabela unit_holders

| Coluna | Tipo | Constraint |
|--------|------|-----------|
| id | uuid | PK |
| unit_id | uuid | FK |
| holder_id | uuid | FK |
| ownership_type | string | - |
| ownership_percentage | decimal | - |
| created_at | timestamp | - |

## Tabela legitimations

| Coluna | Tipo | Constraint |
|--------|------|-----------|
| id | uuid | PK |
| tenant_id | uuid | FK |
| unit_id | uuid | FK |
| protocol | string | UK |
| status | string | - |
| modality | string | - |
| occupation_date | date | - |
| declaration | jsonb | - |
| submitted_at | timestamp | - |
| approved_at | timestamp | - |
| approved_by | uuid | FK |

## Tabela legitimation_holders

| Coluna | Tipo | Constraint |
|--------|------|-----------|
| id | uuid | PK |
| legitimation_id | uuid | FK |
| holder_id | uuid | FK |
| ownership_type | string | - |
| percentage | decimal | - |

## Tabela legitimation_history

| Coluna | Tipo | Constraint |
|--------|------|-----------|
| id | uuid | PK |
| legitimation_id | uuid | FK |
| action | string | - |
| from_status | string | - |
| to_status | string | - |
| user_id | uuid | FK |
| comments | text | - |
| created_at | timestamp | - |

## Tabela unit_photos

| Coluna | Tipo | Constraint |
|--------|------|-----------|
| id | uuid | PK |
| unit_id | uuid | FK |
| url | string | - |
| thumbnail_url | string | - |
| description | string | - |
| order | int | - |
| created_at | timestamp | - |

## Constraints

Todas as tabelas usam UUID como PK gerados via gen_random_uuid(). Foreign keys com ON DELETE RESTRICT preservam integridade. Unique constraints garantem unicidade de tenants.slug, communities.code, units.code, holders.cpf_hash e legitimations.protocol (todos por tenant).

Check constraints validam units.status IN ('Rascunho', 'Pendente', 'EmAnalise', 'Aprovado', 'Rejeitado', 'RequerAlteracoes'), unit_holders.ownership_percentage BETWEEN 0 AND 100, e legitimations.modality IN ('REURB-S', 'REURB-E').

Indices geoespaciais GIST em units.boundary, units.centroid e communities.boundary para queries espaciais performaticas.
