---
type: workflow
status: approved
updated: 2026-01-25
part: 2
step: 6
---

# Passo 6: Autenticacao no Plugin

Autenticacao dupla do Analista no Plugin GEOGIS (Keycloak + AUTHENTICATION KEY).

## Fluxo

1. Analista abre o QGIS
2. Analista ativa o Plugin GEOGIS
3. Plugin exibe tela de login
4. **Autenticacao dupla obrigatoria:**
   - **6.1** Login via Keycloak (OAuth2 PKCE desktop flow)
   - **6.2** Informar AUTHENTICATION KEY (chave adicional do plugin)
5. Plugin valida ambas credenciais contra o backend
6. Plugin armazena tokens de forma segura (QSettings encrypted)
7. Sessao iniciada com sucesso

## Autenticacao Dupla

### 6.1 Login Keycloak (OAuth2 PKCE)

```
Plugin ──> Keycloak Login Page ──> Usuario/Senha
                                        │
                                        v
                                  Token JWT
```

### 6.2 AUTHENTICATION KEY

```
Plugin ──> Input AUTHENTICATION KEY ──> Backend Validacao
                                              │
                                              v
                                        Key Valida
```

## AUTHENTICATION KEY

A AUTHENTICATION KEY e diferente do login Keycloak:
- Formato: String alfanumerica (ex: `carf_key_abc123xyz789`)
- Pode ser revogada independentemente do usuario
- Adiciona camada extra de seguranca
- Vincula a sessao/ambiente ao backend

## Armazenamento Seguro

O Plugin armazena credenciais de forma segura:
- Tokens em QSettings criptografado
- AUTHENTICATION KEY encriptada
- Renovacao automatica de tokens

## Resultado

- Analista autenticado no Plugin
- Tokens Keycloak armazenados
- AUTHENTICATION KEY validada
- Sessao ativa para operacoes

## Proximo Passo

Passo 7: Acesso as Ortofotos
