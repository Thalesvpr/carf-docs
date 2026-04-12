---
type: template
template_for: rnf
status: review
updated: 2026-01-22
validation:
  max_words: 350
  required_sections:
    - Descricao
    - Metricas
    - Criterios de Aceitacao
  forbidden:
    - "```"
    - "- [ ]"
---

# RNF-XXX: Titulo do Requisito Nao-Funcional

## Regras

- Maximo 350 palavras
- Foco em atributos de qualidade: performance, seguranca, usabilidade, etc
- Metricas devem ser quantificaveis e verificaveis
- Proibido: blocos de codigo, checklists
- Criterios objetivos com valores numericos quando possivel

## Descricao

Qual atributo de qualidade? Por que e importante? Qual contexto de aplicacao? Quais restricoes tecnicas?

## Metricas

- Metrica principal: valor alvo
- Metrica secundaria: valor alvo
- Condicoes de medicao: ambiente, carga, etc

## Criterios de Aceitacao

1. Primeiro criterio mensuravel
2. Segundo criterio mensuravel
3. Terceiro criterio mensuravel
