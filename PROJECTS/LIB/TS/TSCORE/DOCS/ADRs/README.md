---
type: readme
status: review
updated: 2026-01-24
---

# Decisoes Arquiteturais

Registro de ADRs que fundamentam decisoes tecnicas da biblioteca @carf/tscore.

A [ADR-001](./ADR-001-shared-library-tscore.md) define a criacao de @carf/tscore como biblioteca compartilhada publicada no GitHub Packages. Rejeitou alternativas como monorepo Turborepo/Nx por complexidade de setup, Git Submodules por dificuldade de versionamento e duplicacao de codigo por risco de inconsistencia. A decisao estabelece value objects imutaveis com validacao no construtor, peer dependencies opcionais para React/Vue e subpath exports para tree-shaking.

A [ADR-002](./ADR-002-auth-storage-abstraction.md) estabelece abstracao de storage e navegacao para suporte cross-platform. KeycloakClient original dependia de localStorage e window.location, APIs exclusivas de browser. A decisao introduz interfaces StorageAdapter e NavigationAdapter injetadas no construtor, permitindo adapters especificos para web usando localStorage e para mobile usando expo-secure-store. Esta abordagem compartilha logica OAuth2 PKCE entre plataformas enquanto permite implementacoes de storage seguro nativas.

Novas decisoes arquiteturais que impactam a biblioteca devem ser registradas como ADRs seguindo template padrao com secoes Contexto, Decisao, Consequencias e Alternativas Rejeitadas.

<!-- CARF-INDEX-START -->
<!-- CARF-INDEX-END -->
