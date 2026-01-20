---
status: review
updated: 2026-01-17
---

# Rotas Protegidas

Middleware de autorização protege rotas /dev/* verificando autenticação e role dev antes de renderizar conteúdo. Implementado em src/middleware.ts usando API de middleware do Astro.

Fluxo de verificação em cada requisição para /dev/* extrai cookie de sessão, decodifica tokens, valida expiração do access token, e verifica presença de role dev no claim realm_access.roles. Qualquer falha resulta em redirect ou erro apropriado.

Usuário não autenticado (cookie ausente ou inválido) recebe redirect 302 para /auth/login com return_url preservando destino original. Após login bem-sucedido, usuário retorna para página que tentou acessar.

Usuário autenticado sem role dev recebe página 403 renderizada com explicação de que acesso requer permissão de desenvolvedor. Página inclui informações sobre como solicitar role e link para logout.

Token expirado dispara refresh silencioso. Se refresh falhar (token revogado ou sessão expirada), usuário recebe redirect para login. Processo transparente quando refresh bem-sucedido.

Verificação de role usa claim realm_access.roles do JWT que contém array de roles atribuídas ao usuário. Role dev é transversal, não herdada de roles operacionais, então mesmo admin ou super-admin precisam atribuição explícita.

Performance otimizada com validação de assinatura JWT usando chave pública cacheada do Keycloak JWKS endpoint. Cache atualizado a cada 24 horas ou quando validação falha indicando possível rotação de chaves.
