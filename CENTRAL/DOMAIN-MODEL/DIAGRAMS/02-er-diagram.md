# ER Diagram

Diagrama Entity-Relationship do banco de dados CARF.

## Diagrama Mermaid

```mermaid
erDiagram
    tenants ||--o{ units : contains
    tenants ||--o{ holders : contains
    tenants ||--o{ communities : contains
    tenants ||--o{ legitimations : contains

    communities ||--o{ units : "contains"

    units ||--o{ unit_photos : has
    units ||--o{ unit_holders : linked_to
    units ||--o{ unit_documents : has

    holders ||--o{ unit_holders : linked_to
    holders ||--o{ holder_documents : has

    legitimations ||--|| units : references
    legitimations ||--o{ legitimation_holders : includes
    legitimations ||--o{ legitimation_documents : requires
    legitimations ||--o{ legitimation_history : tracks

    holders ||--o{ legitimation_holders : participates

    tenants {
        uuid id PK
        string name
        string slug UK
        jsonb settings
        timestamp created_at
    }

    communities {
        uuid id PK
        uuid tenant_id FK
        string code UK
        string name
        text description
        geometry boundary
        decimal area_m2
        string reurb_modality
        timestamp created_at
    }

    units {
        uuid id PK
        uuid tenant_id FK
        uuid community_id FK
        string code UK
        string status
        jsonb address
        geometry boundary
        decimal area_m2
        point centroid
        timestamp created_at
        timestamp updated_at
    }

    unit_photos {
        uuid id PK
        uuid unit_id FK
        string url
        string thumbnail_url
        string description
        int order
        timestamp created_at
    }

    holders {
        uuid id PK
        uuid tenant_id FK
        string code UK
        string name
        string cpf_encrypted
        string cpf_hash UK
        date birth_date
        string gender
        string marital_status
        jsonb contact
        jsonb income
        timestamp created_at
    }

    unit_holders {
        uuid id PK
        uuid unit_id FK
        uuid holder_id FK
        string ownership_type
        decimal ownership_percentage
        timestamp created_at
    }

    legitimations {
        uuid id PK
        uuid tenant_id FK
        uuid unit_id FK
        string protocol UK
        string status
        string modality
        date occupation_date
        jsonb declaration
        timestamp submitted_at
        timestamp approved_at
        uuid approved_by FK
    }

    legitimation_holders {
        uuid id PK
        uuid legitimation_id FK
        uuid holder_id FK
        string ownership_type
        decimal percentage
    }

    legitimation_history {
        uuid id PK
        uuid legitimation_id FK
        string action
        string from_status
        string to_status
        uuid user_id FK
        text comments
        timestamp created_at
    }
```

## Constraints Principais

### Primary Keys
- Todas as tabelas usam UUID como PK
- Gerados via `gen_random_uuid()`

### Foreign Keys
- `tenant_id` em todas tabelas principais (RLS)
- `ON DELETE RESTRICT` para preservar integridade
- Índices em todas FKs

### Unique Constraints
- `tenants.slug`
- `communities.code` (per tenant - compound)
- `units.code` (per tenant)
- `holders.cpf_hash` (per tenant)
- `legitimations.protocol` (per tenant)

### Check Constraints
- `units.status IN ('Rascunho', 'Pendente', 'Aprovado', 'Rejeitado')`
- `unit_holders.ownership_percentage BETWEEN 0 AND 100`
- `legitimations.modality IN ('REURB-S', 'REURB-E')`

## Índices Geoespaciais

```sql
CREATE INDEX idx_units_boundary ON units USING GIST(boundary);
CREATE INDEX idx_units_centroid ON units USING GIST(centroid);
CREATE INDEX idx_communities_boundary ON communities USING GIST(boundary);
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
