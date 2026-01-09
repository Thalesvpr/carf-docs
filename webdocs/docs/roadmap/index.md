# Roadmap

Planejamento de releases e evolução do sistema CARF.

## Versão Atual

**v1.0.0** - MVP (Minimum Viable Product)

Em desenvolvimento inicial.

## Releases Planejadas

### v1.0.0 - MVP (Q1 2026)

**GEOAPI (Backend)**
- ✅ Clean Architecture com CQRS
- ✅ PostgreSQL + PostGIS
- ✅ Multi-tenancy com RLS
- 🚧 CRUD completo de Units
- 🚧 CRUD completo de Holders
- 🚧 CRUD completo de Communities
- 🚧 Autenticação Keycloak

**GEOWEB (Frontend)**
- ✅ Feature-Sliced Design
- 🚧 Interface de cadastro Units
- 🚧 Interface de cadastro Holders
- 🚧 Interface de cadastro Communities
- 🚧 Integração com Keycloak
- 🚧 Mapas interativos

**REURBCAD (Mobile)**
- ✅ Offline-first com WatermelonDB
- 🚧 Cadastro offline de Units
- 🚧 GPS tracking
- 🚧 Sincronização incremental
- 🚧 Captura de fotos

**GEOGIS (Plugin QGIS)**
- 🚧 Conexão com GEOAPI
- 🚧 Exportação shapefile/GeoJSON
- 🚧 Operações geoespaciais básicas

**WEBDOCS (Documentação)**
- ✅ Setup VitePress
- 🚧 Migração docs do CENTRAL
- 🚧 Geração automática sidebar
- 🚧 Deploy GitHub Pages

### v1.1.0 - Processos REURB (Q2 2026)

- Workflow de processos
- Geração de documentos oficiais
- Relatórios básicos
- Histórico de alterações

### v1.2.0 - Melhorias GIS (Q3 2026)

- Operações geoespaciais avançadas
- Análise de sobreposições
- Cálculo de áreas e perímetros
- Buffers e intersecções

### v2.0.0 - Integrações Externas (Q4 2026)

- Integração com sistemas de cartório
- Consulta CPF/CNPJ Receita Federal
- Integração com órgãos municipais
- APIs públicas para terceiros

### v2.1.0 - Analytics e BI (Q1 2027)

- Dashboard executivo
- Relatórios customizáveis
- Exportação para Excel/PDF
- KPIs e métricas

## Funcionalidades em Backlog

- [ ] Notificações push no mobile
- [ ] Chat integrado para equipes
- [ ] Versionamento de documentos
- [ ] Assinatura digital
- [ ] Integração com drones para mapeamento
- [ ] IA para análise de imagens aéreas
- [ ] App mobile iOS

## Legenda

- ✅ Concluído
- 🚧 Em desenvolvimento
- ⏳ Planejado
- 📋 Backlog

## Contribuir

Este roadmap é dinâmico e pode ser ajustado conforme necessidades do projeto.

Para sugestões ou feedback:
- Abra uma issue no [GitHub](https://github.com/Thalesvpr/carf-docs/issues)
- Entre em contato com a equipe
