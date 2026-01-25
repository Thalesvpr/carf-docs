---
type: workflow
status: approved
updated: 2026-01-25
part: 3
step: 11
---

# Passo 11: Designacao ao TENANT

Administrador designa o Agente de Campo a um TENANT especifico.

## Fluxo

1. Administrador designa Agente de Campo a um TENANT (regiao)
2. Designacao registrada no Keycloak (claim `tenant_id`)
3. Agente de Campo so consegue acessar dados do TENANT designado

## Diagrama

```
Administrador ──> Keycloak ──> Registro de TENANT
                                      │
                                      v
                              Agente designado
                              ao TENANT {id}
```

## Claim tenant_id

O token JWT do Agente inclui:
```json
{
  "sub": "user-uuid",
  "tenant_id": "tenant-uuid",
  "roles": ["agente_campo"]
}
```

## Resultado

- Agente de Campo vinculado ao TENANT
- Claim `tenant_id` presente no token JWT
- Acesso restrito aos dados do TENANT

## Proximo Passo

Passo 12: Download do Pacote Temporario
