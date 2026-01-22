---
type: template
template_for: us
status: review
updated: 2026-01-22
validation:
  max_words: 350
  required_sections:
    - Historia
    - Criterios de Aceitacao
    - Rastreabilidade
  forbidden:
    - "```"
    - "- [ ]"
---

# US-XXX: Titulo da User Story

## Regras

- Maximo 350 palavras
- Historia no formato "Como [persona], quero [acao] para que [beneficio]"
- Foco no VALOR para o usuario, nao na implementacao
- Proibido: blocos de codigo, checklists
- Criterios de aceitacao em lista numerada

## Historia

Como [persona/role], quero [acao desejada] para que [beneficio/valor obtido].

Contexto adicional explicando cenario de uso e motivacao.

## Criterios de Aceitacao

1. Primeiro criterio verificavel pelo usuario
2. Segundo criterio verificavel pelo usuario
3. Terceiro criterio verificavel pelo usuario

## Rastreabilidade

- Epic: nome-do-epic
- Requisitos funcionais: RF-XXX, RF-YYY
- Endpoints: GET /api/recurso, POST /api/recurso
