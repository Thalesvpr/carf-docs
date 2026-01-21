---
status: rejected
updated: 2026-01-21
description: "Formato incorreto. Tem secao Implementacao com codigo TSX, estrutura de projeto, comandos bash. ADR valido mas remover implementacao."
---

# ADR-024: Adoção de Keycloakify para Temas Keycloak

## Contexto

O sistema CARF requer customização visual completa das interfaces de autenticação Keycloak, incluindo login, registro, recuperação de senha, e account console. A abordagem tradicional utiliza templates FreeMarker com HTML/CSS/JavaScript vanilla, enquanto Keycloakify oferece desenvolvimento de temas usando React e TypeScript com componentes reutilizáveis.

O projeto possui uma biblioteca de componentes `@carf/ui` construída sobre React, Radix UI e Tailwind CSS, utilizada em GEOWEB, ADMIN e WebDocs. Manter consistência visual entre aplicações e telas de autenticação é requisito de design system. Atualmente existe implementação FreeMarker em `carf-keycloak-theme` funcional porém com duplicação de estilos e lógica de validação CPF que já existem em `@carf/ui`.

## Decisão

Adotar **Keycloakify** como ferramenta padrão para desenvolvimento de novos temas Keycloak no projeto CARF.

### Justificativa Técnica

| Critério | FreeMarker Tradicional | Keycloakify |
|:---------|:-----------------------|:------------|
| Linguagem | FTL + JS vanilla | TypeScript + React |
| Reutilização @carf/ui | Impossível | Direta (import) |
| Type Safety | Nenhuma | Completa |
| Validações client-side | Reimplementar JS | Reutilizar hooks existentes |
| Testes | Difícil (E2E only) | Unit + Integration + E2E |
| Hot Reload | Parcial (CSS/JS) | Completo (Vite) |
| Bundle Size | Menor (~50KB) | Maior (~150KB gzip) |
| Complexidade Build | Baixa | Média (Keycloakify CLI) |

### Escopo de Aplicação

**Aplicações que usarão @carf/ui via Keycloakify:**
- GEOWEB (Next.js)
- ADMIN (React + Vite)
- WebDocs (Astro + Starlight)
- Keycloak Login Theme (Keycloakify)

**Fora do escopo:**
- REURBCAD (React Native - design system mobile separado)

## Consequências

### Positivas

**Reutilização de código**: Componentes `Button`, `Input`, `FormField`, `Alert` de `@carf/ui` podem ser importados diretamente no tema Keycloakify, eliminando duplicação de estilos e comportamentos.

**Consistência visual**: Telas de login utilizam exatamente os mesmos componentes que o restante do sistema, garantindo que mudanças no design system propaguem automaticamente para autenticação.

**Developer experience**: Desenvolvedores trabalham com stack familiar (React + TypeScript + Vite), com autocomplete, type checking e hot reload completo durante desenvolvimento.

**Testabilidade**: Páginas de login podem ser testadas com Testing Library da mesma forma que componentes regulares, além de testes E2E com Playwright.

**Manutenibilidade**: Código TypeScript é mais fácil de refatorar e manter que templates FreeMarker com JavaScript inline.

### Negativas

**Build step adicional**: Keycloakify CLI precisa compilar o projeto React em artefatos FreeMarker compatíveis com Keycloak, adicionando complexidade ao pipeline de CI/CD.

**Bundle size maior**: Incluir React e componentes aumenta o tamanho do tema de ~50KB para ~150KB (gzip), impactando marginalmente o tempo de carregamento inicial.

**Curva de aprendizado**: Desenvolvedores precisam entender KcContext, hooks específicos do Keycloakify e como o build funciona.

**Compatibilidade**: Major updates do Keycloak podem exigir atualizações no Keycloakify, introduzindo delay na adoção de novas versões.

### Neutras

**Documentação FreeMarker existente**: Permanece válida como referência de como temas funcionam internamente e para troubleshooting, porém marcada como legacy para novos desenvolvimentos.

## Implementação

### Estrutura do Projeto

```
PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak-theme/
├── src/
│   ├── login/                    # Páginas de login
│   │   ├── KcApp.tsx            # Entry point
│   │   ├── pages/
│   │   │   ├── Login.tsx        # Usa @carf/ui Button, Input
│   │   │   ├── Register.tsx
│   │   │   └── ResetPassword.tsx
│   │   └── i18n.ts              # Traduções PT-BR
│   └── account/                  # Account console (futuro)
├── package.json                  # Deps: keycloakify, @carf/ui
├── vite.config.ts               # Build config
└── keycloakify.config.ts        # Keycloakify options
```

### Comandos de Build

```bash
# Desenvolvimento
bun run dev                      # Storybook local

# Build tema
bun run build-keycloak-theme     # Gera .jar deployável

# Deploy
docker build -t carf-keycloak .  # Imagem com tema embutido
```

### Integração @carf/ui

```tsx
// src/login/pages/Login.tsx
import { Button, Input, FormField, Alert } from '@carf/ui'
import { useCpfMask } from '@carf/ui/hooks'
import type { KcContext } from '../kcContext'

export function Login({ kcContext }: { kcContext: KcContext }) {
  const { url, realm, login, message } = kcContext
  const { maskedValue, handleChange } = useCpfMask()

  return (
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
      <Button type="submit" className="w-full">Entrar</Button>
    </form>
  )
}
```

## Alternativas Rejeitadas

### 1. Manter FreeMarker Puro

**Motivo da rejeição**: Impossibilita reutilização de `@carf/ui`, forçando manutenção duplicada de estilos e componentes. Lógica de validação CPF já implementada em React precisaria ser reimplementada em JavaScript vanilla.

### 2. Web Components

**Motivo da rejeição**: Adiciona complexidade de compilar `@carf/ui` para Web Components sem ganho significativo. Keycloakify já resolve o problema de forma mais elegante e mantida pela comunidade.

### 3. Iframe Embedding

**Motivo da rejeição**: Incorporar app React via iframe em páginas Keycloak introduz problemas de UX (loading, scroll, responsive) e segurança (CSP, cross-origin).

## Métricas de Sucesso

- [ ] Tema Keycloakify deployado em homologação até Q1/2026
- [ ] Zero duplicação de componentes UI entre @carf/ui e tema Keycloak
- [ ] Cobertura de testes >80% nas páginas de login
- [ ] Lighthouse Performance Score >90 na página de login

## Referências

- [Keycloakify Documentation](https://keycloakify.dev)
- [ADR-014: shadcn/ui Component Library](./ADR-014-shadcn-ui-component-library.md)
- [ADR-003: Keycloak Autenticação](./ADR-003-keycloak-autenticacao.md)
- [@carf/ui Architecture](../../../PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/ARCHITECTURE/README.md)
- [Keycloak Theme SPI](https://keycloak.org/docs/latest/server_development/#_themes)
