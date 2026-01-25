---
type: workflow
status: approved
updated: 2026-01-25
part: 2
step: 5
---

# Passo 5: Designacao ao TENANT

Administrador designa o Analista a um TENANT especifico.

## Fluxo

1. Administrador designa Analista a um TENANT (regiao)
2. Designacao registrada no Keycloak (claim `tenant_id`)
3. Analista passa a ter acesso ao conjunto de ortofotos dessa regiao

## Diagrama

```
Administrador ──> Keycloak ──> Registro de TENANT
                                      │
                                      v
                              Analista designado
                              ao TENANT {id}
```

## Claim tenant_id

O token JWT do Analista inclui:
```json
{
  "sub": "user-uuid",
  "tenant_id": "tenant-uuid",
  "roles": ["analista"]
}
```

## Resultado

- Analista vinculado ao TENANT
- Claim `tenant_id` presente no token JWT
- Acesso restrito as ortofotos do TENANT

## Proximo Passo

Passo 6: Autenticacao no Plugin
