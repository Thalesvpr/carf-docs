---
modules: [GEOAPI, GEOWEB]
epic: security
---

# RF-005: Validação JWT em Todas Requisições

GEOAPI deve validar JWT (JSON Web Token) em todas requisições protegidas garantindo autenticidade e integridade do token onde verificação de assinatura JWT ocorre utilizando chave pública RSA obtida de endpoint /realms/{realm}/protocol/openid-connect/certs do Keycloak validando que token não foi adulterado, validação de claims obrigatórios inclui verificação de exp (expiration time) garantindo token não expirou iss (issuer) confirmando que token foi emitido pelo Keycloak autorizado aud (audience) validando que token destinado à API correta e outros claims relevantes como sub (subject identificador único do usuário) tenant_id roles conforme necessidade do negócio, rejeição de tokens inválidos deve retornar HTTP 401 Unauthorized com corpo de resposta JSON contendo mensagem descritiva do erro (ex: "Token expirado" "Assinatura inválida" "Emissor não confiável") permitindo cliente identificar causa da falha e tomar ação apropriada como renovação de token ou solicitação de re-autenticação.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
