---
type: leaf
status: review
updated: 2026-02-08
---

# Testes Unitarios - REURBCAD

Padroes e exemplos de testes unitarios para o REURBCAD, cobrindo stores Zustand, modelos WatermelonDB, schemas Zod, funcoes utilitarias e validacoes de formularios.

## Testando Stores Zustand

Stores Zustand sao funcoes puras que gerenciam estado. Para testar, criamos instancias isoladas evitando compartilhamento de estado entre testes.

### Setup Isolado

```typescript
import { createStore } from 'zustand';
import { createAuthSlice, AuthSlice } from '@/stores/auth-slice';

// Criar store isolada para cada teste
function createTestAuthStore() {
  return createStore<AuthSlice>()((...args) => ({
    ...createAuthSlice(...args),
  }));
}

describe('AuthStore', () => {
  let store: ReturnType<typeof createTestAuthStore>;

  beforeEach(() => {
    store = createTestAuthStore();
    jest.clearAllMocks();
  });

  describe('setTokens', () => {
    it('deve armazenar access e refresh tokens', () => {
      const tokens = {
        accessToken: 'eyJhbGciOiJSUzI1NiJ9.test',
        refreshToken: 'refresh-token-mock',
        expiresAt: Date.now() + 300_000,
      };

      store.getState().setTokens(tokens);

      expect(store.getState().accessToken).toBe(tokens.accessToken);
      expect(store.getState().refreshToken).toBe(tokens.refreshToken);
      expect(store.getState().isAuthenticated).toBe(true);
    });
  });

  describe('clearAuth', () => {
    it('deve limpar todos os dados de autenticacao', () => {
      store.getState().setTokens({
        accessToken: 'token',
        refreshToken: 'refresh',
        expiresAt: Date.now() + 300_000,
      });

      store.getState().clearAuth();

      expect(store.getState().accessToken).toBeNull();
      expect(store.getState().refreshToken).toBeNull();
      expect(store.getState().isAuthenticated).toBe(false);
      expect(store.getState().user).toBeNull();
    });
  });

  describe('isTokenExpired', () => {
    it('deve retornar true quando token expirado', () => {
      store.getState().setTokens({
        accessToken: 'token',
        refreshToken: 'refresh',
        expiresAt: Date.now() - 1000, // expirado 1s atras
      });

      expect(store.getState().isTokenExpired()).toBe(true);
    });

    it('deve retornar false quando token valido', () => {
      store.getState().setTokens({
        accessToken: 'token',
        refreshToken: 'refresh',
        expiresAt: Date.now() + 300_000, // expira em 5 min
      });

      expect(store.getState().isTokenExpired()).toBe(false);
    });
  });
});
```

### Testando Selectors Derivados

```typescript
describe('SyncStore selectors', () => {
  let store: ReturnType<typeof createTestSyncStore>;

  beforeEach(() => {
    store = createTestSyncStore();
  });

  describe('pendingChangesCount', () => {
    it('deve somar changes de todas as colecoes', () => {
      store.getState().addPendingChange('units', { id: '1', type: 'create' });
      store.getState().addPendingChange('units', { id: '2', type: 'update' });
      store.getState().addPendingChange('holders', { id: '3', type: 'create' });

      expect(store.getState().pendingChangesCount()).toBe(3);
    });
  });

  describe('lastSyncFormatted', () => {
    it('deve formatar data de ultima sincronizacao em pt-BR', () => {
      store.getState().setLastSync(new Date('2026-02-08T14:30:00Z'));

      expect(store.getState().lastSyncFormatted()).toMatch(
        /08\/02\/2026.*14:30/
      );
    });

    it('deve retornar "Nunca sincronizado" quando nao houver sync', () => {
      expect(store.getState().lastSyncFormatted()).toBe('Nunca sincronizado');
    });
  });
});
```

## Testando Modelos WatermelonDB

Modelos WatermelonDB requerem um database mock com adapter de teste para funcionar corretamente.

### Setup do Database de Teste

