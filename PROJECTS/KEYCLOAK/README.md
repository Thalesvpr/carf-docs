# KEYCLOAK - Sistema de Autenticação e Autorização CARF

Provedor centralizado OAuth2/OIDC customizado para autenticação, autorização e SSO das 6 aplicações do ecossistema CARF (GEOWEB, REURBCAD, GEOAPI, GEOGIS, WEBDOCS, ADMIN) com multi-tenancy dinâmico, temas personalizados PT-BR, validação CPF integrada, e extensões server-side via SPIs Java.

## 📁 Estrutura do Projeto

```
PROJECTS/KEYCLOAK/
├── DOCS/                                   # Documentação técnica completa
│   ├── ARCHITECTURE/                       # Decisões arquiteturais
│   │   ├── 01-customization-strategy.md    # Estratégia de customização
│   │   ├── 02-theme-architecture.md        # Arquitetura dos temas
│   │   └── 03-extension-development.md     # Desenvolvimento de SPIs Java
│   ├── CONCEPTS/                           # Conceitos fundamentais (ultra-compactos)
│   │   ├── 01-keycloak-themes.md           # Sistema de temas
│   │   ├── 02-keycloak-spis.md             # Service Provider Interfaces
│   │   ├── 03-realm-customization.md       # Customização de realms
│   │   ├── 04-oauth2-oidc-flows.md         # OAuth2/OIDC grant types e endpoints
│   │   └── 05-multi-tenancy-strategy.md    # Estratégia multi-tenancy
│   ├── HOW-TO/                             # Guias práticos
│   │   ├── 01-develop-themes.md            # Desenvolver temas customizados
│   │   ├── 02-deploy-extensions.md         # Deploy de SPIs Java
│   │   ├── 03-setup-dev-environment.md     # Setup ambiente de desenvolvimento
│   │   ├── 04-build-custom-image.md        # Build Docker image customizada
│   │   ├── 05-update-keycloak-version.md   # Atualizar versão Keycloak
│   │   └── 06-configure-production.md      # Configuração produção
│   ├── REFERENCE/                          # Referências técnicas
│   │   └── README.md                       # APIs, configurações, schemas
│   └── README.md                           # Índice da documentação
│
└── SRC-CODE/
    └── carf-keycloak/                      # Implementação customizada
        ├── themes/carf/                    # Temas personalizados
        │   ├── login/                      # Tema de login (PT-BR, CPF validation)
        │   ├── account/                    # Tema de conta
        │   └── email/                      # Tema de emails
        ├── extensions/                     # SPIs Java (futuro)
        │   ├── cpf-validator/              # Authenticator CPF
        │   ├── tenant-audit/               # Event Listener audit
        │   └── tenant-mapper/              # Protocol Mapper tenant_id
        ├── scripts/                        # Scripts de automação
        │   ├── setup.sh                    # Inicializar ambiente
        │   ├── backup.sh                   # Backup PostgreSQL + realm
        │   ├── restore.sh                  # Restaurar backup
        │   ├── deploy.sh                   # Build e push imagem
        │   ├── healthcheck.sh              # Validar endpoints
        │   └── generate-secrets.sh         # Gerar secrets seguros
        ├── tests/                          # Testes automatizados
        │   ├── api/                        # Testes API (Node.js)
        │   ├── e2e/                        # Testes E2E (Playwright)
        │   └── run-tests.sh                # Runner completo
        ├── .github/workflows/              # CI/CD
        │   └── test.yml                    # GitHub Actions workflow
        ├── Dockerfile                      # Multi-stage build
        ├── docker-compose.dev.yml          # Desenvolvimento (hot reload)
        ├── docker-compose.yml              # Produção (imagem custom)
        ├── Makefile                        # Comandos simplificados
        ├── BUILD.md                        # Instruções de build/deploy
        ├── CHANGELOG.md                    # Histórico de versões
        └── README.md                       # Quickstart e comandos
```

## 📚 Documentação

### Por Onde Começar

#### 1. **Entendendo Conceitos** (`DOCS/CONCEPTS/`)
Documentos ultra-compactos (estilo GEOAPI) explicando fundamentos:
- **Themes**: Sistema de customização visual FreeMarker
- **SPIs**: Extensões server-side Java
- **Realms**: Configuração OAuth2, clients, roles, users
- **OAuth2/OIDC**: Grant types, endpoints, JWT structure
- **Multi-tenancy**: User attributes → JWT claims → RLS

#### 2. **Arquitetura** (`DOCS/ARCHITECTURE/`)
Decisões técnicas detalhadas:
- **Customization Strategy**: Themes vs Fork vs SaaS
- **Theme Architecture**: Estrutura, build pipeline, deployment
- **Extension Development**: Setup Maven, SPIs Java, testing

#### 3. **Guias Práticos** (`DOCS/HOW-TO/`)
Passo-a-passo para tarefas comuns:
- Desenvolver e testar temas
- Build e deploy de extensões
- Setup ambiente local
- Atualizar versão do Keycloak
- Configurar produção

#### 4. **Referência Técnica** (`DOCS/REFERENCE/`)
APIs, configurações, schemas, códigos de erro.

