---
type: leaf
status: review
updated: 2026-02-08
---

# AnnotationType

Value object enum representando tipo de anotacao que pode ser criada em qualquer entidade do sistema via relacionamento polimorfico, determinando comportamento, campos obrigatorios e apresentacao visual. No banco de dados, corresponde ao campo annotations.annotation_type (varchar(30)).

Cada tipo define regras especificas de validacao e comportamento, como exigencia de prioridade ou prazo.

## Valores Permitidos

| Valor | Descricao |
| --- | --- |
| NOTE | Observacao geral informativa sem necessidade de acao ou prazo. |
| WARNING | Alerta importante destacando atencao necessaria mas sem bloquear processos. |
| ISSUE | Problema identificado que requer resolucao com rastreamento via IsResolved. |
| REMINDER | Lembrete com prazo obrigatorio via DueDate para acoes futuras. |

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Prioridade obrigatoria | ISSUE e REMINDER exigem campo priority preenchido. |
| Data prazo | REMINDER exige DueDate obrigatorio. |
| Resolucao | ISSUE deve ser marcado como resolvido (IsResolved, ResolvedAt, ResolvedBy). |

Usado em Annotation.annotation_type controlando validacoes e comportamento, dispara notificacoes diferentes por tipo (WARNING: in-app, ISSUE: email, REMINDER: push no DueDate), e integra com workflow onde ISSUE em Unit pode bloquear aprovacao ate resolucao.
