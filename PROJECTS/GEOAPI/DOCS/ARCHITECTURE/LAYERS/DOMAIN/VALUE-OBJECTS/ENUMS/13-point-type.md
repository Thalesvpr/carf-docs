---
type: leaf
status: review
updated: 2026-02-08
---

# PointType

Value object enum representando tipo de ponto topografico coletado em campo durante levantamentos geodesicos, determinando precisao esperada, metodo de coleta e uso em processamentos posteriores.

Cada tipo possui requisitos diferentes de precisao e documentacao, influenciando diretamente a qualidade dos memoriais descritivos e plantas de legitimacao.

## Valores Permitidos

| Valor | Descricao |
| --- | --- |
| MARCO | Marco geodesico permanente materializado com concreto, chapa metalica ou estaca. Precisao minima de 2cm. |
| PIQUETE | Piquete temporario cravado no solo marcando vertice de perimetro. Precisao minima de 5cm. |
| NATURAL | Ponto natural estavel como afloramento rochoso ou quina de construcao. Precisao minima de 10cm. |

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Permanencia | Apenas MARCO e permanente; PIQUETE e removivel apos conclusao. |
| Monografia | Apenas MARCO exige monografia descritiva completa com fotos e croqui. |
| Precisao minima | MARCO: 2cm, PIQUETE: 5cm, NATURAL: 10cm. |

Usado em SurveyPoint.Type para classificar pontos coletados, validado em Monograph garantindo que apenas MARCO recebe monografia completa, e influencia apresentacao em LegitimationPlan onde MARCO aparece com simbologia destacada.
