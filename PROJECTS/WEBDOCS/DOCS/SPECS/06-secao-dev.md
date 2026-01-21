---
status: review
updated: 2026-01-21
---

# Seção Dev

Seção /dev/ contém documentação técnica interna acessível apenas para usuários com role dev. Protegida por autenticação Keycloak com verificação de role em middleware SSR.

Estrutura de pastas em src/content/docs/dev/ organiza por tema: get-started/ para setup inicial, arquitetura/ para visão técnica, swagger/ para documentação interativa da API, contribuindo/ para git workflow, e debug/ para logs e troubleshooting.

Conteúdo de get-started inclui requisitos de ambiente (Node, Bun, Docker), clone e setup do repositório, configuração de variáveis de ambiente, e execução local dos serviços. Objetivo: desenvolvedor novo consegue rodar sistema em máquina local seguindo documentação.

Conteúdo de arquitetura documenta visão técnica do sistema incluindo diagrama de componentes, fluxo de dados entre serviços, padrões de código (Clean Architecture, CQRS), e decisões arquiteturais com links para ADRs em CENTRAL.

Conteúdo de swagger embute Swagger UI interativo consumindo especificação OpenAPI da GEOAPI. Permite testar endpoints com token real do desenvolvedor logado.

Conteúdo de contribuindo documenta git workflow (branching, commits, PRs), padrões de code review, processo de CI/CD, e convenções de código.

Conteúdo de debug orienta troubleshooting com acesso a logs de serviços, métricas de performance, e ferramentas de diagnóstico disponíveis em ambiente de desenvolvimento.

Frontmatter define section como dev, audience como dev, e prerender como false para SSR que permite verificação de role antes de renderizar.