```typescript
import { Database } from '@nozbe/watermelondb';
import LokiJSAdapter from '@nozbe/watermelondb/adapters/lokijs';
import { schema } from '@/database/schema';
import { Unit } from '@/database/models/Unit';
import { Holder } from '@/database/models/Holder';
import { Community } from '@/database/models/Community';

function createTestDatabase() {
  const adapter = new LokiJSAdapter({
    schema,
    useWebWorker: false,
    useIncrementalIndexedDB: false,
  });

  return new Database({
    adapter,
    modelClasses: [Unit, Holder, Community],
  });
}

describe('Unit model', () => {
  let database: Database;

  beforeEach(async () => {
    database = createTestDatabase();
  });

  afterEach(async () => {
    await database.write(async () => {
      await database.unsafeResetDatabase();
    });
  });

  it('deve criar unidade com campos obrigatorios', async () => {
    let unit: Unit;

    await database.write(async () => {
      unit = await database.get<Unit>('units').create((u) => {
        u.remoteId = 'uuid-remote';
        u.status = 'DRAFT';
        u.address = 'Rua Exemplo, 123';
        u.communityId = 'community-uuid';
        u.latitude = -23.5505;
        u.longitude = -46.6333;
        u.syncStatus = 'pending';
      });
    });

    expect(unit!.remoteId).toBe('uuid-remote');
    expect(unit!.status).toBe('DRAFT');
    expect(unit!.syncStatus).toBe('pending');
  });

  it('deve atualizar status da unidade', async () => {
    let unit: Unit;

    await database.write(async () => {
      unit = await database.get<Unit>('units').create((u) => {
        u.remoteId = 'uuid-1';
        u.status = 'DRAFT';
        u.syncStatus = 'synced';
      });
    });

    await database.write(async () => {
      await unit!.update((u) => {
        u.status = 'PENDING_REVIEW';
        u.syncStatus = 'pending';
      });
    });

    const updated = await database.get<Unit>('units').find(unit!.id);
    expect(updated.status).toBe('PENDING_REVIEW');
    expect(updated.syncStatus).toBe('pending');
  });

  it('deve consultar unidades por comunidade', async () => {
    await database.write(async () => {
      await database.get<Unit>('units').create((u) => {
        u.communityId = 'comm-1';
        u.status = 'DRAFT';
      });
      await database.get<Unit>('units').create((u) => {
        u.communityId = 'comm-1';
        u.status = 'APPROVED';
      });
      await database.get<Unit>('units').create((u) => {
        u.communityId = 'comm-2';
        u.status = 'DRAFT';
      });
    });

    const units = await database
      .get<Unit>('units')
      .query(Q.where('community_id', 'comm-1'))
      .fetch();

    expect(units).toHaveLength(2);
  });
});
```

## Testando Schemas Zod

Schemas Zod sao funcoes puras ideais para testes unitarios. Cobrir cenarios validos, invalidos e edge cases.

### Validacao de CPF

```typescript
import { cpfSchema, formatCPF } from '@/schemas/cpf-schema';

describe('cpfSchema', () => {
  describe('CPFs validos', () => {
    it.each([
      ['529.982.247-25', 'com formatacao'],
      ['52998224725', 'sem formatacao'],
      ['000.000.001-91', 'com zeros a esquerda'],
    ])('deve aceitar %s (%s)', (cpf) => {
      expect(cpfSchema.safeParse(cpf).success).toBe(true);
    });
  });

  describe('CPFs invalidos', () => {
    it.each([
      ['000.000.000-00', 'todos iguais'],
      ['111.111.111-11', 'todos iguais'],
      ['123.456.789-00', 'digitos invalidos'],
      ['529.982.247-26', 'digito verificador errado'],
      ['12345', 'muito curto'],
      ['', 'vazio'],
    ])('deve rejeitar %s (%s)', (cpf) => {
      const result = cpfSchema.safeParse(cpf);
      expect(result.success).toBe(false);
    });
  });
});

describe('formatCPF', () => {
  it('deve formatar CPF sem pontuacao', () => {
    expect(formatCPF('52998224725')).toBe('529.982.247-25');
  });

  it('deve manter CPF ja formatado', () => {
    expect(formatCPF('529.982.247-25')).toBe('529.982.247-25');
  });
});
```

