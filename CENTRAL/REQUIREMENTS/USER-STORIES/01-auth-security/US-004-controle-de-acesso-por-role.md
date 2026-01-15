---
modules: [GEOAPI, GEOWEB]
epic: security
---

# US-004: Controle de Acesso por Role

Como administrador, quero que usuários vejam apenas funcionalidades do seu role para que dados sensíveis sejam protegidos, onde o sistema implementa uma hierarquia de 6 roles distintos (SUPER_ADMIN, ADMIN, MANAGER, ANALYST, FIELD_AGENT, VIEWER) com permissões granulares específicas para cada nível, garantindo que cada usuário tenha acesso apenas às funcionalidades e dados apropriados ao seu papel no sistema. O cenário principal de uso envolve a verificação contínua de permissões tanto no frontend quanto no backend, onde elementos de interface como menus, botões e seções são dinamicamente ocultados quando o role do usuário é insuficiente, permitindo uma experiência limpa onde apenas opções acessíveis são visíveis, enquanto no backend todas as APIs validam o role antes de executar operações e retornam HTTP 403 Forbidden quando o role é inadequado. Os critérios de aceitação incluem a implementação completa dos 6 roles com suas respectivas permissões claramente definidas, a ocultação automática de menus e botões quando o role do usuário é insuficiente para acessá-los, a validação rigorosa nas APIs onde requisições com role inadequado retornam erro 403, e a execução bem-sucedida de testes automatizados que validam cada role em diferentes cenários de acesso. Esta funcionalidade é implementada pelos módulos GEOAPI (middleware de autorização e decorators de role) e GEOWEB (guards de rota e diretivas de permissão), garantindo rastreabilidade com RF-006 (Controle de Acesso Baseado em Roles) e UC-001 (Caso de Uso de Autenticação), onde a segurança em camadas assegura que mesmo tentativas de bypass do frontend são bloqueadas no backend, incluindo logging de todas as tentativas de acesso negado para monitoramento de segurança.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Pronto
