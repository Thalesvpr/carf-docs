---
id: UC-009-FE-002
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-009-FE-002: Documentacao Incompleta

Fluxo de excecao do UC-009 quando usuario tenta submeter processo com documentos faltantes.

## Condicao

No passo 13 do UC-009, sistema detecta que checklist de documentos nao esta completa.

## Fluxo

1. Usuario clica em Submeter para Aprovacao
2. Sistema valida checklist de documentos
3. Sistema detecta itens obrigatorios pendentes
4. Sistema bloqueia submissao
5. Sistema exibe modal listando documentos faltantes
6. Sistema destaca itens pendentes na checklist
7. Usuario fecha modal e completa uploads
8. Usuario tenta submeter novamente apos completar

## Documentos Tipicos

- Declaracao de posse
- RG e CPF do beneficiario
- Comprovante de residencia recente
- Memorial descritivo
- Planta da unidade

## Retorno

Submissao bloqueada. Usuario completa checklist e tenta novamente.
