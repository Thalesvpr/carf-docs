---
modules: [GEOWEB, REURBCAD]
epic: maintainability
---

# RF-081: Comentários em Unidade

O sistema deve permitir que usuários adicionem comentários e observações em unidades habitacionais criando thread colaborativo de comunicação assíncrona sobre cadastros específicos, onde cada comentário captura texto livre, timestamp de criação e identificação do usuário autor. A funcionalidade implementa thread cronológica ordenada mostrando comentários mais recentes primeiro ou em ordem de postagem conforme preferência do usuário, incluindo interface de resposta que permite criar comentários encadeados formando conversações estruturadas sobre aspectos específicos da unidade. Quando novo comentário é adicionado, sistema dispara notificações automáticas para usuários envolvidos com a unidade incluindo criador original, gestores responsáveis por aprovação e usuários que previamente comentaram no thread, garantindo que partes interessadas sejam informadas sobre discussões relevantes. Implementado nos módulos GEOWEB e GEOAPI com prioridade Should-have, este recurso facilita colaboração entre analistas e gestores permitindo esclarecimento de dúvidas, solicitação de informações complementares, registro de observações de campo e documentação de decisões tomadas durante processo de validação, criando histórico rico de comunicação contextualizada que complementa log técnico de auditoria com narrativa humana sobre evolução do cadastro.

---

**Última atualização:** 2025-12-30
