---
type: workflow
status: approved
updated: 2026-01-25
part: 1
step: 1
---

# Passo 1: Autenticacao

Autenticacao do Analista de Drone no sistema via Keycloak.

## Fluxo

1. Analista de Drone recebe link (endpoint/portal) para enviar ortofotos
2. Analista de Drone acessa o link
3. Sistema redireciona para Keycloak
4. Analista de Drone insere credenciais (usuario/senha)
5. Keycloak valida credenciais e emite token JWT
6. Token contem `tenant_id` do analista
7. Sistema redireciona de volta ao portal de upload

## Diagrama

```
Analista ──> Portal Upload ──> Keycloak ──> Validacao
                                  │
                                  v
                            Token JWT
                         (com tenant_id)
                                  │
                                  v
                          Portal Upload
```

## Resultado

- Analista de Drone autenticado
- Token JWT valido com `tenant_id`
- Acesso ao portal de upload liberado

## Proximo Passo

Passo 2: Upload da Ortofoto
