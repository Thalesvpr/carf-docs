# Notification Triggers (Gatilhos de Notificação)

Sistema implementa mecanismo abrangente de notificações automáticas disparadas por eventos de domínio garantindo que usuários e beneficiários sejam informados tempestivamente sobre mudanças de status ações requeridas prazos próximos de vencimento e conclusão de operações críticas utilizando três canais de comunicação sendo email para notificações detalhadas com links e anexos, SMS para alertas urgentes de prazo e mudanças críticas de status, e notificações in-app para atualizações em tempo real visíveis imediatamente ao acessar sistema sem necessidade de consultar email ou telefone. Notificações relacionadas a unidades habitacionais disparam quando unidade cadastrada por FIELD_AGENT transita de DRAFT para PENDING_ANALYSIS enviando email de confirmação para criador informando que unidade foi submetida para análise com número de protocolo interno estimativa de prazo de 7 dias úteis para revisão e link direto para acompanhar progresso, quando unidade é atribuída a ANALYST para revisão em estado IN_REVIEW enviando notificação in-app para analista responsável listando dados básicos da unidade comunidade de origem e prazo de 7 dias úteis para concluir análise, quando unidade é aprovada transicionando para APPROVED enviando email celebratório para criador original informando aprovação parabenizando pela qualidade do cadastro e indicando próximos passos para vincular unidade a processo de legitimação incluindo documentos adicionais necessários, quando unidade é rejeitada transicionando para REJECTED enviando email detalhado para criador contendo justificativa textual completa de rejeição lista de problemas identificados orientações específicas de como corrigir cada problema e prazo de 15 dias para resubmissão antes de arquivamento automático por desistência tácita, e quando unidade é devolvida para correções em REQUIRES_CHANGES enviando notificação in-app e email para criador listando itens que precisam ser corrigidos prazo de 15 dias e instruções passo-a-passo de como editar unidade e resubmeter. Notificações relacionadas a processos de legitimação disparam quando LegitimationRequest é protocolado transicionando de DRAFT para SUBMITTED enviando email formal para beneficiário titular informando que solicitação foi protocolada com sucesso contendo número de protocolo no formato REURB-YYYY-NNNN prazo legal de 120 dias para conclusão conforme Lei 13.465/2017 e orientação de acompanhar status via portal web ou aplicativo mobile, quando processo é distribuído para analista em UNDER_ANALYSIS enviando notificação in-app para analista atribuído com dados completos do processo documentação anexada modalidade REURB-S ou REURB-E e prazo de 15 dias úteis para concluir análise documental e jurídica preliminar, quando análise identifica documentação incompleta transicionando para DOCUMENT_REVIEW enviando email e SMS para beneficiário listando documentos faltantes prazo de 30 dias para apresentação e aviso que não apresentação no prazo resultará em arquivamento do processo, quando beneficiário apresenta documentação complementar retornando processo para UNDER_ANALYSIS enviando notificação in-app para analista informando que processo está pronto para retomar análise interrompida, quando parecer técnico é solicitado transicionando para TECHNICAL_REVIEW enviando email para topógrafo ou engenheiro responsável contendo link para download de planta georreferenciada memorial descritivo e coordenadas GPS coletadas solicitando elaboração de parecer técnico em até 10 dias úteis, quando edital é publicado em PUBLIC_NOTICE enviando email e SMS para beneficiário informando que solicitação foi aprovada preliminarmente e edital será publicado em diário oficial com prazo de 30 dias para eventuais contestações de terceiros iniciando contagem regressiva de prazo, quando contestação é protocolada durante CONTESTATION_PERIOD enviando notificação urgente in-app para MANAGER responsável e email para beneficiário informando que terceiro apresentou impugnação anexando cópia da contestação e orientando que defesa será elaborada por equipe jurídica do órgão público, quando contestação é analisada em RESOLUTION enviando email para beneficiário informando decisão administrativa sobre contestação se foi rejeitada por improcedência acolhida parcialmente com ajustes ou acolhida integralmente com arquivamento do processo incluindo fundamentação jurídica detalhada, quando processo é aprovado definitivamente em APPROVED enviando email e SMS celebratórios para beneficiário informando que certidão de regularização fundiária será emitida em até 5 dias úteis e orientando próximos passos para apresentar certidão em cartório de registro de imóveis formalizar matrícula individualizada e consolidar transferência de propriedade, quando certidão é emitida enviando email com PDF da certidão anexado contendo QR code para verificação de autenticidade instruções de como apresentar em cartório e lista de documentos complementares necessários para registro, e quando processo é rejeitado em REJECTED enviando email formal para beneficiário contendo justificativa fundamentada de rejeição baseada em impedimento legal insuperável orientação sobre possibilidade de recurso administrativo prazo de 30 dias para recorrer e contatos de Defensoria Pública para assistência jurídica gratuita se elegível. Notificações relacionadas a prazos e SLA disparam quando processo de legitimação atinge 80% do prazo de 120 dias enviando alerta amarelo preventivo in-app para MANAGER responsável e email semanal para ADMIN do tenant listando processos próximos de vencimento com dias restantes e próximas ações requeridas, quando processo atinge 90% do prazo enviando alerta laranja urgente in-app para MANAGER e email diário para ADMIN solicitando ação imediata para concluir análise publicar edital ou emitir certidão evitando mora administrativa, quando processo excede prazo de 120 dias enviando alerta vermelho crítico in-app para MANAGER email diário para ADMIN e notificação semanal para SUPER_ADMIN informando violação de SLA legal com nome do responsável dias de atraso e obrigatoriedade de registrar justificativa administrativa formal, quando unidade em análise excede prazo de 7 dias úteis sem decisão enviando notificação in-app para analista responsável e email para MANAGER solicitando priorização ou reatribuição para outro analista disponível, quando importação em lote excede prazo de processamento enviando email para usuário que iniciou importação informando conclusão com sucesso quantidade de registros importados quantidade de erros detectados e link para download de relatório detalhado de validação, e quando sincronização offline falha repetidamente por mais de 48 horas enviando notificação in-app persistente para FIELD_AGENT orientando verificar conectividade resolver conflitos pendentes ou contactar suporte técnico se problema persistir. Notificações relacionadas a operações administrativas disparam quando novo usuário é criado no tenant enviando email de boas-vindas com credenciais temporárias link para primeiro acesso instruções de como alterar senha e tutorial em vídeo de como usar sistema, quando usuário é adicionado a time enviando notificação in-app informando que foi atribuído a equipe específica listando comunidades acessíveis membros do time e MANAGER responsável, quando comunidade é atribuída a time enviando notificação in-app para todos membros do time informando nova comunidade disponível para trabalho com link direto para visualizar mapa estatísticas e iniciar cadastramento de unidades, quando role de usuário é promovido enviando email formal parabenizando pela promoção informando novas permissões concedidas responsabilidades adicionais e orientação de consultar manual de procedimentos adequado ao novo papel, quando sessão está próxima de expirar (5 minutos restantes) enviando notificação in-app oferecendo renovar sessão automaticamente evitando perda de trabalho não salvo, quando tentativa de login falha 3 vezes consecutivas enviando email de alerta de segurança para usuário informando tentativas de acesso não autorizadas IP de origem timestamp e orientação de alterar senha se não reconhecer tentativas, quando dados sensíveis como CPF completo são acessados por ADMIN enviando log de auditoria para SUPER_ADMIN registrando quem acessou quando qual finalidade justificada e IP de origem garantindo accountability em acesso a dados pessoais conforme LGPD, e quando backup automático diário falha enviando alerta crítico para SUPER_ADMIN e equipe de infraestrutura solicitando verificação imediata de integridade de dados espaço em disco disponível e configurações de job de backup. Notificações relacionadas a beneficiários externos disparam quando beneficiário é cadastrado como titular de unidade pela primeira vez enviando SMS de boas-vindas informando que foi incluído em processo de regularização fundiária com nome da comunidade órgão responsável e telefone de contato para dúvidas, quando documentação complementar é solicitada enviando SMS com lista resumida de documentos prazo de 30 dias e orientação de comparecer presencialmente em endereço específico ou fazer upload via portal web se disponível, quando edital é publicado enviando SMS informando aprovação preliminar início de prazo de contestações e orientação de não realizar benfeitorias dispendiosas até conclusão definitiva do processo, quando certidão é emitida enviando SMS celebratório informando emissão de certidão e orientação de comparecer em local específico para retirar documento original assinado trazendo documentos pessoais atualizados, e quando processo é rejeitado enviando SMS informando decisão desfavorável com orientação de comparecer presencialmente para receber justificativa detalhada por escrito e ser orientado sobre possibilidade de recurso ou solução alternativa. Configurações de preferências de notificação permitem cada usuário customizar quais tipos de notificação deseja receber por qual canal onde por padrão todos usuários recebem notificações críticas de prazo e mudanças de status por todos canais mas podem optar por desabilitar notificações não urgentes de progresso ou estatísticas, beneficiários externos não podem desabilitar notificações SMS ou email de mudanças de status de seus processos garantindo que sejam informados mesmo se não acessarem sistema regularmente, ADMIN pode configurar templates de email personalizados por tenant incluindo logo marca cores e textos customizados mantendo tom e linguagem adequados ao contexto institucional do órgão público, frequência de envio de notificações recorrentes como alertas de prazo pode ser ajustada entre diária semanal ou quinzenal conforme preferência de MANAGER responsável evitando fadiga de notificações, e horário de envio de notificações não urgentes é restrito a horário comercial entre 8h e 18h em dias úteis evitando incomodar usuários fora de expediente enquanto notificações urgentes de prazo excedido ou falha crítica podem ser enviadas a qualquer momento. Sistema de retry automático garante que notificações email ou SMS que falharam por indisponibilidade temporária de servidor de email ou operadora de telefonia são reenviadas automaticamente até 3 vezes com intervalo de 15 minutos entre tentativas, falhas definitivas após 3 tentativas são registradas em log de notificações falhadas com motivo do erro permitindo ADMIN identificar problemas de configuração ou bloqueios de spam, notificações in-app são armazenadas permanentemente no banco de dados permitindo usuário visualizar histórico completo mesmo notificações antigas já lidas ou descartadas, e métricas de engajamento com notificações são coletadas incluindo taxa de abertura de emails taxa de clique em links de ação e tempo médio entre envio de notificação e resposta do usuário permitindo otimização contínua de conteúdo e timing de notificações.

