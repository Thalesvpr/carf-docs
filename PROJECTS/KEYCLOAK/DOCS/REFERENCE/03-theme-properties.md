---
type: leaf
status: review
description: "REFERENCE usa code blocks extensivos para configuracao - formato referencia incompativel com prosa densa"
updated: 2026-01-22
---

# Theme Properties

Arquivo `theme.properties` na raiz de cada theme type (login, account, email) configura herança, recursos e comportamento do tema Keycloak.

## Localização

```
themes/
└── carf/
    ├── login/
    │   └── theme.properties    # Configurações do tema de login
    ├── account/
    │   └── theme.properties    # Configurações do tema de conta
    └── email/
        └── theme.properties    # Configurações do tema de email
```

## Propriedades Principais

### parent

Define tema pai para herança. Recursos não sobrescritos são herdados do pai.

```properties
# Herda do tema padrão Keycloak v2
parent=keycloak.v2

# Herda de outro tema customizado
parent=meu-tema-base
```

**Temas disponíveis para herança:**
- `keycloak` - Tema base legado
- `keycloak.v2` - Tema padrão moderno (recomendado)
- `base` - Tema mínimo sem estilos

### import

Importa recursos de namespaces compartilhados (common themes).

```properties
# Importa recursos do common/keycloak
import=common/keycloak

# Múltiplos imports
import=common/keycloak common/carf-shared
```

### styles

Lista arquivos CSS carregados na página. Ordem importa - CSS posterior sobrescreve anterior.

```properties
# Único arquivo
styles=css/login.css

# Múltiplos arquivos em ordem
styles=css/base.css css/login.css css/custom.css

# Com path do parent
styles=css/login.css lib/patternfly/patternfly.min.css
```

### scripts

Lista arquivos JavaScript carregados na página.

```properties
# Único script
scripts=js/login.js

# Múltiplos scripts
scripts=js/utils.js js/validation.js js/login.js
```

### locales

Define idiomas suportados. Primeiro é o default se `defaultLocale` não especificado.

```properties
# Português Brasil como padrão, inglês como fallback
locales=pt-BR,en

# Múltiplos idiomas
locales=pt-BR,en,es
```

**Arquivos de mensagens correspondentes:**
```
messages/
├── messages_pt_BR.properties
├── messages_en.properties
└── messages_es.properties
```

## Propriedades de Cache

### cacheThemes

Habilita cache de templates compilados. Desabilitar em desenvolvimento.

```properties
# Produção (default true)
cacheThemes=true

# Desenvolvimento
cacheThemes=false
```

### cacheTemplates

Habilita cache de templates FreeMarker.

```properties
# Produção
cacheTemplates=true

# Desenvolvimento
cacheTemplates=false
```

## Propriedades de Layout

### kcHtmlClass

Classes CSS adicionadas ao elemento `<html>`.

```properties
kcHtmlClass=login-pf
```

**Uso no template:**
```ftl
<html class="${properties.kcHtmlClass!}">
```

### kcBodyClass

Classes CSS adicionadas ao elemento `<body>`.

```properties
kcBodyClass=login-pf-page
```

### kcHeaderClass

Classes para container do header.

```properties
kcHeaderClass=login-pf-page-header
```

### kcFormClass

Classes para o formulário principal.

```properties
kcFormClass=login-pf-form
```

### kcInputClass

Classes para campos de input.

```properties
kcInputClass=pf-c-form-control
```

### kcButtonClass

Classes para botões.

```properties
kcButtonClass=pf-c-button pf-m-primary pf-m-block
```

## Propriedades Customizadas

Propriedades customizadas ficam acessíveis em templates via `${properties.nomePropriedade}`.

```properties
# Definir propriedades customizadas
logoUrl=img/logo.svg
primaryColor=#2C5F2D
supportEmail=suporte@carf.gov.br
showSocialLogin=true
```

**Uso no template:**
```ftl
<img src="${url.resourcesPath}/${properties.logoUrl}" alt="Logo">

<#if properties.showSocialLogin?? && properties.showSocialLogin == "true">
  <div class="social-login">...</div>
</#if>

<p>Contato: ${properties.supportEmail}</p>
```

