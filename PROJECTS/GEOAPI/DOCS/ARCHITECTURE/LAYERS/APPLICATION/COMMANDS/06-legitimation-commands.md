---
type: leaf
status: review
updated: 2026-02-08
---

# Legitimation Commands

Os commands de legitimacao implementam o workflow de legitimacao fundiaria conforme Lei 13.465/2017. Cada command representa uma transicao na maquina de estados do processo, com validacoes de pre-condicoes e emissao de domain events.

---

## CreateRequestCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| UnitId | Guid | sim | Identificador da unidade |

O handler valida duas pre-condicoes obrigatorias. Primeira, a unidade referenciada deve ter status APPROVED. Segunda, a unidade deve ter ao menos um titular vinculado com relationship_type PROPRIETARIO em unit_holders. Adicionalmente, verifica que nao existe outro processo ativo para a mesma unidade (constraint parcial onde deleted_at IS NULL e status NOT IN REJECTED). Ao satisfazer todas as condicoes, cria registro em legitimation_requests com status DRAFT e requested_by do contexto.

Emite RequestSubmittedEvent com Id e UnitId. Erros possiveis: VALIDATION_ERROR quando pre-condicoes nao sao satisfeitas.

---

## SubmitRequestCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| RequestId | Guid | sim | Identificador do processo |

O handler transiciona o status de DRAFT para SUBMITTED, registrando analyst_id do contexto. O processo entra na fila de analise.

---

## ApproveRequestCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| RequestId | Guid | sim | Identificador do processo |
| Justification | string | sim | Justificativa obrigatoria |

O handler verifica role manager ou superior. Transiciona o status para APPROVED, registra manager_id, decision APPROVED, decision_reason com a justificativa e decision_at com timestamp. Emite RequestApprovedEvent com Id e ManagerId.

---

## RejectRequestCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| RequestId | Guid | sim | Identificador do processo |
| Reason | string | sim | Motivo com minimo 100 caracteres citando fundamento legal |

O handler verifica role manager ou superior e valida que o motivo tem ao menos 100 caracteres. Transiciona o status para REJECTED, registra decision REJECTED e decision_reason. Emite RequestRejectedEvent com Id e Reason.

---

## IssueCertificateCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| RequestId | Guid | sim | Identificador do processo aprovado |

O handler verifica que o processo tem status APPROVED. Gera numero sequencial unico no formato CERT-AAAA-NNNNN, produz PDF da certidao via IPdfGenerator contendo dados da unidade, titular e decisao, armazena o PDF no S3 e persiste registro em legitimation_certificates. Transiciona status do processo para TITLE_ISSUED.

Emite CertificateIssuedEvent com RequestId e CertificateNumber.
