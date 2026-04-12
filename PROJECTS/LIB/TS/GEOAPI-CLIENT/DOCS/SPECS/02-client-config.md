---
type: leaf
status: active
updated: 2026-02-09
---

# Configuracao do Cliente - @carf/geoapi-client

Interface de configuracao do createApiClient.

## Interface ApiClientConfig

### Campos Obrigatorios

| Propriedade | Tipo | Descricao |
|:------------|:-----|:----------|
| baseURL | string | URL base da API (ex: https://api.carf.gov.br ou http://localhost:5127) |
| getToken | () => Promise<string> | Callback async que retorna o JWT access token atual |
| getTenantId | () => string | Callback que retorna o ID do tenant ativo |

### Campos Opcionais

| Propriedade | Tipo | Padrao | Descricao |
|:------------|:-----|:-------|:----------|
| timeout | number | 30000 | Timeout para requisicoes em ms |
| retryAttempts | number | 3 | Numero maximo de tentativas de retry |
| headers | Record<string, string> | {} | Headers customizados adicionais |

## Exemplos de Configuracao

**Configuracao minima:** requer baseURL, getToken e getTenantId. A funcao getToken tipicamente delega para o auth provider da aplicacao (KeycloakClient no REURBWEB, SecureStore adapter no REURBCAD).

**Desenvolvimento:** usa http://localhost:5127 como baseURL, getToken retornando token de teste, getTenantId retornando tenant fixo.

**Producao:** usa URL de producao via variavel de ambiente, getToken delegando para KeycloakClient com refresh automatico, getTenantId obtendo do contexto do usuario.

## Valores Padrao

| Opcao | Valor Padrao |
|:------|:-------------|
| timeout | 30000 |
| retryAttempts | 3 |
| headers | {} |

## Notas

- `getToken` e chamado antes de cada request. Deve retornar token valido ou fazer refresh internamente.
- `getTenantId` e chamado sincronamente. O tenant deve estar disponivel antes de fazer requests.
- Headers customizados sao mesclados com os headers de auth e tenant (auth e tenant tem prioridade).
