# SLA Rules (Regras de Acordo de Nível de Serviço)

Sistema estabelece acordos de nível de serviço (SLA - Service Level Agreement) definindo prazos máximos para execução de operações críticas garantindo qualidade responsividade e conformidade legal onde SLA primário de 120 dias corridos para processamento completo de processo de legitimação fundiária desde protocolo de solicitação até emissão de certidão ou decisão fundamentada de rejeição deriva diretamente de Lei 13.465/2017 artigo 34 estabelecendo penalidade de responsabilização administrativa para gestor público em caso de mora injustificada constituindo obrigação legal imperativa não meramente meta operacional. Processo de legitimação fundiária possui deadline_date calculado automaticamente ao transitar status de DRAFT para SUBMITTED adicionando 120 dias corridos à data de submissão sendo exibido em dashboard de gestão com indicadores visuais de progresso onde processos com menos de 30 dias para deadline são marcados com aviso amarelo, processos com menos de 15 dias são marcados com alerta laranja, e processos que excederam deadline são marcados com alerta vermelho crítico disparando notificações diárias por email para MANAGER responsável e semanais para ADMIN do tenant até resolução do atraso ou registro de justificativa administrativa. Prazos intermediários do workflow de legitimação estabelecem que transição de SUBMITTED para UNDER_ANALYSIS deve ocorrer em até 5 dias úteis permitindo distribuição de demanda entre analistas disponíveis sendo processos não atribuídos após 5 dias escalados automaticamente para MANAGER atribuir manualmente, análise documental e jurídica em estado UNDER_ANALYSIS deve completar em até 15 dias úteis incluindo solicitação de documentação complementar se necessário sendo prazo suspenso durante período em que processo está em DOCUMENT_REVIEW aguardando apresentação de documentos pelo beneficiário, revisão técnica especializada em TECHNICAL_REVIEW deve completar em até 10 dias úteis incluindo elaboração de parecer técnico validação de planta georreferenciada e verificação de conformidade com normas ABNT, publicação de edital em PUBLIC_NOTICE deve ocorrer em até 7 dias úteis após aprovação técnica incluindo elaboração de texto de edital envio para diário oficial e confirmação de publicação, período obrigatório de contestações em CONTESTATION_PERIOD tem duração fixa de 30 dias corridos conforme Lei 13.465/2017 não podendo ser abreviado mesmo se nenhuma contestação for protocolada garantindo direito de terceiros interessados, análise de contestações e resolução em RESOLUTION deve completar em até 20 dias úteis após encerramento de prazo de edital incluindo elaboração de parecer sobre cada contestação recebida e decisão fundamentada de manter ou alterar decisão de regularização, e emissão de certidão de regularização fundiária após aprovação final deve ocorrer em até 5 dias úteis incluindo geração de documento PDF assinatura digital por gestor responsável e registro em sistema de controle de certidões. SLA de operações de cadastro estabelece que unidade habitacional submetida para análise em estado PENDING_ANALYSIS deve ser atribuída a analista e transitar para IN_REVIEW em até 3 dias úteis balanceando carga de trabalho entre analistas do tenant, análise de unidade em IN_REVIEW deve completar com decisão de aprovar rejeitar ou solicitar correções em até 7 dias úteis considerando necessidade de conferência visual de geometria espacial contra ortofoto de referência validação de dados de titular e verificação de documentação anexada, unidade devolvida para correções em REQUIRES_CHANGES deve ser corrigida e resubmetida em até 15 dias corridos sendo automaticamente arquivada se prazo for excedido sem manifestação do responsável pelo cadastro original sinalizando desistência tácita, e aprovação ou rejeição definitiva de unidade deve ser notificada ao criador original em até 24 horas via email e notificação in-app contendo justificativa detalhada em caso de rejeição ou próximos passos em caso de aprovação. SLA de sincronização offline estabelece que dados baixados por aplicação mobile para trabalho em campo devem estar disponíveis para visualização e edição offline em até 2 minutos após solicitação de download considerando volume típico de 1 comunidade com até 500 unidades e conectividade 3G mínima, sincronização de dados coletados offline para servidor central quando conexão é restabelecida deve completar em até 5 minutos para volume típico de até 50 unidades criadas ou editadas offline, conflitos de sincronização detectados quando mesmo registro foi editado offline e online simultaneamente devem ser notificados ao usuário em até 30 segundos após tentativa de sincronização apresentando interface de resolução de conflito com opções de manter versão local manter versão servidor ou mesclar alterações manualmente, e falhas de sincronização por problemas de rede ou validação de dados devem ser registradas localmente e reprocessadas automaticamente em background a cada 15 minutos até sucesso ou até 48 horas quando sincronização é marcada como falhada permanentemente requerendo intervenção manual. SLA de processamento de importações em lote estabelece que importação de arquivo CSV ou shapefile contendo até 100 unidades habitacionais deve completar validação inicial em até 30 segundos identificando erros de formato campos obrigatórios faltantes ou valores inválidos, importação aprovada deve persistir dados no banco em até 2 minutos para 100 registros executando validações de negócio como CPF duplicado geometria sobreposta e área fora de limites legais, erros de validação detectados durante importação devem gerar relatório detalhado em formato CSV listando número da linha campo com erro tipo de erro e sugestão de correção sendo disponibilizado para download em até 1 minuto após conclusão de processamento, e importações de grande volume acima de 500 registros devem ser processadas em background job assíncrono notificando usuário via email quando concluída com sucesso ou quando interrompida por erros críticos. SLA de geração de relatórios estabelece que relatório gerencial de progresso de comunidade contendo estatísticas de unidades cadastradas aprovadas rejeitadas e em análise deve ser gerado em até 10 segundos considerando volume típico de até 1000 unidades, relatório de processos de legitimação listando status documentação anexada e prazos restantes deve ser gerado em até 15 segundos para até 200 processos ativos, export de shapefile de comunidade inteira incluindo geometrias de todas unidades aprovadas e atributos alfanuméricos deve completar em até 30 segundos para até 500 unidades gerando arquivo ZIP contendo .shp .shx .dbf .prj e readme explicativo, export de relatório PDF completo de comunidade incluindo mapa de localização estatísticas gráficos e tabelas de unidades deve completar em até 60 segundos utilizando template predefinido e dados atualizados do banco, e dashboards interativos com mapas de calor gráficos de progresso temporal e indicadores de desempenho devem carregar em até 5 segundos após seleção de comunidade utilizando dados cacheados atualizados a cada 15 minutos. SLA de disponibilidade do sistema estabelece uptime mínimo de 99.5% medido mensalmente equivalente a no máximo 3.6 horas de indisponibilidade não planejada por mês excluindo janelas de manutenção programada previamente comunicadas com 48 horas de antecedência, manutenções programadas devem ocorrer preferencialmente em finais de semana ou horários noturnos entre 22h e 6h minimizando impacto em usuários ativos e não devem exceder 4 horas de duração salvo atualizações críticas de segurança previamente aprovadas por ADMIN do tenant, tempo de resposta médio de requisições HTTP da API REST deve ser inferior a 500 milissegundos medido no percentil 95 considerando operações típicas de leitura e escrita excluindo operações complexas de análise espacial ou geração de relatórios que possuem SLA próprio, operações de leitura simples como GET de unidade por ID devem responder em até 100 milissegundos garantindo experiência responsiva em interface web, operações de escrita como POST ou PUT de unidade com validações de negócio devem completar em até 1 segundo incluindo persistência no banco validações síncronas e disparo de eventos assíncronos, e operações de análise espacial como cálculo de sobreposições entre 100 geometrias ou agregação de estatísticas de 1000 unidades devem completar em até 10 segundos utilizando índices espaciais e otimizações de query. SLA de suporte técnico estabelece que incidentes críticos bloqueando completamente uso do sistema por todos usuários devem ter tempo de primeira resposta de 1 hora e tempo de resolução de 4 horas durante horário comercial (9h-18h dias úteis) sendo escalados automaticamente para equipe de desenvolvimento se não resolvidos em 2 horas, incidentes graves afetando funcionalidade importante mas com workaround disponível devem ter tempo de primeira resposta de 4 horas e tempo de resolução de 1 dia útil, incidentes moderados com impacto limitado ou afetando apenas poucos usuários devem ter tempo de primeira resposta de 8 horas e tempo de resolução de 3 dias úteis, e solicitações de melhoria ou dúvidas sobre uso do sistema devem ter tempo de primeira resposta de 24 horas com resolução ou orientação fornecida em até 5 dias úteis. Monitoramento de SLA é automatizado através de jobs programados executando a cada hora verificando prazos de processos de legitimação unidades em análise e importações pendentes, alertas são disparados quando prazo está 80% consumido (alerta amarelo preventivo), 90% consumido (alerta laranja requerendo ação imediata), ou 100% excedido (alerta vermelho crítico com escalação automática), dashboard de SLA acessível por MANAGER e ADMIN exibe indicadores em tempo real de processos próximos de vencimento taxa de cumprimento de SLA por analista tempo médio de análise por tipo de operação e histórico de violações de SLA com justificativas registradas, e relatório mensal de performance de SLA é gerado automaticamente no primeiro dia útil de cada mês contendo estatísticas consolidadas gráficos de tendência comparação com meses anteriores e ações corretivas implementadas sendo enviado por email para ADMIN e gestores do órgão público responsável pelo tenant.

