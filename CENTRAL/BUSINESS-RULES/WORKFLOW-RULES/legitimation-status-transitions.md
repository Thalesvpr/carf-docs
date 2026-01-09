# Legitimation Status Transitions (Transições de Status de Legitimação)

Regras governando workflow completo de LegitimationRequest (solicitação de regularização fundiária) através de 11 estados distintos estabelecidos por Lei 13.465/2017 desde submissão inicial até emissão de certidão de regularização ou rejeição final incluindo etapas obrigatórias de análise documental técnica e jurídica edital público período de contestações e resolução de eventuais conflitos garantindo due process legal e transparência em todo processo que culminará na transferência formal de propriedade a beneficiários. Estado inicial DRAFT permite que manager ou analyst prepare solicitação de legitimação vinculando Unit já aprovada preenchendo dados complementares específicos do processo legal (modalidade REURB-S ou REURB-E, base legal, justificativa, relação de beneficiários) e anexando documentação obrigatória conforme modalidade escolhida antes de protocolar formalmente request perante órgão público responsável sendo DRAFT editável livremente e não gerando obrigações procedimentais até que seja submetido para processamento oficial. Transição DRAFT → SUBMITTED ocorre quando manager clica em "Protocolar Solicitação" após confirmar que toda documentação obrigatória foi anexada e dados foram revisados sendo gerado automaticamente número de protocolo único sequencial por tenant no formato "REURB-YYYY-NNNN" (ex: REURB-2025-0347) registrado em campo protocol_number que será utilizado em toda comunicação oficial relacionada ao processo e calculado deadline_date adicionando 120 dias corridos à data de submissão conforme prazo legal estabelecido por Lei 13.465/2017 para conclusão de processamento sob pena de mora administrativa, onde transição dispara evento RequestSubmittedEvent notificando beneficiário titular via email que solicitação foi protocolada informando número de protocolo e prazo estimado de conclusão além de registrar entry em AuditLog documentando quem submeteu quando e qual versão de dados estava presente no momento da submissão para fins de compliance e rastreabilidade. Transição SUBMITTED → UNDER_ANALYSIS ocorre automaticamente ou manualmente quando analista jurídico ou técnico assume responsabilidade por processar request clicando em "Iniciar Análise" sendo registrado em campo analyst_id identificador do usuário responsável e em analyzed_at timestamp de início permitindo cálculo de métricas de tempo de processamento e identificação de gargalos no fluxo de trabalho onde múltiplos analistas podem trabalhar em paralelo em aspectos diferentes (um verifica documentação pessoal outro valida planta técnica outro revisa situação fundiária) mas sistema mantém histórico de qual analista realizou qual verificação através de registros auxiliares em tabela LegitimationResponse vinculada a request. Transição UNDER_ANALYSIS → DOCUMENT_REVIEW ocorre quando análise preliminar identifica que documentação anexada está incompleta incorreta ou requer esclarecimentos adicionais sendo pausado processamento principal enquanto se aguarda regularização documental por parte de beneficiário ou equipe de campo onde analista cria registro detalhando exatamente quais documentos faltam ou precisam ser refeitos especificando prazo de 30 dias para apresentação complementar sob pena de arquivamento do processo por desistência tácita conforme regulamentação municipal e notificando titular automaticamente via email e SMS sobre pendências documentais com link direto para portal web onde pode fazer upload de documentos faltantes sem precisar comparecer presencialmente facilitando regularização rápida. Transição DOCUMENT_REVIEW → UNDER_ANALYSIS ocorre quando beneficiário apresenta documentação complementar solicitada dentro de prazo estabelecido sendo documentos anexados automaticamente vinculados a request através de entity Document com document_type específico e analista notificado que processo está pronto para retomar análise interrompida permitindo continuidade do workflow sem perda de contexto ou necessidade de recomeçar verificações já realizadas previamente economizando tempo e recursos públicos escassos. Transição UNDER_ANALYSIS → TECHNICAL_REVIEW ocorre quando análise documental e jurídica preliminar foi concluída satisfatoriamente e processo avança para verificação técnica especializada realizada por engenheiro ou arquiteto habilitado que confere precisão de planta georreferenciada valida cálculos de área e perímetro verifica se memorial descritivo está conforme normas ABNT confirma que geometria declarada não apresenta sobreposições com propriedades vizinhas já regularizadas e atesta que ocupação consolidada atende requisitos de habitabilidade segurança e salubridade estabelecidos por código de obras municipal sendo emitido parecer técnico fundamentado aprovando ou rejeitando aspectos técnicos da solicitação. Transição TECHNICAL_REVIEW → PUBLIC_NOTICE ocorre quando pareceres técnico e jurídico são favoráveis à regularização sendo publicado edital público em diário oficial e jornal de grande circulação conforme exigência legal anunciando intenção do poder público de emitir certidão de regularização fundiária em favor de beneficiário identificado sobre imóvel descrito com confrontações registrais informando que terceiros interessados (supostos proprietários credores hipotecários herdeiros ou qualquer pessoa que se julgue prejudicada) têm prazo de 30 dias corridos a partir da publicação para apresentar impugnação fundamentada contestando direito alegado pelo ocupante onde publicação de edital é registrada em campo public_notice_date e sistema calcula automaticamente contestation_deadline_date adicionando 30 dias para controle de prazo. Transição PUBLIC_NOTICE → CONTESTATION_PERIOD é automática após publicação de edital estabelecendo período de 30 dias durante qual sistema monitora apresentação de contestações por terceiros através de protocolo administrativo presencial ou digital criando entity Contestation vinculada a request sempre que nova impugnação é registrada contendo identificação do contestador fundamentos jurídicos alegados provas documentais apresentadas e pedido formulado (anulação do processo reconhecimento de propriedade concorrente indenização prévia ou qualquer outra pretensão) sendo cada contestação distribuída para analista jurídico elaborar manifestação do poder público respondendo argumentos apresentados e propondo encaminhamento (manter decisão de regularizar rejeitar solicitação ou buscar acordo entre partes). Transição CONTESTATION_PERIOD → RESOLUTION ocorre após decurso de prazo de 30 dias de edital sendo verificado se houve apresentação de contestações onde se não houver nenhuma impugnação processo avança diretamente para aprovação mas se houver uma ou mais contestações processo entra em fase de resolução durante qual analista jurídico elabora parecer detalhado sobre cada contestação recebida avaliando se possui fundamentação jurídica plausível se foi apresentada dentro de prazo legal se contestador possui legitimidade para impugnar (demonstra interesse jurídico direto) e se provas apresentadas são suficientes para invalidar ou modificar decisão de regularizar emitindo decisão administrativa fundamentada que pode rejeitar contestação por improcedência acolher parcialmente ajustando termos da regularização ou excepcionalmente acolher integralmente determinando arquivamento do processo de legitimação. Transição RESOLUTION → APPROVED ocorre quando todas contestações foram analisadas e rejeitadas ou não houve contestações no prazo legal e pareceres técnico e jurídico recomendam aprovação da regularização sendo request marcado como approved e disparado workflow de geração de certidão de regularização fundiária através de entity LegitimationCertificate contendo número único de certidão descrição completa do imóvel com coordenadas registrais lista de beneficiários com percentuais de propriedade data de emissão assinatura digital do gestor público responsável e QR code para verificação de autenticidade permitindo que certidão seja apresentada em cartório de registro de imóveis para formalização de matrícula individualizada em nome dos beneficiários consolidando transferência de propriedade. Transição RESOLUTION → REJECTED ocorre quando análise técnica ou jurídica identifica impedimento legal insuperável para regularização como ocupação em área non aedificandi (faixa de domínio de rodovia ferrovia ou rede elétrica) situação fundiária do terreno que impossibilita transferência de domínio (propriedade privada sem anuência do proprietário área de preservação permanente sem consolidação prévia a 2008) contestação de terceiro procedente que demonstra propriedade legítima concorrente ou qualquer outro óbice jurídico que inviabilize emissão de certidão com segurança jurídica sendo obrigatório preenchimento de campo rejection_reason com justificativa fundamentada em legislação aplicável e parecer técnico ou jurídico que embasou decisão permitindo beneficiário compreender motivos e eventualmente apresentar recurso administrativo ou buscar solução judicial se discordar da conclusão. Transição UNDER_ANALYSIS → NEEDS_CORRECTION ocorre quando analista identifica inconsistências ou erros nos dados cadastrais da Unit vinculada que impedem prosseguimento da análise como geometria espacial com problemas topológicos área calculada muito discrepante da realidade dados de titular desatualizados ou documentos anexados insuficientes para comprovação de requisitos legais sendo request devolvida para status NEEDS_CORRECTION com detalhamento de correções necessárias em campo correction_notes e notificação enviada a field agent ou analyst responsável pelo cadastro original solicitando que corrija problemas apontados antes de resubmeter solicitação sendo Unit associada temporariamente retornada para status REQUIRES_CHANGES até que correções sejam implementadas e validadas permitindo então que legitimation request retorne para UNDER_ANALYSIS e prossiga no workflow normal. Reversão de status APPROVED para estados anteriores é vedada por lei pois certidão de regularização uma vez emitida gera direito adquirido protegido constitucionalmente podendo apenas ser anulada por decisão judicial transitada em julgado em ação específica movida por terceiro prejudicado ou Ministério Público mas sistema permite marcar certidão como cancelled em casos excepcionais de fraude comprovada ou erro grosseiro mediante decisão administrativa fundamentada de gestor com role SUPER_ADMIN e registro completo de justificativa em AuditLog para fins de prestação de contas e eventual responsabilização civil ou criminal de quem praticou irregularidade.

