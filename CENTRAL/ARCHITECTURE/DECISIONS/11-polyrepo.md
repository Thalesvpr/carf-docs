---
type: adr
status: approved
updated: 2026-01-24
---

# ADR-011: Arquitetura Polyrepo

## Contexto

O CARF consiste em sete projetos distintos com tecnologias diferentes: backend .NET, frontend React, mobile React Native, plugin QGIS Python, e portal VitePress. Cada projeto tem ciclo de release independente e equipe responsavel distinta. Mudancas em um projeto raramente exigem alteracoes simultaneas em outros.

## Decisao

Adotamos arquitetura polyrepo com um repositorio Git separado para cada projeto. Cada repositorio tem ownership claro por uma equipe especifica com autonomia sobre decisoes tecnicas. Deploys sao independentes, permitindo hotfix no backend sem rebuild do frontend. CI/CD executa apenas no repositorio modificado, reduzindo tempo e custo de builds.

## Consequencias

Onboarding e focado pois desenvolvedores frontend clonam apenas o repositorio web sem carregar codigo backend ou mobile. Permissoes de acesso sao granulares por repositorio. A coordenacao de releases entre projetos requer comunicacao explicita e matriz de compatibilidade documentada. Codigo compartilhado entre projetos TypeScript exige biblioteca publicada como pacote NPM.

## Alternativas Rejeitadas

Monorepo foi descartado porque a diversidade tecnologica dos projetos eliminaria beneficios de tooling unificado. Nx e Turborepo focam em ecossistemas JavaScript, nao suportando .NET e Python no mesmo workspace. O overhead de builds completos a cada commit seria excessivo dado que alteracoes sao tipicamente isoladas em um projeto.
