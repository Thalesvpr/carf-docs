---
type: leaf
status: approved
updated: 2026-01-24
---

> **REVIEW**: Tipo diagram nao tem template definido. Arquivo usa multiplas H2s e bloco de codigo Mermaid.

# Aggregates Diagram

Diagrama dos aggregates e seus relacionamentos no modelo de dominio CARF, seguindo padroes de Domain-Driven Design.

## Diagrama Mermaid

```mermaid
graph TB
    subgraph "Unit Aggregate"
        Unit[Unit<br/>Aggregate Root]
        UnitAddress[Address<br/>Value Object]
        UnitGeometry[Geometry<br/>Value Object]
        UnitPhoto[Photo<br/>Entity]
        Unit --> UnitAddress
        Unit --> UnitGeometry
        Unit --> UnitPhoto
    end

    subgraph "Holder Aggregate"
        Holder[Holder<br/>Aggregate Root]
        HolderCPF[CPF<br/>Value Object]
        HolderContact[Contact<br/>Value Object]
        HolderIncome[Income<br/>Value Object]
        Holder --> HolderCPF
        Holder --> HolderContact
        Holder --> HolderIncome
    end

    subgraph "Community Aggregate"
        Community[Community<br/>Aggregate Root]
        CommunityGeometry[Geometry<br/>Value Object]
        CommunityContact[Contact<br/>Entity]
        Community --> CommunityGeometry
        Community --> CommunityContact
    end

    subgraph "Legitimation Aggregate"
        Legitimation[Legitimation<br/>Aggregate Root]
        LegitimationDoc[Document<br/>Entity]
        LegitimationHist[History<br/>Entity]
        Legitimation --> LegitimationDoc
        Legitimation --> LegitimationHist
    end

    %% Cross-aggregate references (by ID only)
    Unit -.->|"unit_holders<br/>(junction)"| Holder
    Unit -.->|"community_id"| Community
    Legitimation -.->|"unit_id"| Unit
    Legitimation -.->|"holder_ids"| Holder

    style Unit fill:#e1f5fe
    style Holder fill:#fff3e0
    style Community fill:#e8f5e9
    style Legitimation fill:#fce4ec
```

## Regras de Aggregate

Cada aggregate possui invariantes que devem ser mantidas. Unit exige geometria valida e area maior que zero. Holder requer CPF unico por tenant e idade minima de 18 anos. Community precisa de nome unico por tenant e geometria que nao sobreponha outras comunidades. Legitimation segue state machine de workflow e exige documentos obrigatorios antes da aprovacao.

Referencias entre aggregates sao por ID apenas. Tabela unit_holders e junction table que nao pertence a nenhum aggregate. Cada aggregate e boundary de transacao. Multi-tenancy aplicado em todos via TenantId com RLS.
