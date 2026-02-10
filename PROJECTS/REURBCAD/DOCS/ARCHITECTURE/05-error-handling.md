---
type: leaf
status: review
updated: 2026-02-08
---

# Tratamento de Erros

Estrategia completa de tratamento de erros no REURBCAD, incluindo Error Boundaries, erros de rede, sync, formularios e integracao com Sentry.

## Visao Geral

O REURBCAD opera em ambiente de campo com conectividade instavel. O tratamento de erros prioriza: (1) nunca perder dados do usuario, (2) degradar graciosamente quando offline, (3) mensagens claras em portugues, (4) recuperacao automatica sempre que possivel.

## React Error Boundaries

Tres niveis de Error Boundary capturam erros de renderizacao em escopos diferentes:

### AppErrorBoundary

Envolve toda a aplicacao no `RootLayout`. Captura erros fatais que impedem o funcionamento do app.

```typescript
// src/components/errors/AppErrorBoundary.tsx
class AppErrorBoundary extends React.Component<Props, State> {
  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    Sentry.captureException(error, { extra: errorInfo });
  }

  render() {
    if (this.state.hasError) {
      return (
        <SafeAreaView style={styles.container}>
          <Text style={styles.title}>Erro inesperado</Text>
          <Text style={styles.message}>
            O aplicativo encontrou um problema. Tente reiniciar.
          </Text>
          <Button title="Reiniciar" onPress={() => Updates.reloadAsync()} />
          <Button
            title="Limpar dados e reiniciar"
            variant="destructive"
            onPress={this.handleClearAndRestart}
          />
        </SafeAreaView>
      );
    }
    return this.props.children;
  }
}
```

### ScreenErrorBoundary

Envolve cada tela individualmente. Permite que o resto do app continue funcionando se uma tela falhar.

```typescript
// src/components/errors/ScreenErrorBoundary.tsx
function ScreenErrorBoundary({ children, screenName }: Props) {
  return (
    <ErrorBoundary
      fallback={({ error, resetError }) => (
        <View style={styles.container}>
          <AlertTriangle color="#EF4444" size={48} />
          <Text style={styles.title}>Erro na tela</Text>
          <Text style={styles.message}>
            Nao foi possivel carregar esta tela.
          </Text>
          <Button title="Tentar novamente" onPress={resetError} />
          <Button title="Voltar" onPress={() => router.back()} />
        </View>
      )}
      onError={(error) => {
        Sentry.captureException(error, { tags: { screen: screenName } });
      }}
    >
      {children}
    </ErrorBoundary>
  );
}
```

### FormErrorBoundary

Envolve formularios para evitar perda de dados em caso de erro de renderizacao. Antes de exibir o fallback, salva o rascunho do formulario no MMKV.

```typescript
// src/components/errors/FormErrorBoundary.tsx
function FormErrorBoundary({ children }: Props) {
  return (
    <ErrorBoundary
      fallback={({ resetError }) => (
        <View style={styles.container}>
          <Text style={styles.title}>Erro no formulario</Text>
          <Text style={styles.message}>
            Seus dados foram salvos como rascunho.
            Tente novamente para continuar.
          </Text>
          <Button title="Recuperar rascunho" onPress={resetError} />
        </View>
      )}
      onError={(error) => {
        // Salva rascunho antes de exibir fallback
        const formStore = useFormStore.getState();
        if (formStore.isDirty) {
          mmkvStorage.setItem('form-emergency-draft', JSON.stringify(formStore.formData));
        }
        Sentry.captureException(error, { tags: { component: 'form' } });
      }}
    >
      {children}
    </ErrorBoundary>
  );
}
```

## Erros de Rede

### Deteccao de Conectividade

O app monitora conectividade via `@react-native-community/netinfo`:

```typescript
// src/hooks/useNetworkStatus.ts
export function useNetworkStatus() {
  const [isOnline, setIsOnline] = useState(true);
  const [connectionType, setConnectionType] = useState<string>('unknown');

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsOnline(state.isConnected ?? false);
      setConnectionType(state.type);
    });
    return unsubscribe;
  }, []);

  return { isOnline, connectionType };
}
```

