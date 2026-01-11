# Unit Status Transitions (Transições de Status da Unidade)

Regras governando transições de status de Unit (unidade habitacional) ao longo de ciclo de vida desde criação inicial como rascunho até aprovação final ou rejeição estabelecendo máquina de estados que define quais mudanças de status são permitidas a partir de cada estado atual quais validações devem ser satisfeitas antes de cada transição e quais roles (papéis) têm permissão para executar cada mudança garantindo integridade do processo de cadastramento validação e legitimação de propriedades. Status inicial de Unit recém-criada é sempre DRAFT (rascunho) permitindo que field agent cadastre informações básicas de forma incremental sem obrigatoriedade de completude imediata possibilitando trabalho offline com salvamento frequente de progresso parcial e sincronização posterior quando conexão for restabelecida, onde Unit em DRAFT pode ser editada livremente pelo criador ou membros da mesma equipe (Team) sem restrições mas não é visível para analistas ou gestores que trabalham apenas com unidades submetidas para validação. Transição DRAFT → PENDING_ANALYSIS ocorre quando field agent considera cadastro completo e submete Unit para validação clicando em botão "Enviar para Análise" sendo validado automaticamente que unidade possui ao menos um Holder vinculado como titular primário com CPF validado endereço preenchido geometria espacial definida (polígono ou ponto GPS) área calculada status de ocupação declarado e ao menos uma fotografia anexada como Document comprovando existência física da edificação, onde transição é permitida para qualquer usuário com permissão units.submit (roles FIELD_AGENT ANALYST MANAGER ADMIN SUPER_ADMIN) mas tipicamente executada por field agent que coletou dados em campo podendo ser revertida para DRAFT pelo próprio usuário caso identifique erro antes que analista inicie revisão. Transição PENDING_ANALYSIS → IN_REVIEW ocorre quando analyst assume responsabilidade por validar Unit clicando em botão "Iniciar Análise" estabelecendo lock otimista que impede outros analistas de editarem mesma unidade simultaneamente evitando conflitos de edição concorrente e garantindo que cada Unit é revisada por exatamente um analista por vez, onde transição é permitida apenas para usuários com permissão units.review (roles ANALYST MANAGER ADMIN SUPER_ADMIN) e sistema automaticamente registra quem iniciou análise em campo reviewed_by_account_id e timestamp de início em reviewed_at permitindo rastreabilidade e métricas de produtividade individual de analistas. Transição IN_REVIEW → APPROVED ocorre quando analyst valida que todas informações cadastradas estão corretas completas e consistentes clicando em botão "Aprovar Unidade" após verificar visualmente que geometria espacial corresponde a footprint de edificação visível em ortofoto de referência WMS dados de titular são coerentes com documentos anexados área calculada está dentro de limites legais para REURB e não há sobreposição significativa com unidades vizinhas já aprovadas, onde transição é permitida apenas para usuários com permissão units.approve (roles MANAGER ADMIN SUPER_ADMIN) sendo vedada a analistas comuns que podem apenas recomendar aprovação mas não efetivá-la estabelecendo segregação de responsabilidades que exige dupla verificação (analyst revisa e manager aprova) para decisões críticas que habilitam Unit a participar de processo de legitimação fundiária. Transição IN_REVIEW → REJECTED ocorre quando analyst ou manager identifica problemas graves que impedem aprovação de Unit como cadastro de titular com CPF inválido ou duplicado geometria espacial com auto-interseção ou área muito discrepante da realidade visível em ortofoto evidências de que ocupação não é residencial mas comercial ou industrial documentos anexados ilegíveis ou adulterados ou qualquer outra irregularidade que comprometa validade do cadastro para fins de regularização fundiária, onde transição exige preenchimento obrigatório de campo rejection_reason explicando motivo da rejeição em linguagem clara acessível para que field agent possa corrigir problemas identificados e resubmeter unidade posteriormente sendo vedado rejeitar sem justificativa detalhada que oriente correções necessárias, e após rejeição Unit retorna automaticamente para status DRAFT permitindo edições pelo criador original ou outros membros da equipe para correção de problemas antes de nova submissão. Transição IN_REVIEW → REQUIRES_CHANGES ocorre quando analyst identifica problemas menores que podem ser corrigidos rapidamente sem exigir nova coleta de campo como pequenas inconsistências em dados de endereço fotografias adicionais necessárias para melhor documentar propriedade ou esclarecimentos sobre situação fundiária declarada onde transição registra lista de correções solicitadas em campo required_changes_notes sendo Unit retornada para status DRAFT mas mantendo histórico de tentativa de aprovação anterior e motivos de devolução permitindo field agent corrigir apenas itens apontados sem refazer cadastro completo economizando tempo e evitando retrabalho desnecessário. Transições reversas de APPROVED ou REJECTED de volta para estados anteriores são geralmente vedadas para preservar integridade de decisões já tomadas e evitar manipulação retroativa de dados após aprovação formal mas podem excepcionalmente ser autorizadas por usuários com role ADMIN ou SUPER_ADMIN mediante justificativa documentada em campo override_reason registrada em AuditLog para fins de compliance e auditoria posterior quando identificado erro grave que justifique revisão de decisão já efetivada como descoberta posterior de fraude duplicação não detectada inicialmente ou mudança de interpretação legal que invalida aprovação anterior. Validações automáticas executadas antes de cada transição incluem verificação de completude de campos obrigatórios conforme status destino conferência de integridade referencial garantindo que entidades relacionadas (Holder Community Block Documents) existem e estão em estados válidos cálculo de regras de negócio como área dentro de limites REURB ou ausência de overlaps críticos com unidades vizinhas e confirmação de permissões do usuário executante verificando que possui role adequado e que Unit pertence a Community para qual tem CommunityAuthorization ativa com permissão de edição garantindo isolamento multi-tenant e controle de acesso granular por comunidade.

