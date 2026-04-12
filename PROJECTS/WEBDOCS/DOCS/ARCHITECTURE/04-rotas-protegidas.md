---
type: leaf
status: review
updated: 2026-02-07
---

# Rotas Protegidas

Todas as rotas do WEBDOCS sao protegidas e requerem autenticacao. O middleware de autorizacao em src/middleware.ts verifica autenticacao e roles do usuario antes de renderizar qualquer conteudo, controlando acesso as diferentes secoes do portal baseado na hierarquia RBAC definida em PROJECTS/KEYCLOAK/DOCS/INTEGRATION/RBAC/.

## Hierarquia de Roles

O sistema CARF define seis roles com permissoes de visualizacao especificas. A hierarquia segue modelo de heranca onde roles superiores incluem permissoes das inferiores, exceto dev que e transversal.

| Role | Secoes permitidas | Herda de |
|------|-------------------|----------|
| user | guia | nenhuma |
| field-cadastrator | guia, manuais | user |
| field-coordinator | guia, manuais | field-cadastrator |
| analyst | guia, sistema, manuais | field-coordinator |
| admin | guia, sistema, manuais, status, changelog | analyst |
| super-admin | guia, sistema, manuais, api, status, changelog | admin |
| dev | guia, sistema, manuais, api, dev, status, changelog | nenhuma (transversal) |

A role dev e transversal e nao participa da hierarquia de heranca. Deve ser atribuida explicitamente e pode ser combinada com qualquer role operacional.

## Mapeamento Rota para Secao

| Rota | Secao |
|------|-------|
| /guia/ | guia |
| /sistema/ | sistema |
| /manuais/ | manuais |
| /api/ | api |
| /dev/ | dev |
| /status/ | status |
| /changelog/ | changelog |

## Logica do Middleware

O middleware executa em toda requisicao seguindo fluxo sequencial. Primeiro verifica presenca do cookie access_token. Se ausente, redireciona para /auth/login preservando URL original. Se presente, decodifica JWT e extrai roles do claim realm_access.roles.

Determina a secao da rota e verifica se alguma role do usuario permite acesso considerando heranca. Se nenhuma role permitir, retorna pagina 403. Se token expirado, tenta refresh silencioso.

Detalhes de implementacao do middleware, tratamento de erros e performance estao em 04-rotas-protegidas-detalhes.md.
