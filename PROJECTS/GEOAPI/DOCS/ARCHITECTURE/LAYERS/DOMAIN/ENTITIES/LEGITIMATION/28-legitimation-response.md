---
type: leaf
status: approved
updated: 2026-02-07
---

# LegitimationResponse

Entidade representando resposta ou parecer vinculado a um processo de legitimacao fundiaria. Inclui pareceres tecnicos de analistas, decisoes de managers e contestacoes de terceiros. Herda de BaseEntity fornecendo auditoria temporal.

## Papel no Dominio

Cada LegitimationResponse documenta uma interacao formal no processo de legitimacao. Pareceres tecnicos fundamentam a decisao do manager, contestacoes de terceiros podem suspender o andamento, e correcoes solicitadas exigem acao do requerente. O historico completo de respostas permite rastrear toda a evolucao do processo.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| RequestId | Guid | nao | FK para LegitimationRequest. Relacionamento 1:N, multiplas respostas por processo. |
| ResponderId | Guid | nao | UUID do responsavel pela resposta: analyst, manager ou protocolo externo para contestacoes. |
| ResponseType | string | nao | Tipo da resposta: PARECER_TECNICO (analise do analyst), DECISAO (aprovacao ou rejeicao pelo manager), CONTESTACAO (impugnacao de terceiro), CORRECAO (solicitacao de ajustes ao requerente). |
| Content | string | nao | Texto completo da resposta. Pareceres devem citar Lei 13.465/2017 e normas tecnicas. Minimo 100 caracteres para PARECER_TECNICO e DECISAO. |
| RespondedAt | DateTime | nao | Quando a resposta foi registrada. |

## Relacionamentos

Pertence a um LegitimationRequest (obrigatorio). Referencia um Account como ResponderI.

## Invariantes de Negocio

ResponseType PARECER_TECNICO e DECISAO so podem ser criados por accounts com role ANALYST ou MANAGER respectivamente. Contestacoes podem ser registradas por qualquer account com acesso administrativo. O Content nao pode ser alterado apos criacao para preservar integridade do historico.