**SLA primário - Lei 13.465/2017:**

- **Legitimação completa**: 120 dias corridos (SUBMITTED → APPROVED/REJECTED)
- **Penalidade**: Responsabilização administrativa do gestor público por mora
- **Avisos automáticos**:
  - 🟡 Amarelo: <30 dias restantes
  - 🟠 Laranja: <15 dias restantes
  - 🔴 Vermelho: Prazo excedido (notificações diárias)

**Prazos intermediários - Workflow legitimação:**

| Transição | Prazo | Tipo | Observações |
|-----------|-------|------|-------------|
| SUBMITTED → UNDER_ANALYSIS | 5 dias úteis | Distribuição | Escalação automática se não atribuído |
| UNDER_ANALYSIS (análise) | 15 dias úteis | Análise | Suspenso durante DOCUMENT_REVIEW |
| TECHNICAL_REVIEW | 10 dias úteis | Revisão | Parecer técnico + validação planta |
| Publicação PUBLIC_NOTICE | 7 dias úteis | Edital | Elaboração + envio diário oficial |
| CONTESTATION_PERIOD | 30 dias corridos | Legal | Fixo, não pode ser abreviado |
| RESOLUTION (contestações) | 20 dias úteis | Análise | Parecer por contestação |
| Emissão certidão | 5 dias úteis | Certificação | Geração PDF + assinatura digital |

