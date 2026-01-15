---
modules: [GEOAPI, GEOWEB]
epic: compatibility
---

# US-006: Revogar API Key

Como administrador, quero revogar API keys comprometidas para que acessos não autorizados sejam bloqueados, onde a revogação imediata invalida permanentemente uma chave de API previamente emitida, garantindo que qualquer sistema ou integração utilizando essa chave seja instantaneamente bloqueado de fazer novas requisições ao sistema. O cenário principal de uso ocorre quando um administrador identifica uma API key que foi comprometida, vazada, ou simplesmente não é mais necessária, permitindo que ele acesse o painel de gerenciamento de API keys, localize a chave específica na lista, e execute a ação de revogação que marca a key como inválida no banco de dados com timestamp de revogação. Os critérios de aceitação incluem a revogação imediata onde requisições subsequentes usando a key revogada são instantaneamente rejeitadas, o registro completo em audit log incluindo quem revogou, quando, e opcionalmente o motivo da revogação, e a validação de que todas as requests subsequentes usando a key revogada retornam HTTP 401 Unauthorized com mensagem clara indicando que a API key é inválida ou foi revogada. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint DELETE /api/auth/api-keys/{id} e middleware de validação de API keys) e GEOWEB (interface de lista e gerenciamento de keys com botão de revogação), garantindo rastreabilidade com RF-003 (Gestão de API Keys), onde o histórico completo de criação e revogação de cada key é mantido para fins de auditoria e compliance, incluindo notificações opcionais para administradores quando keys são revogadas e tratamento gracioso de casos onde integrações ativas são afetadas pela revogação.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Pronto
