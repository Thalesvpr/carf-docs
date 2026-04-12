---
type: leaf
status: review
updated: 2026-02-08
---

# Autenticacao Offline

## Visao Geral

Offline authentication no REURBCAD permite field collectors trabalhar semanas sem internet mantendo autenticacao valida via offline refresh tokens com duracao estendida, obtidos incluindo o scope `offline_access` no OAuth2 authorization request.

## Token Lifetimes

| Token | Duracao | Armazenamento | Observacao |
|---|---|---|---|
| Access Token | 5 minutos | Memoria (class property) | Curto, renovado via refresh |
| ID Token | 5 minutos | Memoria | Usado para extrair claims |
| Refresh Token (offline) | 30 dias idle / 60 dias max | SecureStore (Keychain/Keystore) | Encrypted via hardware |

Quando usuario faz login online pela primeira vez, o app obtem:

- `access_token` (5 min)
- `id_token` (5 min)
- `refresh_token` offline (30 dias) - armazenado em SecureStore encrypted via Keychain/Keystore

O `access_token` cached em memoria dura apenas 5 minutos, mas o `refresh_token` permite renovacao sem internet porque Keycloak permite refresh offline se sessao ainda valida.

## Workflow Tipico (Segunda a Sexta)

```
Segunda (com WiFi)
  └─> Login online → obtem tokens incluindo offline refresh_token

Terca-Quinta (sem internet, em campo)
  └─> App usa cached access_token para assinar requests locais
      (nao enviados porque offline)
  └─> Quando access_token expira apos 5 min, app tenta refresh
      que falha porque offline - mas nao e problema porque
      requests sao queued localmente mesmo sem token valido

Sexta (volta ao escritorio com WiFi)
  └─> App detecta conexao via NetInfo
  └─> Chama getAccessToken() que tenta refresh usando
      offline refresh_token armazenado
  └─> POST /protocol/openid-connect/token com:
      - grant_type=refresh_token
      - refresh_token=<stored_token>
      - client_id=reurbcad
  └─> Keycloak valida refresh_token, checa que sessao
      offline ainda valida (nao passou 30 dias idle)
  └─> Retorna novo access_token fresco com exp renovado
  └─> App atualiza cached token
  └─> Processa sync queue enviando occupations coletadas
      durante semana com Authorization header atualizado
```

### Refresh Token Expirado

Se refresh falha porque passou 30 dias idle, o offline token expirou. O app mostra login screen forcando re-autenticacao antes de sync.

## Token Refresh Offline

O refresh token offline funciona diferente do refresh token padrao:

- **Refresh padrao**: requer comunicacao com Keycloak a cada refresh
- **Refresh offline**: armazenado localmente, Keycloak valida apenas quando ha conexao

Durante periodos sem internet, o app nao envia requests reais - apenas enfileira operacoes localmente. O refresh so e necessario no momento de reconexao.

## Multi-Device

Se user loga mesmo account em tablet + phone:

- Cada device tem proprio `refresh_token` independente
- Sessoes offline separadas, nao compartilhadas
- Revogacao de um token nao afeta outro ate proximo refresh

## Security Trade-offs

| Aspecto | Beneficio | Risco |
|---|---|---|
| Tokens longos (30 dias) | Convenience para trabalho em campo | Maior attack window se device comprometido |
| Armazenamento local | Funciona offline | Token pode ser extraido se device roubado |
| Sem re-autenticacao frequente | Produtividade do field collector | Sem validacao de credencial por semanas |

### Mitigacao

- Device PIN/biometric required para abrir app
- Auto-lock apos inatividade
- SecureStore usa hardware-backed encryption (Keychain/Keystore) prevenindo acesso mesmo com device rooted/jailbroken
- Nunca AsyncStorage porque plain text JSON visivel em backups ou com root access

## Configuracao Keycloak

Sessao offline configurada no Keycloak realm settings:

| Parametro | Valor | Significado |
|---|---|---|
| Offline Session Idle | 30 days | 30 dias sem nenhum refresh attempt |
| Offline Session Max | 60 days | 60 dias desde login inicial, mesmo com refresh frequente |

## Best Practices

- Field collectors devem fazer login semanal quando tem conexao para renovar sessao offline, evitando expiracao
- Sincronizar dados assim que conexao disponivel para minimizar risco de perda
- Manter device com PIN/biometria ativo sempre
- Nao compartilhar device entre usuarios diferentes

## Referencias

- [Authentication](./01-authentication.md)
- [Secure Storage](./03-secure-storage.md)
- [Keycloak Integration](../ARCHITECTURE/01-keycloak-integration.md)
