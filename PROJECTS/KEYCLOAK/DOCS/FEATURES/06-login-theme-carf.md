---
status: approved
updated: 2026-01-21
---

# Login Theme CARF

Tema de login Keycloak CARF implementado com **Keycloakify**, utilizando React, TypeScript e componentes @carf/ui. O layout split-screen profissional combina branding institucional com usabilidade otimizada para servidores publicos e cidadaos.

## Stack Tecnologico

| Tecnologia | Uso |
|:-----------|:----|
| Keycloakify | Build de temas React para Keycloak |
| React 18 | Componentes de UI |
| TypeScript | Tipagem estatica |
| @carf/ui | Design System CARF |
| Tailwind CSS | Estilizacao utilitaria |
| Vite | Bundler e dev server |

## Layout Split-Screen

O design segue padroes modernos de autenticacao (Airbnb, TED):

```
+------------------+-------------------------+
|                  |                         |
|  PAINEL VERDE    |    PAINEL BRANCO        |
|  (Branding)      |    (Formulario)         |
|                  |                         |
|  Logo CARF       |    Campos Login         |
|  Subtitulo       |    CPF/Email            |
|                  |    Senha                |
|                  |    [Entrar]             |
|                  |                         |
+------------------+-------------------------+
      42%                    58%
```

### Responsividade

| Breakpoint | Comportamento |
|:-----------|:--------------|
| Desktop (>1024px) | Split horizontal 42%/58% |
| Tablet (768-1024px) | Split horizontal 38%/62% |
| Mobile (<768px) | Stack vertical, branding no topo |

## Integracao @carf/ui

Os componentes do Design System sao usados diretamente:

```tsx
// src/login/pages/Login.tsx
import { Button, Input, FormField, Alert } from '@carf/ui'
import { useCpfMask } from '@carf/ui/hooks'

export function Login({ kcContext }: { kcContext: KcContext }) {
  const { url, realm, login, message } = kcContext
  const { maskedValue, handleChange } = useCpfMask()

  return (
    <div className="login-container">
      <aside className="login-brand">
        <div className="brand-content">
          <h1>CARF</h1>
          <p>Sistema de Regularizacao Fundiaria Urbana</p>
        </div>
      </aside>

      <main className="login-main">
        <form action={url.loginAction} method="post">
          {message && (
            <Alert variant={message.type}>{message.summary}</Alert>
          )}

          <FormField label="CPF ou Email">
            <Input
              name="username"
              value={maskedValue || login.username}
              onChange={handleChange}
              autoFocus
            />
          </FormField>

          <FormField label="Senha">
            <Input name="password" type="password" />
          </FormField>

          <Button type="submit" className="w-full">
            Entrar
          </Button>
        </form>
      </main>
    </div>
  )
}
```

## Paleta de Cores

Cores institucionais definidas via Design System ([ADR-023](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-023-color-palette-design-system.md)):

| Token | Cor | Uso |
|:------|:----|:----|
| `--color-primary` | #2C5F2D | Painel branding, botoes, links |
| `--color-primary-dark` | #1a3d1b | Hover states, gradients |
| `--color-error` | #dc2626 | Alertas de erro |
| `--color-gray-*` | Escala Tailwind | Textos, borders, backgrounds |

## Internacionalizacao

Suporte bilingue PT-BR e EN via sistema i18n do Keycloakify:

```typescript
// src/login/i18n.ts
export const messages = {
  'pt-BR': {
    loginTitle: 'CARF - Login',
    usernameOrEmail: 'CPF ou Email',
    password: 'Senha',
    doLogIn: 'Entrar',
    forgotPassword: 'Esqueceu a senha?',
    noAccount: 'Nao tem uma conta?',
    register: 'Criar conta'
  },
  en: {
    loginTitle: 'CARF - Login',
    usernameOrEmail: 'CPF or Email',
    password: 'Password',
    doLogIn: 'Sign In',
    forgotPassword: 'Forgot password?',
    noAccount: "Don't have an account?",
    register: 'Create account'
  }
}
```

## Validacao CPF Client-Side

Hook `useCpfMask` de @carf/ui aplica mascara automaticamente:

- Detecta 11 digitos e formata como XXX.XXX.XXX-XX
- Valida digitos verificadores
- Feedback visual de erro inline

## Desenvolvimento

```bash
# Iniciar ambiente dev com hot reload
cd PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak-theme
pnpm dev

# Testar com Keycloak real
pnpm dev:keycloak

# Build para producao
pnpm build-keycloak-theme
```

## Deploy

O build gera um JAR em `dist_keycloak/`:

```bash
# Copiar para Keycloak
cp dist_keycloak/keycloak-theme-carf.jar /opt/keycloak/providers/

# Ou via Docker
docker build -t carf-keycloak .
```

Ativar no Admin Console: Realm Settings > Themes > Login Theme: "carf"

## Paginas Implementadas

| Pagina | Arquivo | Status |
|:-------|:--------|:-------|
| Login | Login.tsx | Completo |
| Registro | Register.tsx | Completo |
| Reset Password | ResetPassword.tsx | Completo |
| Verify Email | VerifyEmail.tsx | Completo |
| Error | Error.tsx | Completo |
| Info | Info.tsx | Completo |

## Referencias

- [HOW-TO/01-develop-themes.md](../HOW-TO/01-develop-themes.md) - Guia desenvolvimento Keycloakify
- [CONCEPTS/01-keycloak-themes.md](../CONCEPTS/01-keycloak-themes.md) - Conceitos Keycloakify
- [REFERENCE/04-keycloakify-api.md](../REFERENCE/04-keycloakify-api.md) - API Keycloakify
- [ADR-024](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-024-keycloakify-adoption.md) - Decisao de adocao Keycloakify
- [Keycloakify Docs](https://keycloakify.dev) - Documentacao oficial
