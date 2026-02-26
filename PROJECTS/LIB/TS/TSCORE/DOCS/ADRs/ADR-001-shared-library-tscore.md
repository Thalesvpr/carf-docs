---
type: adr
status: approved
updated: 2026-01-24
---

# ADR-001: Biblioteca TypeScript Compartilhada

## Contexto

Projetos frontend REURBWEB, ADMIN, WEBDOCS e REURBCAD duplicavam codigo de validacoes brasileiras, tipos de dominio e integracao Keycloak. Inconsistencias entre implementacoes causavam bugs e dificultavam manutencao. Atualizacoes em regras de validacao requeriam modificacoes em multiplos repositorios.

## Decisao

Criar biblioteca @carf/tscore publicada no GitHub Packages como NPM package privado. Centralizar value objects CPF, CNPJ, Email e Phone com validacao no construtor. Compartilhar tipos TypeScript sincronizados com backend .NET. Fornecer KeycloakClient com OAuth2 PKCE e hooks para React e Vue. Usar subpath exports habilitando tree-shaking.

## Consequencias

Manutencao centralizada elimina duplicacao de codigo. Bug fixes propagam automaticamente via atualizacao de versao. Versionamento semantico comunica breaking changes claramente. Type safety end-to-end previne erros de runtime. Overhead de publicacao adiciona latencia durante desenvolvimento, mitigado por npm link local.

## Alternativas Rejeitadas

Duplicar codigo em cada projeto implicaria manutencao insustentavel com risco de inconsistencias. Monorepo com Turborepo ou Nx exigiria migracao complexa e tooling pesado. Git submodules oferece experiencia developer ruim com comandos obscuros e dificuldade de trabalhar em feature branches.