**Notificações - Unidades habitacionais:**

| Evento | Canal | Destinatário | Conteúdo |
|--------|-------|--------------|----------|
| DRAFT → PENDING_ANALYSIS | Email | Criador (FIELD_AGENT) | Confirmação submissão, protocolo, prazo 7 dias |
| Atribuída IN_REVIEW | In-app | Analista atribuído | Dados unidade, comunidade, prazo 7 dias |
| IN_REVIEW → APPROVED | Email | Criador | Parabéns, próximos passos legitimação |
| IN_REVIEW → REJECTED | Email | Criador | Justificativa detalhada, como corrigir, prazo 15 dias |
| IN_REVIEW → REQUIRES_CHANGES | Email + In-app | Criador | Lista correções, instruções, prazo 15 dias |

**Notificações - Processos legitimação:**

| Evento | Canal | Destinatário | Conteúdo |
|--------|-------|--------------|----------|
| DRAFT → SUBMITTED | Email | Beneficiário titular | Protocolo REURB-YYYY-NNNN, prazo 120 dias Lei 13.465 |
| SUBMITTED → UNDER_ANALYSIS | In-app | Analista atribuído | Dados processo, docs, modalidade, prazo 15 dias |
| UNDER_ANALYSIS → DOCUMENT_REVIEW | Email + SMS | Beneficiário | Docs faltantes, prazo 30 dias, risco arquivamento |
| Docs apresentados | In-app | Analista | Processo pronto para retomar análise |
| UNDER_ANALYSIS → TECHNICAL_REVIEW | Email | Topógrafo/engenheiro | Download planta, memorial, prazo 10 dias |
| TECHNICAL_REVIEW → PUBLIC_NOTICE | Email + SMS | Beneficiário | Aprovação preliminar, edital 30 dias |
| Contestação protocolada | In-app + Email | MANAGER + Beneficiário | Notificação impugnação, cópia contestação |
| Contestação analisada | Email | Beneficiário | Decisão administrativa, fundamentação jurídica |
| RESOLUTION → APPROVED | Email + SMS | Beneficiário | Certidão em 5 dias, próximos passos cartório |
| Certidão emitida | Email com PDF | Beneficiário | Certidão anexada, QR code, instruções registro |
| RESOLUTION → REJECTED | Email | Beneficiário | Justificativa, recurso 30 dias, contato Defensoria |

