---
id: RNF-015
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-015: Tamanho do Bundle - Frontend

## Descricao

O bundle inicial do GEOWEB deve ser compacto para garantir carregamento rapido mesmo em conexoes lentas. Tamanho reduzido melhora experiencia especialmente em primeiro acesso.

## Metricas

- Tamanho maximo: <= 500KB (gzip)
- Escopo: bundle inicial (assets criticos para primeira renderizacao)
- Ferramenta de medicao: webpack-bundle-analyzer

## Criterios de Aceitacao

1. Bundle inicial abaixo de 500KB apos compressao gzip
2. Code splitting por rota implementado
3. Tree shaking habilitado no processo de build
