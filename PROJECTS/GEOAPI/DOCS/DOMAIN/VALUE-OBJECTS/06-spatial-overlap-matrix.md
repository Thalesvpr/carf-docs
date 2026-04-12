---
type: leaf
status: review
updated: 2026-02-08
---

# Spatial Overlap Detection

Matriz de deteccao de sobreposicao espacial entre Units, Communities, Blocks e outras geometrias poligonais, usando analise geometrica via PostGIS para identificacao e resolucao de conflitos territoriais.

## Classificacao de Sobreposicao

| Severidade | Percentual | Acao |
|------------|-----------|------|
| Minor | menor que 10% | Ajustavel via refinamento de boundaries. Auto-approve com flag de revisao. |
| Moderate | 10-50% | Exige analise de documentacao e priorizacao por antiguidade de posse. Aprovacao de MANAGER obrigatoria. |
| Severe | maior que 50% | Cancelamento de uma das Units. Prioriza ocupacao mais antiga ou titulo formal. Bloqueado ate resolucao manual. |
| Total | 100% | Duplicacao completa. Exige merge ou exclusao preservando dados via soft delete. |

## Casos Edge

| Caso | Descricao | Resolucao |
|------|-----------|-----------|
| Divisa imprecisa | Duas Units compartilham segmento por imprecisao GPS. | Ajuste para grade com tolerancia 0.5m. |
| Servidao publica | Unit sobrepoe via de acesso ou rede de infraestrutura. | Area Restriction preservando Unit. |
| APP | Unit invade Area de Preservacao Permanente. | Operacao ST_Difference subtraindo APP da geometria. |
| Cross-community | Units de communities diferentes se sobrepoem. | Escalacao para gestor municipal. |
| Propriedade formal | Overlap com matricula georreferenciada de cartorio. | Bloqueio automatico e notificacao ao titular formal. |
| Condominio | Multiplas Units representam fracoes ideais do mesmo lote. | Shared geometry com Holders somando 100%. |

## Algoritmo de Deteccao

Consulta espacial busca todas Units dentro de buffer de 100m da Unit sendo validada. Calcula area de intersecao via ST_Intersection e percentual (area_intersecao / area_unit * 100). Classifica severity e dispara workflow apropriado. Visualizacao em mapa destaca overlaps com camada semi-transparente colorida por severity.
