---
type: leaf
status: review
updated: 2026-02-08
---

# Estrutura de Navegacao

Documentacao completa da estrutura de navegacao do REURBCAD usando Expo Router com file-based routing, tabs condicionais por role, deep linking OAuth2 e tipagem segura de rotas.

## Visao Geral

O REURBCAD usa Expo Router como biblioteca de navegacao, implementando routing baseado em sistema de arquivos no diretorio `app/`. A estrutura de navegacao e composta por tres grupos principais: autenticacao (telas de login), tabs (telas principais com bottom navigation) e modais (telas sobrepostas). A visibilidade de tabs e condicionada pelo role do usuario autenticado.

## Diretorio de Rotas

```
app/
  _layout.tsx                    # RootLayout: providers, AuthGuard, fonts
  index.tsx                      # Splash: redirect para /(auth) ou /(tabs)
  (auth)/
    _layout.tsx                  # AuthLayout: sem tabs, sem header
    login.tsx                    # E2 - Tela de login com botao "Entrar"
  (tabs)/
    _layout.tsx                  # TabsLayout: BottomNavigation role-aware
    mapa/
      _layout.tsx                # MapStack layout
      index.tsx                  # E5 - Mapa principal
      [unitId].tsx               # E7 - Detalhe da unidade
      nova-unidade.tsx           # E8 - Formulario nova unidade
    unidades/
      _layout.tsx                # UnidadesStack layout
      index.tsx                  # Listagem de unidades (coordinator only)
      [unitId]/
        index.tsx                # Detalhe da unidade
        editar.tsx               # Edicao da unidade
        titular/
          novo.tsx               # E9 - Novo titular
          [holderId].tsx         # Edicao de titular existente
    equipe/
      _layout.tsx                # EquipeStack layout
      index.tsx                  # Lista de equipes (coordinator only)
      [teamId].tsx               # Detalhe da equipe
    sync/
      _layout.tsx                # SyncStack layout
      index.tsx                  # Status de sincronizacao
      conflitos.tsx              # Lista de conflitos pendentes
    perfil/
      _layout.tsx                # PerfilStack layout
      index.tsx                  # E11 - Configuracoes
      sobre.tsx                  # Sobre o app
  (modals)/
    assinatura.tsx               # E10 - Canvas assinatura (landscape)
    foto-viewer.tsx              # PhotoViewer com pinch-to-zoom
    conflito-dialog.tsx          # Resolucao de conflito side-by-side
    ocr/
      selecao.tsx                # N1 - Selecao documento OCR
      instrucao.tsx              # N2 - Instrucao pre-captura
      camera.tsx                 # N3 - Camera com overlay
      revisao.tsx                # N4 - Revisao foto
      processamento.tsx          # N5 - Processamento OCR
      resultado.tsx              # N6 - Formulario pre-preenchido
      confirmacao.tsx            # N7 - Confirmacao
    permissoes.tsx               # E3 - Solicitacao de permissoes
    preparar-regiao.tsx          # E4 - Download pacote de campo
```

## Layout Raiz (RootLayout)

O arquivo `app/_layout.tsx` e o ponto de entrada de toda a navegacao. Ele configura providers globais e o AuthGuard:

```typescript
// app/_layout.tsx
export default function RootLayout() {
  const { isAuthenticated, isLoading } = useAuthStore();

  if (isLoading) return <SplashScreen />;

  return (
    <DatabaseProvider database={database}>
      <QueryClientProvider client={queryClient}>
        <GestureHandlerRootView style={{ flex: 1 }}>
          <Stack screenOptions={{ headerShown: false }}>
            <Stack.Screen name="(auth)" redirect={isAuthenticated} />
            <Stack.Screen name="(tabs)" redirect={!isAuthenticated} />
            <Stack.Screen
              name="(modals)/assinatura"
              options={{ presentation: 'fullScreenModal', orientation: 'landscape' }}
            />
            <Stack.Screen
              name="(modals)/conflito-dialog"
              options={{ presentation: 'modal' }}
            />
            <Stack.Screen
              name="(modals)/foto-viewer"
              options={{ presentation: 'transparentModal' }}
            />
          </Stack>
        </GestureHandlerRootView>
      </QueryClientProvider>
    </DatabaseProvider>
  );
}
```

## Tabs com Visibilidade por Role

O `TabsLayout` em `app/(tabs)/_layout.tsx` controla a visibilidade das tabs baseado no role do usuario:

