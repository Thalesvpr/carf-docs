---
type: leaf
status: review
updated: 2026-02-08
---

# PointStatus

Value object enum representando o estado no workflow de processamento de pontos topograficos desde coleta em campo ate aprovacao final para uso em documentos tecnicos de regularizacao. Controla o fluxo de vida de cada ponto geodesico coletado por receptores GPS.

O fluxo segue sequencia linear com possibilidade de rejeicao: COLLECTED -> PROCESSED -> APPROVED ou REJECTED.

## Valores Permitidos

| Valor | Descricao |
| --- | --- |
| COLLECTED | Ponto coletado em campo com coordenadas brutas do receptor GPS, ainda nao processado. |
| PROCESSED | Coordenadas processadas usando estacoes RBMC base com calculo de precisoes. |
| APPROVED | Ponto validado e aprovado para uso em memoriais descritivos e plantas oficiais. |
| REJECTED | Ponto rejeitado por precisao insuficiente, devendo ser recoletado. |

## Transicoes Validas

| De | Para | Condicao |
| --- | --- | --- |
| COLLECTED | PROCESSED | Processamento com correcao diferencial concluido. |
| PROCESSED | APPROVED | Precisao atende requisito do tipo de ponto. |
| PROCESSED | REJECTED | Precisao insuficiente para o tipo de ponto. |

## Metodos Principais

| Metodo | Retorno | Descricao |
| --- | --- | --- |
| CanProcess() | bool | Verifica se esta em COLLECTED. |
| CanApprove() | bool | Verifica se esta em PROCESSED. |
| CanUseInDocuments() | bool | Retorna true apenas para APPROVED. |
| ValidateTransition(PointStatus) | void | Lanca exception se transicao invalida. |

Usado em SurveyPoint.Status controlando fluxo com domain events disparados nas transicoes, validado em DescriptiveMemorial e LegitimationPlan garantindo que apenas pontos APPROVED sao incluidos em documentos oficiais.
