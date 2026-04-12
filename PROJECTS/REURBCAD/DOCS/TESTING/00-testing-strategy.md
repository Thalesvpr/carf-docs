---
type: leaf
status: review
updated: 2026-02-08
---

# Estrategia de Testes - REURBCAD

Estrategia completa de testes para o aplicativo mobile REURBCAD, cobrindo desde testes unitarios ate testes end-to-end, com foco especial nos desafios de apps offline-first React Native.

## Piramide de Testes

O REURBCAD segue a piramide de testes adaptada para React Native:

| Nivel | Percentual | Ferramenta | Foco |
|-------|-----------|------------|------|
| Unitarios | 60% | Jest | Stores Zustand, schemas Zod, modelos WatermelonDB, utils |
| Integracao | 25% | React Native Testing Library | Componentes com providers, formularios, navegacao |
| E2E | 15% | Maestro | Fluxos completos login, coleta, sync |

## Ferramentas do Ecossistema

### Jest (Runner Principal)

Configuracao base no `jest.config.ts`:

```typescript
import type { Config } from 'jest';

const config: Config = {
  preset: 'jest-expo',
  setupFilesAfterSetup: ['./jest.setup.ts'],
  transformIgnorePatterns: [
    'node_modules/(?!((jest-)?react-native|@react-native(-community)?)|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@sentry/react-native|native-base|react-native-svg|@carf/.*)',
  ],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@carf/tscore$': '<rootDir>/__mocks__/@carf/tscore.ts',
    '^@carf/geoapi-client$': '<rootDir>/__mocks__/@carf/geoapi-client.ts',
    '^@carf/ui-native$': '<rootDir>/__mocks__/@carf/ui-native.ts',
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/index.ts',
    '!src/**/*.stories.tsx',
  ],
  coverageThresholds: {
    global: {
      statements: 80,
      branches: 70,
      functions: 75,
      lines: 80,
    },
  },
};

export default config;
```

### React Native Testing Library (RNTL)

Biblioteca principal para testes de integracao de componentes, renderizando componentes reais sem DOM do navegador.

### Maestro

Framework de testes E2E baseado em YAML, escolhido por simplicidade de setup com Expo e suporte nativo a gestos mobile.

### MSW (Mock Service Worker)

Intercepta requests HTTP para simular respostas da GEOAPI durante testes, permitindo testar cenarios online/offline sem backend real.

```typescript
// msw/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('*/api/sync/changes', ({ request }) => {
    const url = new URL(request.url);
    const since = url.searchParams.get('since');
    return HttpResponse.json({
      changes: { units: [], holders: [], communities: [] },
      timestamp: new Date().toISOString(),
    });
  }),

  http.post('*/api/sync/push', () => {
    return HttpResponse.json({ conflicts: [], accepted: true });
  }),

  http.post('*/api/units', () => {
    return HttpResponse.json(
      { id: 'uuid-mock', status: 'DRAFT' },
      { status: 201 }
    );
  }),
];
```

## Metas de Cobertura

| Modulo | Statements | Branches | Justificativa |
|--------|-----------|----------|---------------|
| stores/ (Zustand) | 90% | 85% | Logica de negocio critica |
| schemas/ (Zod) | 95% | 90% | Validacoes de entrada |
| models/ (WatermelonDB) | 85% | 75% | Persistencia offline |
| utils/ | 90% | 85% | Funcoes puras |
| hooks/ | 80% | 70% | Logica reativa |
| screens/ | 70% | 60% | UI com muita interacao |
| components/ | 75% | 65% | Componentes reutilizaveis |

## Integracao CI (GitHub Actions)

### PR Check (a cada push)

```yaml
name: REURBCAD Tests
on:
  pull_request:
    paths: ['apps/reurbcad/**', 'packages/tscore/**', 'packages/ui-native/**']

jobs:
  unit-integration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'yarn'
      - run: yarn install --frozen-lockfile
      - run: yarn workspace @carf/reurbcad test --coverage
      - uses: codecov/codecov-action@v4
        with:
          flags: reurbcad
```

