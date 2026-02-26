---
type: leaf
status: review
updated: 2026-02-08
---

# Tipos Enum

Este documento descreve todos os enums exportados pelo modulo types do tscore, utilizados para classificacao, controle de fluxo e referencia polimorfica em todo o ecossistema CARF. Cada enum corresponde a um CHECK constraint ou conjunto de valores aceitos no [schema PostgreSQL](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/INFRA/PERSISTENCE/02-database-schema.md).

## Enums de Status

UnitStatus define os seis estados do workflow de aprovacao de unidades habitacionais, correspondendo ao CHECK constraint da coluna status da tabela units.

| Valor | Descricao | Transicoes Possiveis |
|:------|:----------|:---------------------|
| DRAFT | Rascunho em edicao pelo agente de campo | PENDING_ANALYSIS |
| PENDING_ANALYSIS | Submetida para analise, aguardando analista | IN_REVIEW |
| IN_REVIEW | Em analise tecnica pelo analista | APPROVED, REJECTED, REQUIRES_CHANGES |
| APPROVED | Aprovada pelo manager | (terminal) |
| REJECTED | Rejeitada pelo manager com justificativa | (terminal) |
| REQUIRES_CHANGES | Devolvida com solicitacao de correcoes | DRAFT |

LegitimationStatus define os onze estados do processo de legitimacao fundiaria conforme Lei 13.465/2017, correspondendo ao CHECK constraint da coluna status da tabela legitimation_requests.

| Valor | Descricao |
|:------|:----------|
| DRAFT | Rascunho do requerimento |
| SUBMITTED | Protocolado oficialmente |
| UNDER_ANALYSIS | Em analise tecnica |
| NOTIFICATION_PUBLISHED | Edital publicado em diario oficial |
| CONTESTATION_PERIOD | Prazo de 30 dias para contestacoes em andamento |
| CONTESTATION_RECEIVED | Contestacao recebida de terceiro |
| DECISION_PENDING | Aguardando decisao do gestor |
| APPROVED | Aprovado para emissao de titulo |
| REJECTED | Rejeitado com fundamento legal |
| TITLE_ISSUED | Certidao de legitimacao emitida |
| REGISTERED | Registrado em cartorio de imoveis |

SyncStatus define os cinco estados de sincronizacao offline entre REURBCAD mobile e servidor GEOAPI, utilizados na tabela sync_logs e no protocolo de sync bidirecional.

| Valor | Descricao |
|:------|:----------|
| PENDING | Operacao aguardando envio ao servidor |
| IN_PROGRESS | Sincronizacao em andamento |
| SUCCESS | Sincronizado com sucesso |
| CONFLICT | Conflito detectado entre versao local e servidor |
| FAILED | Falha na sincronizacao por erro de rede ou validacao |

AttendanceStatus define situacao de atendimento em campo registrada pelo agente ao visitar a unidade, correspondendo aos valores aceitos na coluna attendance_status da tabela units.

| Valor | Descricao |
|:------|:----------|
| AUSENTE | Morador ausente no momento da visita |
| PRESENTE | Morador presente e atendeu |
| NAO_QUIS | Morador presente mas recusou atendimento |
| ASSINADO | Morador presente, atendeu e assinou documentos |

OccupantType distingue a natureza da ocupacao da unidade, correspondendo a coluna occupant_type da tabela units.

| Valor | Descricao |
|:------|:----------|
| POSSUIDOR | Ocupa o imovel como posseiro |
| LOCATARIO | Ocupa o imovel como locatario |

UtilizationType define a finalidade de uso da unidade, correspondendo a coluna utilization_type da tabela units.

| Valor | Descricao |
|:------|:----------|
| RESIDENCIAL | Uso exclusivamente residencial |
| COMERCIAL | Uso exclusivamente comercial |
| MISTO | Uso misto residencial e comercial |
| TERRENO_VAZIO | Terreno sem construcao |
| NAO_HABITADO | Construcao existente mas nao habitada |

UnitCondition define condicao fisica da unidade, correspondendo a coluna unit_condition da tabela units.

| Valor | Descricao |
|:------|:----------|
| OCUPADA | Unidade ocupada por moradores |
| VAZIA | Unidade sem ocupantes |
| EM_CONSTRUCAO | Unidade em obras |
| ABANDONADA | Unidade abandonada |

## Enums de Roles

Role define hierarquia de permissoes com seis niveis organizados em arvore com dois ramos sob manager, espelhando a configuracao de realm roles no Keycloak.

