---
modules: [GEOAPI, GEOWEB]
epic: security
---

# RF-004: Refresh Token Automático

Sistema deve renovar automaticamente tokens de acesso expirados utilizando refresh_token sem requerer re-autenticação do usuário onde detecção de token expirado ocorre através de verificação do claim exp no JWT ou captura de resposta HTTP 401 Unauthorized de API, processo de renovação transparente para usuário implementado via interceptor HTTP ou middleware que captura falha de autenticação tenta renovar token usando refresh_token armazenado e reexecuta requisição original com novo access_token obtido, logout forçado deve ocorrer se refresh_token for inválido expirado ou revogado indicando necessidade de re-autenticação completa onde sistema limpa tokens armazenados localmente e redireciona usuário para tela de login com mensagem informativa sobre expiração de sessão, implementação aplicável a todos módulos GEOAPI GEOWEB REURBCAD GEOGIS garantindo experiência de usuário consistente e minimizando interrupções durante uso prolongado da plataforma.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
