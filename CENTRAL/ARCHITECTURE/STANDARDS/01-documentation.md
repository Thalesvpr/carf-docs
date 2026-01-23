---
type: standard
status: current
updated: 2026-01-22
---

# STD-001: Documentacao

## Regra

Todo documento markdown deve seguir template correspondente ao seu tipo definido em .template/. Tipos suportados sao readme, leaf, adr, standard, rf, rnf, uc e us. Frontmatter obrigatorio com type, status e updated. Texto em prosa corrida sem bullets ou tabelas exceto onde template permite.

## Justificativa

Consistencia de formato permite automacao de validacao, geracao de indices e renderizacao no portal WEBDOCS. Prosa densa e mais legivel que listas fragmentadas.

## Aplicacao

Aplica-se a toda documentacao em CENTRAL/ e PROJECTS/*/DOCS/. Arquivos de configuracao, codigo-fonte e assets nao seguem esta regra. Validador automatico rejeita PRs com documentos fora do padrao.