**Estados de Unit (UnitStatus enum):**
- **DRAFT**: Rascunho em edição, não validado
- **PENDING_ANALYSIS**: Aguardando análise de analista
- **IN_REVIEW**: Em revisão por analista específico
- **APPROVED**: Aprovado, pronto para legitimação
- **REJECTED**: Rejeitado, requer correções
- **REQUIRES_CHANGES**: Requer alterações menores

**Transições permitidas:**

| De → Para | Condições | Permissão | Validações |
|-----------|-----------|-----------|------------|
| DRAFT → PENDING_ANALYSIS | Cadastro completo | units.submit | Holder vinculado, geometria, fotos |
| PENDING_ANALYSIS → IN_REVIEW | Analyst assume | units.review | Analyst disponível, sem lock |
| IN_REVIEW → APPROVED | Validação OK | units.approve | Área válida, sem overlaps, docs OK |
| IN_REVIEW → REJECTED | Problemas graves | units.approve | rejection_reason obrigatório |
| IN_REVIEW → REQUIRES_CHANGES | Correções menores | units.review | required_changes_notes obrigatório |
| REQUIRES_CHANGES → DRAFT | Auto após registro | - | Retorna para edição |
| REJECTED → DRAFT | Auto após registro | - | Permite correções |
| APPROVED → DRAFT | Excepcional | units.override | override_reason + AuditLog |

**Permissões por role:**
- **FIELD_AGENT**: DRAFT → PENDING_ANALYSIS (submit)
- **ANALYST**: PENDING_ANALYSIS → IN_REVIEW (review), IN_REVIEW → REQUIRES_CHANGES
- **MANAGER**: IN_REVIEW → APPROVED/REJECTED (approve)
- **ADMIN/SUPER_ADMIN**: Todas transições + overrides

**Validações automáticas por transição:**
- **DRAFT → PENDING_ANALYSIS**: Holder primário, geometria válida, área > 0, 1+ foto, endereço completo
- **IN_REVIEW → APPROVED**: Área 20-500m², sem overlaps >1%, docs obrigatórios, geometria topológica válida
- **IN_REVIEW → REJECTED**: rejection_reason preenchido, analyst_id registrado
- **Overrides**: override_reason + aprovação ADMIN + AuditLog entry

**Lock otimista IN_REVIEW:**
- Campo `reviewed_by_account_id` registra analyst
- Campo `reviewed_at` registra timestamp início
- Timeout 2 horas libera lock automaticamente
- Outro analyst não pode assumir enquanto locked

**Relacionamento com Domain Model:**
- Implementa: `DOMAIN-MODEL/VALUE-OBJECTS/03-unit-status.md` (enum)
- Valida: `DOMAIN-MODEL/AGGREGATES/01-unit-aggregate.md` (state machine)
- Eventos: `DOMAIN-MODEL/EVENTS/02-unit-status-changed-event.md`

**Implementações por projeto:**
- Backend .NET: (caminho de implementação)
- Frontend React: (caminho de implementação)
- Mobile React Native: (caminho de implementação) (submit button enabled/disabled)

---

**Última atualização:** 2025-01-06
