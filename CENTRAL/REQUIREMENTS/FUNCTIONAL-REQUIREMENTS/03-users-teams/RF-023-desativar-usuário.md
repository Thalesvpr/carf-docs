---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: security
---

# RF-023: Desativar Usuário

Usuários com role ADMIN podem desativar usuário utilizando soft delete onde usuário marcado como inativo através de flag is_active=false sem exclusão física de registro preservando integridade referencial com dados criados/modificados por usuário, login imediatamente bloqueado para usuário desativado onde tentativas subsequentes de autenticação retornam mensagem "Usuário inativo. Contate o administrador." impedindo acesso a sistema e APIs mesmo que credenciais estejam corretas, dados históricos preservados integralmente incluindo unidades cadastradas documentos anexados aprovações realizadas e logs de auditoria mantendo rastreabilidade de ações passadas e permitindo reativação futura sem perda de contexto ou histórico operacional, implementação em módulos GEOWEB e GEOAPI com sincronização para Keycloak desabilitando conta no Identity Provider adicionalmente a marcação local garantindo bloqueio efetivo em todas camadas de autenticação e autorização.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