**Estados LegitimationRequest (11 estados Lei 13.465/2017):**

1. **DRAFT**: Rascunho em preparação, não protocolado
2. **SUBMITTED**: Protocolado, aguarda distribuição
3. **UNDER_ANALYSIS**: Em análise técnica e jurídica
4. **DOCUMENT_REVIEW**: Aguarda regularização documental
5. **TECHNICAL_REVIEW**: Em verificação técnica especializada
6. **PUBLIC_NOTICE**: Edital publicado, aguarda contestações
7. **CONTESTATION_PERIOD**: Período de 30 dias para impugnações
8. **RESOLUTION**: Análise de contestações recebidas
9. **APPROVED**: Aprovado, certidão emitida
10. **REJECTED**: Rejeitado por impedimento legal
11. **NEEDS_CORRECTION**: Aguarda correções cadastrais

**Transições principais:**

| De → Para | Trigger | Prazo | Documentação | Permissão |
|-----------|---------|-------|--------------|-----------|
| DRAFT → SUBMITTED | Protocolar | - | Completa conforme modalidade | legitimation.submit (MANAGER+) |
| SUBMITTED → UNDER_ANALYSIS | Assumir análise | 5 dias | - | legitimation.analyze (ANALYST+) |
| UNDER_ANALYSIS → DOCUMENT_REVIEW | Docs incompletos | - | Lista pendências | legitimation.analyze |
| DOCUMENT_REVIEW → UNDER_ANALYSIS | Docs apresentados | 30 dias | Complementação | - |
| UNDER_ANALYSIS → TECHNICAL_REVIEW | Análise OK | 15 dias | Parecer preliminar | legitimation.analyze |
| TECHNICAL_REVIEW → PUBLIC_NOTICE | Parecer favorável | 10 dias | Parecer técnico | legitimation.approve (MANAGER+) |
| PUBLIC_NOTICE → CONTESTATION_PERIOD | Edital publicado | - | Publicação oficial | - |
| CONTESTATION_PERIOD → RESOLUTION | Prazo decorrido | 30 dias | Contestações ou nenhuma | - |
| RESOLUTION → APPROVED | Sem contestações procedentes | 20 dias | Decisão fundamentada | legitimation.approve (MANAGER+) |
| RESOLUTION → REJECTED | Impedimento legal | 20 dias | rejection_reason | legitimation.approve |
| UNDER_ANALYSIS → NEEDS_CORRECTION | Erros cadastrais | - | correction_notes | legitimation.analyze |

