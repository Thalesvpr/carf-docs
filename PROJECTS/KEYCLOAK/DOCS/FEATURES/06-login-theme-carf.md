---
type: leaf
status: review
updated: 2026-02-08
---

# Login Theme CARF

Tema de login FreeMarker com layout split-screen, validacao CPF client-side e internacionalizacao pt-BR/en. Deployado em /opt/keycloak/themes/carf/login/ via imagem Docker customizada. Herda de keycloak base via theme.properties.

## Layout Split-Screen

Dois paineis: esquerdo (42%, fundo verde #2C5F2D, logo CARF, tagline "Sistema de Regularizacao Fundiaria Urbana") e direito (58%, formulario login fundo branco). Tablets ajustam para 38/62. Mobile abaixo de 768px empilha verticalmente com painel verde colapsando em header compacto.

## Paginas

| Pagina | Template | Descricao |
|:-------|:---------|:----------|
| Login | login.ftl | CPF/email + senha, checkbox lembrar-me, link "esqueceu senha?" |
| Register | register.ftl | Campos nome, sobrenome, CPF, telefone, email, senha |
| Reset Password | login-reset-password.ftl | Campo email para envio de link de recuperacao |
| Error | error.ftl | Mensagem de erro amigavel em portugues |
| Info | info.ftl | Mensagem informativa (ex: email enviado) |
| Base Layout | template.ftl | Estrutura split-screen compartilhada por todas as paginas |

## Validacao CPF

Campo CPF recebe mascara automatica XXX.XXX.XXX-XX durante digitacao via login.js. No evento blur, validacao Mod11 dos dois digitos verificadores com feedback visual inline (borda vermelha e mensagem de erro se invalido). Implementado em window.CarfValidations carregado via carf-validations.js (bundle minificado).

## Paleta de Cores

| Variable CSS | Valor | Uso |
|:-------------|:------|:----|
| --carf-primary | #2C5F2D | Painel esquerdo, botoes, links |
| --carf-primary-dark | #1a3d1b | Hover em botoes |
| --carf-secondary | #97BC62 | Gradiente header email |
| --carf-error | #dc2626 | Alertas de erro, validacao CPF |

## Internacionalizacao

| Chave | Portugues | Ingles |
|:------|:----------|:-------|
| loginAccountTitle | Entrar no Sistema CARF | Sign in to CARF |
| usernameOrEmail | CPF ou E-mail | CPF or Email |
| password | Senha | Password |
| doLogIn | Entrar | Sign In |
| forgotPassword | Esqueceu a senha? | Forgot password? |
| noAccount | Nao tem conta? | No account? |
| register | Criar conta | Create account |
| invalidCpf | CPF invalido | Invalid CPF |

## Migracao Planejada

O ADR-001 decidiu migrar este tema de FreeMarker para Keycloakify (React 18, TypeScript, @carf/ui, Tailwind) para reutilizar componentes da biblioteca @carf/ui e eliminar duplicacao de estilos. A migracao ainda nao foi implementada. O tema FreeMarker descrito aqui e a implementacao atual em producao. Ver [ADR-001](../ADRs/ADR-001-keycloakify-adoption.md).
