---
type: template
template_for: rf
status: review
updated: 2026-01-22
validation:
  max_words: 400
  required_sections:
    - Descricao
    - Criterios de Aceitacao
    - Rastreabilidade
  forbidden:
    - "```"
    - "- [ ]"
---

# RF-XXX: Titulo do Requisito

## Regras

- Maximo 400 palavras
- Texto corrido descrevendo O QUE o sistema deve fazer
- Nunca detalhar COMO implementar
- Proibido: blocos de codigo, checklists
- Criterios de aceitacao em lista numerada

## Descricao

O que o sistema deve fazer? Qual comportamento esperado? Quais dados envolvidos? Quais restricoes de negocio?

## Criterios de Aceitacao

1. Primeiro criterio verificavel
2. Segundo criterio verificavel
3. Terceiro criterio verificavel

## Rastreabilidade

- Modulos: GEOAPI, REURBWEB (quais implementam)
- User Stories relacionadas: US-XXX
- Requisitos dependentes: RF-YYY
