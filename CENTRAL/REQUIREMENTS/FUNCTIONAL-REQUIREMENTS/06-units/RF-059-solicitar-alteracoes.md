---
modules: [REURBCAD]
epic: approval
---

# RF-059: Solicitar Alterações

O sistema deve permitir que gestores com perfil MANAGER solicitem alterações em unidades pendentes quando identificarem problemas que não justifiquem rejeição completa mas requeiram ajustes antes da aprovação final. A solicitação de alterações inclui campo de texto detalhando as modificações necessárias, onde o gestor especifica quais campos precisam ser corrigidos, complementados ou validados, garantindo clareza sobre as expectativas. Ao confirmar a solicitação, o sistema altera o status da unidade para CHANGES_REQUESTED e envia notificação ao analista responsável incluindo a descrição das alterações solicitadas e link direto para edição do registro. O analista com perfil ANALYST pode então editar a unidade conforme orientações recebidas e reenviar para aprovação alterando o status novamente para PENDING_APPROVAL, reiniciando o ciclo de validação. Este mecanismo intermediário entre aprovação e rejeição otimiza o fluxo de trabalho colaborativo, permitindo iterações rápidas sem descontinuidade do processo e mantendo registro histórico de todas as solicitações e correções realizadas.

---

**Última atualização:** 2025-12-30
