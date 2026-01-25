---
type: leaf
status: approved
updated: 2026-01-24
---

# Multi-Tenancy Diagram

Diagrama do fluxo de isolamento multi-tenant via JWT e Row-Level Security no PostgreSQL, demonstrando as camadas de seguranca defense-in-depth.

## Diagrama Mermaid

```mermaid
graph LR
    User[Usuario GEOWEB] -->|HTTP Request| Gateway[GEOAPI Gateway<br/>Controller]
    Gateway -->|JWT Header| Middleware[JWT Validation<br/>Middleware]

    Middleware -->|Extract Claims| Claims["JWT Claims:<br/>- sub (user_id)<br/>- email<br/>- roles<br/>- tenant_id"]

    Claims -->|Set Session| DbContext[EF Core<br/>DbContext]

    DbContext -->|"SET app.current_tenant"| SessionVar["PostgreSQL<br/>Session Variable<br/>current_setting('app.current_tenant')"]

    SessionVar -->|Execute| Query["SQL Query:<br/>SELECT * FROM units<br/>WHERE status = 'Aprovado'"]

    Query -->|Intercept| RLS["RLS Policy<br/>units_tenant_isolation"]

    RLS -->|Auto-add Filter| FilteredQuery["SELECT * FROM units<br/>WHERE status = 'Aprovado'<br/>AND tenant_id = current_setting(...)::uuid"]

    FilteredQuery -->|Return| Results["Apenas linhas do Tenant<br/>Isolamento garantido"]

    Results --> DbContext
    DbContext --> Gateway
    Gateway --> User

    subgraph "PostgreSQL Database"
        SessionVar
        Query
        RLS
        FilteredQuery

        RLSPolicy["CREATE POLICY<br/>units_tenant_isolation<br/>ON units<br/>USING (tenant_id = current_setting('app.current_tenant')::uuid)"]

        EnableRLS["ALTER TABLE units<br/>ENABLE ROW LEVEL SECURITY"]

        RLSPolicy -.->|Applied| RLS
        EnableRLS -.->|Enables| RLS
    end

    subgraph "Camadas de Seguranca"
        Layer1["Camada 1:<br/>Middleware valida<br/>tenant_id claim"]

        Layer2["Camada 2:<br/>RLS PostgreSQL<br/>filtro no kernel"]

        Layer1 -.->|Primeira verificacao| Middleware
        Layer2 -.->|Segunda verificacao| RLS
    end

    style RLS fill:#ffcccc
    style SessionVar fill:#ccffcc
    style FilteredQuery fill:#ccccff
    style Layer1 fill:#ffffcc
    style Layer2 fill:#ffccff
```

Arquitetura defense-in-depth com duas camadas de protecao. Middleware valida token JWT e extrai tenant_id dos claims. PostgreSQL RLS aplica filtro automatico em todas as queries, impossibilitando vazamento de dados entre tenants mesmo em caso de SQL injection.
