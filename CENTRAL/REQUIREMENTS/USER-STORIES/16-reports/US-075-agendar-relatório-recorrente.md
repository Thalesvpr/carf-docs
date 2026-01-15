---
modules: [GEOAPI, GEOWEB]
epic: compatibility
---

# US-075: Agendar Relatório Recorrente

Como gestor, quero agendar geração e envio automático de relatórios em frequência recorrente (diária semanal mensal) para que acompanhamento contínuo de indicadores seja garantido sem necessidade de gerar manualmente a cada período, onde a funcionalidade deve permitir configuração de frequência de execução (DIÁRIO SEMANAL MENSAL), garantindo envio automático por email com relatório anexado para lista configurável de destinatários, permitindo gerenciamento completo de agendamentos incluindo criação edição e cancelamento de schedules ativos. Esta funcionalidade é implementada pelo módulo GEOWEB com interface de agendamento consumindo GEOAPI através do endpoint POST /api/reports/schedules que persiste configuração e aciona job scheduler backend (Hangfire Quartz ou similar), integrada ao RF-205 (Agendamento de Relatórios) e UC-006 (Gerar Relatórios). Os critérios de aceitação incluem formulário de criação de agendamento solicitando tipo de relatório comunidade alvo e frequência desejada, opções de frequência incluindo DIÁRIO (todo dia em horário específico) SEMANAL (dia da semana específico) e MENSAL (dia do mês específico), configuração de lista de destinatários de email que receberão relatório automaticamente, seleção de formato de anexo (PDF Excel ou ambos) a ser enviado por email, ativação de agendamento criando job recorrente no scheduler backend que executa em horários configurados, geração automática do relatório na frequência especificada sem intervenção manual, envio de email com relatório anexado para todos destinatários configurados incluindo corpo de email descritivo, listagem de agendamentos ativos mostrando próxima execução prevista e histórico de execuções passadas, capacidade de editar agendamento existente alterando frequência destinatários ou formato, e opção de pausar ou cancelar agendamento definitivamente quando não for mais necessário. A rastreabilidade conecta esta user story ao RF-205 (Automação de Relatórios) UC-006 (Gerar Relatórios) e endpoint POST /api/reports/schedules, garantindo distribuição proativa e contínua de indicadores para stakeholders.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
