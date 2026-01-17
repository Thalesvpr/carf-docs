# Aggregates Diagram

Diagrama dos aggregates e seus relacionamentos no modelo de domínio CARF.

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

### Unit Aggregate
- **Aggregate Root**: Unit
- **Boundary**: Unit, Address, Geometry, Photos
- **Invariantes**:
  - Geometria deve ser polígono válido
  - Área > 0
  - Status só avança via eventos de workflow

### Holder Aggregate
- **Aggregate Root**: Holder
- **Boundary**: Holder, CPF, Contact, Income
- **Invariantes**:
  - CPF único por tenant
  - Idade >= 18 anos

### Community Aggregate
- **Aggregate Root**: Community
- **Boundary**: Community, Geometry, Contacts
- **Invariantes**:
  - Nome único por tenant
  - Geometria não sobrepõe outras comunidades

### Legitimation Aggregate
- **Aggregate Root**: Legitimation (Process)
- **Boundary**: Process, Documents, History
- **Invariantes**:
  - Workflow state machine válido
  - Documentos obrigatórios presentes antes de aprovação

## Notas

- Referências entre aggregates são por ID apenas
- Tabela `unit_holders` é junction table, não pertence a nenhum aggregate
- Cada aggregate é boundary de transação
- Multi-tenancy aplicado em todos aggregates via TenantId

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
