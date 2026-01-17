# ADR-017: Escolha do GitHub Actions como Plataforma CI/CD

Decisão arquitetural escolhendo GitHub Actions como solução de CI/CD para todos projetos CARF justificada por integração nativa com GitHub eliminando necessidade de autorização/webhook external service, workflow-as-code em YAML versionado no repositório permitindo code review de CI config garantindo auditability, matrix builds executando tests em múltiplas versões Node/Bun/.NET paralelamente detectando incompatibilidades precocemente, artifacts e caching automático acelerando builds em 50-70% reutilizando dependencies entre runs, secrets management integrado protegendo API keys tokens credentials com encryption at rest, environments com protection rules exigindo approval manual para deploy produção impedindo deploys acidentais, status checks obrigatórios bloqueando merge de PRs com testes falhando garantindo qualidade, scheduled workflows para tasks periódicos (sync docs nightly dependency updates security scans), e custo zero para repositórios públicos ou 2000 minutos grátis privados suficiente para projetos small-medium.

GitHub Actions marketplace fornece actions prontas para setup Node/Bun/Docker, Vercel deploy, Docker build/push, Playwright tests, code coverage, reduzindo boilerplate workflow configs.

Alternativas consideradas incluem GitLab CI (rejeitado por exigir migration de GitHub), CircleCI (rejeitado por custo superior sem benefícios claros), Jenkins (rejeitado por overhead operacional enorme self-hosting), TravisCI (rejeitado por declínio e pricing confusion), e Azure Pipelines (rejeitado por complexity desnecessária para stack JavaScript/.NET simples).

Consequências positivas incluem simplicidade de configuração, custo zero, integração perfeita GitHub, observability built-in, e ecosystem rico de actions. Consequências negativas incluem vendor lock-in GitHub, debugging workflows ocasionalmente complexo, e cold start ocasional de runners adicionando ~1-2min em builds.

Configuração utiliza workflows em `.github/workflows/` executando em `ubuntu-latest` runners, cache de `node_modules` via `actions/cache@v3`, parallel matrix tests, e deploy condicional apenas em branch `main`.

Status aprovado e implementado desde início 2024-Q3.

---

**Data:** 2025-01-10
**Status:** Aprovado e Implementado
**Decisor:** Equipe de Arquitetura + DevOps
**Última revisão:** 2025-01-10
**Última atualização:** 2026-01-15
**Status do arquivo**: Review
