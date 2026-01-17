# INTEGRATIONS

Integrações do GEOAPI com sistemas externos abstraídas por interfaces no Domain e implementadas no Infrastructure isolando detalhes técnicos de comunicação HTTP, autenticação e tratamento erros. KeycloakClient implementa ICurrentUser e IPermissionChecker comunicando via Admin API REST para validar tokens JWT, obter dados usuário autenticado (sub, email, roles) e verificar permissões RBAC injetadas em cada request. CpfValidationClient consome APIs Receita Federal validando CPF/CNPJ verificando situação cadastral, nome contribuinte e status regularidade fiscal com cache Redis para reduzir chamadas externas e retry policy Polly para transient failures. GeoCodingClient integra serviços de geocoding transformando endereços em coordenadas lat/lon e vice-versa validando CEPs via ViaCEP API. WmsClient comunica com servidores WMS externos (IBGE, prefeituras) via GetCapabilities/GetMap verificando disponibilidade layers e proxy imagens para frontend. NotificationService envia notificações push via Firebase Cloud Messaging, emails via SendGrid SMTP e webhooks para sistemas legados quando eventos críticos ocorrem (legitimação aprovada, documento enviado).

## Arquivos Principais (a criar)

**Keycloak:**
- 01-keycloak-client.md - Admin API para usuários/roles
- 02-jwt-validator.md - Validação tokens OAuth2
- 03-permission-checker.md - Verificação RBAC

**Validação Externa:**
- 04-cpf-validation-client.md - API Receita Federal
- 05-geocoding-client.md - ViaCEP e geocoding

**GeoServices:**
- 06-wms-client.md - Comunicação servidores WMS

**Notificações:**
- 07-notification-service.md - FCM/SendGrid/Webhooks
- 08-email-templates.md - Templates HTML emails

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Incompleto
Descrição: Falta seção GENERATED com índice automático; Muitas listas com bullets (8) antes do rodapé - considerar converter para parágrafo denso.
