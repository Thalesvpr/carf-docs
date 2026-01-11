# DIAGRAMS - Diagramas do Modelo de Domínio

Diagramas conceituais do modelo de domínio CARF incluindo diagramas de classe entity-relationship diagrams (ERD) diagramas de agregados e visualizações de workflows de negócio documentando graficamente relacionamentos cardinalidade fronteiras de consistência e fluxos de dados entre entidades do sistema.

## Tipos de Diagramas

### Class Diagrams
Diagramas de classe mostrando entidades value objects e aggregates com seus atributos métodos e relacionamentos seguindo notação UML.

### Entity-Relationship Diagrams (ERD)
ERDs detalhando relacionamentos entre entidades com cardinalidade (1:1, 1:N, N:N) foreign keys e constraints de integridade referencial.

### Aggregate Diagrams
Diagramas mostrando fronteiras de aggregates com aggregate roots entidades internas e invariantes garantidos destacando boundaries transacionais.

### Workflow Diagrams
Diagramas de estado (state machines) mostrando transições de status para Unit e LegitimationRequest com triggers e condições de transição.

## Ferramentas Recomendadas

**Para criação de diagramas:**
- **PlantUML** - Diagramas como código versionáveis
- **Mermaid** - Diagramas markdown-embeddable para documentação
- **draw.io** - Editor visual para diagramas complexos
- **Lucidchart** - Colaboração em tempo real

**Para sincronização código-diagrama:**
- **Entity Framework Core Power Tools** - Reverse engineer para ERD
- **SchemaSpy** - Geração automática de ERD de database
- **TypeDoc** - Documentação TypeScript com diagramas

## Relacionado

Ver também:
- **[ENTITIES/](../ENTITIES/README.md)** - Definições de entidades
- **[AGGREGATES/](../AGGREGATES/README.md)** - Fronteiras de agregados
- **[RELATIONSHIPS/](../RELATIONSHIPS/README.md)** - Relacionamentos detalhados
- **[WORKFLOWS/](../../WORKFLOWS/README.md)** - Workflows de negócio

---

**Última atualização:** 2026-01-10
