---
type: rf
status: rejected
description: "Formato inconsistente. RFs e RNFs misturados, duplicacao com BUSINESS-RULES. Stub de 9 linhas - incompleto."
updated: 2025-12-30
---

# RF-058: Rejeitar Unidade

O sistema deve permitir que usuários com perfil MANAGER rejeitem unidades inadequadas ou com problemas de cadastro, onde a rejeição exige obrigatoriamente o preenchimento de campo de justificativa explicando os motivos da não aprovação. A justificativa deve ser clara e detalhada, orientando o analista responsável sobre quais aspectos precisam ser corrigidos ou complementados para que a unidade possa ser reaprovada em nova submissão. Ao confirmar a rejeição, o sistema altera o status da unidade para REJECTED, registra a ação no histórico incluindo timestamp, gestor responsável e justificativa completa, e envia notificação automática ao usuário criador da unidade. A notificação inclui a justificativa da rejeição e link para edição da unidade, permitindo que o analista corrija os problemas identificados e reenvie para nova análise, garantindo um ciclo de feedback produtivo entre analistas e gestores no processo de validação de cadastros.
