# KEYCLOAK - Documentação Técnica Completa

Documentação aprofundada sobre customização, desenvolvimento e operação do Keycloak para o projeto CARF.

## 📖 Índice por Categoria

### 🏗️ ARCHITECTURE/ - Decisões Arquiteturais
Documentos extensos com diagramas, decisões técnicas justificadas e trade-offs.

- **[01-customization-strategy.md](./ARCHITECTURE/01-customization-strategy.md)** - Estratégia completa: themes vs fork vs SaaS, Docker image custom, CI/CD
- **[02-theme-architecture.md](./ARCHITECTURE/02-theme-architecture.md)** - Arquitetura temas CARF: estrutura, build pipeline, @carf/tscore integration, performance
- **[03-extension-development.md](./ARCHITECTURE/03-extension-development.md)** - SPIs Java: Maven setup, interfaces, testing Arquillian, debugging remoto

### 💡 CONCEPTS/ - Conceitos Fundamentais
Documentos ultra-compactos (estilo GEOAPI) em sentença única com todos os detalhes técnicos.

- **[01-keycloak-themes.md](./CONCEPTS/01-keycloak-themes.md)** - Sistema de temas, FreeMarker, theme.properties, herança, i18n, deployment
- **[02-keycloak-spis.md](./CONCEPTS/02-keycloak-spis.md)** - Service Provider Interfaces: Authenticator, EventListener, ProtocolMapper, testing, hot-reload
- **[03-realm-customization.md](./CONCEPTS/03-realm-customization.md)** - Configuração realms: clients OAuth2, roles, user attributes, protocol mappers, realm-export
- **[04-oauth2-oidc-flows.md](./CONCEPTS/04-oauth2-oidc-flows.md)** - Grant types (PKCE, client_credentials, refresh), JWT structure, endpoints, token lifecycle
- **[05-multi-tenancy-strategy.md](./CONCEPTS/05-multi-tenancy-strategy.md)** - Multi-tenancy: user attributes → JWT tenant_id → RLS PostgreSQL, tenant switcher

### 🔧 HOW-TO/ - Guias Práticos
Passo-a-passo para tarefas de desenvolvimento e deployment.

- **[01-develop-themes.md](./HOW-TO/01-develop-themes.md)** - Desenvolver temas: setup local, hot reload, testing browsers
- **[02-deploy-extensions.md](./HOW-TO/02-deploy-extensions.md)** - Deploy SPIs: build Maven, JAR packaging, copy /providers/, rollback
- **[03-setup-dev-environment.md](./HOW-TO/03-setup-dev-environment.md)** - Setup dev: Docker Compose, IDE config, debugging, quick iteration
- **[04-build-custom-image.md](./HOW-TO/04-build-custom-image.md)** - Build image: multi-stage Dockerfile, tagging, registry push, scanning
- **[05-update-keycloak-version.md](./HOW-TO/05-update-keycloak-version.md)** - Atualizar versão: changelog, compatibility, theme fixes, staged rollout
- **[06-configure-production.md](./HOW-TO/06-configure-production.md)** - Produção: PostgreSQL externo, HTTPS, clustering, performance tuning, backup

### 📚 REFERENCE/ - Referências Técnicas
APIs, configurações, schemas, códigos de erro.

- **[README.md](./REFERENCE/README.md)** - Admin REST API, OIDC endpoints, theme.properties, FreeMarker vars, env vars, realm schema, error codes, performance tuning

## 🎯 Guia de Navegação por Objetivo

### Quero entender como funciona
1. Leia [CONCEPTS/](./CONCEPTS/) sequencialmente (01→05)
2. Consulte [ARCHITECTURE/README.md](./ARCHITECTURE/README.md) para visão geral

### Quero customizar temas
1. Leia [CONCEPTS/01-keycloak-themes.md](./CONCEPTS/01-keycloak-themes.md)
2. Siga [HOW-TO/01-develop-themes.md](./HOW-TO/01-develop-themes.md)
3. Consulte [REFERENCE/README.md](./REFERENCE/README.md) para FreeMarker vars

### Quero criar extensão Java
1. Leia [CONCEPTS/02-keycloak-spis.md](./CONCEPTS/02-keycloak-spis.md)
2. Siga [ARCHITECTURE/03-extension-development.md](./ARCHITECTURE/03-extension-development.md)
3. Use [HOW-TO/02-deploy-extensions.md](./HOW-TO/02-deploy-extensions.md)