| Tab | Icone | FIELD_CADASTRATOR | FIELD_COORDINATOR | Descricao |
|-----|-------|-------------------|-------------------|-----------|
| Mapa | `map-pin` | Visivel (unica tab) | Visivel | Tela principal do mapa |
| Unidades | `list` | Oculta | Visivel | Listagem de unidades |
| Equipe | `users` | Oculta | Visivel | Gestao de equipes |
| Sync | `refresh-cw` | Oculta | Visivel | Status de sincronizacao |
| Perfil | `settings` | Oculta | Visivel | Configuracoes e logout |

### Implementacao da Visibilidade Condicional

```typescript
// app/(tabs)/_layout.tsx
export default function TabsLayout() {
  const { user } = useAuthStore();
  const isCadastrator = user?.role === 'FIELD_CADASTRATOR';

  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: '#1E40AF',
        tabBarInactiveTintColor: '#94A3B8',
        tabBarStyle: {
          display: isCadastrator ? 'none' : 'flex',
          height: 60,
          paddingBottom: 8,
        },
      }}
    >
      <Tabs.Screen
        name="mapa"
        options={{ title: 'Mapa', tabBarIcon: MapPinIcon }}
      />
      <Tabs.Screen
        name="unidades"
        options={{
          title: 'Unidades',
          tabBarIcon: ListIcon,
          href: isCadastrator ? null : '/(tabs)/unidades',
        }}
      />
      <Tabs.Screen
        name="equipe"
        options={{
          title: 'Equipe',
          tabBarIcon: UsersIcon,
          href: isCadastrator ? null : '/(tabs)/equipe',
        }}
      />
      <Tabs.Screen
        name="sync"
        options={{
          title: 'Sync',
          tabBarIcon: RefreshIcon,
          href: isCadastrator ? null : '/(tabs)/sync',
        }}
      />
      <Tabs.Screen
        name="perfil"
        options={{
          title: 'Perfil',
          tabBarIcon: SettingsIcon,
          href: isCadastrator ? null : '/(tabs)/perfil',
        }}
      />
    </Tabs>
  );
}
```

Para o `FIELD_CADASTRATOR`, a barra de tabs e completamente oculta via `display: 'none'` e as rotas das outras tabs sao desabilitadas via `href: null`. O cadastrador so ve o mapa em tela cheia e navega para formularios via botao flutuante e interacao com poligonos.

## Rotas Protegidas (AuthGuard)

A protecao de rotas funciona em dois niveis:

### Nivel 1 - Redirect por Autenticacao

O `RootLayout` usa a prop `redirect` nas `Stack.Screen` para redirecionar usuarios nao autenticados para `(auth)` e usuarios autenticados para `(tabs)`.

### Nivel 2 - Guarda por Role

Telas especificas de coordenador verificam o role no `_layout.tsx` do grupo:

```typescript
// app/(tabs)/equipe/_layout.tsx
export default function EquipeLayout() {
  const { user } = useAuthStore();

  if (user?.role === 'FIELD_CADASTRATOR') {
    return <Redirect href="/(tabs)/mapa" />;
  }

  return <Stack screenOptions={{ headerShown: true }} />;
}
```

## Deep Linking

### Schema de Deep Link

| URL | Rota | Descricao |
|-----|------|-----------|
| `carf://oauth/callback?code=xxx&state=yyy` | Handler OAuth | Callback do Keycloak apos login |
| `carf://unit/{unitId}` | `/(tabs)/mapa/[unitId]` | Abre detalhe da unidade |
| `carf://sync` | `/(tabs)/sync` | Abre tela de sincronizacao |

### Configuracao no app.json

```json
{
  "expo": {
    "scheme": "carf",
    "android": {
      "intentFilters": [
        {
          "action": "VIEW",
          "autoVerify": true,
          "data": [
            { "scheme": "carf", "host": "oauth", "pathPrefix": "/callback" }
          ],
          "category": ["BROWSABLE", "DEFAULT"]
        }
      ]
    },
    "ios": {
      "bundleIdentifier": "com.carf.reurbcad"
    }
  }
}
```

O callback OAuth2 usa o scheme `carf://oauth/callback` conforme documentado em [Keycloak Integration](./01-keycloak-integration.md). O Expo Router intercepta automaticamente o deep link e roteia para o handler que extrai o authorization code e completa o fluxo PKCE.

