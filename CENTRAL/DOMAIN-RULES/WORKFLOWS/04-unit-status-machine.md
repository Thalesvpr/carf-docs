---
type: leaf
status: approved
updated: 2026-02-07
---

# Unit Status Machine

Maquina de estados formal que governa o ciclo de vida de uma unidade habitacional desde sua criacao em campo ate a aprovacao ou rejeicao final. Cada unidade nasce no estado DRAFT e progride conforme acoes de usuarios com roles especificas, respeitando pre-condicoes rigorosas em cada transicao. O sistema emite domain events a cada mudanca de status, permitindo que handlers assincrono disparem notificacoes, atualizem caches e registrem auditoria sem acoplar a logica de transicao.

## Tabela de Transicoes

| Estado Origem | Acao | Estado Destino | Roles Permitidas | Pre-condicoes | Evento Emitido | Notifica |
|---------------|------|----------------|------------------|---------------|----------------|----------|
| DRAFT | submit | PENDING_ANALYSIS | field-cadastrator, field-coordinator, analyst | Ao menos um titular vinculado via unit_holders com is_primary true. Todos os campos obrigatorios preenchidos (endereco, community_id). | UnitStatusChangedEvent | Todos os analysts do tenant recebem notificacao de nova unidade para analise. |
| PENDING_ANALYSIS | claim | IN_REVIEW | analyst | Analyst deve estar designado ao tenant. Unidade nao pode ja estar claimed por outro analyst. | UnitStatusChangedEvent | Nenhuma notificacao adicional. |
| IN_REVIEW | approve | APPROVED | manager | Analyst responsavel deve ter registrado parecer favoravel. Documentacao completa: ao menos uma foto de fachada vinculada e todos os titulares com CPF validado. | UnitStatusChangedEvent, RequestApprovedEvent | Criador original da unidade recebe notificacao de aprovacao. |
| IN_REVIEW | reject | REJECTED | manager | Justificativa obrigatoria com minimo de 50 caracteres explicando motivo da rejeicao. | UnitStatusChangedEvent | Criador original da unidade recebe notificacao de rejeicao com justificativa. |
| IN_REVIEW | requestChanges | REQUIRES_CHANGES | analyst, manager | Lista de correcoes obrigatoria como array de strings descrevendo cada item a corrigir. | CorrectionRequestedEvent | Criador original da unidade recebe notificacao com lista de correcoes necessarias. |
| REQUIRES_CHANGES | resubmit | PENDING_ANALYSIS | criador original da unidade | Ao menos uma alteracao aplicada desde a ultima rejeicao, verificada comparando updated_at com a data da solicitacao de correcao. | UnitStatusChangedEvent | Todos os analysts do tenant recebem notificacao de resubmissao. |

## Invariantes

APPROVED e REJECTED sao estados terminais. Nenhuma transicao e permitida a partir deles. Uma unidade aprovada ou rejeitada nao pode ser editada, excluida ou ter seus vinculos com titulares alterados. A unica operacao permitida em estados terminais e a leitura.

A operacao DELETE so e permitida quando a unidade esta no estado DRAFT. Tentativas de exclusao em qualquer outro estado retornam erro NOT_DRAFT com HTTP 400.

Edicao de campos da unidade (endereco, geometria, dados de ocupacao) so e permitida nos estados DRAFT e REQUIRES_CHANGES. Tentativas de edicao em outros estados retornam erro UNIT_LOCKED com HTTP 403.

## Controle de Concorrencia

Cada transicao verifica o campo version da unidade antes de aplicar a mudanca. Se a versao no banco for maior que a versao enviada pelo client, a operacao falha com erro SYNC_CONFLICT e HTTP 409, indicando que outro usuario modificou a unidade desde a ultima leitura. O client deve recarregar os dados e tentar novamente.

## Auditoria

Toda transicao de status gera um registro em audit_logs contendo o estado anterior em old_values, o novo estado em new_values, o account_id do usuario que executou a acao, timestamp e IP de origem. A justificativa de rejeicao e a lista de correcoes solicitadas tambem sao incluidas no registro de auditoria quando aplicaveis.
