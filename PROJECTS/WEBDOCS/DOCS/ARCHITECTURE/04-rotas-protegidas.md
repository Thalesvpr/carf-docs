---
status: review
updated: 2026-01-20
---

# Rotas Protegidas

Todas as rotas do WEBDOCS são protegidas e requerem autenticação. O middleware de autorização em src/middleware.ts verifica autenticação e roles do usuário antes de renderizar qualquer conteúdo, controlando acesso às diferentes seções do portal baseado na hierarquia RBAC definida em CENTRAL/INTEGRATION/KEYCLOAK.

## Hierarquia de Roles

O sistema CARF define seis roles com permissões de visualização específicas no WEBDOCS. A hierarquia segue modelo de herança onde roles superiores incluem permissões das inferiores, exceto a role dev que é transversal.

```json
{
  "roles": {
    "user": {
      "description": "Usuário padrão com acesso a documentação básica",
      "sections": ["guia"],
      "inherits": null
    },
    "field-agent": {
      "description": "Agente de campo com acesso aos manuais REURBCAD",
      "sections": ["guia", "manuais"],
      "inherits": "user"
    },
    "analyst": {
      "description": "Analista REURB com acesso ao sistema e relatórios",
      "sections": ["guia", "sistema", "manuais"],
      "inherits": "field-agent"
    },
    "admin": {
      "description": "Administrador de tenant com acesso a status e changelog",
      "sections": ["guia", "sistema", "manuais", "status", "changelog"],
      "inherits": "analyst"
    },
    "super-admin": {
      "description": "Super administrador multi-tenant com acesso à API",
      "sections": ["guia", "sistema", "manuais", "api", "status", "changelog"],
      "inherits": "admin"
    },
    "dev": {
      "description": "Desenvolvedor com acesso total incluindo seção dev",
      "sections": ["guia", "sistema", "manuais", "api", "dev", "status", "changelog"],
      "inherits": null,
      "note": "Role transversal - pode ser combinada com qualquer role operacional"
    }
  }
}
```

A role dev é transversal e não participa da hierarquia de herança. Deve ser atribuída explicitamente e pode ser combinada com qualquer role operacional. Um usuário com role analyst e dev terá acesso tanto às seções de analyst quanto à seção dev.

## Mapeamento Rota para Seção

Cada rota do portal é mapeada para uma seção que determina quais roles podem acessá-la. O mapeamento é simples e baseado no primeiro segmento do path.

```json
{
  "routeMapping": {
    "/guia/*": "guia",
    "/sistema/*": "sistema",
    "/manuais/*": "manuais",
    "/api/*": "api",
    "/dev/*": "dev",
    "/status/*": "status",
    "/changelog/*": "changelog"
  }
}
```

## Lógica do Middleware

O middleware executa em toda requisição seguindo fluxo sequencial de verificação. Primeiro verifica presença do cookie access_token. Se ausente, redireciona para /auth/login preservando URL original no parâmetro redirect para retorno após autenticação.

Se cookie presente, decodifica o JWT sem validar assinatura no edge (validação completa acontece apenas para operações sensíveis). Extrai roles do claim realm_access.roles que contém array com todas roles atribuídas ao usuário no Keycloak.

Determina a seção da rota atual baseado no mapeamento acima. Verifica se alguma das roles do usuário permite acesso à seção, considerando herança. Se nenhuma role permitir acesso, retorna página 403 com explicação e sugestão de contato com administrador.

Se token expirado (claim exp menor que timestamp atual), tenta refresh silencioso usando refresh_token. Se refresh falhar por token revogado ou sessão expirada, redireciona para login.

## Cookies Esperados

```json
{
  "cookies": {
    "access_token": {
      "httpOnly": true,
      "secure": true,
      "sameSite": "lax",
      "path": "/",
      "description": "JWT de acesso para autenticação"
    },
    "refresh_token": {
      "httpOnly": true,
      "secure": true,
      "sameSite": "lax",
      "path": "/auth",
      "description": "Token para renovação do access_token"
    }
  }
}
```

O cookie access_token é enviado em todas requisições (path /) enquanto refresh_token é enviado apenas para rotas /auth/* onde a renovação acontece, minimizando exposição.

## Tratamento de Erros

Usuário não autenticado recebe redirect 302 para /auth/login?redirect={url_atual} preservando destino original. Após login bem-sucedido, callback redireciona para URL preservada.

Usuário autenticado sem permissão recebe página 403 customizada renderizada pelo Astro com explicação clara de que a seção requer permissão específica, lista das roles que teriam acesso, e link para logout ou retorno à home.

Token expirado dispara tentativa de refresh silencioso antes de qualquer resposta de erro. Sucesso no refresh é transparente ao usuário. Falha no refresh resulta em redirect para login com mensagem de sessão expirada.

## Performance

Validação de assinatura JWT usa chave pública obtida do Keycloak JWKS endpoint. Cache da chave pública é mantido por 24 horas ou até falha de validação indicando possível rotação de chaves. Decodificação do JWT no edge não valida assinatura para reduzir latência, confiando no httpOnly do cookie para integridade.

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
