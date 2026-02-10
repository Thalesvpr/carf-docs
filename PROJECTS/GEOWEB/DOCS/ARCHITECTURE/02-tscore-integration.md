---
type: leaf
status: review
updated: 2026-02-07
---

# Integracao @carf/tscore no GEOWEB

Esta documentacao descreve como GEOWEB utiliza @carf/tscore para autenticacao, validacoes e types compartilhados. A biblioteca e instalada como dependencia NPM via GitHub Packages.

## Autenticacao Keycloak

GEOWEB utiliza @carf/tscore/auth/react para integracao com Keycloak. No ponto de entrada da aplicacao, uma instancia de KeycloakClient e criada com URL, realm carf e clientId geoweb. O AuthProvider envolve a arvore de componentes disponibilizando contexto de autenticacao. O hook useAuth fornece acesso ao usuario, funcao hasRole e logout. O componente ProtectedRoute protege rotas exigindo autenticacao ou roles especificas.

## Validacoes e Types

GEOWEB utiliza value objects de @carf/tscore/validations nos formularios, integrando com React Hook Form e Zod para validar CPF, CNPJ, Email e Phone. Types de dominio como Unit, Holder e Community sao importados de @carf/tscore/types para sincronia com backend, usados em queries e mutations do TanStack Query. Type guards permitem narrowing seguro de tipos.

## API Client

GEOWEB configura interceptors Axios via @carf/tscore. O request interceptor adiciona Authorization Bearer automaticamente. O response interceptor redireciona para login quando recebe status 401.

## Value Objects

| Value Object | Validacao | Formatacao |
|-------------|-----------|------------|
| CPF | Digitos verificadores e sequencias invalidas | 000.000.000-00 |
| CNPJ | Digitos verificadores | 00.000.000/0000-00 |
| Email | Formato RFC 5322 | Lowercase normalizado |
| Phone | Formato brasileiro com DDD | (00) 00000-0000 |

## Beneficios e Atualizacoes

A adocao garante type safety em compile-time, validacoes consistentes em toda a aplicacao e reducao de bugs por sincronia de interfaces. Para atualizacoes minor, executar update via bun e reiniciar o dev server. Para major, consultar CHANGELOG, verificar migration guide e testar antes do deploy. O pacote adiciona aproximadamente 50KB ao bundle, otimizavel via imports especificos para tree-shaking.
