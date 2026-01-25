---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-005: Validacao JWT em Todas Requisicoes

## Descricao

O backend GEOAPI deve validar token JWT em todas as requisicoes autenticadas. Validacao inclui verificacao de assinatura usando chave publica do Keycloak, verificacao de claims obrigatorios (sub, exp, iat, iss, aud), confirmacao de token nao expirado e extracao de tenant_id e roles para controle de acesso. Requisicoes com token invalido retornam HTTP 401 Unauthorized.

## Criterios de Aceitacao

1. Toda requisicao autenticada passa por validacao JWT
2. Assinatura verificada contra chave publica do Keycloak
3. Token expirado retorna 401 Unauthorized
4. Claims tenant_id e roles extraidos para contexto
5. Mensagem de erro descritiva no corpo da resposta

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-001