## Parametros de Rota Dinamicos

| Parametro | Tipo | Tela | Exemplo |
|-----------|------|------|---------|
| `unitId` | `string` | `[unitId].tsx` | `/(tabs)/mapa/abc-123` |
| `holderId` | `string` | `[holderId].tsx` | `/(tabs)/unidades/abc/titular/def` |
| `teamId` | `string` | `[teamId].tsx` | `/(tabs)/equipe/ghi-456` |

Parametros sao acessados via `useLocalSearchParams()`:

```typescript
// app/(tabs)/mapa/[unitId].tsx
export default function UnitDetailScreen() {
  const { unitId } = useLocalSearchParams<{ unitId: string }>();
  const unit = useUnit(unitId); // hook WatermelonDB observe

  if (!unit) return <NotFoundScreen entity="unidade" />;
  return <UnitDetail unit={unit} />;
}
```

## Telas Modais

Modais abrem sobre o conteudo atual sem substituir a stack de tabs:

| Modal | Presentation | Orientacao | Trigger |
|-------|-------------|------------|---------|
| `assinatura.tsx` | `fullScreenModal` | Landscape forcado | Botao "Coletar Assinatura" no formulario |
| `foto-viewer.tsx` | `transparentModal` | Portrait | Toque em thumbnail de foto |
| `conflito-dialog.tsx` | `modal` | Portrait | Sync detecta conflito pendente |
| `permissoes.tsx` | `fullScreenModal` | Portrait | Primeiro acesso apos login |
| `preparar-regiao.tsx` | `fullScreenModal` | Portrait | Antes do primeiro acesso ao mapa |
| `ocr/*` | `card` | Portrait | Botao OCR no formulario de titular |

### Navegacao para Modal

```typescript
import { router } from 'expo-router';

// Abrir modal de assinatura
router.push('/(modals)/assinatura');

// Abrir photo viewer com params
router.push({
  pathname: '/(modals)/foto-viewer',
  params: { photoUri: photo.file_path },
});
```

## Hierarquia Completa de Telas

```
RootLayout
  ├── SplashScreen (index.tsx)
  ├── (auth)
  │     └── LoginScreen
  ├── (tabs)
  │     ├── mapa/
  │     │     ├── MapScreen (E5)
  │     │     ├── UnitDetailScreen (E7) [unitId]
  │     │     └── NewUnitFormScreen (E8)
  │     ├── unidades/ [coordinator only]
  │     │     ├── UnitListScreen
  │     │     └── [unitId]/
  │     │           ├── UnitDetailScreen
  │     │           ├── EditUnitScreen
  │     │           └── titular/
  │     │                 ├── NewHolderScreen (E9)
  │     │                 └── EditHolderScreen [holderId]
  │     ├── equipe/ [coordinator only]
  │     │     ├── TeamListScreen
  │     │     └── TeamDetailScreen [teamId]
  │     ├── sync/ [coordinator only]
  │     │     ├── SyncStatusScreen
  │     │     └── ConflictListScreen
  │     └── perfil/ [coordinator only]
  │           ├── SettingsScreen (E11)
  │           └── AboutScreen
  └── (modals)
        ├── SignatureScreen (E10)
        ├── PhotoViewerScreen
        ├── ConflictDialogScreen
        ├── PermissionsScreen (E3)
        ├── PrepareRegionScreen (E4)
        └── ocr/
              ├── SelectDocScreen (N1)
              ├── InstructionScreen (N2)
              ├── CameraScreen (N3)
              ├── ReviewScreen (N4)
              ├── ProcessingScreen (N5)
              ├── ResultScreen (N6)
              └── ConfirmationScreen (N7)
```

## Tipagem de Rotas

Expo Router gera tipos automaticamente a partir da estrutura de arquivos. Para habilitar, configurar `tsconfig.json`:

```json
{
  "compilerOptions": {
    "types": ["expo-router/types"]
  }
}
```

Isso permite autocomplete e type checking para `router.push()`, `useLocalSearchParams()` e `Link` components. Erros de digitacao em nomes de rota sao detectados em tempo de compilacao.

## Referencias

- [ADR-003 - Expo Router](../ADRs/ADR-003-navigation.md)
- [Keycloak Integration](./01-keycloak-integration.md)
- [Screen Specs](../UI/01-screen-specs.md)
- [Lib Integration - ui-native BottomNavigation](./02-lib-integration.md)
