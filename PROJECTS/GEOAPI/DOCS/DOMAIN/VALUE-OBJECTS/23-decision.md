---
type: leaf
status: review
updated: 2026-02-08
---

# Decision

Value object enum imutavel representando a decisao tomada sobre um processo de legitimacao fundiaria. Persiste na coluna decision varchar(30) da tabela legitimation_requests, nullable (preenchido apenas quando decisao e tomada).

## Valores Permitidos

| Valor | Descricao |
|-------|-----------|
| APPROVED | Processo aprovado. Permite emissao de LegitimationCertificate. decision_reason opcional. |
| REJECTED | Processo rejeitado. decision_reason obrigatoria justificando a rejeicao. |

## Uso no Dominio

Decision e preenchida junto com decision_reason e decision_at pelo MANAGER ao tomar decisao final. APPROVED transiciona LegitimationStatus para APPROVED e habilita emissao de certidao. REJECTED transiciona para REJECTED e encerra o workflow. Decisao e irreversivel sem intervencao administrativa (ADMIN).