### Validacao de Area e Coordenadas

```typescript
import { unitSchema } from '@/schemas/unit-schema';

describe('unitSchema - area', () => {
  const baseUnit = {
    address: 'Rua Teste, 100',
    communityId: 'comm-uuid',
    latitude: -23.5505,
    longitude: -46.6333,
  };

  it('deve aceitar area dentro dos limites (1 a 100000 m2)', () => {
    const result = unitSchema.safeParse({ ...baseUnit, area: 250.5 });
    expect(result.success).toBe(true);
  });

  it('deve rejeitar area negativa', () => {
    const result = unitSchema.safeParse({ ...baseUnit, area: -10 });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0].message).toContain('Area deve ser positiva');
  });

  it('deve rejeitar area zero', () => {
    const result = unitSchema.safeParse({ ...baseUnit, area: 0 });
    expect(result.success).toBe(false);
  });

  it('deve rejeitar area acima do limite', () => {
    const result = unitSchema.safeParse({ ...baseUnit, area: 150_000 });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0].message).toContain('100.000');
  });
});

describe('unitSchema - coordenadas', () => {
  const baseUnit = {
    address: 'Rua Teste, 100',
    communityId: 'comm-uuid',
    area: 200,
  };

  it('deve aceitar coordenadas validas do Brasil', () => {
    const result = unitSchema.safeParse({
      ...baseUnit,
      latitude: -15.7801,
      longitude: -47.9292,
    });
    expect(result.success).toBe(true);
  });

  it('deve rejeitar latitude fora do Brasil (> 5.3)', () => {
    const result = unitSchema.safeParse({
      ...baseUnit,
      latitude: 10.0,
      longitude: -47.9292,
    });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0].message).toContain('territorio brasileiro');
  });

  it('deve rejeitar longitude fora do Brasil (> -34.7)', () => {
    const result = unitSchema.safeParse({
      ...baseUnit,
      latitude: -15.7801,
      longitude: -20.0,
    });
    expect(result.success).toBe(false);
  });
});
```

## Testando Funcoes Utilitarias

```typescript
import {
  calculatePolygonArea,
  isPointInsidePolygon,
  formatCoordinate,
  metersToHectares,
} from '@/utils/geo-utils';

describe('calculatePolygonArea', () => {
  it('deve calcular area de quadrado 100x100m', () => {
    const polygon = [
      [-46.633, -23.550],
      [-46.632, -23.550],
      [-46.632, -23.551],
      [-46.633, -23.551],
      [-46.633, -23.550], // fecha o poligono
    ];

    const area = calculatePolygonArea(polygon);
    // Area aproximada de ~10000 m2 (variacao por projecao)
    expect(area).toBeGreaterThan(9000);
    expect(area).toBeLessThan(11000);
  });

  it('deve retornar 0 para poligono degenerado (< 3 pontos)', () => {
    expect(calculatePolygonArea([[-46, -23], [-45, -22]])).toBe(0);
  });
});

describe('metersToHectares', () => {
  it('deve converter 10000 m2 para 1 hectare', () => {
    expect(metersToHectares(10000)).toBe(1);
  });

  it('deve arredondar para 4 casas decimais', () => {
    expect(metersToHectares(12345)).toBe(1.2345);
  });
});

describe('formatCoordinate', () => {
  it('deve formatar latitude Sul', () => {
    expect(formatCoordinate(-23.5505, 'lat')).toBe('23.5505 S');
  });

  it('deve formatar longitude Oeste', () => {
    expect(formatCoordinate(-46.6333, 'lng')).toBe('46.6333 O');
  });
});
```

## Testando Validacao React Hook Form

