---
id: RNF-026
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-026: Protecao contra CSRF

## Descricao

Endpoints de mutacao (POST, PUT, PATCH, DELETE) protegidos contra Cross-Site Request Forgery. Double submit cookie com token em header X-CSRF-Token. SameSite cookie como camada adicional.

## Metricas

- Token: aleatorio, criptograficamente seguro
- Cookie: SameSite=Strict ou Lax
- Validacao: middleware no pipeline de requisicoes

## Criterios de Aceitacao

1. HTTP 403 para requisicoes sem token valido
2. Formularios HTML incluem token como campo hidden
3. Mobile e integracao server-to-server isentos quando autenticados via OAuth2
