---
type: leaf
status: review
updated: 2026-02-07
---

# Theme Properties - Customizacao e Exemplos

Propriedades customizadas, meta tags e exemplos de temas Keycloak para o sistema CARF.

## Propriedades Customizadas

Acessiveis em templates FreeMarker via properties.nomePropriedade:

| Propriedade | Valor | Descricao |
|:------------|:------|:----------|
| logoUrl | img/logo-carf.svg | Caminho do logo |
| logoAlt | Sistema CARF | Texto alternativo |
| brandTitle | Sistema CARF | Titulo da marca |
| brandSubtitle | Regularizacao Fundiaria Urbana | Subtitulo |
| primaryColor | #2C5F2D | Cor primaria |
| secondaryColor | #97BC62 | Cor secundaria |
| showRememberMe | true | Opcao lembrar-me |
| showForgotPassword | true | Link esqueci senha |
| showRegistration | true | Link de registro |
| supportEmail | suporte@carf.gov.br | Email de suporte |
| footerText | 2026 CARF | Texto do rodape |
| showLgpdBanner | true | Banner LGPD |

## Meta Tags e Favicon

A propriedade meta define tags adicionais no formato chave==valor separados por espaco, como viewport==width=device-width,initial-scale=1 robots==noindex,nofollow. A propriedade favicon define o caminho do icone.

## Tema de Login CARF

Usa parent keycloak.v2, import common/keycloak, css/login.css como estilo, js/cpf-mask.js e js/login.js como scripts. Suporta locales pt-BR e en. Define classes carf-login, carf-login-body, carf-form, carf-input e carf-button para layout. Inclui meta viewport e robots noindex.

## Tema de Email CARF

Herda de keycloak.v2, import common/keycloak, locales pt-BR e en. Define logoUrl, primaryColor, footerText e supportEmail.

## Keycloakify

Em projetos Keycloakify, theme.properties e gerado pelo build. Configuracoes ficam em keycloakify.config.ts com themeNames e extraThemeProperties. Properties podem ser sobrescritas via variaveis de ambiente.

Ver [03-theme-properties](./03-theme-properties.md) para propriedades principais, cache e layout.
