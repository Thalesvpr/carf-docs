---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-088: OAuth2 Providers

## Descricao

Login via provedores externos OAuth2: Google, Microsoft, Login.gov. Keycloak configura identity providers federados. Mapeamento de atributos sincroniza perfil automaticamente.

## Metricas

- Provedores: Google, Microsoft, Login.gov
- Fluxo: Authorization Code via Keycloak
- Atributos: nome, email, foto sincronizados

## Criterios de Aceitacao

1. Primeiro login cria conta local vinculada ao provedor
2. Logins subsequentes sincronizam informacoes de perfil
3. Revogacao no provedor externo impede login no sistema
