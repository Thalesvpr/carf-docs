---
type: leaf
status: review
updated: 2026-02-08
---

# Legitimation DTOs

Os Data Transfer Objects de legitimacao definem os contratos de entrada e saida da API para o workflow de legitimacao fundiaria.

## DTOs de Resposta

LegitimationRequestDto e o DTO completo retornado em operacoes de leitura individual.

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| Id | Guid | Identificador unico |
| UnitId | Guid | Unidade objeto da legitimacao |
| UnitCode | string | Codigo da unidade |
| Status | string | Status atual do processo |
| RequestedAt | DateTime | Data de protocolo |
| RequestedBy | Guid | Quem iniciou |
| AnalystId | Guid | Analista responsavel (nullable) |
| ManagerId | Guid | Gestor decisor (nullable) |
| Decision | string | APPROVED ou REJECTED (nullable) |
| DecisionReason | string | Justificativa (nullable) |
| DecisionAt | DateTime | Quando decidiu (nullable) |
| Deadline | DateTime | Prazo decisao (nullable) |
| ContestationDeadline | DateTime | Prazo contestacao (nullable) |
| Certificate | CertificateDto | Dados da certidao (nullable) |
| Responses | lista de ResponseDto | Historico de respostas |

LegitimationListItemDto e o DTO reduzido para listagens contendo Id, UnitCode, HolderName, Status, RequestedAt, Deadline e AnalystName.

CertificateDto contem CertificateNumber (string CERT-AAAA-NNNNN), Situation (COVERED, CONFRONTING, BOTH), IssuedAt (DateTime) e IssuedBy (Guid).

ResponseDto contem Id, ResponseType (PARECER_TECNICO, DECISAO, CONTESTACAO, CORRECAO), Content (texto) e RespondedAt (DateTime).

## DTOs de Request

CreateLegitimationRequest contem unitId (UUID obrigatorio).

ApproveLegitimationRequest contem justification (string obrigatoria).

RejectLegitimationRequest contem reason (string obrigatoria, minimo 100 caracteres).
