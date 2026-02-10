---
type: leaf
status: rejected
updated: 2026-02-08
description: Valores BOUNDARY e REFERENCE nao existem no dominio documentado. Diverge do arquivo ARCHITECTURE/LAYERS/DOMAIN/VALUE-OBJECTS/ENUMS/13-point-type.md que lista MARCO, PIQUETE, NATURAL.
---

# PointType

Value object enum imutavel representando o tipo de ponto topografico coletado em campo. Classifica a finalidade do ponto dentro do levantamento geodesico para processamento adequado.

## Valores Permitidos

| Valor | Descricao |
|-------|-----------|
| BASE | Estacao base GPS para processamento diferencial. Permanece fixa durante coleta. |
| ROVER | Ponto movel coletado pelo receptor GPS em campo. |
| CONTROL | Ponto de controle com coordenadas conhecidas para validacao. |
| BOUNDARY | Vertice de perimetro de unidade ou comunidade. |
| REFERENCE | Ponto de referencia para orientacao do levantamento. |

PointType determina o processamento aplicado: pontos BASE e CONTROL passam por ajustamento de rede, ROVER sao processados em pos-processamento diferencial, e BOUNDARY sao utilizados para gerar poligonos de perimetro.
