---
type: workflow
status: approved
updated: 2026-02-07
part: 2
step: 5
---

# Passo 5: Designacao ao TENANT

Administrador designa o Analista a um TENANT especifico.

## Fluxo

1. Administrador designa Analista a um TENANT (regiao)
2. Designacao registrada no Keycloak (claim tenant_id)
3. Analista passa a ter acesso ao conjunto de ortofotos dessa regiao

## Designacao

O Administrador registra a designacao no Keycloak, vinculando o Analista a um tenant especifico. O token JWT passa a incluir o claim tenant_id, restringindo o acesso do Analista exclusivamente as ortofotos daquele tenant.

## Claims do Token JWT

| Claim | Valor | Descricao |
|-------|-------|-----------|
| sub | UUID do usuario | Identificador unico |
| tenant_id | UUID do tenant | Tenant designado |
| roles | analista | Papel do usuario |

## Resultado

- Analista vinculado ao TENANT
- Claim tenant_id presente no token JWT
- Acesso restrito as ortofotos do TENANT

## Proximo Passo

Passo 6: Autenticacao no Plugin