## Propriedades de Meta Tags

### meta

Define meta tags adicionais na página.

```properties
# Viewport para responsividade
meta=viewport==width=device-width,initial-scale=1

# Múltiplas meta tags
meta=viewport==width=device-width,initial-scale=1 robots==noindex,nofollow
```

**Resultado HTML:**
```html
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
```

## Propriedades de Favicon

### favicon

Path para favicon.

```properties
favicon=img/favicon.ico
```

**Uso no template:**
```ftl
<link rel="icon" href="${url.resourcesPath}/${properties.favicon}">
```

## Exemplo Completo - Login Theme

```properties
# themes/carf/login/theme.properties

# Herança
parent=keycloak.v2
import=common/keycloak

# Recursos
styles=css/login.css
scripts=js/cpf-mask.js js/login.js

# Internacionalização
locales=pt-BR,en

# Layout classes
kcHtmlClass=carf-login
kcBodyClass=carf-login-body
kcFormClass=carf-form
kcInputClass=carf-input
kcButtonClass=carf-button carf-button-primary

# Meta tags
meta=viewport==width=device-width,initial-scale=1 robots==noindex,nofollow

# Favicon
favicon=img/favicon.ico

# Propriedades customizadas CARF
logoUrl=img/logo-carf.svg
logoAlt=Sistema CARF
brandTitle=Sistema CARF
brandSubtitle=Regularização Fundiária Urbana
primaryColor=#2C5F2D
secondaryColor=#97BC62
showRememberMe=true
showForgotPassword=true
showRegistration=true
supportEmail=suporte@carf.gov.br
supportPhone=(XX) XXXX-XXXX
footerText=© 2026 CARF - Todos os direitos reservados
showLgpdBanner=true

# Cache (desenvolvimento)
# cacheThemes=false
# cacheTemplates=false
```

## Exemplo Completo - Email Theme

```properties
# themes/carf/email/theme.properties

parent=keycloak.v2
import=common/keycloak

locales=pt-BR,en

# Propriedades customizadas para emails
logoUrl=https://carf.gov.br/images/logo.png
primaryColor=#2C5F2D
footerText=Sistema CARF - Regularização Fundiária Urbana
supportEmail=suporte@carf.gov.br
```

## Acessando Properties em Templates

### Acesso Direto

```ftl
<#-- Acesso com fallback -->
${properties.brandTitle!"Default Title"}

<#-- Verificação de existência -->
<#if properties.showLgpdBanner?? && properties.showLgpdBanner == "true">
  <div class="lgpd-banner">...</div>
</#if>
```

### Iteração sobre Properties

```ftl
<#-- Listar todas styles -->
<#if properties.styles?has_content>
  <#list properties.styles?split(' ') as style>
    <link href="${url.resourcesPath}/${style}" rel="stylesheet">
  </#list>
</#if>
```

### Properties em CSS Inline

```ftl
<style>
  :root {
    --primary-color: ${properties.primaryColor!"#2C5F2D"};
    --secondary-color: ${properties.secondaryColor!"#97BC62"};
  }
</style>
```

## Variáveis de Ambiente

Properties podem ser sobrescritas via variáveis de ambiente (útil para diferentes ambientes).

```bash
# docker-compose.yml
environment:
  KC_SPI_THEME_DEFAULT_LOGIN: carf
  KC_SPI_THEME_CARF_LOGIN_LOGO_URL: img/logo-dev.svg
```

## Keycloakify

Em projetos Keycloakify, `theme.properties` é gerado automaticamente pelo build. Configurações são definidas em `keycloakify.config.ts`.

```ts
// keycloakify.config.ts
export default {
  themeNames: ['carf'],
  extraThemeProperties: [
    'logoUrl=img/logo.svg',
    'primaryColor=#2C5F2D',
  ],
}
```

Ver [04-keycloakify-api](./04-keycloakify-api.md) para detalhes.

## Referencias

- [Keycloak Theme Properties](https://keycloak.org/docs/latest/server_development/#theme-properties)
- [04-keycloakify-api](./04-keycloakify-api.md) - API Keycloakify
- [01-keycloak-themes](../CONCEPTS/01-keycloak-themes.md) - Conceitos de temas
