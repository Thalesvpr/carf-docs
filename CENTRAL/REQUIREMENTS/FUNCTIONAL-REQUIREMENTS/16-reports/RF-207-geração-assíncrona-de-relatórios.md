---
modules: [GEOWEB, REURBCAD]
epic: scalability
---

# RF-207: Geração Assíncrona de Relatórios

O sistema implementa processamento assíncrono para geração de relatórios complexos ou volumosos através de fila de jobs gerenciada por sistema como BullMQ ou similar, onde requisições de relatórios que demandam processamento intensivo são enfileiradas e executadas em background por workers dedicados sem bloquear interface do usuário ou consumir recursos do servidor web. Quando usuário solicita relatório que exigiria tempo de processamento superior a limite configurável (tipicamente 30 segundos), o sistema imediatamente retorna resposta indicando que relatório está sendo gerado e fornece identificador único do job que permite acompanhamento posterior, permitindo que usuário continue trabalhando normalmente em outras tarefas enquanto processamento ocorre em segundo plano. Ao concluir geração do relatório, o sistema envia notificação automática ao usuário através de múltiplos canais incluindo notificação in-app exibida quando usuário estiver autenticado e email com link direto para download, garantindo que usuário seja prontamente informado sobre disponibilidade do documento solicitado mesmo se tiver saído do sistema durante processamento. O arquivo gerado é armazenado temporariamente em storage seguro com link de download válido por período configurável (tipicamente 7 dias), após o qual arquivo é automaticamente removido para liberar espaço de armazenamento, equilibrando conveniência de acesso com gestão eficiente de recursos computacionais.

---

**Última atualização:** 2025-12-30
