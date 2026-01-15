---
modules: [GEOWEB]
epic: scalability
---

# UC-006-FE-001: Timeout de Geração

Fluxo de exceção do UC-006 Gerar Relatório de Comunidade ocorrendo no passo 11 durante processamento assíncrono do job quando worker executa etapas de geração (buscar dados calcular estatísticas gerar gráficos renderizar PDF) e excede timeout configurado de 10 minutos tipicamente causado por comunidade muito grande (>5000 unidades) com queries lentas sem índices adequados, geração de mapa complexo com milhares de geometrias sobrecarregando Puppeteer, ou contenção de recursos com múltiplos jobs concorrentes disputando CPU/memória, onde BullMQ monitora tempo de execução do job comparando Date.now() - job.processedOn com threshold 600000 ms detectando excesso, automaticamente marca job como failed interrompendo processamento via signal SIGTERM enviado ao worker prevenindo consumo infinito de recursos, salva erro em job.failedReason armazenando stack trace e timestamp para debug posterior, sistema detecta falha do job via listener BullMQ on('failed') disparando callback que busca user_id do payload carrega preferências de notificação e envia notificação push via WebSocket e/ou email com título "Erro ao Gerar Relatório" mensagem "A geração excedeu o tempo limite (10 minutos). Sugestões: Reduza o período selecionado, desmarque seções complexas (Mapa), ou entre em contato com suporte técnico" oferecendo ações clicáveis, usuário recebe notificação e decide entre Tentar Novamente com Menos Seções abrindo formulário pré-preenchido com parâmetros anteriores permitindo desmarcar Mapa de Situação que consome ~70% do tempo de processamento, Reduzir Período ajustando date_range para últimos 3 meses ao invés de ano completo diminuindo volume de dados processados, ou Contatar Suporte abrindo ticket com detalhes do erro anexando job_id para investigação técnica de possíveis otimizações query ou aumento de timeout para casos específicos, garantindo sistema não trava indefinidamente e usuário recebe feedback claro com soluções práticas ao invés de espera sem resposta típica de jobs travados.

**Ponto de Desvio:** Passo 11 do UC-006 (durante processamento do worker)

**Retorno:** Job cancelado, usuário notificado com sugestões de ajuste e retry

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
