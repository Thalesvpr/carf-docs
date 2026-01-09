# KEYCLOAK - Documentação Específica de Implementação

Este diretório contém a documentação técnica específica da implementação customizada do Keycloak para o projeto CARF.

## Estrutura da Documentação

### ARCHITECTURE/
Documentação de decisões arquiteturais e estratégias de customização do Keycloak.

- **01-customization-strategy.md** - Estratégia de customização (temas, extensions, SPIs)
- **02-theme-architecture.md** - Arquitetura dos temas customizados
- **03-extension-development.md** - Desenvolvimento de extensions e SPIs Java

### CONCEPTS/
Conceitos fundamentais sobre customização do Keycloak.

- **01-keycloak-themes.md** - Sistema de temas do Keycloak
- **02-keycloak-spis.md** - Service Provider Interfaces (SPIs)
- **03-realm-customization.md** - Customização de realms

### HOW-TO/
Guias práticos de implementação e desenvolvimento.

- **01-develop-themes.md** - Como desenvolver temas customizados
- **02-deploy-extensions.md** - Como fazer deploy de extensions
- **03-setup-dev-environment.md** - Configurar ambiente de desenvolvimento
- **04-build-custom-image.md** - Build de imagem Docker customizada

## Relação com CENTRAL/

A documentação em `CENTRAL/INTEGRATION/KEYCLOAK/` contém:
- Configurações de clientes OAuth2
- Documentação de integração com outros projetos
- Realm export (configuração base)
- Docker Compose para desenvolvimento

Esta documentação em `PROJECTS/KEYCLOAK/DOCS/` foca em:
- Customizações visuais (temas)
- Extensões funcionais (SPIs)
- Build e deployment de versão customizada

## Tecnologias

- **Keycloak:** 24.0.0+
- **Java:** 17+ (para extensions)
- **FreeMarker:** Template engine para temas
- **Docker:** Para build e deployment
- **Maven/Gradle:** Para build de extensions Java

## Links Úteis

- [Keycloak Server Developer Guide](https://www.keycloak.org/docs/latest/server_development/)
- [Keycloak Theme Documentation](https://www.keycloak.org/docs/latest/server_development/#_themes)
- [Keycloak SPI Documentation](https://www.keycloak.org/docs/latest/server_development/#_providers)