### Fila Offline

Quando offline, operacoes que exigem rede sao enfileiradas automaticamente na `sync_queue` do WatermelonDB. O usuario recebe feedback visual via `OfflineIndicator` na barra superior.

### Estrategia de Retry

| Tentativa | Delay | Descricao |
|-----------|-------|-----------|
| 1a | 0s | Tentativa imediata |
| 2a | 5s | Backoff inicial |
| 3a | 15s | Backoff exponencial |
| 4a (max) | 30s | Ultima tentativa automatica |
| Manual | - | Usuario aciona manualmente apos falha |

```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) throw error;
      const delay = Math.min(5000 * Math.pow(2, attempt), 30000);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  throw new Error('Retry exhausted');
}
```

## Erros de Sincronizacao

### Fluxo de Recuperacao

```
Sync inicia
  ├── Pull (GET /api/sync/changes)
  │     ├── Sucesso → aplica changes locais
  │     ├── Timeout → retry com backoff (max 3)
  │     ├── 401 → refresh token → retry
  │     └── 500 → marca erro, notifica usuario
  └── Push (POST /api/sync/push)
        ├── Sucesso → remove da sync_queue
        ├── 409 Conflict → cria SyncConflict → notifica usuario
        ├── 422 Validation → marca FAILED na queue
        └── Network error → mantem na queue para proximo ciclo
```

### Erros que Bloqueiam Sync

| Erro | Comportamento | Acao do Usuario |
|------|--------------|-----------------|
| Token expirado (30+ dias offline) | Cancela sync, forca logout | Re-login com credenciais |
| Tenant invalido | Cancela sync | Contatar administrador |
| Schema incompativel | Cancela sync | Atualizar app na store |
| Disco cheio | Cancela pull | Liberar espaco no dispositivo |

## Tabela de Codigos de Erro

### AUTH - Autenticacao

| Codigo | Mensagem Tecnica | Mensagem ao Usuario (pt-BR) |
|--------|------------------|------------------------------|
| AUTH_001 | Token refresh failed | Sua sessao expirou. Faca login novamente. |
| AUTH_002 | Invalid credentials | Credenciais invalidas. Verifique usuario e senha. |
| AUTH_003 | Offline token expired | Voce esta offline ha mais de 30 dias. Conecte-se para renovar. |
| AUTH_004 | Tenant not allowed | Voce nao tem acesso a este municipio. |
| AUTH_005 | SecureStore read error | Erro ao acessar credenciais armazenadas. Faca login novamente. |

### SYNC - Sincronizacao

| Codigo | Mensagem Tecnica | Mensagem ao Usuario (pt-BR) |
|--------|------------------|------------------------------|
| SYNC_001 | Pull changes timeout | Sincronizacao lenta. Tente novamente com melhor conexao. |
| SYNC_002 | Push rejected 422 | Dados invalidos detectados. Revise os registros marcados. |
| SYNC_003 | Conflict detected 409 | Conflito encontrado. Escolha qual versao manter. |
| SYNC_004 | Batch size exceeded | Muitos dados pendentes. Sincronizando em partes. |
| SYNC_005 | Schema version mismatch | Versao do app incompativel. Atualize o aplicativo. |

### FORM - Formularios

| Codigo | Mensagem Tecnica | Mensagem ao Usuario (pt-BR) |
|--------|------------------|------------------------------|
| FORM_001 | Validation failed | Preencha todos os campos obrigatorios. |
| FORM_002 | Invalid CPF checksum | CPF invalido. Verifique os digitos. |
| FORM_003 | Photo capture failed | Nao foi possivel capturar a foto. Tente novamente. |
| FORM_004 | Signature empty | Assinatura obrigatoria. Desenhe a assinatura na tela. |
| FORM_005 | Draft restore failed | Nao foi possivel recuperar o rascunho. |

### MAP - Mapa

