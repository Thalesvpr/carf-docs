---
type: template
template_for: adr
status: template
updated: 2026-01-21
validation:
  max_words: 300
  max_words_per_section: 80
  required_sections:
    - Contexto
    - Decisao
    - Consequencias
    - Alternativas Rejeitadas
  forbidden:
    - "```"
    - "http"
    - "|--|"
    - "- ["
---

# ADR-XXX: Titulo

## Regras

- Maximo 300 palavras total, 80 por secao
- Texto corrido, frases curtas
- Foco no "por que", nunca "como implementar"
- Proibido: codigo, links, tabelas, bullets

## Contexto

Qual problema? Qual restricao? Por que decidir agora?

## Decisao

O que foi decidido? Por que essa opcao?

## Consequencias

O que melhora? O que piora? Quais riscos?

## Alternativas Rejeitadas

Quais outras opcoes? Por que descartadas?
