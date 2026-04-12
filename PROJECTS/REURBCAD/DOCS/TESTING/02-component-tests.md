---
type: leaf
status: review
updated: 2026-02-08
---

# Testes de Componentes - REURBCAD

Padroes para testes de componentes React Native usando React Native Testing Library (RNTL), cobrindo renderizacao com providers, interacoes, formularios, mocks de modulos Expo e cenarios offline.

## Setup React Native Testing Library

### Arquivo jest.setup.ts

```typescript
import '@testing-library/react-native/extend-expect';
import { server } from './msw/server';

// MSW para interceptar HTTP
beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Mock global de modulos nativos
jest.mock('expo-secure-store', () => ({
  getItemAsync: jest.fn().mockResolvedValue(null),
  setItemAsync: jest.fn().mockResolvedValue(undefined),
  deleteItemAsync: jest.fn().mockResolvedValue(undefined),
}));

jest.mock('expo-location', () => ({
  requestForegroundPermissionsAsync: jest.fn().mockResolvedValue({
    status: 'granted',
  }),
  getCurrentPositionAsync: jest.fn().mockResolvedValue({
    coords: { latitude: -23.5505, longitude: -46.6333, accuracy: 10 },
  }),
  watchPositionAsync: jest.fn().mockReturnValue({ remove: jest.fn() }),
  Accuracy: { High: 4, Balanced: 3, Low: 2 },
}));

jest.mock('expo-camera', () => ({
  Camera: {
    requestCameraPermissionsAsync: jest.fn().mockResolvedValue({
      status: 'granted',
    }),
  },
  CameraView: 'CameraView',
}));

jest.mock('@react-native-community/netinfo', () => ({
  addEventListener: jest.fn().mockReturnValue(jest.fn()),
  fetch: jest.fn().mockResolvedValue({
    isConnected: true,
    isInternetReachable: true,
    type: 'wifi',
  }),
}));

jest.mock('expo-file-system', () => ({
  documentDirectory: '/mock/documents/',
  cacheDirectory: '/mock/cache/',
  writeAsStringAsync: jest.fn().mockResolvedValue(undefined),
  readAsStringAsync: jest.fn().mockResolvedValue('mock-content'),
  deleteAsync: jest.fn().mockResolvedValue(undefined),
  getInfoAsync: jest.fn().mockResolvedValue({ exists: true, size: 1024 }),
  EncodingType: { UTF8: 'utf8', Base64: 'base64' },
}));
```

## Renderizacao com Providers

Componentes REURBCAD dependem de multiplos providers. Criar um wrapper reutilizavel para testes.

### AllProviders Wrapper

```typescript
import React, { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react-native';
import { NavigationContainer } from '@react-navigation/native';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DatabaseProvider } from '@nozbe/watermelondb/DatabaseProvider';
import { createTestDatabase } from '../test-utils/database';

interface WrapperProps {
  children: React.ReactNode;
}

function createAllProviders(overrides?: { database?: any }) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0 },
      mutations: { retry: false },
    },
  });

  const database = overrides?.database ?? createTestDatabase();

  return function AllProviders({ children }: WrapperProps) {
    return (
      <QueryClientProvider client={queryClient}>
        <DatabaseProvider database={database}>
          <NavigationContainer>
            {children}
          </NavigationContainer>
        </DatabaseProvider>
      </QueryClientProvider>
    );
  };
}

export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'> & { database?: any }
) {
  const { database, ...renderOptions } = options ?? {};
  return render(ui, {
    wrapper: createAllProviders({ database }),
    ...renderOptions,
  });
}
```

### Uso nos Testes

```typescript
import { renderWithProviders } from '../test-utils/render';
import { UnitCard } from '@/components/UnitCard';

describe('UnitCard', () => {
  const defaultProps = {
    unit: {
      id: '1',
      address: 'Rua Exemplo, 123',
      status: 'DRAFT',
      area: 250.5,
      holdersCount: 2,
    },
    onPress: jest.fn(),
  };

  it('deve renderizar endereco e status', () => {
    const { getByText } = renderWithProviders(
      <UnitCard {...defaultProps} />
    );

    expect(getByText('Rua Exemplo, 123')).toBeTruthy();
    expect(getByText('Rascunho')).toBeTruthy();
  });

  it('deve exibir area formatada em m2', () => {
    const { getByText } = renderWithProviders(
      <UnitCard {...defaultProps} />
    );

    expect(getByText('250,5 m2')).toBeTruthy();
  });
});
```

## Snapshot Testing

### Quando Usar Snapshots

| Usar | Nao Usar |
|------|----------|
| Componentes de apresentacao pura (cards, badges, labels) | Componentes com estado dinamico (formularios, listas) |
| Layouts que nao mudam frequentemente | Componentes com dados mockados complexos |
| Componentes de UI do @carf/ui-native | Telas inteiras (muito frageis) |

