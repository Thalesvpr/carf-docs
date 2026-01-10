# 014 - Create Integration Guides (Theory Only)

🟡 **Prioridade:** Alta
📅 **Criado em:** 2026-01-09
⏱️ **Estimativa:** 1 dia

## Descrição

Criar guias teóricos de integração mostrando COMO os projetos devem se integrar entre si e com as bibliotecas compartilhadas. Não precisa de código funcionando - apenas documentação clara de como será quando implementar.

## Checklist

### Main Integration Doc
- [ ] Criar `CENTRAL/INTEGRATION/LIBRARIES/README.md`

### Library Integration Guides
- [ ] `CENTRAL/INTEGRATION/LIBRARIES/01-tscore-integration.md`
  - Como instalar `@carf/tscore`
  - Como configurar KeycloakClient (teoria)
  - Como usar validações (teoria)
  - Como importar types
  - Exemplo teórico de código

- [ ] `CENTRAL/INTEGRATION/LIBRARIES/02-geoapi-client-integration.md`
  - Como instalar `@carf/geoapi-client`
  - Como configurar com auth
  - Como usar endpoints (teoria)
  - Como tratar erros (teoria)
  - Exemplo teórico de código

- [ ] `CENTRAL/INTEGRATION/LIBRARIES/03-ui-components-integration.md`
  - Como instalar `@carf/ui`
  - Como configurar Tailwind
  - Como usar ThemeProvider (teoria)
  - Como usar componentes (teoria)
  - Exemplo teórico de código

### Project Integration Guides
- [ ] `CENTRAL/INTEGRATION/PROJECTS/01-geoweb-integration.md`
  - Quais libs usa (tscore, geoapi-client, ui)
  - Como se conecta ao GEOAPI
  - Como faz auth com Keycloak
  - Diagrama de integração

- [ ] `CENTRAL/INTEGRATION/PROJECTS/02-reurbcad-integration.md`
  - Quais libs usa
  - Como sincroniza com GEOAPI
  - Offline-first strategy
  - Diagrama de integração

- [ ] `CENTRAL/INTEGRATION/PROJECTS/03-admin-integration.md`
  - Quais libs usa
  - Como acessa Keycloak Admin API
  - Diagrama de integração

### Full Stack Integration
- [ ] `CENTRAL/INTEGRATION/00-full-stack-overview.md`
  - Diagrama completo mostrando TODOS os projetos
  - Como se comunicam entre si
  - Fluxo de autenticação end-to-end
  - Fluxo de dados end-to-end

## Conteúdo Deve Incluir

### Para Cada Guia
- ✅ Diagrama de integração
- ✅ Dependências necessárias
- ✅ Configuração (teórica)
- ✅ Exemplo de código (pseudo-código ok)
- ✅ Links para docs de referência
- ✅ Troubleshooting comum
- ❌ Nenhum código real precisa funcionar

### Exemplo de Estrutura

```markdown
# Integração GEOWEB com Bibliotecas

## Visão Geral
GEOWEB é um frontend React que usa...

## Dependências
- @carf/tscore - auth, validations, types
- @carf/geoapi-client - HTTP client para GEOAPI
- @carf/ui - componentes React

## Instalação (Teórica)
\`\`\`bash
bun add @carf/tscore @carf/geoapi-client @carf/ui
\`\`\`

## Configuração

### 1. Setup Keycloak Auth
\`\`\`typescript
// Pseudo-código - não precisa funcionar
import { KeycloakClient } from '@carf/tscore/auth';

const keycloak = new KeycloakClient({
  url: process.env.KEYCLOAK_URL,
  realm: 'carf',
  clientId: 'geoweb-client'
});
\`\`\`

[... continua com mais exemplos teóricos]
```

## Localização

`CENTRAL/INTEGRATION/`

## Referências

- [CENTRAL/API/](../API/README.md)
- PROJECTS/*/DOCS/ (documentação de cada projeto)

## Objetivo

Qualquer desenvolvedor que ler esses guias deve entender TEORICAMENTE como tudo se integra, mesmo que o código ainda não exista.
