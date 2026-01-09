# 013 - Complete Remaining Projects Documentation

🟢 **Prioridade:** Média
📅 **Criado em:** 2026-01-09
⏱️ **Estimativa:** 2-3 dias

## Descrição

Completar documentação dos projetos restantes: GEOGIS, ADMIN e WEBDOCS. São projetos importantes mas menos críticos que backend/frontend/mobile.

---

## GEOGIS (Plugin QGIS)

**Status:** 18% (3/16 arquivos)

### Arquivos Faltando (13)
- [ ] DOCS/ARCHITECTURE/README.md
- [ ] DOCS/ARCHITECTURE/01-overview.md (Python plugin architecture)
- [ ] DOCS/ARCHITECTURE/03-data-flow.md
- [ ] DOCS/ARCHITECTURE/04-integration.md (QGIS API, GEOAPI)
- [ ] DOCS/ARCHITECTURE/05-deployment.md (QGIS plugin install)
- [ ] DOCS/CONCEPTS/README.md
- [ ] DOCS/CONCEPTS/01-key-concepts.md (PyQGIS, Layers, Features)
- [ ] DOCS/CONCEPTS/02-terminology.md
- [ ] DOCS/CONCEPTS/03-design-principles.md
- [ ] DOCS/HOW-TO/README.md
- [ ] DOCS/HOW-TO/02-build-and-run.md
- [ ] DOCS/HOW-TO/03-testing.md
- [ ] SRC-CODE/carf-geogis/README.md

### Conteúdo Específico
- Como desenvolver plugin QGIS
- Como integrar com PyQGIS API
- Como consumir GEOAPI
- Como exportar Shapefile/GeoJSON
- Como instalar plugin

---

## ADMIN (Console React)

**Status:** 12% (2/16 arquivos)

### Arquivos Faltando (14)
- [ ] DOCS/ARCHITECTURE/01-overview.md (React SPA architecture)
- [ ] DOCS/ARCHITECTURE/03-data-flow.md
- [ ] DOCS/ARCHITECTURE/04-integration.md (GEOAPI admin endpoints, Keycloak Admin API)
- [ ] DOCS/ARCHITECTURE/05-deployment.md
- [ ] DOCS/CONCEPTS/README.md
- [ ] DOCS/CONCEPTS/01-key-concepts.md (Admin operations, User management)
- [ ] DOCS/CONCEPTS/02-terminology.md
- [ ] DOCS/CONCEPTS/03-design-principles.md
- [ ] DOCS/HOW-TO/README.md
- [ ] DOCS/HOW-TO/01-setup-dev-environment.md
- [ ] DOCS/HOW-TO/02-build-and-run.md
- [ ] DOCS/HOW-TO/03-testing.md
- [ ] DOCS/HOW-TO/04-troubleshooting.md
- [ ] SRC-CODE/carf-admin/README.md (precisa atualizar)

### Conteúdo Específico
- Diferença entre Admin e GEOWEB (analistas vs admin)
- Operações administrativas (user management, realm config)
- Integração com Keycloak Admin Client
- RBAC (quem pode acessar admin)

---

## WEBDOCS (Portal VitePress)

**Status:** 6% (1/16 arquivos)

### Arquivos Faltando (15)
- [ ] DOCS/ARCHITECTURE/README.md
- [ ] DOCS/ARCHITECTURE/01-overview.md (VitePress static site)
- [ ] DOCS/ARCHITECTURE/03-data-flow.md (markdown → VitePress → static HTML)
- [ ] DOCS/ARCHITECTURE/04-integration.md (consume CENTRAL docs)
- [ ] DOCS/ARCHITECTURE/05-deployment.md (GitHub Pages)
- [ ] DOCS/CONCEPTS/README.md
- [ ] DOCS/CONCEPTS/01-key-concepts.md (VitePress, Static Site, Markdown)
- [ ] DOCS/CONCEPTS/02-terminology.md
- [ ] DOCS/CONCEPTS/03-design-principles.md (docs structure)
- [ ] DOCS/HOW-TO/README.md
- [ ] DOCS/HOW-TO/01-setup-dev-environment.md
- [ ] DOCS/HOW-TO/02-build-and-run.md (VitePress dev server)
- [ ] DOCS/HOW-TO/03-testing.md (link validation)
- [ ] DOCS/HOW-TO/04-troubleshooting.md
- [ ] SRC-CODE/carf-webdocs/README.md

### Conteúdo Específico
- Como consumir markdown do CENTRAL
- Como configurar VitePress
- Como organizar sidebar
- Como fazer deploy para GitHub Pages
- Como fazer search funcionar

---

## Prioridade de Execução

1. **ADMIN** (console importante)
2. **GEOGIS** (integração GIS)
3. **WEBDOCS** (documentação pública)

## Localização

- `PROJECTS/GEOGIS/DOCS/`
- `PROJECTS/ADMIN/DOCS/`
- `PROJECTS/WEBDOCS/DOCS/`

## Referências do Template

Ver: `CENTRAL/TEMPLATES/PROJECT-DOCS-TEMPLATE.md`
