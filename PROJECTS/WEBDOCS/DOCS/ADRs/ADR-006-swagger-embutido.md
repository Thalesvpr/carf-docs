# ADR-006: Swagger Embutido na Seção Dev

Decisão integrando Swagger UI interativo na seção /dev/swagger/ justificada por centralizar documentação de API no mesmo portal que demais documentação evitando navegação entre múltiplos sites, permitir try-it-out autenticado usando token JWT real do desenvolvedor logado para testar endpoints sem configurar ferramentas externas, e manter consistência visual com restante do portal usando tema customizado.

Implementação via componente Astro que carrega swagger-ui-dist renderizando especificação obtida via fetch do endpoint /swagger.json da GEOAPI. Token JWT do usuário logado é automaticamente configurado como authorization header para requisições de teste. Componente só renderiza se usuário tem role dev, caso contrário mostra mensagem de acesso negado.

Especificação OpenAPI é source of truth mantida na GEOAPI e gerada automaticamente dos controllers .NET via Swashbuckle. WEBDOCS apenas consome e renderiza sem duplicar definições. Atualização automática quando GEOAPI é atualizada sem necessidade de redeploy do WEBDOCS.

Alternativas rejeitadas: Swagger hospedado separadamente (fragmentação), documentação de API estática (perde interatividade), ReDoc (sem try-it-out), Postman público (complexidade desnecessária).

---

**Data:** 2026-01-17
**Status:** Aprovado
**Decisor:** Equipe de Arquitetura
**Última atualização:** 2026-01-17
**Status do arquivo**: Review
