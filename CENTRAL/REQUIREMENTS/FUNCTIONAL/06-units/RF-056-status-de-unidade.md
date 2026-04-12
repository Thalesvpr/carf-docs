---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-056: Status de Unidade

## Descricao

Sistema deve implementar fluxo de aprovacao de unidades baseado em estados: DRAFT, PENDING_APPROVAL, APPROVED, REJECTED, CHANGES_REQUESTED. Cada status representa uma etapa no processo de validacao e cadastramento. Transicoes entre status seguem regras especificas garantindo que apenas caminhos validos sejam permitidos. Somente usuarios com perfil MANAGER podem executar acoes de aprovar ou rejeitar. Log de auditoria registra automaticamente todas as mudancas de status.

## Criterios de Aceitacao

1. Enum com status de workflow predefinidos
2. Transicoes de status validadas por regras
3. MANAGER pode aprovar e rejeitar
4. Log de auditoria registra mudancas de status
5. Comentarios opcionais em transicoes

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-049, RF-057, RF-058
