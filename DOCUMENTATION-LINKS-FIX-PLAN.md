# Plano de Correção de Links da Documentação CARF

**Problema:** 80% da documentação está desconectada (sem links entre arquivos)
**Objetivo:** Criar uma rede interconectada de documentação com navegação bidire

cional

---

## 📊 Estatísticas Atuais

| Métrica | Valor | Status |
|---------|-------|--------|
| Total de arquivos markdown | 876 | - |
| Arquivos SEM links | ~80+ | ⚠️ Crítico |
| CENTRAL → PROJECTS links | 81 refs | ⚠️ Fraco |
| PROJECTS → CENTRAL links | 8/10 projetos | ✅ Bom |
| ADR cross-references | 0 | 🔴 Crítico |
| RF cross-references | 0 | 🔴 Crítico |
| API docs → GEOAPI links | 0 | 🔴 Crítico |

---

## 🎯 Prioridades de Correção

### 🔴 PRIORIDADE CRÍTICA

#### 1. API Documentation → GEOAPI Implementation
**Impacto:** Alto - Quebra a rastreabilidade de requisitos para implementação

**Arquivos a corrigir:**
- `CENTRAL/API/README.md` - Adicionar links para GEOAPI
- `CENTRAL/API/AUTHENTICATION/README.md` → `PROJECTS/GEOAPI/DOCS/ARCHITECTURE/01-keycloak-integration.md`
- `CENTRAL/API/UNITS/README.md` → `PROJECTS/GEOAPI/DOCS/HOW-TO/`
- `CENTRAL/API/HOLDERS/README.md` → `PROJECTS/GEOAPI/DOCS/HOW-TO/`
- `CENTRAL/API/COMMUNITIES/README.md` → `PROJECTS/GEOAPI/DOCS/HOW-TO/`
- `CENTRAL/API/LEGITIMATION/README.md` → `PROJECTS/GEOAPI/DOCS/HOW-TO/`
- `CENTRAL/API/REPORTS/README.md` → `PROJECTS/GEOAPI/DOCS/HOW-TO/`

**Template de link:**
```markdown
## Implementação

- [Documentação GEOAPI](../../../PROJECTS/GEOAPI/DOCS/ARCHITECTURE/)
- [Guia de uso da API](../../../PROJECTS/GEOAPI/DOCS/HOW-TO/)
- [Cliente TypeScript](../../../PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/README.md)
```

#### 2. Functional Requirements → Use Cases → API → Implementation
**Impacto:** Alto - Rastreabilidade completa de requisitos

**Exemplo: RF-001-integração-com-keycloak.md**
Adicionar seção:
```markdown
## Rastreabilidade

### Decisões Arquiteturais
- [ADR-003: Keycloak Autenticação](../../ARCHITECTURE/ADRs/ADR-003-keycloak-autenticacao.md)

### Casos de Uso
- [UC-001: Autenticar Usuário](../USE-CASES/UC-001-autenticar-usuario.md)

### Implementação
- [GEOAPI Keycloak Integration](../../../PROJECTS/GEOAPI/DOCS/ARCHITECTURE/01-keycloak-integration.md)
- [GEOWEB Keycloak Integration](../../../PROJECTS/GEOWEB/DOCS/ARCHITECTURE/01-keycloak-integration.md)
- [REURBCAD Keycloak Integration](../../../PROJECTS/REURBCAD/DOCS/ARCHITECTURE/01-keycloak-integration.md)

### Configuração
- [Keycloak Setup Guide](../../INTEGRATION/KEYCLOAK/README.md)
- [Client Configurations](../../INTEGRATION/KEYCLOAK/05-client-configurations.md)
```

**Arquivos a corrigir:** 222 RFs em `CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/`

#### 3. ADR Cross-References
**Impacto:** Médio-Alto - Contexto de decisões técnicas

**Arquivos a corrigir:**
- `ADR-001-dotnet-backend.md` → Link to ADR-008 (Clean Architecture)
- `ADR-002-postgresql-postgis.md` → Link to ADR-005 (Multi-tenancy RLS)
- `ADR-003-keycloak-autenticacao.md` → Link to ADR-005, ADR-011
- `ADR-004-react-native-mobile.md` → Link to ADR-006, ADR-007
- `ADR-005-multi-tenancy-rls.md` → Link to ADR-002, ADR-003
- `ADR-006-offline-first-watermelondb.md` → Link to ADR-004
- `ADR-007-bun-runtime-bundler.md` → Link to ADR-011
- `ADR-008-clean-architecture-ddd.md` → Link to ADR-009, ADR-010
- `ADR-009-cqrs-pattern.md` → Link to ADR-008, ADR-010
- `ADR-010-event-driven-architecture.md` → Link to ADR-009
- `ADR-011-shared-library.md` → Link to ADR-007

**Template:**
```markdown
## Decisões Relacionadas

- [ADR-XXX: Título](./ADR-XXX-titulo.md) - Descrição breve da relação
```

---

### 🟡 PRIORIDADE ALTA

#### 4. PATTERNS → ADRs
**Impacto:** Médio - Conectar padrões arquiteturais com decisões

