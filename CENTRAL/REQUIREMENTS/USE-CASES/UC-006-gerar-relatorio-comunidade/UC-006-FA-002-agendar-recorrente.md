---
modules: [GEOWEB, REURBCAD]
epic: compatibility
---

# UC-006-FA-002: Agendar Geração Recorrente

Fluxo alternativo do UC-006 Gerar Relatório de Comunidade desviando no passo 6 onde ao invés de gerar relatório uma única vez sob demanda, usuário marca checkbox Agendar Envio Recorrente expandindo formulário revelando campos adicionais de periodicidade oferecendo radio buttons (Semanal toda segunda-feira, Mensal dia 1 de cada mês, Trimestral primeiro dia do trimestre), campo de texto múltiplo para emails destinatários aceitando lista separada por vírgulas validando formato email via regex e limitando máximo 10 destinatários prevenindo spam, usuário preenche periodicidade selecionando opção desejada e informa emails de gestores municipais técnicos responsáveis coordenadores regionais que receberão relatório automaticamente, clica Agendar disparando validação verificando permissão agendamento restrita a MANAGER e ADMIN rejeitando ANALYST com erro 403 Forbidden, se autorizado sistema cria registro em tabela scheduled_reports armazenando user_id community_id report_config JSON com seções e formato, cron_expression calculada baseado em periodicidade selecionada (0 8 * * 1 para semanal segunda 8h, 0 8 1 * * para mensal dia 1 às 8h usando timezone tenant), recipient_emails array, active=true permitindo desabilitar sem deletar, sistema registra cron job usando node-cron ou BullMQ repeatable jobs configurando pattern de execução e associando handler que ao disparar no horário agendado executa fluxo completo do UC-006 gerando relatório com parâmetros salvos enviando email para cada destinatário via serviço SMTP (SendGrid AWS SES) com anexo PDF ou link para download e subject "Relatório Automático - Comunidade Vila Nova - 2025-12-30", exibe toast verde confirmação "Agendamento criado com sucesso. Próximo envio: Segunda-feira 08:00" mostrando data próxima execução calculada, usuário pode gerenciar agendamentos acessando menu Meus Agendamentos listando todos scheduled_reports do tenant com ações Editar Desativar Deletar permitindo ajustar periodicidade ou cancelar, relatórios gerados automaticamente registram audit log rastreando execution_date status success/failed recipient_count permitindo monitoramento e troubleshooting de falhas em envios recorrentes garantindo gestores sempre atualizados sobre progresso de regularização sem precisar requisitar manualmente economizando tempo e garantindo consistência de acompanhamento.

**Ponto de Desvio:** Passo 6 do UC-006 (checkbox de agendamento antes de gerar)

**Retorno:** Agendamento criado, relatório gerado e enviado automaticamente no período configurado

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
