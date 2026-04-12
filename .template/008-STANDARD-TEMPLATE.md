---
type: template
template_for: standard
status: review
updated: 2026-01-22
validation:
  max_words: 200
  max_words_per_section: 60
  required_sections:
    - Regra
    - Justificativa
    - Aplicacao
  forbidden:
    - "```"
    - http
    - "|--|"
---

# STD-XXX: Titulo

## Regras

- Maximo 200 palavras total, 60 por secao
- Texto prescritivo, direto, sem justificativas longas
- Foco no "o que fazer", nao "por que decidimos"
- Proibido: codigo, links, tabelas

## Regra

O que deve ser feito. Imperativo. Claro. Sem ambiguidade.

## Justificativa

Por que essa regra existe. Uma ou duas frases.

## Aplicacao

Onde se aplica: projetos, contextos, excecoes.
