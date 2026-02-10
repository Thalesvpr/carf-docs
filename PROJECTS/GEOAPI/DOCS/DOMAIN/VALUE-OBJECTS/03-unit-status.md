---
type: leaf
status: review
updated: 2026-02-08
---

# UnitStatus

Value object enum imutavel representando o estado atual de uma Unit no workflow de cadastro e aprovacao. Persiste na coluna status varchar(30) da tabela units com CHECK constraint nos valores DRAFT, PENDING_ANALYSIS, IN_REVIEW, APPROVED, REJECTED e REQUIRES_CHANGES. Default DRAFT ao criar nova unidade.

## Valores Permitidos

| Valor | Descricao |
|-------|-----------|
| DRAFT | Rascunho inicial. Unidade criada mas nao submetida para analise. Editavel livremente. |
| PENDING_ANALYSIS | Submetida e aguardando atribuicao de analista. Nao editavel por campo. |
| IN_REVIEW | Em analise pelo analista designado. Pode solicitar correcoes. |
| APPROVED | Aprovada apos validacao de todos os dados e documentos. Imutavel exceto por ADMIN. |
| REJECTED | Rejeitada com justificativa obrigatoria. Pode retornar a DRAFT para correcao. |
| REQUIRES_CHANGES | Devolvida ao agente de campo para correcoes especificas antes de prosseguir. |

## Transicoes Validas

| De | Para | Quem | Condicao |
|----|------|------|----------|
| DRAFT | PENDING_ANALYSIS | FIELD_COORDINATOR, FIELD_CADASTRATOR | Documentacao minima preenchida e ao menos um Holder vinculado. |
| PENDING_ANALYSIS | IN_REVIEW | ANALYST | Analista assumiu a analise. |
| IN_REVIEW | APPROVED | MANAGER | Parecer tecnico favoravel. |
| IN_REVIEW | REJECTED | MANAGER | Parecer tecnico desfavoravel com justificativa obrigatoria. |
| IN_REVIEW | REQUIRES_CHANGES | ANALYST | Correcoes necessarias identificadas. |
| REQUIRES_CHANGES | DRAFT | FIELD_COORDINATOR | Apos correcao pelo agente de campo. |
| REJECTED | DRAFT | ADMIN | Apos correcao pelo requerente, reprocessamento excepcional. |

Transicoes invalidas sao impedidas pelo dominio lancando ValidationException. Edicao da unidade so e permitida nos estados DRAFT e REQUIRES_CHANGES. Exclusao so e permitida em DRAFT.