### Quero fazer deploy
1. Siga [HOW-TO/04-build-custom-image.md](./HOW-TO/04-build-custom-image.md)
2. Configure produção: [HOW-TO/06-configure-production.md](./HOW-TO/06-configure-production.md)
3. Consulte scripts em `../SRC-CODE/carf-keycloak/scripts/`

### Quero troubleshooting
1. Consulte [REFERENCE/README.md](./REFERENCE/README.md) para códigos de erro
2. Veja runbooks em `../../../CENTRAL/INTEGRATION/KEYCLOAK/runbooks/`
3. Use [HOW-TO/03-setup-dev-environment.md](./HOW-TO/03-setup-dev-environment.md) para debugging

## 🔗 Documentação Relacionada

### Central (Integrações e Operações)
- **[CENTRAL/INTEGRATION/KEYCLOAK/](../../../CENTRAL/INTEGRATION/KEYCLOAK/)** - Configurações realm, clients OAuth2, exemplos de integração (6 apps), runbooks operacionais (6 guias)
- **[ADR-003](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-003-keycloak-autenticacao.md)** - Decisão de usar Keycloak
- **[ADR-005](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-005-multi-tenancy-rls.md)** - Estratégia multi-tenancy

### Source Code
- **[SRC-CODE/carf-keycloak/](../SRC-CODE/carf-keycloak/)** - Implementação: themes/, extensions/, scripts/, tests/

### Outros Projetos
- **[GEOAPI/DOCS/](../../GEOAPI/DOCS/)** - Backend .NET que valida JWT do Keycloak
- **[GEOWEB/DOCS/](../../GEOWEB/DOCS/)** - Frontend React com keycloak-js
- **[ADMIN/DOCS/](../../ADMIN/DOCS/)** - Admin app usando Keycloak Admin API

## 📋 Convenções de Documentação

### Estilo de Escrita

**CONCEPTS/**: Ultra-compacto, sentença única com todos os detalhes técnicos (estilo GEOAPI).

**ARCHITECTURE/**: Extenso, formal, com diagramas ASCII, tabelas, exemplos de código, justificativas de decisões.

**HOW-TO/**: Passo-a-passo claro, comandos com output esperado, troubleshooting ao final.

**REFERENCE/**: Tabelas, listas, snippets, schemas, sem narrativa.

### Atualização
- Documentar antes de implementar (design docs)
- Atualizar após mudanças significativas
- Manter exemplos de código sincronizados com implementação
- Revisar anualmente ou após major version upgrade

## 🛠️ Stack Tecnológico

| Componente | Versão | Link |
|-----------|--------|------|
| **Keycloak** | 24.0.0+ | [Docs](https://www.keycloak.org/documentation) |
| **Java** | 17+ | [Docs](https://docs.oracle.com/en/java/javase/17/) |
| **FreeMarker** | 2.3.32 | [Manual](https://freemarker.apache.org/docs/) |
| **Maven** | 3.9+ | [Guide](https://maven.apache.org/guides/) |
| **Docker** | 24+ | [Docs](https://docs.docker.com/) |
| **PostgreSQL** | 16 | [Docs](https://www.postgresql.org/docs/16/) |

## 📖 Recursos Externos

### Keycloak
- [Server Development Guide](https://www.keycloak.org/docs/latest/server_development/)
- [Admin REST API](https://www.keycloak.org/docs-api/24.0/rest-api/)
- [Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/)
- [Upgrading Guide](https://www.keycloak.org/docs/latest/upgrading/)

### OAuth2/OIDC
- [OAuth 2.0 RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)
- [PKCE RFC 7636](https://datatracker.ietf.org/doc/html/rfc7636)
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
- [JWT RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519)

### Desenvolvimento
- [FreeMarker Manual](https://freemarker.apache.org/docs/)
- [Maven Central](https://search.maven.org/)
- [Arquillian Testing](http://arquillian.org/guides/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## ✅ Checklist de Qualidade

### Antes de Implementar
- [ ] Conceitos documentados em CONCEPTS/
- [ ] Arquitetura documentada em ARCHITECTURE/
- [ ] Guia prático criado em HOW-TO/
- [ ] APIs/configs em REFERENCE/

### Após Implementar
- [ ] Exemplos de código testados
- [ ] Screenshots atualizados (se aplicável)
- [ ] Links internos funcionando
- [ ] Referências externas válidas
- [ ] Versionamento atualizado

**Última atualização:** 2026-01-09