**Notificações - Prazos e SLA:**

| Situação | Canal | Destinatário | Frequência |
|----------|-------|--------------|------------|
| 80% prazo 120 dias (24 dias restantes) | In-app + Email | MANAGER | Semanal |
| 90% prazo 120 dias (12 dias restantes) | In-app + Email | MANAGER + ADMIN | Diário |
| 100% prazo excedido | In-app + Email | MANAGER + ADMIN + SUPER_ADMIN | Diário (crítico) |
| Unidade >7 dias sem decisão | In-app + Email | Analista + MANAGER | Único |
| Importação lote concluída | Email | Usuário iniciador | Único |
| Sync offline falha >48h | In-app persistente | FIELD_AGENT | Contínuo até resolver |

**Notificações - Operações administrativas:**

| Evento | Canal | Destinatário | Conteúdo |
|--------|-------|--------------|----------|
| Novo usuário criado | Email | Novo usuário | Credenciais temporárias, tutorial vídeo |
| Adicionado a time | In-app | Usuário | Comunidades acessíveis, membros time |
| Comunidade atribuída | In-app | Todos membros time | Nova comunidade, link mapa |
| Role promovido | Email | Usuário | Novas permissões, responsabilidades |
| Sessão expirando (5min) | In-app | Usuário ativo | Oferta renovar automaticamente |
| 3 logins falhados | Email | Usuário | Alerta segurança, IPs, orientação senha |
| Acesso dados sensíveis | Log auditoria | SUPER_ADMIN | Quem, quando, finalidade, IP |
| Backup diário falhou | Email crítico | SUPER_ADMIN + Infra | Verificação imediata integridade |

