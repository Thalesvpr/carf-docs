---
type: workflow
status: approved
updated: 2026-02-07
part: 3
step: 11
---

# Passo 11: Designacao ao TENANT

Administrador designa Coordenador de Campo ou Cadastrador de Campo a um TENANT especifico.

## Atores

- **Administrador**: realiza a designacao
- **Coordenador de Campo (field-coordinator)**: lider de equipe
- **Cadastrador de Campo (field-cadastrator)**: executor de cadastros

## Fluxo

1. Administrador designa Coordenador ou Cadastrador a um TENANT (regiao)
2. Designacao registrada no Keycloak (claim tenant_id)
3. Usuario so consegue acessar dados do TENANT designado

## Designacao

O Administrador registra a designacao no Keycloak, vinculando o usuario de campo ao tenant. O token JWT passa a incluir o claim tenant_id e a role correspondente (field-coordinator ou field-cadastrator), restringindo acesso exclusivamente aos dados do tenant designado.

## Claims do Token JWT

| Claim | Coordenador | Cadastrador |
|-------|-------------|-------------|
| sub | UUID do usuario | UUID do usuario |
| tenant_id | UUID do tenant | UUID do tenant |
| roles | field-coordinator | field-cadastrator |

## Diferenca na Designacao

| Aspecto | Coordenador | Cadastrador |
|---------|-------------|-------------|
| Designado pelo | Admin/Manager | Admin/Manager |
| Recebe | TENANT + Equipe | TENANT + Regiao especifica |
| Seleciona regiao | SIM (no app) | NAO (recebe atribuicao) |

## Resultado

- Usuario de campo vinculado ao TENANT
- Claim tenant_id presente no token JWT
- Acesso restrito aos dados do TENANT

## Proximo Passo

Passo 12: Download do Pacote Temporario
