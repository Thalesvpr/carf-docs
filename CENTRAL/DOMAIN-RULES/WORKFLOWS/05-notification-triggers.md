---
type: leaf
status: approved
updated: 2026-01-25
---

# Notification Triggers

Sistema de notificacoes automaticas disparadas por eventos de dominio atraves de tres canais: email para comunicacoes detalhadas com links e anexos, SMS para alertas urgentes de prazo, e in-app para atualizacoes em tempo real. Beneficiarios externos recebem SMS obrigatorio em mudancas de status.

Unidades disparam notificacoes ao submeter para analise (email de confirmacao com protocolo), ao atribuir analista (in-app), ao aprovar (email celebratorio), ao rejeitar (email com justificativa e prazo 15 dias para correcao) e ao solicitar alteracoes (email com lista de correcoes).

## Legitimacao e Prazos

Processos notificam beneficiario ao protocolar (email com numero REURB-YYYY-NNNN e prazo 120 dias), ao solicitar documentos (email e SMS com prazo 30 dias), ao publicar edital (SMS informando aprovacao preliminar), ao receber contestacao (email com copia da impugnacao) e ao emitir certidao (email com PDF anexado e instrucoes de registro em cartorio).

Alertas de SLA disparam semanalmente em 80% do prazo, diariamente em 90% e criticamente em 100% com escalacao para ADMIN. Preferencias permitem customizar frequencia exceto notificacoes obrigatorias de status para beneficiarios.
