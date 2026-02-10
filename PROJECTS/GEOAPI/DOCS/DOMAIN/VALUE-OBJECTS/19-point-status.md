---
type: leaf
status: rejected
updated: 2026-02-08
description: Valores divergem do ARCHITECTURE/LAYERS/DOMAIN/VALUE-OBJECTS/STATUS/14-point-status.md que lista COLLECTED, PROCESSED, APPROVED, REJECTED (sem PROCESSING). Necessario alinhar.
---

# PointStatus

Value object enum imutavel representando o estado de processamento de um ponto topografico (SurveyPoint). Indica se o ponto foi coletado, processado e aprovado para uso em memoriais e plantas.

## Valores Permitidos

| Valor | Descricao |
|-------|-----------|
| COLLECTED | Coletado em campo. Coordenadas brutas sem pos-processamento. |
| PROCESSING | Em processamento diferencial usando dados de estacao base ou RBMC. |
| PROCESSED | Processamento concluido. Coordenadas ajustadas disponiveis. |
| APPROVED | Aprovado para uso em memoriais descritivos e plantas tecnicas. |
| REJECTED | Rejeitado por erro de coleta ou precisao insuficiente. Requer nova coleta. |

Somente pontos com status APPROVED podem ser utilizados para gerar DescriptiveMemorial e LegitimationPlan.
