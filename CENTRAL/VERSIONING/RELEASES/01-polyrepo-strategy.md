---
status: rejected
description: "Conteudo operacional. Git workflows pertencem a .github ou CONTRIBUTING."
updated: 2026-01-20
---

# Estratégia Polyrepo

Arquitetura polyrepo do CARF com repositórios Git independentes permitindo deploy, versionamento e ownership separados por equipe especializada. A lista completa de repositórios está documentada em 04-repository-catalog.md.

## Justificativa

A escolha por polyrepo ao invés de monorepo foi motivada por necessidades específicas do projeto. Deploys independentes permitem hotfix no backend sem rebuild do frontend reduzindo tempo de resposta a incidentes. Ownership claro atribui cada repositório a uma equipe específica com autonomia sobre decisões técnicas e priorização. CI/CD otimizado executa pipelines apenas no repositório modificado reduzindo tempo e custo de builds. Onboarding focado permite que desenvolvedor frontend clone apenas carf-geoweb sem carregar código backend ou mobile. Controle de acesso granular configura permissões específicas por repositório no GitHub. Histórico limpo mantém commits organizados por contexto de negócio facilitando debugging e auditoria.

## Desvantagens e Mitigações

Coordenação de releases é mais complexa com múltiplos repositórios. A mitigação é usar matriz de compatibilidade documentando combinações testadas e processo de release coordenado. Code sharing entre projetos TypeScript requer biblioteca compartilhada. A mitigação é publicar @carf/tscore como NPM package consumido por frontends. Dependency hell entre repositórios pode causar incompatibilidades. A mitigação é adotar versionamento semântico estrito com Dependabot para updates automáticos. Mudanças cross-repo são mais difíceis de coordenar. A mitigação é usar PRs coordenados referenciando uns aos outros e feature flags para rollout gradual.

## Estrutura de Diretórios

Cada repositório de código é clonado na pasta SRC-CODE correspondente dentro de PROJECTS/ no repositório carf-docs. Esta estrutura mantém documentação em carf-docs como fonte única de verdade enquanto código de implementação fica em repositórios separados. Pastas SRC-CODE estão no .gitignore do carf-docs evitando conflitos entre repositórios aninhados e permitindo que cada desenvolvedor clone apenas os projetos necessários.

## Workflow de Trabalho

Para atualizar documentação, criar branch no carf-docs, editar arquivos em CENTRAL/ ou PROJECTS/, commitar e criar PR. Para desenvolver feature em projeto específico, entrar na pasta SRC-CODE do projeto, criar branch, desenvolver, commitar e criar PR no repositório do projeto. Para mudanças cross-repo que afetam backend e frontend, implementar backend primeiro criando PR, depois implementar frontend criando PR que referencia o PR do backend no body indicando dependência.

## Sincronização

Para manter todos os repositórios atualizados, executar git pull na raiz do carf-docs seguido por git pull em cada pasta SRC-CODE de projetos clonados. Script de automação pode iterar sobre diretórios PROJECTS/*/SRC-CODE/ executando pull em cada um.

## Evolução Futura

Se o projeto crescer significativamente com mais equipes e interdependências frequentes entre repositórios, considerar migração para monorepo com tooling como Nx ou Turborepo. A decisão deve ser reavaliada quando overhead de coordenação superar benefícios de isolamento.
