---
status: rejected
description: "Conteudo operacional. Git workflows pertencem a .github ou CONTRIBUTING."
updated: 2026-01-20
---

# Configurações de Repositório

Configurações padronizadas para repositórios GitHub do CARF garantindo consistência, segurança e experiência uniforme de desenvolvimento em todos os projetos.

## Settings Gerais

Todos os repositórios devem seguir configurações padronizadas. O campo Description deve conter descrição concisa do propósito do repositório em português. Website deve apontar para documentação relevante quando aplicável. Topics devem incluir tags como carf, regularizacao-fundiaria e stack específica. Visibility é Private para todos os repositórios de código e documentação.

## Features Habilitadas

Issues devem estar habilitadas para tracking de bugs e features. Projects devem estar habilitados para gestão de sprints quando o time utilizar. Wiki deve estar desabilitada pois documentação fica em carf-docs. Discussions devem estar desabilitadas pois comunicação acontece em canais externos. Preserve this repository deve estar habilitado para repositórios críticos.

## Merge Options

Allow merge commits deve estar desabilitado para manter histórico linear. Allow squash merging deve estar habilitado como opção padrão. Allow rebase merging deve estar habilitado como alternativa. Default commit message deve ser Pull request title para squash commits. Automatically delete head branches deve estar habilitado para limpeza automática após merge.

## Pull Requests

Allow auto-merge deve estar habilitado permitindo merge automático quando checks passam. Require approval of the most recent reviewable push deve estar habilitado invalidando approvals quando novos commits são adicionados. Always suggest updating pull request branches deve estar habilitado para manter PRs atualizados.

## Configuração via CLI

Para configurar repository settings usar gh api repos/OWNER/REPO com método PATCH passando JSON com configurações desejadas. Para listar settings atuais usar gh repo view REPO --json name,description,visibility,isTemplate.

## Template de Repositório

Ao criar novo repositório CARF, usar carf-docs como referência para estrutura de diretórios. Incluir arquivos README.md, LICENSE, .gitignore apropriado para stack e .github/ com templates de PR e issue.
