---
type: template
template_for: uc
status: review
updated: 2026-01-22
validation:
  max_words: 500
  required_sections:
    - Atores
    - Pre-condicoes
    - Fluxo Principal
    - Fluxos Alternativos
    - Pos-condicoes
  forbidden:
    - "```"
    - "- [ ]"
---

# UC-XXX: Titulo do Caso de Uso

## Regras

- Maximo 500 palavras
- Fluxo principal em passos numerados
- Fluxos alternativos referenciam passo do fluxo principal
- Proibido: blocos de codigo, checklists
- Foco na interacao ator-sistema

## Atores

- Ator primario: quem inicia
- Atores secundarios: quem participa

## Pre-condicoes

- O que deve ser verdade antes de iniciar

## Fluxo Principal

1. Ator faz acao
2. Sistema responde
3. Ator faz proxima acao
4. Sistema finaliza

## Fluxos Alternativos

**FA-01: Nome do fluxo alternativo**
No passo X, se condicao alternativa:
1. Sistema faz acao alternativa
2. Retorna ao passo Y

## Pos-condicoes

- O que deve ser verdade apos conclusao
