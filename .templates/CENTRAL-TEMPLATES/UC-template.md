---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: "category"
---

# UC-NNN-nome-caso-uso

Descrição objetivo caso uso atores envolvidos roles ADMIN MANAGER ANALYST FISCAL FIELD_AGENT CITIZEN sistemas interagindo GEOAPI backend GEOWEB frontend REURBCAD mobile Keycloak SSO PostgreSQL database Redis cache RabbitMQ messaging pré-condições estado inicial esperado usuário autenticado role específica permissions adequadas tenant configurado database seed data existente unidades holders communities pós-condições garantias após execução bem-sucedida entity criada atualizada status transitado events publicados handlers executados side effects occurred emails enviados notifications pushed cache invalidated audit logs escritos consistency eventual garantida fluxo principal passos sequenciais numerados 1 usuário navega tela específica 2 clica botão ação 3 sistema valida input sanitiza dados 4 executa business logic domain aggregate methods 5 persiste changes database transaction ACID 6 publica domain events MediatR async handlers 7 retorna response HTTP 200 201 payload JSON entity atualizado 8 frontend atualiza UI Redux state React components re-render validações regras negócio aplicadas CPF válido ownership 100% polygon fechado primary holder único integrações externas chamadas Serpro CPF validation ViaCEP address geocoding Nominatim coordinates retry exponential backoff circuit breaker fallback graceful degradation.

## Fluxos Alternativos

- **Alt 1**: Quando usuário escolhe opção diferente filtro adicional ordenação customizada visualização alternativa mapa lista tabela grid cards sistema comporta variação mantendo objetivo alcançado resultado equivalente funcionalmente satisfazendo requisito negócio use case completado sucesso.

## Fluxos de Exceção

- **Exc 1**: Erro validação campo obrigatório faltando formato inválido sistema retorna HTTP 422 Unprocessable Entity payload JSON errors array field message descritivo frontend exibe toast notification error message vermelho ícone alerta usuário corrige input retry.
- **Exc 2**: Autenticação expirada token JWT expired sistema retorna HTTP 401 Unauthorized frontend interceptor Axios detecta tenta refresh token automático usando refresh_token stored localStorage secure HttpOnly cookie renovando access_token retry original request transparentemente usuário unaware se refresh falha redireciona login page Keycloak SSO.
- **Exc 3**: Network timeout backend indisponível database down sistema exibe erro genérico amigável usuário "Sistema temporariamente indisponível, tente novamente" retry button exponential backoff attempts 3 logging error Sentry alerting ops team PagerDuty incident response.
- **Exc 4**: Concurrent update version mismatch optimistic locking Entity Framework RowVersion column conflict detected sistema retorna HTTP 409 Conflict mensagem "Registro foi modificado por outro usuário, recarregue e tente novamente" frontend recarrega entity atualizado merge changes se possível ou solicita usuário resolver conflict manual.

## Regras de Negócio

- RN-001: CPF único por tenant
- RN-002: Ownership percentages totalizando 100%
- RN-003: Apenas 1 holder primary por unit
- RN-004: Polygon fechado mínimo 3 pontos área positiva
- RN-005: Status transitions workflow válidas Draft->Pending->InReview->Approved

## Rastreabilidade

- **Requisitos Funcionais**: RF-NNN, RF-MMM
- **User Stories**: US-NNN, US-MMM
- **Technical Specs**: [links implementação código]

---

**Última atualização:** YYYY-MM-DD