### Nightly E2E

```yaml
name: REURBCAD E2E
on:
  schedule:
    - cron: '0 3 * * *' # 03:00 UTC diariamente

jobs:
  e2e-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: 17
      - run: yarn install --frozen-lockfile
      - run: yarn workspace @carf/reurbcad build:android:debug
      - uses: mobile-dev-inc/action-maestro-cloud@v1
        with:
          api-key: ${{ secrets.MAESTRO_CLOUD_KEY }}
          app-file: apps/reurbcad/android/app/build/outputs/apk/debug/app-debug.apk
          workspace: apps/reurbcad/.maestro
```

## O Que Testar vs Nao Testar

### Testar

- Logica de validacao Zod (CPF, area minima, coordenadas)
- Transicoes de estado nas stores Zustand (auth, sync, form wizard)
- Operacoes CRUD no WatermelonDB (create, update, query, delete)
- Resolucao de conflitos no sync (last-write-wins, merge)
- Fluxo de formularios multi-step (wizard de coleta)
- Comportamento offline (fallback, cache, queue)
- Permissoes por role (field-cadastrator vs field-coordinator)
- Interceptors HTTP (retry, token refresh, error mapping)

### Nao Testar

- Implementacao interna de bibliotecas (expo-camera, expo-location)
- Estilos visuais puros (cor, tamanho fonte) - cobrir com design review
- Codigo gerado automaticamente (types do @carf/tscore)
- Animacoes e transicoes (Reanimated) - muito frageis para assertions
- Plataforma nativa (permissoes OS, notificacoes push) - cobrir em E2E

## Convencoes de Nomenclatura

Testes em portugues usando `describe` e `it`:

```typescript
describe('useAuthStore', () => {
  describe('login', () => {
    it('deve salvar tokens no SecureStore apos login com sucesso', async () => {
      // arrange, act, assert
    });

    it('deve retornar erro quando credenciais invalidas', async () => {
      // arrange, act, assert
    });

    it('deve limpar estado anterior antes de novo login', async () => {
      // arrange, act, assert
    });
  });

  describe('logout', () => {
    it('deve remover tokens e redirecionar para tela de login', async () => {
      // arrange, act, assert
    });
  });
});
```

### Padrao de Nomeacao de Arquivos

| Tipo | Padrao | Exemplo |
|------|--------|---------|
| Unitario | `*.test.ts` | `cpf-schema.test.ts` |
| Componente | `*.test.tsx` | `UnitForm.test.tsx` |
| Integracao | `*.integration.test.ts` | `sync-flow.integration.test.ts` |
| E2E | `*.maestro.yaml` | `field-collection.maestro.yaml` |

## Estrutura de Diretorios de Teste

```
src/
  stores/
    __tests__/
      auth-store.test.ts
      sync-store.test.ts
      unit-store.test.ts
  schemas/
    __tests__/
      unit-schema.test.ts
      holder-schema.test.ts
  models/
    __tests__/
      Unit.test.ts
      Holder.test.ts
  screens/
    __tests__/
      FieldCollectionScreen.test.tsx
  components/
    __tests__/
      UnitCard.test.tsx
      OfflineIndicator.test.tsx
__tests__/
  integration/
    sync-flow.integration.test.ts
    auth-flow.integration.test.ts
.maestro/
  field-collection.maestro.yaml
  login-flow.maestro.yaml
  offline-sync.maestro.yaml
```

## Referencias

- [01-unit-tests.md](./01-unit-tests.md) - Padroes de testes unitarios
- [02-component-tests.md](./02-component-tests.md) - Padroes de testes de componentes
- [03-e2e-tests.md](./03-e2e-tests.md) - Testes end-to-end
- [CONCEPTS/01-authentication.md](../CONCEPTS/01-authentication.md) - Contexto de autenticacao
- [CONCEPTS/02-offline-authentication.md](../CONCEPTS/02-offline-authentication.md) - Contexto offline
