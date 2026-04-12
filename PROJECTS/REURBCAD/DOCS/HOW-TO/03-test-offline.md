---
type: leaf
status: review
updated: 2026-02-08
---

# Testar Modo Offline

## Pre-Requisitos

- App REURBCAD instalado e funcional
- Conexao WiFi disponivel para login inicial
- Device fisico ou emulador com controle de rede
- User teste criado no Keycloak com roles e tenant configurados

### Monitoramento de Conectividade

```typescript
NetInfo.addEventListener('change', state => {
  console.log('Connection:', state.isConnected, state.isInternetReachable);
});
```

Util para verificar que detection de conectividade funciona corretamente.

### Simular Offline

Habilitar Airplane Mode em device settings ou emulator toolbar para simular offline completo (desabilita WiFi + cellular + Bluetooth).

## Cenarios de Teste

### Cenario 1: Offline Workflow Completo

| Passo | Acao | Resultado Esperado |
|---|---|---|
| 1 | Fazer login com WiFi ativo | Tokens obtidos incluindo offline refresh_token |
| 2 | Habilitar Airplane Mode | Desconecta completamente |
| 3 | Navegar app | Telas carregam dados cached do WatermelonDB sem loading spinners infinitos |
| 4 | Criar nova Occupation | Formulario com address, area, GPS coordinates salva localmente |
| 5 | Capturar photos via camera | Photos salvos localmente |
| 6 | Submit form | Salva em WatermelonDB com `synced=false` flag |
| 7 | Verificar lista de Occupations | Nova ocupacao visivel com badge "Pendente sync" |
| 8 | Verificar banner | Banner top "Sem conexao - Dados serao sincronizados quando online" visivel |
| 9 | Tentar fazer logout | Mostra alert "Impossivel fazer logout offline - Tente quando online" |
| 10 | Fechar app completamente (swipe-up kill) | App encerrado |
| 11 | Reabrir app | Session restaurada via cached refresh_token sem internet |
| 12 | Verificar Occupation criada | Ainda visivel na lista, persistida em WatermelonDB |

### Cenario 2: Reconexao e Sync

| Passo | Acao | Resultado Esperado |
|---|---|---|
| 1 | Desabilitar Airplane Mode | Re-conecta WiFi |
| 2 | Aguardar alguns segundos | NetInfo detecta conexao |
| 3 | Observar sync | Sync automatico inicia, toast "Sincronizando..." |
| 4 | Verificar network logs (DevTools) | POST `/api/sync/push` envia Occupation criada offline com batch |
| 5 | Verificar response | Success remove `synced=false` flag, badge "Pendente sync" desaparece |
| 6 | Verificar pull | GET `/api/sync/pull` busca changes remotos (caso outro user modificou dados enquanto offline) |

### Cenario 3: Token Caching

| Passo | Acao | Resultado Esperado |
|---|---|---|
| 1 | Ficar offline | Access_token expira apos 5 min |
| 2 | Continuar usando app | App funciona normalmente offline, requests nao enviados imediatamente |
| 3 | Reconectar | App faz refresh com offline refresh_token obtendo novo access_token antes de sync |

### Cenario 4: Long-term Offline (7+ dias)

| Passo | Acao | Resultado Esperado |
|---|---|---|
| 1 | Deixar app offline por 7+ dias | Offline refresh_token ainda valido (30 dias idle) |
| 2 | Reconectar | Sync funciona normalmente |
| 3 | Deixar offline por 30+ dias | Refresh falha, app mostra login screen forcando re-autenticacao |

### Cenario 5: Sync Conflict

| Passo | Acao | Resultado Esperado |
|---|---|---|
| 1 | Device A cria Occupation offline (id=1, address="Rua A") | Salvo local |
| 2 | Device B cria Occupation offline (id=1, address="Rua B") | Salvo local |
| 3 | Device A conecta primeiro | Sync sucesso |
| 4 | Device B conecta depois | Recebe 409 Conflict do backend (`response.status === 409`) |
| 5 | Observar dialog | "Conflito detectado - Dados foram modificados por outro usuario" |
| 6 | Opcoes apresentadas | "Manter minha versao" (overwrite remote) ou "Usar versao remota" (discard local) |

### Cenario 6: Network Interruption Mid-Sync

| Passo | Acao | Resultado Esperado |
|---|---|---|
| 1 | Iniciar sync | Sync em andamento |
| 2 | Habilitar Airplane Mode mid-sync | Requests pendentes sao aborted |
| 3 | Verificar dados | Dados parcialmente sincronizados marcados como `synced=true`, dados nao sincronizados permanecem `synced=false` |
| 4 | Reconectar | Retry automatico com exponential backoff (1s, 2s, 4s, 8s entre tentativas) |

### Cenario 7: Performance (Bulk Data)

| Passo | Acao | Resultado Esperado |
|---|---|---|
| 1 | Criar 1000+ Occupations offline | Salvo localmente |
| 2 | Reconectar e iniciar sync | Sync batch nao trava UI (background processing com AsyncTask/GCD) |
| 3 | Observar progress | Indicador mostra "Sincronizando 47/1000" dando feedback visual |
| 4 | Cancel sync button | Permite user interromper sync long-running se mudar de ideia |

## Checklist de Validacao

- [ ] App funciona 100% offline apos login inicial
- [ ] Dados criados offline persistem apos kill/reopen do app
- [ ] Sync automatico ao reconectar
- [ ] Conflitos detectados e apresentados ao usuario
- [ ] Exponential backoff em caso de falha de sync
- [ ] Performance aceitavel com grande volume de dados offline
- [ ] Banner de status de conexao visivel

## Referencias

- [Offline Authentication](../CONCEPTS/02-offline-authentication.md)
- [Authentication](../CONCEPTS/01-authentication.md)
- [Keycloak Integration](../ARCHITECTURE/01-keycloak-integration.md)
