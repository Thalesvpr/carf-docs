# ADR-005: Status Page com Health Checks

Decisão implementando página /status/ mostrando health check tempo real dos serviços CARF justificada por transparência com usuários sobre disponibilidade do sistema especialmente importante para órgãos públicos que dependem do CARF, redução de tickets de suporte quando usuários podem verificar se problema é do sistema ou local, e histórico de incidentes documentando manutenções programadas e falhas passadas.

Implementação via componente Astro que executa fetch para endpoints /health de cada serviço (GEOAPI, PostgreSQL proxy, Keycloak, MinIO) no servidor durante SSR. Resposta inclui status (up/down/degraded), latência, e timestamp do check. Página atualiza via polling client-side a cada 30 segundos para usuários que permanecem na página.

Serviços monitorados: GEOAPI verificando endpoint /health que testa conexão com banco e serviços dependentes, Keycloak verificando /.well-known/openid-configuration, MinIO verificando endpoint de health nativo. Histórico de incidentes mantido em arquivo JSON ou collection do Decap CMS permitindo edição via interface visual.

Alternativas rejeitadas: serviço externo tipo Statuspage.io (custo, dependência externa), apenas logs internos (sem transparência para usuários), monitoring complexo (overengineering para necessidade atual).

---

**Data:** 2026-01-17
**Status:** Aprovado
**Decisor:** Equipe de Arquitetura + Operações
**Última atualização:** 2026-01-17
**Status do arquivo**: Review
