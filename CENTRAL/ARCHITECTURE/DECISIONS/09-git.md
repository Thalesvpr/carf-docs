---
type: adr
status: current
updated: 2026-01-22
---

# ADR-009: Git como Sistema de Controle de Versao

## Contexto

O CARF precisa de um sistema de controle de versao para gerenciar codigo entre multiplas equipes trabalhando em sete repositorios independentes. A equipe trabalha parcialmente remoto e precisa versionar codigo mesmo sem conexao com servidor central. O mercado brasileiro de desenvolvedores possui forte familiaridade com Git, facilitando contratacao e onboarding.

## Decisao

Adotamos Git como sistema de controle de versao distribuido. Git permite commits locais sem dependencia de servidor, essencial para cenarios offline comuns em campo. O modelo de branching leve suporta desenvolvimento paralelo de features sem interferencia. A integracao nativa com GitHub simplifica a infraestrutura de CI/CD e colaboracao.

## Consequencias

Desenvolvedores podem trabalhar offline e sincronizar posteriormente. O historico completo fica replicado em cada maquina, eliminando ponto unico de falha. A curva de aprendizado e menor devido a familiaridade da maioria dos desenvolvedores. Conflitos de merge requerem resolucao manual em cenarios de trabalho paralelo intenso.

## Alternativas Rejeitadas

Subversion foi descartado por ser centralizado, bloqueando commits quando offline e criando dependencia de servidor. Mercurial oferece funcionalidades similares mas possui ecossistema menor e comunidade em declinio no Brasil. Perforce atenderia bem arquivos binarios grandes mas o custo de licenciamento e excessivo para um projeto predominantemente baseado em texto e codigo.