| Codigo | Mensagem Tecnica | Mensagem ao Usuario (pt-BR) |
|--------|------------------|------------------------------|
| MAP_001 | GPS unavailable | GPS indisponivel. Verifique as permissoes de localizacao. |
| MAP_002 | Tile load failed | Falha ao carregar mapa. Usando cache local. |
| MAP_003 | Polygon render error | Erro ao exibir poligonos. Tente reduzir o zoom. |

### STORAGE - Armazenamento

| Codigo | Mensagem Tecnica | Mensagem ao Usuario (pt-BR) |
|--------|------------------|------------------------------|
| STORAGE_001 | Disk space low | Espaco insuficiente. Libere espaco no dispositivo. |
| STORAGE_002 | WatermelonDB write failed | Erro ao salvar dados locais. Tente novamente. |
| STORAGE_003 | File system permission denied | Sem permissao para acessar arquivos. Verifique permissoes. |

## Degradacao Offline Graciosa

| Funcionalidade | Online | Offline | Observacao |
|----------------|--------|---------|------------|
| Cadastro de unidade | Completo | Completo | Dados salvos localmente |
| Cadastro de titular | Completo | Completo | Validacao CPF offline |
| Captura de fotos | Completo | Completo | Armazenamento local |
| Coleta de assinatura | Completo | Completo | PNG salvo localmente |
| Visualizar mapa | Tiles ao vivo | Tiles em cache | Cache de tiles pre-baixados |
| Sincronizacao | Automatica | Enfileirada | Sync quando reconectar |
| Autocomplete CEP | Disponivel | Indisponivel | Input manual como fallback |
| Metricas de equipe | Tempo real | Dados da ultima sync | Indicador "dados de DD/MM" |
| Trocar tenant | Disponivel | Bloqueado | Exige conexao para re-sync |
| Logout | Revoke + limpar | Apenas limpar local | Revoke na proxima conexao |
| OCR de documentos | Completo | Completo | Processamento 100% on-device |

## Integracao Sentry

### Configuracao

```typescript
// src/utils/sentry.ts
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: process.env.EXPO_PUBLIC_SENTRY_DSN,
  environment: __DEV__ ? 'development' : 'production',
  tracesSampleRate: 0.2,
  enableAutoSessionTracking: true,
  attachStacktrace: true,
  beforeSend(event) {
    // Remover dados sensiveis
    if (event.extra) {
      delete event.extra.accessToken;
      delete event.extra.refreshToken;
      delete event.extra.cpf;
    }
    return event;
  },
});
```

### Breadcrumbs

Breadcrumbs automaticos rastreiam acoes do usuario para contexto de debugging:

```typescript
// Navegacao
Sentry.addBreadcrumb({ category: 'navigation', message: 'MapScreen -> UnitDetail', level: 'info' });

// Sync
Sentry.addBreadcrumb({ category: 'sync', message: `Push ${pendingCount} records`, level: 'info' });

// Formulario
Sentry.addBreadcrumb({ category: 'form', message: 'Step 3 -> Step 4', level: 'info' });
```

### Contexto do Usuario

```typescript
Sentry.setUser({
  id: user.id,
  email: user.email,
  role: user.role,
  tenantId: user.tenantId,
});

Sentry.setTag('app_version', Constants.expoConfig?.version ?? 'unknown');
Sentry.setTag('sync_status', syncStore.syncStatus);
```

### Buffering Offline

Sentry SDK para React Native suporta buffering offline nativamente. Eventos capturados sem conexao sao persistidos no filesystem do dispositivo e enviados automaticamente quando conexao e restabelecida. O buffer local armazena ate 30 eventos, descartando os mais antigos quando o limite e atingido.

## Referencias

- [Sync Feature](../FEATURES/03-offline-sync.md)
- [Conflict Resolution](../DATA/02-conflict-resolution.md)
- [Authentication](../CONCEPTS/01-authentication.md)
- [Build and Release - Sentry](../DEPLOYMENT/01-build-and-release.md)
- [Form Library ADR](../ADRs/ADR-004-form-library.md)
