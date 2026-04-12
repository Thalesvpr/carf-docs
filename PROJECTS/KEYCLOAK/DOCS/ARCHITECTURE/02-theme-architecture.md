---
type: leaf
status: review
updated: 2026-02-08
---

# Arquitetura de Temas Keycloak

O tema Keycloak do CARF utiliza templates FreeMarker com CSS customizado, deployado em /opt/keycloak/themes/carf/ na imagem Docker. Tres tipos de tema sao customizados: login (split-screen com branding CARF), account (perfil e sessoes) e email (verificacao e reset de senha). A identidade visual segue a paleta institucional CARF com verde primario #2C5F2D e fonte Inter.

## Implementacao Atual: FreeMarker

O tema reside em PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/themes/carf/ com tres subdiretorios (login, account, email). Cada subdirectorio contem theme.properties definindo parent theme, templates .ftl com HTML customizado, CSS em resources/css/, imagens em resources/img/, e traducoes em messages/.

O tema de login herda de keycloak base e sobreescreve seis templates: login.ftl (formulario CPF/email + senha), template.ftl (layout base split-screen), register.ftl (cadastro com campos CPF e telefone), login-reset-password.ftl (recuperacao de senha), error.ftl (pagina de erro customizada) e info.ftl (pagina informativa). O CSS (login.css, 437 linhas) implementa layout split-screen com painel esquerdo 42% (fundo verde, logo CARF) e painel direito 58% (formulario). Breakpoint em 768px colapsa para stack vertical.

O tema de account herda de keycloak.v2 e customiza account.ftl e password.ftl com CSS proprio (account.css).

O tema de email contem templates HTML e texto puro para email-verification e password-reset, com branding CARF (header verde, logo).

## Validacao CPF Client-Side

O login.js (337 linhas) registra window.CarfValidations com mascara CPF automatica (XXX.XXX.XXX-XX) e validacao Mod11 dos digitos verificadores. O script carf-validations.js e um bundle minificado que complementa as validacoes. Ambos sao carregados via tag script no template.ftl.

## CSS Variables

As cores institucionais sao definidas via CSS custom properties consumidas por todos os templates.

| Variable | Valor | Uso |
|:---------|:------|:----|
| --carf-primary | #2C5F2D | Painel branding, botoes, links |
| --carf-primary-dark | #1a3d1b | Hover states |
| --carf-secondary | #97BC62 | Gradiente header, destaques |
| --carf-accent | #FFB300 | Enfase pontual |
| --carf-error | #dc2626 | Alertas de erro |

Tipografia usa Inter com fallback para Segoe UI e sans-serif. Border-radius padrao 0.5rem.

## Internacionalizacao

Traducoes em messages_pt_BR.properties (334 chaves) como idioma principal e messages_en.properties (40 chaves) como secundario. Realm configurado com internationalizationEnabled: true, supportedLocales: ["pt-BR", "en"], defaultLocale: "pt-BR".

| Chave | Portugues | Ingles |
|:------|:----------|:-------|
| loginAccountTitle | Entrar no Sistema CARF | Sign in to CARF |
| usernameOrEmail | CPF ou E-mail | CPF or Email |
| password | Senha | Password |
| doLogIn | Entrar | Sign In |
| forgotPassword | Esqueceu a senha? | Forgot password? |

## Deploy

O Dockerfile multi-stage copia themes/ para /opt/keycloak/themes/carf/ na imagem customizada baseada em quay.io/keycloak/keycloak:24.0.0. Em desenvolvimento, docker-compose.dev.yml monta themes/ como volume bind com cache de tema desabilitado para hot reload. Em producao, a imagem final e deployada com docker-compose.yml. Ativacao no Admin Console em Realm Settings, Themes, selecionando "carf" para Login, Account e Email.

## Migracao Planejada: Keycloakify

O ADR-001 decidiu migrar de FreeMarker para Keycloakify (React 18, TypeScript, @carf/ui, Tailwind, Vite) para reutilizar diretamente a biblioteca de componentes @carf/ui nas telas de autenticacao, eliminando duplicacao de estilos entre login e aplicacoes web. A migracao ainda nao foi implementada. O tema FreeMarker atual permanece como implementacao de referencia ate que o projeto Keycloakify seja criado. Para detalhes da decisao, ver [ADR-001](../ADRs/ADR-001-keycloakify-adoption.md).