| Valor | Descricao | Herda de |
|:------|:----------|:---------|
| SUPER_ADMIN | Acesso total a todos os tenants | REURBMASTER |
| REURBMASTER | Administrador de tenant especifico | MANAGER |
| MANAGER | Gestor com poder de decisao | ANALYST, FIELD_COORDINATOR |
| ANALYST | Analista tecnico de escritorio | - |
| FIELD_COORDINATOR | Coordenador de equipe de campo | FIELD_CADASTRATOR |
| FIELD_CADASTRATOR | Cadastrador com acesso restrito a coleta | - |

TeamRole define papeis dentro de uma equipe de campo, correspondendo ao CHECK constraint da coluna role da tabela team_members.

| Valor | Descricao |
|:------|:----------|
| COORDINATOR | Coordenador lider da equipe |
| CADASTRATOR | Membro cadastrador da equipe |

## Enums de Classificacao

CommunityType categoriza comunidades por natureza da ocupacao, correspondendo ao CHECK constraint da coluna community_type da tabela communities.

| Valor | Descricao |
|:------|:----------|
| URBANA | Nucleo urbano informal |
| RURAL | Assentamento rural |
| QUILOMBOLA | Comunidade quilombola |
| RIBEIRINHA | Comunidade ribeirinha |

DocumentType classifica documentos anexados no sistema, correspondendo ao CHECK constraint da coluna document_type da tabela documents.

| Valor | Descricao |
|:------|:----------|
| RG | Registro geral de identidade |
| CPF | Cadastro de pessoa fisica |
| CNH | Carteira nacional de habilitacao |
| COMPROVANTE_RESIDENCIA | Comprovante de endereco |
| FOTO_FACHADA | Fotografia da fachada da unidade |
| FOTO_DOCUMENTO | Fotografia de documento em campo |
| CERTIDAO | Certidao (nascimento, casamento, obito) |
| OUTRO | Outro tipo de documento |

AnnotationType classifica anotacoes vinculadas a entidades, correspondendo ao CHECK constraint da coluna annotation_type da tabela annotations.

| Valor | Descricao |
|:------|:----------|
| NOTE | Nota informativa geral |
| WARNING | Alerta sobre situacao relevante |
| ISSUE | Problema identificado que requer acao |
| REMINDER | Lembrete com prazo |

Decision define parecer final do processo de legitimacao, correspondendo aos valores aceitos na coluna decision da tabela legitimation_requests.

| Valor | Descricao |
|:------|:----------|
| APPROVED | Processo aprovado para emissao de titulo |
| REJECTED | Processo rejeitado com fundamentacao legal |

CertificateSituation classifica situacao do imovel na certidao de legitimacao, correspondendo ao CHECK constraint da coluna situation da tabela legitimation_certificates.

| Valor | Descricao |
|:------|:----------|
| COVERED | Imovel integralmente abrangido pela REURB |
| CONFRONTING | Imovel confrontante com area de REURB |
| BOTH | Imovel abrangido e confrontante simultaneamente |

RelationshipType define natureza do vinculo entre titular e unidade, correspondendo ao CHECK constraint da coluna relationship_type da tabela unit_holders.

| Valor | Descricao |
|:------|:----------|
| PROPRIETARIO | Titular proprietario do imovel |
| CONJUGE | Conjuge do proprietario |
| MORADOR | Morador sem propriedade formal |
| PROCURADOR | Procurador legal do proprietario |
| HERDEIRO | Herdeiro do proprietario falecido |

## Enums de Referencia

EntityType identifica tipo de entidade em contextos polimorficos onde Document, Annotation e AuditLog referenciam entidades pelo par entityType e entityId, correspondendo aos valores aceitos na coluna entity_type das tabelas documents, annotations e audit_logs.

| Valor | Descricao |
|:------|:----------|
| UNIT | Unidade habitacional |
| HOLDER | Titular ou posseiro |
| COMMUNITY | Comunidade ou nucleo urbano |
| BLOCK | Quadra |
| PLOT | Lote |

Priority define nivel de prioridade com SLA associado para anotacoes do tipo ISSUE e REMINDER, correspondendo aos valores aceitos na coluna priority da tabela annotations.

| Valor | SLA | Descricao |
|:------|:----|:----------|
| LOW | 168 horas (7 dias) | Prioridade baixa |
| NORMAL | 72 horas (3 dias) | Prioridade normal |
| HIGH | 24 horas (1 dia) | Prioridade alta |
| URGENT | 4 horas | Prioridade urgente |
