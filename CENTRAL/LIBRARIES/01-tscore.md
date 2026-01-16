# @carf/tscore

Biblioteca core TypeScript fornecendo a camada base de validações, types e autenticação compartilhada entre todos os frontends do ecossistema CARF.

## Conteúdo

Value Objects implementam validações de domínio brasileiro incluindo CPF com dígitos verificadores, CNPJ com validação completa, Email com regex RFC 5322 e PhoneNumber com formato brasileiro. Types TypeScript são sincronizados com as entidades do backend .NET garantindo type-safety end-to-end entre frontend e API.

Hooks React de autenticação encapsulam integração com Keycloak oferecendo useAuth para estado de sessão, useUser para dados do usuário logado, usePermissions para verificação de roles e useToken para acesso ao JWT. Composables Vue 3 equivalentes permitem uso da biblioteca em aplicações VitePress como WEBDOCS.

Cliente Keycloak OAuth2/OIDC implementa fluxos Authorization Code com PKCE para SPAs e mobile, refresh token automático com renovação silenciosa, logout com revogação de tokens e detecção de sessão expirada com redirect para login.

## Instalação

Executar comando bun add @carf/tscore no projeto consumidor configurando .npmrc com registry @carf apontando para https://npm.pkg.github.com com GITHUB_TOKEN para autenticação no GitHub Packages.

## Documentação Técnica

Documentação de implementação disponível em PROJECTS/LIB/TS/TSCORE/DOCS/ contendo API reference, guias de uso e exemplos de integração.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
