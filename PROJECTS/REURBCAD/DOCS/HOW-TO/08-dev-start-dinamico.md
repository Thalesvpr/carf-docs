---
type: leaf
status: review
updated: 2026-02-10
---

# Dev Start Dinamico — IP, .env e Keycloak Automatizados

Toda vez que o desenvolvedor troca de rede WiFi ou reinicia o computador, o IP da LAN muda. Isso quebra o `.env` (URL da API e Keycloak) e invalida o redirect URI registrado no Keycloak. O script `dev-start.js` automatiza as tres operacoes num unico comando.

## Problema

| Etapa manual | O que quebra quando IP muda |
|-------------|----------------------------|
| Editar `.env` com IP correto | API e Keycloak ficam inacessiveis pelo celular |
| Adicionar `exp://<IP>:8081/*` no Keycloak Admin | Keycloak rejeita o `redirect_uri` com erro `invalid_redirect_uri` |
| Iniciar Expo em modo LAN | Sem as etapas anteriores, QR code funciona mas login falha |

## Solucao

O script `scripts/dev-start.js` executa em sequencia:

```
1. getLanIp()       → detecta IP via os.networkInterfaces()
2. updateEnvFile()  → reescreve .env com URLs corretas
3. updateKeycloak() → Admin API: atualiza redirectUris do client "reurbcad"
4. startExpo()      → spawn("npx", ["expo", "start", "--lan"])
```

Zero dependencias externas — usa apenas modulos built-in do Node.js (`os`, `fs`, `http`, `child_process`).

## Pre-Requisitos

| Ferramenta | Verificacao | Descricao |
|------------|-------------|-----------|
| Node.js 20+ | `node --version` | Runtime para executar o script |
| Docker Compose | `docker compose ps` | Keycloak + GEOAPI devem estar rodando |
| Keycloak | `http://localhost:8080` | Acessivel com admin/admin |
| GEOAPI | `http://localhost:5127/swagger` | Backend .NET rodando |
| Rede WiFi/Ethernet | IP na faixa 192.168.x.x ou 10.x.x.x | Celular e PC na mesma rede |

## Passo 1: Executar o Script

```bash
npm run dev
```

O script exibe cada etapa com cores no terminal:

```
============================================================
  REURBCAD Dev Start
============================================================

[dev-start] Detectando IP da LAN...
[dev-start] IP detectado: 192.168.1.101

============================================================
  Atualizando .env
============================================================

[dev-start] .env atualizado:
  EXPO_PUBLIC_API_URL=http://192.168.1.101:5127/api
  EXPO_PUBLIC_KEYCLOAK_URL=http://192.168.1.101:8080
  EXPO_PUBLIC_KEYCLOAK_REALM=carf
  EXPO_PUBLIC_KEYCLOAK_CLIENT_ID=reurbcad

============================================================
  Atualizando Keycloak
============================================================

[dev-start] Obtendo token admin do Keycloak...
[dev-start] Buscando UUID do client "reurbcad"...
[dev-start] UUID: reurbcad-client-id
[dev-start] Atualizando redirect URIs...
[dev-start] Redirect URIs registradas:
  + exp://192.168.1.101:8081/*
  + exp://localhost:8081/*
  + carf://oauth/callback
  + carf://callback
  + http://localhost:19006/*
[dev-start] Keycloak atualizado com sucesso!

============================================================
  Iniciando Expo
============================================================

[dev-start] Iniciando Expo dev server (--lan)...
```

## Passo 2: Conectar o Celular

1. Abrir Expo Go no celular (mesma rede WiFi)
2. Escanear QR code exibido no terminal
3. Aguardar bundle carregar

## Passo 3: Testar Login

1. Tocar "Entrar" no app
2. Browser abre `http://<IP>:8080/realms/carf/protocol/openid-connect/auth?redirect_uri=exp://<IP>:8081/...`
3. Keycloak aceita o redirect_uri porque o script registrou `exp://<IP>:8081/*`
4. Apos login, callback retorna ao app com authorization code

## Flags Opcionais

| Flag | Descricao | Uso |
|------|-----------|-----|
| `--skip-keycloak` | Pula atualizacao de redirect URIs | Quando Keycloak nao esta rodando |
| `--skip-expo` | Pula inicio do Expo dev server | Quando quer apenas atualizar .env e Keycloak |

Exemplos:

```bash
# Atualizar tudo mas nao iniciar Expo
npm run dev -- --skip-expo

# Apenas atualizar .env (Keycloak offline)
npm run dev -- --skip-keycloak --skip-expo
```

## Variaveis de Ambiente do Script

