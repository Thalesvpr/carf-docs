---
modules: [GEOWEB]
epic: maintainability
---

# RF-057: Aprovar Unidade

O sistema deve permitir que usuários com perfil MANAGER aprovem unidades que estejam no status PENDING_APPROVAL, onde a interface GEOWEB exibe botão de aprovação visível apenas para gestores ao visualizar detalhes de unidades pendentes. Durante o processo de aprovação, o gestor pode opcionalmente adicionar comentário explicando os motivos da aprovação ou destacando aspectos positivos do cadastro, garantindo documentação do processo decisório. Ao confirmar a aprovação, o sistema altera automaticamente o status da unidade para APPROVED, registra a ação no histórico de auditoria incluindo timestamp e usuário responsável, e dispara notificação automática ao usuário que criou a unidade informando sobre a aprovação. A notificação inclui link direto para a unidade aprovada e, caso exista, o comentário do gestor, permitindo que o analista tenha feedback sobre seu trabalho e acesse rapidamente o registro aprovado para futuras referências ou complementações de dados.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
