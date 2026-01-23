---
type: adr
status: current
updated: 2026-01-22
---

# ADR-010: GitHub como Plataforma de Hospedagem

## Contexto

O CARF requer uma plataforma para hospedar repositorios Git que ofereca colaboracao via pull requests, revisao de codigo, e integracao com pipelines de CI/CD. A equipe e pequena e nao possui recursos para manter infraestrutura propria de hospedagem. O orcamento e limitado, exigindo solucao com tier gratuito ou baixo custo.

## Decisao

Adotamos GitHub como plataforma de hospedagem de codigo. GitHub oferece interface intuitiva que reduz fricao no onboarding de novos desenvolvedores. O GitHub Actions fornece CI/CD integrado com minutos gratuitos suficientes para o volume atual. Features de seguranca como Dependabot e CodeQL estao incluidas sem custo adicional para repositorios privados.

## Consequencias

A equipe utiliza uma unica plataforma para codigo, issues, CI/CD e documentacao tecnica. Dependabot atualiza dependencias vulneraveis automaticamente. A familiaridade dos desenvolvedores com GitHub acelera produtividade desde o primeiro dia. Existe dependencia de servico externo, mas mitigada pela natureza distribuida do Git que mantem historico local.

## Alternativas Rejeitadas

GitLab self-hosted foi descartado por exigir equipe DevOps dedicada para manutencao, backups e atualizacoes de seguranca. Bitbucket oferece integracao com Jira mas possui CI/CD mais limitado e comunidade menor. Azure Repos criaria lock-in no ecossistema Microsoft sem beneficios claros dado que o backend utiliza .NET mas frontends sao React e React Native.