**Validações por transição:**

- **DRAFT → SUBMITTED**: Unit APPROVED, docs obrigatórios anexados, modality definida (REURB_S ou REURB_E), beneficiários identificados
- **UNDER_ANALYSIS → TECHNICAL_REVIEW**: Análise documental completa, parecer jurídico emitido
- **TECHNICAL_REVIEW → PUBLIC_NOTICE**: Parecer técnico favorável, planta georreferenciada validada
- **PUBLIC_NOTICE → CONTESTATION_PERIOD**: Edital publicado em diário oficial, public_notice_date registrada
- **RESOLUTION → APPROVED**: Contestações analisadas e rejeitadas OU sem contestações, pareceres favoráveis
- **RESOLUTION → REJECTED**: rejection_reason fundamentado, impedimento legal identificado

**Prazos legais (Lei 13.465/2017):**
- **Total SUBMITTED → APPROVED**: 120 dias (prazo legal máximo)
- **Parciais**: SUBMITTED → UNDER_ANALYSIS (5 dias), análises (40 dias), edital (30 dias), resolução (20 dias), emissão certidão (5 dias)
- **Penalidade**: Mora administrativa se exceder 120 dias sem justificativa

**Documentação obrigatória por modalidade:**

**REURB-S:**
- Docs pessoais: CPF, RG, certidão nascimento/casamento
- Comprovantes ocupação: contas serviços públicos 5 anos, declarações vizinhos (3)
- Docs técnicos: croqui simplificado, fotos (6 mínimo)
- Certidões: negativa propriedade

**REURB-E:**
- Todos de REURB-S +
- Planta técnica georreferenciada (profissional habilitado)
- Memorial descritivo ABNT
- ART/RRT do profissional
- Licença ambiental (se APP/ZPA)
- Certidão negativa débitos municipais

**Relacionamento com Domain Model:**
- Implementa: `DOMAIN-MODEL/VALUE-OBJECTS/21-legitimation-status.md` (11 estados enum)
- Valida: `DOMAIN-MODEL/AGGREGATES/03-legitimation-request-aggregate.md` (workflow completo)
- Eventos: `DOMAIN-MODEL/EVENTS/12-request-submitted-event.md` a `19-correction-requested-event.md`
- Certidão: `DOMAIN-MODEL/ENTITIES/27-legitimation-certificate.md` (gerada em APPROVED)

**Implementações por projeto:**
- Backend .NET: `PROJECTS/GEOAPI/LAYERS/APPLICATION/STATE-MACHINES/LegitimationStateMachine.cs`
- Backend .NET: `PROJECTS/GEOAPI/LAYERS/APPLICATION/SERVICES/LegitimationWorkflowService.cs`
- Frontend React: `PROJECTS/GEOWEB/COMPONENTS/legitimation/StatusTimeline.tsx`
- Frontend React: `PROJECTS/GEOWEB/COMPONENTS/legitimation/WorkflowDiagram.tsx`

---

**Última atualização:** 2025-01-06
