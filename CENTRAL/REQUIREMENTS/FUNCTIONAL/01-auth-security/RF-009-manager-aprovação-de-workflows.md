---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
  - REURBWEB
---

# RF-009: MANAGER - Aprovacao de Workflows

## Descricao

Usuarios com role MANAGER possuem responsabilidade de aprovar ou rejeitar unidades e processos de legitimacao submetidos para revisao. Podem aprovar unidades transitando status de PENDING_ANALYSIS para APPROVED, rejeitar com justificativa ou solicitar alteracoes retornando para REQUIRES_CHANGES. Acesso a relatorios gerenciais e metricas de produtividade da equipe.

## Criterios de Aceitacao

1. MANAGER aprova ou rejeita unidades em analise
2. Rejeicao exige justificativa obrigatoria
3. Pode solicitar alteracoes com comentarios especificos
4. Visualiza metricas de produtividade da equipe
5. Aprovacao em lote disponivel para eficiencia

## Rastreabilidade

- Modulos: GEOAPI, REURBWEB
- Requisitos dependentes: RF-006
