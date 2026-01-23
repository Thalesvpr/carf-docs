---
type: adr
status: rejected
updated: 2026-01-21
description: "Granularidade errada. Config de OAuth2 por client e detalhe de implementacao Keycloak, nao decisao arquitetural. Mover para PROJECTS/KEYCLOAK. Contem blocos de codigo."
---

# ADR-002: OAuth2 Flows por Tipo de Client

## Contexto

O ecossistema CARF possui diferentes tipos de aplicacoes cliente: SPAs web (GEOWEB, ADMIN, WebDocs), aplicacoes mobile (REURBCAD), e integracao server-to-server (GEOGIS plugin QGIS). Cada tipo de cliente tem caracteristicas de seguranca distintas que determinam qual OAuth2 flow e mais apropriado.

Principais consideracoes: SPAs nao podem armazenar secrets de forma segura pois codigo JavaScript e publico, mobile apps tem secure storage mas devem usar app-native flows, backends podem usar client_secret pois codigo fica no servidor.

## Decisao

Definir **OAuth2 flow padrao por tipo de cliente** conforme tabela:

| Tipo de Cliente | Aplicacoes | OAuth2 Flow | Motivo |
|:----------------|:-----------|:------------|:-------|
| SPA (Public Client) | GEOWEB, ADMIN, WebDocs | Authorization Code + PKCE | Sem client_secret exposto |
| Mobile (Public Client) | REURBCAD | Authorization Code + PKCE | App-native com secure storage |
| Backend Service (Confidential) | GEOGIS | Client Credentials | M2M sem contexto de usuario |

### Authorization Code + PKCE (SPAs e Mobile)

Recomendado pela RFC 8252 e OAuth 2.1 draft para clientes publicos.

**Fluxo:**
1. App gera `code_verifier` aleatorio (43-128 chars)
2. App calcula `code_challenge = BASE64URL(SHA256(code_verifier))`
3. App redireciona para Keycloak com code_challenge
4. Usuario autentica e consente
5. Keycloak redireciona com authorization code
6. App troca code por tokens enviando code_verifier original
7. Keycloak valida code_verifier contra code_challenge
8. Tokens emitidos (access_token, refresh_token, id_token)

**Seguranca**: PKCE previne authorization code interception - atacante que captura o code nao consegue troca-lo sem o code_verifier.

### Client Credentials (Backend Services)

Para comunicacao machine-to-machine sem contexto de usuario humano.

**Fluxo:**
1. Service faz POST direto para token endpoint
2. Envia client_id e client_secret (Basic Auth ou form-encoded)
3. Keycloak valida credenciais e emite access_token
4. Token contem roles do service account, sem claims de usuario

**Uso no CARF**: GEOGIS plugin QGIS usa client credentials para autenticar requisicoes WFS/WMS para GEOAPI. Token representa o servico, nao um usuario especifico.

### Configuracao por Client

| Client | Tipo | PKCE | Secret | Redirect URIs |
|:-------|:-----|:-----|:-------|:--------------|
| geoweb | public | required | - | `https://geoweb.carf.example.com/*` |
| admin | public | required | - | `https://admin.carf.example.com/*` |
| webdocs | public | required | - | `https://docs.carf.example.com/*` |
| reurbcad | public | required | - | `carf.reurbcad://*` (deep link) |
| geogis | confidential | - | sim | - (sem redirect, M2M) |

## Consequencias

### Positivas

**Seguranca maximizada**: Cada tipo de cliente usa flow otimizado para seu modelo de ameacas.

**Compliance com standards**: Implementacao segue RFC 6749, RFC 7636, RFC 8252 e OAuth 2.1 draft.

**Interoperabilidade**: Bibliotecas padrao (keycloak-js, oidc-client-ts, python-keycloak) suportam nativamente os flows escolhidos.

**Eliminacao de secrets expostos**: Nenhuma SPA ou mobile app armazena client_secret, eliminando vetor de ataque comum.

### Negativas

**Complexidade de PKCE**: Desenvolvedores devem entender geracao de code_verifier/code_challenge, embora bibliotecas abstraiam isso.

**Service accounts**: GEOGIS requer gerenciamento de client_secret com rotacao periodica.

### Neutras

**Refresh tokens**: Disponivel para public clients (PKCE) e opcional para confidential clients (client_credentials geralmente nao usa).

## Alternativas Rejeitadas

### Implicit Flow para SPAs

Flow legado que retorna tokens diretamente na URL fragment.

**Motivo da rejeicao**: Deprecado pelo OAuth 2.0 Security BCP. Tokens expostos em browser history e logs de servidor. Authorization Code + PKCE e o substituto recomendado.

### Resource Owner Password Credentials (ROPC)

Usuario fornece credenciais diretamente para aplicacao cliente.

**Motivo da rejeicao**: Expoe credenciais do usuario para aplicacao, violando principio de delegacao OAuth. Apenas aceitavel para migracao de sistemas legados.

### Client Secret para SPAs

Usar confidential client com secret embutido no JavaScript.

**Motivo da rejeicao**: Secret exposto no codigo fonte acessivel pelo browser. Qualquer pessoa pode extrair e impersonar a aplicacao.

## Implementacao

### Keycloak Client Configuration (JSON)

```json
// GEOWEB - Public Client com PKCE
{
  "clientId": "geoweb",
  "publicClient": true,
  "standardFlowEnabled": true,
  "pkce.code.challenge.method": "S256",
  "redirectUris": ["https://geoweb.carf.example.com/*"],
  "webOrigins": ["https://geoweb.carf.example.com"]
}

// GEOGIS - Confidential Client
{
  "clientId": "geogis",
  "publicClient": false,
  "serviceAccountsEnabled": true,
  "standardFlowEnabled": false,
  "directAccessGrantsEnabled": false
}
```

### Frontend (keycloak-js)

```typescript
const keycloak = new Keycloak({
  url: 'https://auth.carf.example.com',
  realm: 'carf',
  clientId: 'geoweb'
})

// PKCE habilitado automaticamente para public clients
await keycloak.init({
  onLoad: 'check-sso',
  pkceMethod: 'S256'
})
```

## Metricas de Sucesso

- [ ] Zero clients usando Implicit Flow
- [ ] 100% SPAs configuradas como public client com PKCE obrigatorio
- [ ] Client secrets rotacionados a cada 90 dias
- [ ] Audit log de emissao de tokens por client

## Referencias

- [RFC 6749 - OAuth 2.0](https://tools.ietf.org/html/rfc6749)
- [RFC 7636 - PKCE](https://tools.ietf.org/html/rfc7636)
- [RFC 8252 - OAuth for Native Apps](https://tools.ietf.org/html/rfc8252)
- [OAuth 2.0 Security BCP](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [Clients Configuration](../../PROJECTS/KEYCLOAK/DOCS/INTEGRATION/CLIENTS/)
