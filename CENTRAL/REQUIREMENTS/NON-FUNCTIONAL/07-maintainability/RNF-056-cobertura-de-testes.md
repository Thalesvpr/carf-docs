---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-056: Cobertura de Testes

## Descricao

Cobertura minima de 80% em testes automatizados. Testes unitarios para metodos isolados, integracao para fluxos entre camadas, E2E para happy paths completos.

## Metricas

- Cobertura: >= 80% de linhas de codigo
- Unitarios: metodos, funcoes e componentes isolados
- E2E: caminhos principais de uso

## Criterios de Aceitacao

1. Relatorios de coverage gerados no pipeline CI
2. Testes de integracao cobrem comunicacao entre camadas
3. E2E valida fluxos completos desde interface ate persistencia
