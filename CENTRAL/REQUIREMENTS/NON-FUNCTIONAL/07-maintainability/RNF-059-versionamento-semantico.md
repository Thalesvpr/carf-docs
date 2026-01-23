---
id: RNF-059
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-059: Versionamento Semantico

## Descricao

Releases seguem SemVer (x.y.z): MAJOR para breaking changes, MINOR para novas funcionalidades compativeis, PATCH para correcoes. CHANGELOG documentado por versao.

## Metricas

- MAJOR (x): breaking changes
- MINOR (y): novas funcionalidades compativeis
- PATCH (z): correcoes de bugs e seguranca

## Criterios de Aceitacao

1. Todas as releases seguem formato x.y.z
2. CHANGELOG atualizado com Added, Changed, Deprecated, Removed, Fixed, Security
3. Consumidores de API podem planejar atualizacoes baseado em versao
