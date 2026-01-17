---
modules: [GEOAPI]
epic: security
---

# US-002: Renovar Token Automaticamente

Como usuário com sessão ativa, quero que meu token seja renovado automaticamente para que eu não perca meu trabalho por sessão expirada, onde o sistema monitora constantemente o tempo de expiração do access token e executa o processo de refresh automaticamente 5 minutos antes da expiração prevista, garantindo uma experiência contínua sem interrupções perceptíveis ao usuário. O cenário principal de uso ocorre em background enquanto o usuário está trabalhando no sistema, permitindo que o mecanismo de renovação silenciosa utilize o refresh token armazenado para obter um novo access token através do endpoint de refresh do Keycloak, onde todo o processo acontece de forma transparente sem requerer interação do usuário. Os critérios de aceitação incluem a execução do refresh token 5 minutos antes da expiração do access token, a renovação completamente silenciosa onde o usuário não percebe a operação, o logout automático do usuário caso a renovação falhe (indicando sessão realmente expirada ou refresh token inválido), e o registro completo em logs de todas as operações de renovação para fins de auditoria e debugging. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint POST /api/auth/refresh) e GEOWEB (interceptor HTTP e serviço de gerenciamento de tokens), garantindo rastreabilidade com RF-004 (Renovação Automática de Tokens) e UC-001 (Caso de Uso de Autenticação), onde sessões longas permanecem ativas automaticamente e apenas falhas legítimas de autenticação resultam em logout, incluindo tratamento de casos edge como perda de conectividade temporária durante a renovação.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Review