**Notificações - Beneficiários externos:**

| Evento | Canal | Conteúdo |
|--------|-------|----------|
| Cadastrado titular pela 1ª vez | SMS | Boas-vindas, comunidade, órgão, contato |
| Docs complementares solicitados | SMS | Lista docs, prazo 30 dias, comparecimento/upload |
| Edital publicado | SMS | Aprovação preliminar, prazo 30 dias contestações |
| Certidão emitida | SMS | Retirada presencial, local, docs necessários |
| Processo rejeitado | SMS | Decisão desfavorável, comparecimento justificativa |

**Preferências customizáveis:**

- Usuários podem desabilitar notificações não urgentes
- Beneficiários NÃO podem desabilitar mudanças de status
- ADMIN customiza templates email (logo, cores, texto)
- Frequência alertas prazo: diária/semanal/quinzenal
- Horário envio: 8h-18h dias úteis (urgentes: qualquer horário)

**Sistema retry automático:**

- Email/SMS falhados: até 3 tentativas, intervalo 15min
- Falhas definitivas: log notificações falhadas (motivo erro)
- In-app: armazenadas permanentemente (histórico completo)
- Métricas engajamento: taxa abertura, taxa clique, tempo resposta

**Relacionamento com Domain Model:**

- Dispara: `DOMAIN-MODEL/EVENTS/` (todos 19 eventos disparam notificações)
- Implementa: Listeners para domain events (async background jobs)
- Templates: Armazenados em banco, customizáveis por tenant

**Implementações por projeto:**

- Backend .NET: (caminho de implementação)
- Backend .NET: (caminho de implementação) (background)
- Backend .NET: (caminho de implementação) (Razor views)
- Frontend React: (caminho de implementação)
- Frontend React: (caminho de implementação)

---

**Última atualização:** 2025-01-06
**Status do arquivo**: Review