**Arquivos a corrigir:**
- `CENTRAL/ARCHITECTURE/PATTERNS/01-clean-architecture.md` → ADR-008
- `CENTRAL/ARCHITECTURE/PATTERNS/02-cqrs.md` → ADR-009
- `CENTRAL/ARCHITECTURE/PATTERNS/03-repository-uow.md` → ADR-008
- `CENTRAL/ARCHITECTURE/PATTERNS/04-domain-events.md` → ADR-010
- `CENTRAL/ARCHITECTURE/PATTERNS/05-frontend-patterns.md` → ADR-004, ADR-006
- `CENTRAL/ARCHITECTURE/PATTERNS/06-mobile-offline-first.md` → ADR-006
- `CENTRAL/ARCHITECTURE/PATTERNS/07-gis-spatial-patterns.md` → ADR-002

#### 5. WORKFLOWS → Requirements → Domain Model
**Impacto:** Médio - Rastreabilidade de processos de negócio

**Exemplo: WORKFLOWS/06-legitimation-workflow.md**
```markdown
## Rastreabilidade

### Requisitos Funcionais
- [RF-055: Iniciar processo de legitimação](../REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/RF-055-iniciar-processo-legitimacao.md)
- [RF-056 a RF-070: Requisitos de legitimação](../REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/)

### Casos de Uso
- [UC-009: Gerenciar Processo de Legitimação](../REQUIREMENTS/USE-CASES/UC-009-gerenciar-processo-legitimacao.md)

### Modelo de Domínio
- [Legitimation Request Aggregate](../DOMAIN-MODEL/AGGREGATES/03-legitimation-request-aggregate.md)
- [Legitimation Entity](../DOMAIN-MODEL/ENTITIES/legitimation.md)

### Implementação
- [GEOAPI Legitimation API](../../PROJECTS/GEOAPI/DOCS/ARCHITECTURE/)
- [GEOWEB Legitimation Module](../../PROJECTS/GEOWEB/DOCS/LAYERS/features/legitimation.md)
```

#### 6. INTEGRATION/KEYCLOAK → All Projects
**Impacto:** Médio - Autenticação é cross-cutting

**Arquivo base:** `CENTRAL/INTEGRATION/KEYCLOAK/README.md`
Adicionar seção:
```markdown
## Implementações por Projeto

### Backend
- [GEOAPI: Keycloak Integration](../../../PROJECTS/GEOAPI/DOCS/ARCHITECTURE/01-keycloak-integration.md)
  - JWT validation middleware
  - RBAC authorization
  - Multi-tenancy support

### Frontend Web
- [GEOWEB: Keycloak Integration](../../../PROJECTS/GEOWEB/DOCS/ARCHITECTURE/01-keycloak-integration.md)
  - OAuth2 PKCE flow
  - Protected routes
  - Token refresh

### Mobile
- [REURBCAD: Keycloak Integration](../../../PROJECTS/REURBCAD/DOCS/ARCHITECTURE/01-keycloak-integration.md)
  - Offline token storage
  - Biometric authentication
  - Token refresh

### Desktop Plugin
- [GEOGIS: Keycloak Integration](../../../PROJECTS/GEOGIS/DOCS/ARCHITECTURE/01-keycloak-integration.md)
  - Client credentials flow
  - Service account authentication

### Admin Console
- [ADMIN: Keycloak Integration](../../../PROJECTS/ADMIN/DOCS/ARCHITECTURE/README.md)
  - Keycloak Admin API
  - User management
  - Realm administration

### Customization
- [KEYCLOAK: Theme Customization](../../../PROJECTS/KEYCLOAK/DOCS/ARCHITECTURE/01-customization-strategy.md)
```

---

### 🟢 PRIORIDADE MÉDIA

#### 7. Projects Inter-linking
**Impacto:** Baixo-Médio - Facilita navegação entre projetos relacionados

**Exemplo: GEOWEB → GEOAPI + TSCORE + GEOAPI-CLIENT + UI**
Em `PROJECTS/GEOWEB/DOCS/README.md`:
```markdown
## Dependências

### Backend API
- [GEOAPI](../../GEOAPI/DOCS/README.md) - REST API .NET 9

### Bibliotecas Compartilhadas
- [TSCORE](../../LIB/TS/TSCORE/DOCS/README.md) - Validações, auth, types
- [GEOAPI-CLIENT](../../LIB/TS/GEOAPI-CLIENT/DOCS/README.md) - HTTP client
- [UI-COMPONENTS](../../LIB/TS/UI-COMPONENTS/DOCS/README.md) - Componentes React

### Autenticação
- [Keycloak Integration](../../../CENTRAL/INTEGRATION/KEYCLOAK/README.md)
```

#### 8. DOMAIN-MODEL Internal Links
**Impacto:** Baixo - Melhor compreensão do modelo de domínio

Adicionar links entre:
- Aggregates → Entities
- Entities → Value Objects
- Entities → Events
- Relationships documentation

---

## 🛠️ Implementação

