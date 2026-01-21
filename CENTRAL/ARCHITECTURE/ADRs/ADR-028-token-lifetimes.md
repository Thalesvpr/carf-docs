---
status: rejected
updated: 2026-01-21
description: "Nao e decisao arquitetural. Configuracao de tokens e detalhe operacional. Mover para PROJECTS/KEYCLOAK/CONFIG. Contem blocos de codigo."
---

# ADR-028: Token Lifetimes e Session Configuration

## Contexto

Configuracao de tempo de vida de tokens e sessoes impacta diretamente a seguranca e usabilidade do sistema. Tokens de vida longa melhoram UX (menos reautenticacoes) mas aumentam janela de exposicao em caso de vazamento. Tokens de vida curta sao mais seguros mas podem causar interrupcoes frequentes na experiencia do usuario.

O CARF possui diferentes cenarios de uso: analistas trabalhando longas horas em escritorio, agentes de campo em areas com conectividade intermitente, e servicos M2M executando operacoes batch.

## Decisao

Configurar **lifetimes diferenciados** por tipo de token com **refresh token rotation** obrigatorio.

### Configuracao de Tokens

| Token | Lifetime | Motivo |
|:------|:---------|:-------|
| Access Token | 5 minutos | Minimiza janela de exposicao |
| Refresh Token (idle) | 30 minutos | Sessoes ociosas expiram rapidamente |
| Refresh Token (max) | 8 horas | Jornada de trabalho sem reautenticacao |
| SSO Session (idle) | 30 minutos | Logout automatico por inatividade |
| SSO Session (max) | 10 horas | Expiracao absoluta de sessao |
| Offline Session | 30 dias | REURBCAD modo offline |

### Refresh Token Rotation

Configuracao `Refresh Token Max Reuse = 0` garante que cada refresh token so pode ser usado uma vez. Apos uso, novo refresh token e emitido e o anterior e invalidado.

**Beneficios:**
- Previne replay attacks (token roubado nao pode ser reutilizado)
- Detecta token theft (uso simultaneo invalida ambos)
- Reduz janela de abuso de tokens comprometidos

### Configuracao Keycloak

```
Realm Settings > Tokens:
  - Access Token Lifespan: 5 minutes
  - Access Token Lifespan For Implicit Flow: disabled (nao usamos)

Realm Settings > Sessions:
  - SSO Session Idle: 30 minutes
  - SSO Session Max: 10 hours
  - Offline Session Idle: 30 days
  - Offline Session Max Lifespan: enabled
  - Offline Session Max Lifespan: 30 days

Realm Settings > Tokens:
  - Revoke Refresh Token: ON
  - Refresh Token Max Reuse: 0
```

## Consequencias

### Positivas

**Seguranca com UX**: Access token curto limita exposicao, refresh silencioso mantem sessao sem interrupcao para usuario.

**Suporte offline**: Offline tokens de 30 dias permitem agentes de campo trabalhar em areas remotas por periodos estendidos.

**Deteccao de comprometimento**: Refresh token rotation detecta uso malicioso quando atacante e usuario legitimo tentam refresh simultaneamente.

**Logout por inatividade**: Sessoes ociosas por 30+ minutos expiram automaticamente, reduzindo risco de sessoes abandonadas.

### Negativas

**Overhead de refresh**: Access token de 5 minutos requer refresh a cada 4-5 minutos em uso continuo, adicionando carga no Keycloak.

**Complexidade de handling**: Frontend deve implementar interceptor para refresh automatico e tratamento de refresh token expirado.

**Offline token management**: Tokens offline de 30 dias requerem secure storage adequado em mobile (Keychain/Keystore).

### Neutras

**Tokens offline vs online**: REURBCAD usa offline tokens por necessidade de operacao desconectada; demais apps usam online tokens padrao.

## Alternativas Rejeitadas

### Access Token Longo (1 hora+)

Configurar access token com vida longa para reduzir refreshes.

**Motivo da rejeicao**: Token vazado permanece valido por hora inteira. Access token nao pode ser revogado (stateless), apenas refresh token. Vida curta e mitigacao essencial.

### Sem Refresh Token Rotation

Manter refresh token fixo durante toda sessao.

**Motivo da rejeicao**: Token roubado pode ser usado indefinidamente ate expiracao. Rotation limita uso a uma unica vez, detectando theft por invalidacao simultanea.

### SSO Session Infinita

Nao expirar sessao SSO enquanto usuario tiver refresh token valido.

**Motivo da rejeicao**: Usuarios que esquecem logout permanecem autenticados indefinidamente. Timeout absoluto forca reautenticacao periodica para verificar credenciais ainda validas.

## Implementacao Frontend

### Axios Interceptor para Refresh Silencioso

```typescript
// Interceptor detecta 401 e faz refresh
axiosInstance.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true

      try {
        await keycloak.updateToken(30) // refresh se expira em 30s
        error.config.headers.Authorization = `Bearer ${keycloak.token}`
        return axiosInstance(error.config)
      } catch {
        keycloak.login() // refresh falhou, redireciona para login
      }
    }
    return Promise.reject(error)
  }
)
```

### Refresh Proativo

```typescript
// Agenda refresh antes de expirar
setInterval(() => {
  keycloak.updateToken(60) // refresh se expira em menos de 60s
    .catch(() => keycloak.login())
}, 30000) // verifica a cada 30s
```

## Metricas de Sucesso

- [ ] Zero sessoes ativas apos 10 horas sem reautenticacao
- [ ] Taxa de refresh < 5% de falhas
- [ ] Tempo medio de refresh < 200ms
- [ ] Zero incidentes de replay de refresh token

## Referencias

- [OAuth 2.0 Token Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics#section-4.13)
- [Keycloak Session Configuration](https://www.keycloak.org/docs/latest/server_admin/#_timeouts)
- [Token Configuration](../../PROJECTS/KEYCLOAK/DOCS/INTEGRATION/TOKENS/)
