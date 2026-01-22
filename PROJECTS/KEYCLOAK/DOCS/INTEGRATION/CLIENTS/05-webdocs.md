---
type: leaf
status: review
updated: 2026-01-19
---

# Client WEBDOCS

Portal de documentação Astro + Starlight configurado como public client com PKCE S256 para autenticação de seções protegidas.

Redirect URIs incluem http://localhost:4321/* para desenvolvimento Astro e https://docs.carf.example.com/* para produção. Maior parte do conteúdo é pública sem necessidade de autenticação, mas seção /dev/ requer login e role dev para acesso.

Middleware Astro verifica presença de token JWT em todas as rotas, extrai roles do token decodificado, e protege rotas /dev/* exigindo role dev no array de roles. Usuários sem role dev são redirecionados para página de acesso negado ou login.

Seção /dev/ inclui Swagger interativo com try-it-out conectando diretamente à GEOAPI, documentação técnica interna de arquitetura, guias de contribuição e debug. Token do usuário dev é usado para autenticar requisições ao Swagger permitindo teste de endpoints protegidos.