### Fase 1: Scripts de Automação (Recomendado)
Criar scripts para adicionar links automaticamente:

```bash
# Script 1: Adicionar seção "Rastreabilidade" em todos RFs
./scripts/add-rf-traceability.sh

# Script 2: Adicionar seção "Decisões Relacionadas" em ADRs
./scripts/add-adr-cross-refs.sh

# Script 3: Adicionar seção "Implementação" em API docs
./scripts/add-api-implementation-links.sh

# Script 4: Validar links quebrados
./scripts/validate-markdown-links.sh
```

### Fase 2: Manual (Críticos primeiro)
1. **Semana 1:** API docs → GEOAPI (7 arquivos)
2. **Semana 2:** RFs → UCs → API (222 arquivos - automatizar!)
3. **Semana 3:** ADRs cross-references (11 arquivos)
4. **Semana 4:** PATTERNS → ADRs (7 arquivos)
5. **Semana 5:** WORKFLOWS → Requirements (6 arquivos)

### Fase 3: Validação
```bash
# Usar ferramenta de validação de links
npm install -g markdown-link-check
find . -name "*.md" -exec markdown-link-check {} \;
```

---

## 📋 Templates de Seções

### Template: Seção "Rastreabilidade" (RFs)
```markdown
## Rastreabilidade

### Decisões Arquiteturais
- [ADR-XXX: Título](caminho/relativo)

### Casos de Uso
- [UC-XXX: Título](caminho/relativo)

### Histórias de Usuário
- [US-XXX: Título](caminho/relativo)

### API Endpoints
- [Endpoint Name](caminho/relativo)

### Implementação
- [PROJETO: Título](caminho/relativo)

### Testes
- [Test Suite](caminho/relativo)
```

### Template: Seção "Decisões Relacionadas" (ADRs)
```markdown
## Decisões Relacionadas

### Dependências
- [ADR-XXX: Título](./ADR-XXX.md) - Esta decisão depende de...

### Impactadas por esta decisão
- [ADR-XXX: Título](./ADR-XXX.md) - Esta decisão impacta...

### Alternativas consideradas
- [ADR-XXX: Título](./ADR-XXX.md) - Alternativa rejeitada porque...
```

### Template: Seção "Implementação" (API Docs)
```markdown
## Implementação

### Backend
- [GEOAPI: Arquitetura](caminho/relativo)
- [GEOAPI: Como Usar](caminho/relativo)

### Frontend/Mobile
- [GEOWEB: Integração](caminho/relativo)
- [REURBCAD: Integração](caminho/relativo)

### Cliente TypeScript
- [GEOAPI-CLIENT: API Reference](caminho/relativo)
- [Exemplo de uso](caminho/relativo)

### Testes
- [Test Cases](caminho/relativo)
```

---

## ✅ Checklist de Progresso

### CENTRAL/
- [ ] API/ (7 arquivos)
- [ ] ARCHITECTURE/ADRs/ (11 arquivos)
- [ ] ARCHITECTURE/PATTERNS/ (7 arquivos)
- [ ] REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/ (222 arquivos)
- [ ] WORKFLOWS/ (6 arquivos)
- [ ] INTEGRATION/KEYCLOAK/ (1 arquivo - README)

### PROJECTS/
- [ ] GEOAPI/DOCS/ (10 arquivos)
- [ ] GEOWEB/DOCS/ (13 arquivos)
- [ ] REURBCAD/DOCS/ (12 arquivos)
- [ ] GEOGIS/DOCS/ (11 arquivos)
- [ ] LIB/TS/TSCORE/DOCS/ (5 arquivos)
- [ ] LIB/TS/GEOAPI-CLIENT/DOCS/ (criar mais docs)
- [ ] LIB/TS/UI-COMPONENTS/DOCS/ (criar docs)
- [ ] KEYCLOAK/DOCS/ (5 arquivos)
- [ ] ADMIN/DOCS/ (2 arquivos)
- [ ] WEBDOCS/DOCS/ (1 arquivo)

---

## 📊 Métricas de Sucesso

**Antes:**
- 80+ arquivos sem links (isolados)
- 0 ADR cross-references
- 0 RF rastreabilidade
- 0 API → Implementation links

**Depois (Meta):**
- <10 arquivos sem links
- 11 ADRs com cross-references
- 222 RFs com rastreabilidade completa
- 7 API docs linkados para GEOAPI

**KPI:** Reduzir documentação desconectada de 80% para <10%

---

## 🚀 Próximos Passos

1. ✅ **Criar este plano** (FEITO)
2. ⏳ **Revisar e aprovar o plano** (aguardando)
3. ⏳ **Desenvolver scripts de automação**
4. ⏳ **Executar Fase 1 (Críticos)**
5. ⏳ **Executar Fase 2 (Altos)**
6. ⏳ **Executar Fase 3 (Médios)**
7. ⏳ **Validar todos os links**
8. ⏳ **Commitar mudanças**

---

**Criado em:** 2026-01-09
**Última atualização:** 2026-01-09
**Status:** 📋 Planejamento
**Responsável:** Equipe CARF Dev
