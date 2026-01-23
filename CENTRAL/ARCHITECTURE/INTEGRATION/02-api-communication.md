---
type: leaf
status: review
updated: 2026-01-22
---

# API Communication

Padrao de comunicacao entre clientes e GEOAPI via REST sobre HTTPS usando JSON como formato de dados. Todas as requisicoes autenticadas incluem JWT bearer token no header Authorization e identificador de tenant no header X-Tenant-Id.

GEOAPI expoe recursos RESTful com verbos HTTP semanticos: GET para leitura, POST para criacao, PUT/PATCH para atualizacao, DELETE para remocao. Respostas seguem formato consistente com data para payload, pagination para listas e errors para falhas. Versionamento via header Accept-Version.

## Headers Obrigatorios

Authorization com Bearer token JWT obtido do Keycloak. X-Tenant-Id com UUID do municipio para isolamento multi-tenant. Content-Type application/json para requisicoes com body. Accept application/json para respostas. Accept-Language para mensagens de erro localizadas.
