# Workflows - Fluxos de Trabalho do Sistema

Workflows descrevem sequências de atividades coordenadas entre atores humanos e sistema atravessando múltiplos aggregates e bounded contexts para completar processos de negócio end-to-end garantindo orquestração correta de operações e transições de estado conforme regras estabelecidas. Documentação segue princípio technology-agnostic usando termos genéricos como "banco de dados relacional" "ferramenta GIS desktop com plugin" "motor de sincronização bidirecional" sem mencionar PostgreSQL WatermelonDB QGIS React Native ou bibliotecas específicas. Detalhes de implementação com tecnologias concretas pertencem a PROJECTS/[PROJECT_NAME]/DOCS/ conforme arquitetura polyrepo. Ordem lógica reflete sequência temporal do processo real desde configuração inicial até certificação final seguindo fluxo configuração preparação coleta sincronização validação refinamento legitimação garantindo compreensão progressiva do sistema.

## Workflows Principais (6 documentados)

1. **[01-wms-integration-workflow.md](./01-wms-integration-workflow.md)** - Configuração e consumo de ortofotos via WMS/WMTS OGC
2. **[02-field-data-collection-workflow.md](./02-field-data-collection-workflow.md)** - Coleta de dados em campo usando app mobile offline-first
3. **[03-offline-sync-workflow.md](./03-offline-sync-workflow.md)** - Sincronização bidirecional mobile ↔ backend com conflict resolution
4. **[04-analyst-validation-workflow.md](./04-analyst-validation-workflow.md)** - Validação e correção em massa de geometrias usando GIS desktop
5. **[05-topography-workflow.md](./05-topography-workflow.md)** - Levantamento topográfico GNSS profissional com pós-processamento RBMC
6. **[06-legitimation-workflow.md](./06-legitimation-workflow.md)** - Processo completo legitimação fundiária Lei 13465/2017 (11 estados)

## Tecnologias Envolvidas (Implementação Específica em PROJECTS/)

NÃO mencionar neste diretório PostgreSQL WatermelonDB React Native QGIS NetTopologySuite Turf.js Keycloak ou bibliotecas específicas. Usar termos genéricos banco de dados relacional banco de dados local embarcado ferramenta GIS desktop com plugin biblioteca geometria computacional motor de sincronização provedor identidade OAuth2. Detalhes de implementação com tecnologias concretas stacks escolhidas configurações específicas pertencem a PROJECTS/[PROJECT_NAME]/DOCS/ conforme decisão ADR-008 sobre separação entre documentação conceitual agnóstica e documentação técnica específica de implementação.

## Relacionado

Ver também:
- **[BUSINESS-RULES/](../BUSINESS-RULES/README.md)** - Regras de negócio aplicadas durante workflows
- **[DOMAIN-MODEL/ENTITIES/](../DOMAIN-MODEL/ENTITIES/README.md)** - Entidades manipuladas pelos workflows
- **[DOMAIN-MODEL/AGGREGATES/](../DOMAIN-MODEL/AGGREGATES/README.md)** - Fronteiras de consistência atravessadas
- **[DOMAIN-MODEL/00-INDEX.md](../DOMAIN-MODEL/00-INDEX.md)** - Índice completo do modelo de domínio

---

**Última atualização:** 2025-01-08