### Exemplo de Snapshot

```typescript
import { renderWithProviders } from '../test-utils/render';
import { StatusBadge } from '@carf/ui-native';

describe('StatusBadge', () => {
  it.each([
    ['DRAFT', 'Rascunho'],
    ['PENDING_REVIEW', 'Aguardando Revisao'],
    ['APPROVED', 'Aprovado'],
    ['REJECTED', 'Rejeitado'],
  ])('deve renderizar badge para status %s', (status, label) => {
    const tree = renderWithProviders(
      <StatusBadge status={status} label={label} />
    ).toJSON();

    expect(tree).toMatchSnapshot();
  });
});
```

## Testes de Interacao

### fireEvent para Gestos

```typescript
import { fireEvent, waitFor } from '@testing-library/react-native';
import { renderWithProviders } from '../test-utils/render';
import { CommunitySelector } from '@/components/CommunitySelector';

describe('CommunitySelector', () => {
  const communities = [
    { id: '1', name: 'Comunidade Sol Nascente', unitCount: 45 },
    { id: '2', name: 'Vila Esperanca', unitCount: 120 },
    { id: '3', name: 'Jardim Primavera', unitCount: 78 },
  ];

  it('deve chamar onSelect ao pressionar comunidade', () => {
    const onSelect = jest.fn();
    const { getByText } = renderWithProviders(
      <CommunitySelector
        communities={communities}
        onSelect={onSelect}
      />
    );

    fireEvent.press(getByText('Comunidade Sol Nascente'));

    expect(onSelect).toHaveBeenCalledWith('1');
  });

  it('deve filtrar comunidades pelo texto digitado', () => {
    const { getByPlaceholderText, queryByText } = renderWithProviders(
      <CommunitySelector
        communities={communities}
        onSelect={jest.fn()}
      />
    );

    fireEvent.changeText(
      getByPlaceholderText('Buscar comunidade...'),
      'Esperanca'
    );

    expect(queryByText('Vila Esperanca')).toBeTruthy();
    expect(queryByText('Comunidade Sol Nascente')).toBeNull();
    expect(queryByText('Jardim Primavera')).toBeNull();
  });
});
```

## Renderizacao Assincrona

### waitFor e findBy

```typescript
import { waitFor } from '@testing-library/react-native';
import { renderWithProviders } from '../test-utils/render';
import { UnitListScreen } from '@/screens/UnitListScreen';

describe('UnitListScreen', () => {
  it('deve exibir loading enquanto carrega unidades', () => {
    const { getByTestId } = renderWithProviders(<UnitListScreen />);
    expect(getByTestId('loading-spinner')).toBeTruthy();
  });

  it('deve exibir lista de unidades apos carregamento', async () => {
    const { findByText } = renderWithProviders(<UnitListScreen />);

    // findBy ja inclui waitFor internamente
    expect(await findByText('Rua Exemplo, 123')).toBeTruthy();
    expect(await findByText('Av. Brasil, 456')).toBeTruthy();
  });

  it('deve exibir empty state quando sem unidades', async () => {
    // Sobrescrever handler MSW para retornar lista vazia
    server.use(
      http.get('*/api/units', () => {
        return HttpResponse.json({ data: [], total: 0 });
      })
    );

    const { findByText } = renderWithProviders(<UnitListScreen />);

    expect(
      await findByText('Nenhuma unidade cadastrada')
    ).toBeTruthy();
  });
});
```

## Testando Indicadores Offline

```typescript
import NetInfo from '@react-native-community/netinfo';
import { renderWithProviders } from '../test-utils/render';
import { OfflineIndicator } from '@/components/OfflineIndicator';

describe('OfflineIndicator', () => {
  it('deve exibir banner offline quando sem conexao', async () => {
    (NetInfo.fetch as jest.Mock).mockResolvedValueOnce({
      isConnected: false,
      isInternetReachable: false,
    });

    const { findByText } = renderWithProviders(<OfflineIndicator />);

    expect(await findByText('Voce esta offline')).toBeTruthy();
  });

  it('nao deve exibir banner quando online', async () => {
    (NetInfo.fetch as jest.Mock).mockResolvedValueOnce({
      isConnected: true,
      isInternetReachable: true,
    });

    const { queryByText } = renderWithProviders(<OfflineIndicator />);

    await waitFor(() => {
      expect(queryByText('Voce esta offline')).toBeNull();
    });
  });

  it('deve exibir contagem de changes pendentes quando offline', async () => {
    (NetInfo.fetch as jest.Mock).mockResolvedValueOnce({
      isConnected: false,
      isInternetReachable: false,
    });

    // Simular 5 changes pendentes no sync store
    useSyncStore.getState().setPendingCount(5);

    const { findByText } = renderWithProviders(<OfflineIndicator />);

    expect(await findByText('5 alteracoes pendentes')).toBeTruthy();
  });
});
```