```typescript
import { renderHook, act } from '@testing-library/react-hooks';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { holderSchema, HolderFormData } from '@/schemas/holder-schema';

describe('HolderForm validation', () => {
  it('deve validar formulario completo com sucesso', async () => {
    const { result } = renderHook(() =>
      useForm<HolderFormData>({
        resolver: zodResolver(holderSchema),
        defaultValues: {
          name: 'Maria da Silva',
          cpf: '529.982.247-25',
          phone: '(11) 99999-8888',
          email: 'maria@example.com',
          birthDate: '1990-05-15',
        },
      })
    );

    let isValid = false;
    await act(async () => {
      isValid = await result.current.trigger();
    });

    expect(isValid).toBe(true);
    expect(result.current.formState.errors).toEqual({});
  });

  it('deve retornar erro para nome vazio', async () => {
    const { result } = renderHook(() =>
      useForm<HolderFormData>({
        resolver: zodResolver(holderSchema),
        defaultValues: { name: '', cpf: '529.982.247-25' },
      })
    );

    await act(async () => {
      await result.current.trigger('name');
    });

    expect(result.current.formState.errors.name?.message).toBe(
      'Nome e obrigatorio'
    );
  });

  it('deve retornar erro para CPF invalido', async () => {
    const { result } = renderHook(() =>
      useForm<HolderFormData>({
        resolver: zodResolver(holderSchema),
        defaultValues: { name: 'Teste', cpf: '000.000.000-00' },
      })
    );

    await act(async () => {
      await result.current.trigger('cpf');
    });

    expect(result.current.formState.errors.cpf?.message).toContain(
      'CPF invalido'
    );
  });
});
```

## Testando Logica de Sync

```typescript
import { buildSyncPayload, mergeSyncResponse } from '@/services/sync-service';

describe('buildSyncPayload', () => {
  it('deve agrupar changes por colecao', () => {
    const pendingChanges = [
      { collection: 'units', id: '1', type: 'create', data: { status: 'DRAFT' } },
      { collection: 'units', id: '2', type: 'update', data: { status: 'PENDING' } },
      { collection: 'holders', id: '3', type: 'create', data: { name: 'Joao' } },
    ];

    const payload = buildSyncPayload(pendingChanges);

    expect(payload.units.created).toHaveLength(1);
    expect(payload.units.updated).toHaveLength(1);
    expect(payload.holders.created).toHaveLength(1);
  });
});

describe('mergeSyncResponse', () => {
  it('deve aplicar last-write-wins para conflito de update', () => {
    const local = { id: '1', address: 'Rua Local', version: 3, updatedAt: 1000 };
    const remote = { id: '1', address: 'Rua Remota', version: 4, updatedAt: 2000 };

    const result = mergeSyncResponse(local, remote);

    expect(result.address).toBe('Rua Remota');
    expect(result.version).toBe(4);
  });

  it('deve manter versao local quando mais recente', () => {
    const local = { id: '1', address: 'Rua Local', version: 5, updatedAt: 3000 };
    const remote = { id: '1', address: 'Rua Remota', version: 4, updatedAt: 2000 };

    const result = mergeSyncResponse(local, remote);

    expect(result.address).toBe('Rua Local');
    expect(result.version).toBe(5);
  });
});
```

## Boas Praticas

| Pratica | Descricao |
|---------|-----------|
| Isolamento | Cada teste cria seu proprio store/database, sem estado compartilhado |
| AAA | Seguir Arrange-Act-Assert em todos os testes |
| Nomes descritivos | `deve rejeitar CPF com todos digitos iguais` em vez de `testa CPF` |
| Edge cases | Sempre testar limites (0, negativo, maximo, vazio, null) |
| Sem side effects | Mocks para SecureStore, FileSystem, Network |
| Fast feedback | Testes unitarios devem rodar em < 30s total |

## Referencias

- [00-testing-strategy.md](./00-testing-strategy.md) - Estrategia geral de testes
- [02-component-tests.md](./02-component-tests.md) - Testes de componentes
- [DATA/01-watermelondb-schema.md](../DATA/01-watermelondb-schema.md) - Schema WatermelonDB
