---
type: leaf
status: review
updated: 2026-02-08
---

# LegitimationRequest Aggregate

Agregado de dominio estabelecendo LegitimationRequest como aggregate root, controlando o processo completo de legitimacao fundiaria conforme Lei 13.465/2017. Coordena multiplas entidades e value objects relacionados a solicitacao, analise e emissao de certidao de regularizacao.

## Raiz do Agregado

LegitimationRequest e a entidade raiz que coordena o workflow de 11 estados do processo de legitimacao. Estende BaseAggregateRoot com suporte a Domain Events e concorrencia otimista.

## Componentes Internos

| Componente | Cardinalidade | Descricao |
|------------|---------------|-----------|
| LegitimationResponse | 1:N | Pareceres tecnicos e juridicos formando trail de decisao. Tipos: PARECER_TECNICO, DECISAO, CONTESTACAO, CORRECAO. |
| LegitimationCertificate | 0:1 | Certidao oficial emitida ao aprovar processo. Numero unico CERT-AAAA-NNNNN. |
| DescriptiveMemorial | 0:1 | Memorial descritivo tecnico com coordenadas e descricao de perimetro. |
| LegitimationPlan | 0:1 | Planta tecnica grafica mostrando o imovel. |
| Document | 1:N | Anexos polimorficos: fotos, comprovantes, plantas, laudos. |
| Annotation | 1:N | Anotacoes rastreando pendencias do processo. |

## Workflow de Status

O processo segue 11 estados com transicoes validas: DRAFT, SUBMITTED, UNDER_ANALYSIS, NOTIFICATION_PUBLISHED, CONTESTATION_PERIOD, CONTESTATION_RECEIVED, DECISION_PENDING, APPROVED, REJECTED, TITLE_ISSUED, REGISTERED. Transicoes invalidas (saltar de DRAFT para APPROVED) sao impedidas.

## Invariantes

| Invariante | Descricao |
|------------|-----------|
| Documentacao completa | Nao pode ser aprovado sem memorial descritivo, planta tecnica, documentos do titular e fotos do imovel. |
| Workflow sequencial | Status deve seguir transicoes validas. Nao se pode pular etapas. |
| Certidao pos-aprovacao | LegitimationCertificate so pode ser emitida com status APPROVED. |
| Contestacoes resolvidas | Contestacoes durante CONTESTATION_PERIOD devem ser resolvidas antes de aprovar. |
| Prazo de 120 dias | Desde SUBMITTED, prazo de 120 dias nao pode ser ultrapassado sem justificativa formal. |
| CPF valido | requester_cpf quando pessoa fisica deve ser valido conforme algoritmo Mod11. |
| Limites de area | Area respeita limites da modalidade: ate 250m2 para REURB-S, ate 500m2 para REURB-E. |

## Operacoes da Raiz

| Operacao | Descricao |
|----------|-----------|
| SubmitRequest() | Transiciona DRAFT para SUBMITTED validando documentacao obrigatoria. Dispara RequestSubmittedEvent. |
| AssignAnalyst(accountId) | Atribui analista responsavel validando role ANALYST ou superior. |
| AddResponse(type, content, decision) | Cria LegitimationResponse atualizando status conforme decision. Dispara ResponseAddedEvent. |
| ApproveRequest() | Transiciona para APPROVED apos validar analises e contestacoes. Dispara RequestApprovedEvent. |
| RejectRequest(reason) | Transiciona para REJECTED com justificativa obrigatoria. Dispara RequestRejectedEvent. |
| IssueCertificate() | Cria LegitimationCertificate com numero unico. Dispara CertificateIssuedEvent. |
| RequestCorrections(issues) | Retorna para NEEDS_CORRECTION com lista de pendencias. Dispara CorrectionRequestedEvent. |

## Eventos de Dominio

| Evento | Contexto |
|--------|----------|
| RequestSubmittedEvent | Ao submeter. Notifica analistas e inicia contagem de prazo. |
| ResponseAddedEvent | Ao adicionar parecer. Atualiza dashboards de progresso. |
| RequestApprovedEvent | Ao aprovar. Permite geracao de relatorios e atualizacao de estatisticas. |
| CertificateIssuedEvent | Ao emitir certidao. Notifica requerente via email ou SMS. |
| ContestationReceivedEvent | Ao receber objecao. Notifica analista e pausa workflow. |
| DeadlineApproachingEvent | Quando faltam 15 dias para prazo de 120 dias. Alerta gestores. |
| RequestRejectedEvent | Ao rejeitar. Notifica requerente com justificativa. |
| CorrectionRequestedEvent | Ao solicitar correcoes. Notifica requerente com pendencias. |

## Motivacao do Boundary

Todos os componentes representam partes de um processo unico com forte acoplamento temporal e logico. Decisoes, aprovacoes e emissao de certidao devem ser atomicas para garantir validade legal. LegitimationResponses imutaveis preservam historico completo para compliance legal e defesa em recursos judiciais.