## Testando Formularios com Validacao

```typescript
import { fireEvent, waitFor } from '@testing-library/react-native';
import { renderWithProviders } from '../test-utils/render';
import { HolderForm } from '@/components/forms/HolderForm';

describe('HolderForm', () => {
  const onSubmit = jest.fn();

  beforeEach(() => {
    onSubmit.mockClear();
  });

  it('deve submeter formulario valido', async () => {
    const { getByPlaceholderText, getByText } = renderWithProviders(
      <HolderForm onSubmit={onSubmit} />
    );

    fireEvent.changeText(getByPlaceholderText('Nome completo'), 'Maria Silva');
    fireEvent.changeText(getByPlaceholderText('CPF'), '529.982.247-25');
    fireEvent.changeText(getByPlaceholderText('Telefone'), '(11) 99999-8888');

    fireEvent.press(getByText('Salvar'));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          name: 'Maria Silva',
          cpf: '529.982.247-25',
          phone: '(11) 99999-8888',
        })
      );
    });
  });

  it('deve exibir erros de validacao inline', async () => {
    const { getByPlaceholderText, getByText, findByText } =
      renderWithProviders(<HolderForm onSubmit={onSubmit} />);

    // Submeter com CPF invalido
    fireEvent.changeText(getByPlaceholderText('Nome completo'), 'Joao');
    fireEvent.changeText(getByPlaceholderText('CPF'), '000.000.000-00');
    fireEvent.press(getByText('Salvar'));

    expect(await findByText('CPF invalido')).toBeTruthy();
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it('deve desabilitar botao durante submissao', async () => {
    onSubmit.mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 1000))
    );

    const { getByPlaceholderText, getByText } = renderWithProviders(
      <HolderForm onSubmit={onSubmit} />
    );

    fireEvent.changeText(getByPlaceholderText('Nome completo'), 'Maria');
    fireEvent.changeText(getByPlaceholderText('CPF'), '529.982.247-25');
    fireEvent.press(getByText('Salvar'));

    await waitFor(() => {
      expect(getByText('Salvando...')).toBeTruthy();
    });
  });
});
```

## Mocking Modulos Expo

### Tabela de Mocks Comuns

| Modulo | Mock | Notas |
|--------|------|-------|
| `expo-secure-store` | `getItemAsync`, `setItemAsync`, `deleteItemAsync` | Simular storage de tokens |
| `expo-location` | `getCurrentPositionAsync`, `watchPositionAsync` | Retornar coords fixas |
| `expo-camera` | `CameraView` como string | Renderiza como View no teste |
| `expo-file-system` | `writeAsStringAsync`, `readAsStringAsync` | Operacoes em memoria |
| `expo-image-picker` | `launchCameraAsync`, `launchImageLibraryAsync` | Retornar URI mock |
| `@react-native-community/netinfo` | `addEventListener`, `fetch` | Controlar online/offline |
| `expo-image-manipulator` | `manipulateAsync` | Retornar URI sem compressao |

### Mock de expo-image-picker

```typescript
jest.mock('expo-image-picker', () => ({
  launchCameraAsync: jest.fn().mockResolvedValue({
    canceled: false,
    assets: [
      {
        uri: 'file:///mock/photo.jpg',
        width: 1920,
        height: 1080,
        type: 'image',
      },
    ],
  }),
  launchImageLibraryAsync: jest.fn().mockResolvedValue({
    canceled: false,
    assets: [
      {
        uri: 'file:///mock/gallery-photo.jpg',
        width: 3024,
        height: 4032,
        type: 'image',
      },
    ],
  }),
  MediaTypeOptions: { Images: 'Images', Videos: 'Videos', All: 'All' },
  CameraType: { front: 'front', back: 'back' },
}));
```

## Boas Praticas para Testes de Componentes

| Pratica | Descricao |
|---------|-----------|
| Queries por acessibilidade | Preferir `getByRole`, `getByLabelText` sobre `getByTestId` |
| Evitar implementation details | Nao testar state interno, testar comportamento visivel |
| Um assert por cenario | Cada `it` testa um comportamento especifico |
| Setup compartilhado | `beforeEach` para estado limpo, factory functions para props |
| Timeout explicito | `waitFor` com timeout customizado para operacoes lentas |
| Cleanup automatico | RNTL faz cleanup automatico apos cada teste |

## Referencias

- [00-testing-strategy.md](./00-testing-strategy.md) - Estrategia geral
- [01-unit-tests.md](./01-unit-tests.md) - Testes unitarios
- [03-e2e-tests.md](./03-e2e-tests.md) - Testes end-to-end
- [ARCHITECTURE/01-keycloak-integration.md](../ARCHITECTURE/01-keycloak-integration.md) - Fluxo de autenticacao