O script aceita configuracao via variaveis de ambiente (para cenarios nao-padrao):

| Variavel | Default | Descricao |
|----------|---------|-----------|
| `KEYCLOAK_ADMIN_URL` | `http://localhost:8080` | URL do Keycloak admin |
| `KEYCLOAK_ADMIN_USER` | `admin` | Usuario admin do Keycloak |
| `KEYCLOAK_ADMIN_PASS` | `admin` | Senha admin do Keycloak |
| `GEOAPI_PORT` | `5127` | Porta da GEOAPI |

## Redirect URIs Registradas

O script registra estas URIs no client `reurbcad` do Keycloak:

| URI | Cenario |
|-----|---------|
| `exp://<IP>:8081/*` | Expo Go via LAN (dinamico, muda com IP) |
| `exp://localhost:8081/*` | Expo Go local (emulador) |
| `carf://oauth/callback` | Deep link para dev build |
| `carf://callback` | Deep link alternativo |
| `http://localhost:19006/*` | Expo web |

## Como o Script Funciona

### Deteccao de IP

Itera sobre `os.networkInterfaces()` e seleciona o primeiro IPv4 nao-interno na faixa `192.168.x.x` ou `10.x.x.x`.

### Atualizacao do .env

Le o `.env` existente, preserva comentarios e variaveis nao-gerenciadas, sobrescreve apenas as 4 variaveis `EXPO_PUBLIC_*`.

### Keycloak Admin API

```
POST /realms/master/protocol/openid-connect/token
  → grant_type=password, client_id=admin-cli
  → retorna bearer token

GET /admin/realms/carf/clients?clientId=reurbcad
  → retorna array com UUID interno do client

GET /admin/realms/carf/clients/{uuid}
  → retorna representacao completa do client

PUT /admin/realms/carf/clients/{uuid}
  → envia representacao atualizada com novas redirectUris
```

> **Nota:** O script faz GET completo do client antes do PUT para preservar todos os campos existentes. Apenas `redirectUris` e sobrescrito.

## Troubleshooting

| Problema | Causa Provavel | Solucao |
|----------|---------------|---------|
| `Nenhuma interface de rede LAN encontrada` | Sem WiFi/Ethernet conectado | Conectar a uma rede |
| `Keycloak token request failed (401)` | Credenciais admin incorretas | Verificar `KEYCLOAK_ADMIN_USER` e `KEYCLOAK_ADMIN_PASS` |
| `Keycloak token request failed` + ECONNREFUSED | Keycloak nao esta rodando | `docker compose up -d` e aguardar 30-60s |
| `Client "reurbcad" not found` | Realm `carf` nao importado | Reimportar `realm-export.json` no Keycloak |
| `invalid_redirect_uri` no login | Script nao atualizou Keycloak | Verificar output do script, rodar sem `--skip-keycloak` |
| Celular nao acessa API | AP isolation no roteador | Usar ngrok ou `.env.tunnel` como fallback |
| IP detectado errado (VPN, Docker) | Varias interfaces de rede | Desconectar VPN, ou editar `.env` manualmente apos o script |

## Quando Usar `.env.tunnel` em vez do Script

Se o roteador WiFi tem **AP isolation** (celular nao consegue acessar o PC por IP), o script nao resolve. Nesse caso:

1. Iniciar ngrok: `ngrok http 8080`
2. Copiar `.env.tunnel` para `.env`
3. Editar `.env` com a URL do ngrok
4. Adicionar a URL do ngrok nos redirect URIs do Keycloak manualmente

Consulte [Environment Variables](./05-environment-variables.md) para detalhes sobre `.env.tunnel`.

## Verificacao

| Item | Como Verificar | Esperado |
|------|---------------|----------|
| IP detectado | Output do script na primeira linha | IP na faixa 192.168.x.x ou 10.x.x.x |
| `.env` atualizado | `cat .env` | URLs com IP correto |
| Keycloak atualizado | Keycloak Admin > Clients > reurbcad > Settings | `exp://<IP>:8081/*` nos redirect URIs |
| Expo inicia | QR code exibido no terminal | URL com IP correto |
| Login funciona | Tocar "Entrar" no celular | Keycloak aceita redirect_uri |

## Referencias

- [Setup Keycloak](./01-setup-keycloak.md) - Configuracao inicial de redirect URIs
- [Handle Callbacks](./02-handle-callbacks.md) - Deep linking e callback OAuth
- [Environment Variables](./05-environment-variables.md) - Referencia completa de variaveis
- [Setup Dev Environment](./04-setup-dev-environment.md) - Setup completo do ambiente
- [Troubleshooting](./06-troubleshooting.md) - Problemas comuns
