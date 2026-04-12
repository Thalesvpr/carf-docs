---
type: leaf
status: review
updated: 2026-02-07
---

# Theme Properties

O arquivo theme.properties na raiz de cada theme type (login, account, email) configura heranca, recursos e comportamento do tema Keycloak. Cada tipo de tema possui seu proprio theme.properties dentro da estrutura themes/carf/login/, themes/carf/account/ e themes/carf/email/.

## Propriedades Principais

| Propriedade | Descricao | Exemplo |
|:------------|:----------|:--------|
| parent | Tema pai para heranca de recursos nao sobrescritos | keycloak.v2 |
| import | Importa recursos de namespaces compartilhados | common/keycloak |
| styles | Arquivos CSS carregados em ordem (posterior sobrescreve anterior) | css/base.css css/login.css |
| scripts | Arquivos JavaScript carregados na pagina | js/cpf-mask.js js/login.js |
| locales | Idiomas suportados, primeiro e default | pt-BR,en |

Temas disponiveis para heranca sao keycloak (legado), keycloak.v2 (moderno, recomendado) e base (minimo sem estilos). Arquivos de mensagens para internacionalizacao ficam em messages/messages_pt_BR.properties e messages/messages_en.properties.

## Propriedades de Cache

| Propriedade | Descricao | Producao | Desenvolvimento |
|:------------|:----------|:---------|:----------------|
| cacheThemes | Cache de templates compilados | true | false |
| cacheTemplates | Cache de templates FreeMarker | true | false |

## Propriedades de Layout

| Propriedade | Descricao | Exemplo |
|:------------|:----------|:--------|
| kcHtmlClass | Classes CSS no elemento html | login-pf |
| kcBodyClass | Classes CSS no elemento body | login-pf-page |
| kcHeaderClass | Classes no container do header | login-pf-page-header |
| kcFormClass | Classes no formulario principal | login-pf-form |
| kcInputClass | Classes nos campos de input | pf-c-form-control |
| kcButtonClass | Classes nos botoes | pf-c-button pf-m-primary pf-m-block |

Estas propriedades sao acessiveis nos templates FreeMarker via properties.nomePropriedade com fallback opcional.

Ver [03a-theme-properties-custom](./03a-theme-properties-custom.md) para propriedades customizadas, meta tags, favicon e exemplos completos.