**SLA operações cadastro:**

| Operação | Prazo | Ação se excedido |
|----------|-------|------------------|
| Atribuir unidade PENDING → IN_REVIEW | 3 dias úteis | Balanceamento carga automático |
| Análise unidade IN_REVIEW | 7 dias úteis | Escalação para MANAGER |
| Correções REQUIRES_CHANGES | 15 dias corridos | Arquivamento automático (desistência) |
| Notificar aprovação/rejeição | 24 horas | Alerta para ADMIN |

**SLA sincronização offline:**

| Operação | Prazo | Volume típico |
|----------|-------|---------------|
| Download dados comunidade | 2 minutos | 1 comunidade, 500 unidades, 3G |
| Upload dados coletados | 5 minutos | 50 unidades editadas offline |
| Notificar conflitos | 30 segundos | Apresentar UI resolução |
| Retry automático falhas | 15 minutos | Até 48h, depois intervenção manual |

**SLA importações lote:**

| Operação | Prazo | Volume |
|----------|-------|--------|
| Validação inicial CSV/SHP | 30 segundos | Até 100 registros |
| Persistência dados | 2 minutos | 100 registros com validações |
| Relatório de erros | 1 minuto | CSV detalhado linha/campo/erro |
| Importações grandes (>500) | Background job | Notificação email conclusão |

**SLA relatórios e exports:**

| Tipo | Prazo | Descrição |
|------|-------|-----------|
| Relatório progresso comunidade | 10 segundos | Estatísticas até 1000 unidades |
| Relatório processos legitimação | 15 segundos | Até 200 processos ativos |
| Export shapefile | 30 segundos | 500 unidades + ZIP completo |
| Relatório PDF completo | 60 segundos | Mapa + gráficos + tabelas |
| Dashboard interativo | 5 segundos | Dados cacheados (refresh 15min) |

**SLA disponibilidade sistema:**

- **Uptime mínimo**: 99.5% mensal (máximo 3.6h indisponibilidade/mês)
- **Manutenção programada**: Finais de semana 22h-6h, máximo 4h, aviso 48h
- **Tempo resposta API**: <500ms (p95) para operações típicas
- **Leitura simples (GET)**: <100ms
- **Escrita com validações (POST/PUT)**: <1 segundo
- **Análise espacial complexa**: <10 segundos (100 geometrias)

**SLA suporte técnico:**

| Severidade | Primeira resposta | Resolução | Horário |
|------------|-------------------|-----------|---------|
| 🔴 Crítico (sistema parado) | 1 hora | 4 horas | 9h-18h dias úteis |
| 🟠 Grave (funcionalidade importante) | 4 horas | 1 dia útil | 9h-18h dias úteis |
| 🟡 Moderado (impacto limitado) | 8 horas | 3 dias úteis | 9h-18h dias úteis |
| 🔵 Melhoria/dúvida | 24 horas | 5 dias úteis | 9h-18h dias úteis |

**Monitoramento automático:**

- Jobs scheduled a cada hora verificando prazos
- Alertas em 80% (🟡), 90% (🟠), 100% (🔴) de consumo de prazo
- Dashboard tempo real para MANAGER/ADMIN
- Relatório mensal automático (primeiro dia útil) enviado por email

**Relacionamento com Domain Model:**

- Implementa: `DOMAIN-MODEL/ENTITIES/25-legitimation-request.md` (deadline_date field)
- Valida: `DOMAIN-MODEL/VALUE-OBJECTS/21-legitimation-status.md` (prazos por status)
- Eventos: Deadline approaching/exceeded events (notificações)

**Implementações por projeto:**

- Backend .NET: `PROJECTS/GEOAPI/SERVICES/SlaMonitoringService.cs`
- Backend .NET: `PROJECTS/GEOAPI/JOBS/DeadlineCheckJob.cs` (scheduled hourly)
- Frontend React: `PROJECTS/GEOWEB/COMPONENTS/dashboard/SlaIndicators.tsx`
- Frontend React: `PROJECTS/GEOWEB/COMPONENTS/legitimation/DeadlineWarning.tsx`

---

**Última atualização:** 2025-01-06
