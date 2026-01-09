# ARCHITECTURE - Decisões Arquiteturais

Documentação técnica detalhada sobre estratégias, decisões e arquitetura da customização Keycloak para CARF.

## Arquivos

### [01-customization-strategy.md](./01-customization-strategy.md)
Estratégia completa de customização do Keycloak incluindo decisão de usar themes ao invés de fork, extensões via SPIs Java para lógica server-side, Docker image customizada com themes embarcados, versionamento Git, CI/CD pipeline, e trade-offs entre approaches (fork vs themes vs proxy vs SaaS).

### [02-theme-architecture.md](./02-theme-architecture.md)
Arquitetura detalhada dos temas CARF (login/account/email) incluindo estrutura de diretórios, herança de keycloak.v2, assets compilation pipeline, integração com @carf/tscore para validações compartilhadas, responsividade mobile-first, acessibilidade WCAG 2.1 AA, performance optimization, e estratégia de hot reload em dev vs baked-in em prod.

### [03-extension-development.md](./03-extension-development.md)
Guidelines para desenvolvimento de extensões Java (SPIs) incluindo setup Maven multi-module, implementação de Authenticator/EventListener/ProtocolMapper interfaces, testing com Arquillian, debugging remoto, packaging em JAR, deployment em `/providers/`, e exemplos práticos como CPF Validator Authenticator e Tenant Audit Event Listener.

## Princípios Arquiteturais

1. **Separation of Concerns**
   - Temas = UI/UX apenas
   - SPIs = Lógica server-side
   - Realm config = Configuração declarativa

2. **Maintainability**
   - Minimizar divergência do Keycloak upstream
   - Facilitar upgrades de versão
   - Documentar todas customizações

3. **Testability**
   - Temas testáveis via Playwright
   - SPIs testáveis via Arquillian
   - Realm config validável via schema

4. **Operability**
   - Docker image self-contained
   - Configuration as Code (realm-export.json)
   - Observability (metrics, logs, events)

## Decisões Técnicas Chave

Ver ADRs em `CENTRAL/ARCHITECTURE/ADRs/`:
- **ADR-003**: Keycloak para autenticação OAuth2/OIDC
- **ADR-005**: Multi-tenancy via RLS + user attributes
- **ADR-010**: Themes customizados ao invés de fork

## Stack Tecnológico

| Componente | Tecnologia | Versão | Justificativa |
|-----------|-----------|---------|---------------|
| **Auth Server** | Keycloak | 24.0 | Open-source, OAuth2/OIDC, multi-tenancy |
| **Template Engine** | FreeMarker | 2.3.32 | Built-in no Keycloak |
| **Frontend Build** | Bun | 1.0+ | Bundling @carf/tscore para browser |
| **Extensions** | Java | 17+ | SPIs requerem Java |
| **Build Tool** | Maven | 3.9+ | Ecosystem padrão Keycloak |
| **Testing** | Playwright + Arquillian | - | E2E + integration tests |
| **Container** | Docker | 24+ | Packaging e deployment |

## Diagramas

### Arquitetura de Customização
```
┌─────────────────────────────────────────────────────────────┐
│                     CARF Keycloak Stack                     │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │              Custom Docker Image                    │   │
│  │  quay.io/keycloak/keycloak:24.0.0 + customizations │   │
│  └────────────────────────────────────────────────────┘   │
│                         │                                   │
│        ┌────────────────┼────────────────┐                │
│        │                                  │                 │
│  ┌─────▼─────┐                   ┌───────▼──────┐         │
│  │  Themes   │                   │  Extensions  │         │
│  │  (UI/UX)  │                   │  (SPIs Java) │         │
│  └───────────┘                   └──────────────┘         │
│       │                                  │                  │
│       │ /themes/carf/                   │ /providers/*.jar │
│       │                                  │                  │
│  ┌────▼──────────────────────────────────▼────┐           │
│  │         Keycloak Server (Quarkus)           │           │
│  │  ┌─────────────────────────────────────┐   │           │
│  │  │  Realms (carf)                       │   │           │
│  │  │  ├─ Clients (6)                      │   │           │
│  │  │  ├─ Roles (4)                        │   │           │
│  │  │  ├─ Users (dynamic)                  │   │           │
│  │  │  └─ Protocol Mappers (tenant_id)    │   │           │
│  │  └─────────────────────────────────────┘   │           │
│  └─────────────────────┬───────────────────────┘           │
│                        │                                    │
└────────────────────────┼────────────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │   PostgreSQL 16     │
              │   Keycloak Database │
              └─────────────────────┘
```

### Deploy Pipeline
```
Developer → Git Push → GitHub Actions
                            │
                    ┌───────▼────────┐
                    │  Build Image   │
                    │  (Themes +     │
                    │   Extensions)  │
                    └───────┬────────┘
                            │
                    ┌───────▼────────┐
                    │  Run Tests     │
                    │  (API + E2E)   │
                    └───────┬────────┘
                            │
                    ┌───────▼────────┐
                    │  Push Registry │
                    │  (ECR/ACR/     │
                    │   Docker Hub)  │
                    └───────┬────────┘
                            │
                    ┌───────▼────────┐
                    │  Deploy K8s    │
                    │  (Rolling)     │
                    └────────────────┘
```

## Referências

- [Keycloak Server Development Guide](https://www.keycloak.org/docs/latest/server_development/)
- [Keycloak Themes](https://www.keycloak.org/docs/latest/server_development/#_themes)
- [Keycloak SPIs](https://www.keycloak.org/docs/latest/server_development/#_providers)
- [FreeMarker Documentation](https://freemarker.apache.org/docs/)
- [ADR-003: Keycloak Authentication](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-003-keycloak-autenticacao.md)
