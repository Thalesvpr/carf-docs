---
status: review
updated: 2026-01-19
---

# Ecosystem

Catálogo canônico das aplicações do ecossistema CARF, definindo identificadores, metadados de autenticação, URLs e configurações de branding para uso consistente em todo o sistema.

## Aplicações

| ID | Nome | Tipo | Descrição |
|:---|:-----|:-----|:----------|
| `geoweb` | GeoWeb | web | Portal web para analistas REURB |
| `reurbcad` | REURBCAD Mobile | mobile | Aplicativo mobile para agentes de campo |
| `geoapi` | GeoAPI | api | Backend API REST |
| `geogis` | GeoGIS | desktop | Plugin QGIS para integração geoespacial |
| `webdocs` | WebDocs | web | Portal de documentação técnica |
| `admin` | Painel Admin | web | Console de administração do sistema |
| `account` | Account Console | internal | Gerenciamento de conta (legacy) |
| `account-console` | Account Console | internal | Gerenciamento de conta (novo) |
| `admin-cli` | Admin CLI | internal | CLI de administração Keycloak |

## Estrutura do Registro

O arquivo `applications.json` contém o registro estruturado com os seguintes campos:

```json
{
  "id": "string",           // Identificador único da aplicação
  "name": "string",         // Nome de exibição (displayName)
  "description": "string",  // Descrição breve
  "type": "web|mobile|api|desktop|internal",
  "visibility": "public|internal",
  "status": "active|deprecated|planned",
  "auth": {
    "clientId": "string",   // Client ID no Keycloak
    "type": "public|confidential|bearer-only|internal",
    "pkce": "boolean"       // Se usa PKCE (opcional)
  },
  "urls": {                 // URLs por ambiente (opcional)
    "dev": "string",
    "prod": "string"
  },
  "branding": {             // Configurações visuais (opcional)
    "icon": "string",
    "color": "string"
  }
}
```

## Consumidores

| Sistema | Uso |
|:--------|:----|
| Keycloak Theme | displayName na tela de login |
| Painel Admin | Lista de aplicações, status, monitoramento |
| WebDocs | Catálogo automático de aplicações |
| Monitoring | Dashboards e métricas por aplicação |
| CI/CD | Validação de deploys e configurações |

## Como Adicionar uma Aplicação

1. Editar `applications.json`
2. Adicionar novo objeto no array `applications`
3. Preencher campos obrigatórios: `id`, `name`, `description`, `type`, `visibility`, `status`, `auth`
4. Validar JSON
5. Atualizar consumidores que fazem cache do registro

## Referências

- [Design System](../DESIGN-SYSTEM/README.md) - Especificações visuais para branding
- [Keycloak Realm](../INTEGRATION/KEYCLOAK/REALM/README.md) - Configuração do realm
- [ADR-023](../ARCHITECTURE/ADRs/ADR-023-color-palette-design-system.md) - Paleta de cores

<!-- CARF-INDEX-START -->

<!-- CARF-INDEX-END -->
