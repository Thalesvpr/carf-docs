---
modules: [GEOAPI, GEOWEB]
epic: compatibility
---

# US-084: Configurar Tenant

Como super administrador do sistema, quero configurar dados institucionais e operacionais do tenant para que personalização organizacional seja aplicada, incluindo identidade visual, limites de recursos e configurações de comunicação. A funcionalidade deve permitir edição de informações corporativas incluindo nome da organização, CNPJ para identificação fiscal, e upload de logotipo institucional que será exibido na interface customizada do tenant. O sistema deve oferecer configuração de limites operacionais definindo número máximo de usuários permitidos no tenant, quota de armazenamento para documentos e geometrias, e thresholds de consumo de recursos computacionais. Adicionalmente, devem ser configuráveis parâmetros de comunicação incluindo servidor SMTP para envio de notificações por email, templates de mensagens personalizados com identidade da organização, e endereços de contato para suporte técnico. Os critérios de aceitação incluem campos editáveis para nome, CNPJ e logo com validação de formato e tamanho, configuração de limites incluindo max_users e max_storage_gb com validação de valores positivos, e seção de configurações de email incluindo host, porta, credenciais e remetente padrão. Esta User Story está relacionada ao RF-013 e é implementada através do endpoint PUT /api/tenants/{id} no backend GEOAPI, com painel administrativo no frontend GEOWEB permitindo super administradores personalizarem tenants no contexto do Epic 11: Administração. O status atual é implemented, com validação através de testes garantindo que apenas super administradores possam modificar configurações críticas de tenant.

---

**Última atualização:** 2025-12-30
