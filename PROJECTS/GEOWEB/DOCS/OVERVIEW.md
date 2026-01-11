# GEOWEB - Overview de Implementação

Portal web React 18 para gestão de regularização fundiária urbana, permitindo cadastro e aprovação de unidades habitacionais, vinculação de titulares, geração de relatórios e acompanhamento de processos de legitimation conforme Lei 13465/2017.

Este projeto implementa os seguintes requisitos e conceitos de negócio documentados em CENTRAL/.

## Requirements Implementados

### Use Cases Principais

- [UC-001: Cadastrar Unidade Habitacional](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-001-cadastrar-unidade-habitacional.md) - Cadastro web de unidades com geometria, fotos e dados
- [UC-002: Aprovar Unidade Habitacional](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-002-aprovar-unidade-habitacional.md) - Workflow de aprovação por analistas
- [UC-003: Vincular Titular à Unidade](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-003-vincular-titular-unidade.md) - Gestão de holders (posseiros)
- [UC-004: Coletar Dados em Campo](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-004-coletar-dados-campo-mobile.md) - Integração com dados coletados no mobile
- [UC-005: Sincronizar Dados Offline](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-005-sincronizar-dados-offline.md) - Receber dados sincronizados do REURBCAD
- [UC-006: Gerar Relatório de Comunidade](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-006-gerar-relatorio-comunidade.md) - Exportação PDF/Excel de dados
- [UC-007: Exportar Dados Geográficos](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-007-exportar-dados-geograficos.md) - GeoJSON, Shapefile para QGIS
- [UC-008: Importar Shapefile](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-008-importar-shapefile.md) - Importação de geometrias externas
- [UC-009: Gerenciar Processo de Legitimação](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-009-gerenciar-processo-legitimacao.md) - Workflow legitimation fundiária
- [UC-010: Configurar Camadas WMS](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-010-configurar-camadas-wms.md) - Integração com ortofotos drone
- [UC-011: Gerenciar Equipes Técnicas](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-011-gerenciar-equipes-tecnicas.md) - Gestão de teams e permissões

### Functional Requirements (principais)

Ver [requirements index](../../../CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/index-by-epic.md) filtrado por módulo GEOWEB. Principais áreas:

- **Autenticação**: RF-001 a RF-015 (Keycloak OAuth2, JWT, RBAC)
- **Cadastro Unidades**: RF-049 a RF-069 (CRUD, validações, geometria, fotos)
- **Gestão Titulares**: RF-070 a RF-089 (CPF validation, vinculação N:N)
- **Relatórios**: RF-150 a RF-170 (PDF, Excel, GeoJSON export)
- **WMS Integration**: RF-180 a RF-195 (ortofotos, layers, caching)
- **Legitimação**: RF-200 a RF-220 (workflow, documentação, certidões)

## Domain Model Implementado

### Entities (principais)

- [Unit](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/02-unit.md) - Unidade habitacional
- [Holder](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/03-holder.md) - Titular/posseiro
- [Community](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/04-community.md) - Comunidade/assentamento
- [Block](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/12-block.md) - Quadra urbana
- [Plot](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/13-plot.md) - Lote individual
- [Document](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/14-document.md) - Anexos (fotos, PDFs)
- [Annotation](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/15-annotation.md) - Observações e notas
- [UnitHolder](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/16-unit-holder.md) - Vínculo N:N unit-holder
- [Team](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/09-team.md) - Equipes técnicas
- [Account](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/08-account.md) - Usuários autenticados
- [LegitimationRequest](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/25-legitimation-request.md) - Processo legitimação
- [WmsServer](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/29-wms-server.md) - Servidores WMS
- [WmsLayer](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/30-wms-layer.md) - Camadas WMS/WMTS

### Value Objects (principais)

- [CPF](../../../CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/01-cpf.md) - Validação CPF brasileiro
- [GeoPolygon](../../../CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/02-geo-polygon.md) - Polígonos geográficos
- [UnitStatus](../../../CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/03-unit-status.md) - Status workflow unidade
- [Email](../../../CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/08-email.md) - Validação email RFC5322
- [PhoneNumber](../../../CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/09-phone-number.md) - Telefone brasileiro
- [Address](../../../CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/10-address.md) - Endereço estruturado
- [LegitimationStatus](../../../CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/22-legitimation-status.md) - Status legitimação Lei 13465

### Aggregates

- [UnitAggregate](../../../CENTRAL/DOMAIN-MODEL/AGGREGATES/01-unit-aggregate.md) - Consistência transacional de Unit + Holders + Documents
- [CommunityAggregate](../../../CENTRAL/DOMAIN-MODEL/AGGREGATES/02-community-aggregate.md) - Community + Blocks + Units
- [LegitimationRequestAggregate](../../../CENTRAL/DOMAIN-MODEL/AGGREGATES/03-legitimation-request-aggregate.md) - Legitimation workflow completo

## Arquitetura Técnica

**Stack:**
- React 18 (framework UI)
- TypeScript 5 (type safety)
- Vite (bundler)
- TanStack Query (server state)
- Zustand (client state)
- React Router 6 (SPA routing)
- Leaflet (mapas interativos)
- shadcn/ui (componentes UI)
- @carf/tscore (biblioteca compartilhada - autenticação, value objects)
- @carf/geoapi-client (cliente tipado HTTP para backend)
- @carf/ui (componentes UI compartilhados)

**Deploy:** Vercel (edge functions, CDN global)

Ver [ARCHITECTURE/](./ARCHITECTURE/README.md) para ADRs técnicos específicos deste projeto.

## Features Documentadas

Ver [FEATURES/](./FEATURES/README.md) para documentação detalhada de cada funcionalidade implementada:

- [Unit Management](./FEATURES/unit-management.md) - Cadastro e gestão de unidades
- [Holder Management](./FEATURES/holder-management.md) - Gestão de titulares
- [GIS Integration](./FEATURES/gis-integration.md) - Mapas Leaflet + WMS
- [Reporting](./FEATURES/reporting.md) - Exportações PDF/Excel/GeoJSON
- [Shapefile Import](./FEATURES/shapefile-import.md) - Importação geometrias
- [Legitimation Process](./FEATURES/legitimation-process.md) - Workflow legitimação
- [Team Management](./FEATURES/team-management.md) - Gestão de equipes técnicas

---

**Última atualização:** 2026-01-10
