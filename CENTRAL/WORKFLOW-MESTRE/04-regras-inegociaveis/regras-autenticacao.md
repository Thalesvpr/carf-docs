---
type: workflow
status: approved
updated: 2026-02-07
category: regras
---

# Regras de Autenticacao

Regras que garantem a seguranca de acesso ao sistema.

## Regras

| Regra | Descricao |
|-------|-----------|
| AUTH-01 | Autenticacao via Keycloak e OBRIGATORIA para TODOS os perfis |
| AUTH-02 | Analista de Drone SO envia ortofotos APOS autenticar no Keycloak |
| AUTH-03 | Analista do Plugin SO acessa ortofotos APOS autenticar Keycloak + AUTHENTICATION KEY |
| AUTH-04 | Equipe de campo SO acessa dados APOS autenticar no Keycloak |
| AUTH-05 | AUTHENTICATION KEY e ADICIONAL ao Keycloak (camada extra) |

## Detalhamento

### AUTH-01: Keycloak Obrigatorio

Todos os perfis devem autenticar via Keycloak:
- Analista de Drone
- Analista do Plugin QGIS
- Coordenador de Campo
- Cadastrador de Campo
- Administradores

### AUTH-02 a AUTH-04: Autenticacao por Perfil

Cada perfil tem seu fluxo de autenticacao:
- **Analista de Drone**: Keycloak apenas
- **Analista Plugin**: Keycloak + AUTHENTICATION KEY (dupla)
- **Equipe de Campo**: Keycloak apenas (via app mobile)

### AUTH-05: Camada Extra

A AUTHENTICATION KEY e uma camada adicional de seguranca:
- Diferente do login Keycloak
- Pode ser revogada independentemente
- Formato: String alfanumerica (ex: `carf_key_abc123xyz789`)