### Documentação Central

Complementar em `CENTRAL/INTEGRATION/KEYCLOAK/`:
- **Configurações**: Realm export, clients OAuth2, protocol mappers
- **Integração**: 6 exemplos de código (geoweb, geoapi, reurbcad, geogis, admin, webdocs)
- **Runbooks**: 6 guias operacionais (criar usuário, tenant, troubleshoot, backup, monitoring)
- **Docker Compose**: Setup desenvolvimento

## 🚀 Quick Start

```bash
# Clone e navegue
cd PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak

# Inicializar (gera secrets, pull images, inicia stack)
make dev

# Acesse
open http://localhost:8080
# User: admin / Pass: admin

# Rodar testes
make test-all

# Ver logs
make logs
```

## 🛠️ Stack Tecnológico

| Componente | Tecnologia | Versão | Justificativa |
|-----------|-----------|---------|---------------|
| **Auth Server** | Keycloak | 24.0.0 | OAuth2/OIDC, multi-tenancy, open-source |
| **Database** | PostgreSQL | 16 | Persistência Keycloak database |
| **Template Engine** | FreeMarker | 2.3.32 | Temas customizados |
| **Frontend Build** | Bun | 1.0+ | Bundle @carf/tscore validations |
| **Extensions** | Java | 17+ | SPIs requerem Java |
| **Build Tool** | Maven | 3.9+ | Build extensões Java |
| **Testing** | Playwright + Node.js | - | E2E + API tests |
| **Container** | Docker | 24+ | Packaging e deployment |
| **CI/CD** | GitHub Actions | - | Build + test + deploy automatizado |

## 📦 Componentes Implementados

### ✅ Temas Customizados
- **Login Theme**: PT-BR, validação CPF com @carf/tscore, responsivo, acessível WCAG 2.1 AA
- **Account Theme**: Editar perfil, trocar senha
- **Email Theme**: Verificação email, reset senha (HTML + text fallback)
- **Identidade Visual**: Verde #2C5F2D, logo placeholder, mobile-first

### ✅ Docker
- **Dockerfile**: Multi-stage build com temas incluídos
- **docker-compose.dev.yml**: Desenvolvimento com hot reload
- **docker-compose.yml**: Produção com imagem customizada

### ✅ Scripts de Automação
- `setup.sh`: Inicializa ambiente completo
- `backup.sh`: Backup PostgreSQL + realm export
- `restore.sh`: Restaura backup
- `deploy.sh`: Build e push imagem
- `healthcheck.sh`: Valida endpoints
- `generate-secrets.sh`: Gera secrets seguros
- `Makefile`: Comandos simplificados

### ✅ Testes Automatizados
- **API Tests** (4 suites): token, discovery, health, admin
- **E2E Tests** (4 suites): login, password-reset, account, theme
- **CI/CD**: GitHub Actions workflow automatizado
- **Coverage**: 20+ test cases

### 🔄 Em Progresso
- **Extensions Java**: CPF Validator Authenticator, Tenant Audit Event Listener
- **Kubernetes**: Deployment manifests, Helm charts
- **Monitoring**: Prometheus integration, Grafana dashboards

## 🔗 Links Úteis

### Documentação Interna
- [Architecture Overview](./DOCS/ARCHITECTURE/README.md)
- [Concepts](./DOCS/CONCEPTS/README.md)
- [How-To Guides](./DOCS/HOW-TO/README.md)
- [Reference](./DOCS/REFERENCE/README.md)
- [Source Code](./SRC-CODE/carf-keycloak/README.md)

### Documentação Central
- [Integration Guide](../../CENTRAL/INTEGRATION/KEYCLOAK/README.md)
- **Examples** - Ver pasta examples/ com múltiplos arquivos de integração
- **Runbooks** - Ver pasta runbooks/ com procedimentos operacionais

### ADRs Relacionadas
- [ADR-003: Keycloak Authentication](../../CENTRAL/ARCHITECTURE/ADRs/ADR-003-keycloak-autenticacao.md)
- [ADR-005: Multi-tenancy RLS](../../CENTRAL/ARCHITECTURE/ADRs/ADR-005-multi-tenancy-rls.md)

### Documentação Externa
- [Keycloak Documentation](https://www.keycloak.org/documentation)
- [Server Development Guide](https://www.keycloak.org/docs/latest/server_development/)
- [Admin REST API](https://www.keycloak.org/docs-api/24.0/rest-api/)
- [OAuth 2.0 RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)

## 🎯 Próximos Passos

1. **Implementar SPIs Java** (cpf-validator, tenant-audit, tenant-mapper)
2. **Kubernetes Deployment** (manifests, Helm charts)
3. **Monitoring Stack** (Prometheus, Grafana, alerts)
4. **High Availability** (clustering, load balancing)
5. **Performance Testing** (load tests, stress tests)
6. **Security Audit** (penetration testing, vulnerability scanning)

## 📄 Licença

UNLICENSED - Proprietary

## 👥 Equipe

Projeto CARF - Sistema de Regularização Fundiária Urbana

**Última atualização:** 2026-01-09
