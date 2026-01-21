---
status: review
updated: 2026-01-21
---

# ADR-002: Conteúdo Protegido por Role Dev

Decisão implementando seção /dev/ protegida por autenticação Keycloak acessível apenas para usuários com role dev justificada por necessidade de documentação técnica interna sensível (arquitetura, padrões, debug) que não deve ser pública, Swagger interativo com try-it-out usando token real do desenvolvedor que exporia endpoints internos se público, e separação clara entre documentação de usuário (pública) e documentação de desenvolvedor (protegida).

Implementação usa hybrid rendering do Astro com adapter Vercel para SSR nas rotas /dev/*. Middleware intercepta requisições verificando JWT token do Keycloak e presença da role dev no claim realm_access.roles. Usuários sem role dev recebem redirect para página de erro 403 explicando necessidade de acesso.

Role dev é transversal não participando da hierarquia operacional (field-collector < analyst < admin < super-admin). Desenvolvedor precisa receber role dev explicitamente mesmo sendo admin ou super-admin garantindo princípio de privilégio mínimo.

Alternativas rejeitadas: tudo público (expõe info sensível), auth por IP (inflexível para devs remotos), senha compartilhada (sem auditabilidade).
