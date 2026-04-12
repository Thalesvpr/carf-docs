---
type: leaf
status: approved
updated: 2026-01-24
---

# Authentication Key

Chave adicional de autenticacao exigida pelo Plugin QGIS (GEOGIS), alem do login Keycloak. Funciona como camada extra de seguranca especifica para o plugin.

Diferente de [API Key](./34-api-key.md) que e para integracao maquina-a-maquina generica, Authentication Key e especifica para habilitar uso do plugin de georreferenciamento.

## Proposito

- Habilita/autoriza uso do Plugin GEOGIS
- Vincula sessao/ambiente ao backend
- Pode ser revogada independentemente do usuario Keycloak
- Adiciona camada extra de seguranca para acesso a ortofotos

## Autenticacao Dupla

Analista que usa Plugin QGIS deve fornecer:
1. Login Keycloak (OAuth2 PKCE desktop flow)
2. Authentication Key valida

Ambas credenciais sao validadas contra o backend. Apenas com as duas o plugin inicia sessao.

## Formato

String alfanumerica unica, exemplo: `carf_key_abc123xyz789`

## Ciclo de Vida

- Administrador gera chave para analista
- Analista recebe chave por canal seguro
- Chave usada em conjunto com login Keycloak
- Administrador pode revogar a qualquer momento
- Revogacao nao afeta conta Keycloak do usuario

## Seguranca

Valor completo da chave e exibido apenas uma vez na geracao. Plugin armazena de forma criptografada (QSettings encrypted). Chave comprometida pode ser revogada sem desativar usuario.

## Referencia

Ver [WORKFLOW-MESTRE/02-georreferenciamento](../../WORKFLOW-MESTRE/02-georreferenciamento.md) para fluxo de autenticacao do plugin.
