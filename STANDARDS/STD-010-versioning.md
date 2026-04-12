---
type: standard
status: current
updated: 2026-01-22
---

# STD-010: Versionamento Semantico

## Regra

Todos os projetos CARF devem usar Semantic Versioning no formato MAJOR.MINOR.PATCH. Incrementar MAJOR para mudancas incompativeis, MINOR para funcionalidades novas compativeis, PATCH para correcoes de bugs. Tags Git devem seguir o padrao vX.Y.Z. Cada release deve documentar versoes compativeis de projetos dependentes.

## Justificativa

Versionamento semantico comunica claramente o impacto de cada release para consumidores da API e bibliotecas compartilhadas. Padronizacao entre repositorios permite automacao de updates e facilita coordenacao polyrepo.

## Aplicacao

Aplica-se a todos os repositorios de codigo do ecossistema CARF. Bibliotecas compartilhadas como tscore requerem atencao especial pois MAJOR bumps impactam multiplos projetos consumidores. Releases de API devem considerar contratos com clientes mobile e web.
