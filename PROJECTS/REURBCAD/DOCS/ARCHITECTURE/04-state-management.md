---
type: leaf
status: review
updated: 2026-02-08
---

# Gerenciamento de Estado

Documentacao das quatro Zustand stores do REURBCAD, suas interfaces TypeScript, estrategias de persistencia e integracao com WatermelonDB e TanStack Query.

## Visao Geral

O REURBCAD usa Zustand como biblioteca de gerenciamento de estado global, dividido em quatro stores isoladas por dominio. Cada store e independente e importavel apenas onde necessaria, evitando re-renders desnecessarios. Estado de servidor (dados remotos) e gerenciado separadamente via TanStack Query. Dados locais persistidos no WatermelonDB sao acessados via hooks de observacao reativa.

| Store | Responsabilidade | Persistencia | Adapter |
|-------|-----------------|--------------|---------|
| `useAuthStore` | Autenticacao e sessao | SecureStore (tokens), MMKV (user/tenant) | MMKV |
| `useSyncStore` | Sincronizacao e conflitos | WatermelonDB (sync_queue) | WatermelonDB adapter |
| `useMapStore` | Estado do mapa e layers | MMKV (preferencias) | MMKV |
| `useFormStore` | Rascunho do formulario wizard | MMKV (draft) | MMKV |

## useAuthStore

Gerencia autenticacao, sessao do usuario, tenant ativo e permissoes.

### Interface

```typescript
interface User {
  id: string;           // sub claim do JWT
  email: string;
  name: string;
  role: 'FIELD_CADASTRATOR' | 'FIELD_COORDINATOR' | 'ANALYST' | 'MANAGER';
  tenantId: string;     // tenant_id claim
  allowedTenants: Array<{ id: string; name: string }>;
}

interface AuthState {
  // Estado
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  tenant: { id: string; name: string } | null;
  allowedTenants: Array<{ id: string; name: string }>;
  isTokenExpired: boolean;

  // Acoes
  login: () => Promise<void>;
  logout: () => Promise<void>;
  restoreSession: () => Promise<boolean>;
  switchTenant: (tenantId: string) => Promise<void>;
  setUser: (user: User) => void;
  setLoading: (loading: boolean) => void;
}
```

### Implementacao

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { mmkvStorage } from '../utils/mmkv-storage';
import { AuthService } from '../services/AuthService';

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: true,
      tenant: null,
      allowedTenants: [],
      isTokenExpired: false,

      login: async () => {
        set({ isLoading: true });
        const authService = AuthService.getInstance();
        const user = await authService.login();
        set({
          user,
          isAuthenticated: true,
          isLoading: false,
          tenant: { id: user.tenantId, name: user.allowedTenants[0]?.name ?? '' },
          allowedTenants: user.allowedTenants,
        });
      },

      logout: async () => {
        await AuthService.getInstance().logout();
        set({
          user: null,
          isAuthenticated: false,
          tenant: null,
          allowedTenants: [],
        });
      },

      restoreSession: async () => {
        set({ isLoading: true });
        try {
          const restored = await AuthService.getInstance().restoreSession();
          if (restored) {
            const user = AuthService.getInstance().getCurrentUser();
            set({ user, isAuthenticated: true, isLoading: false });
            return true;
          }
        } catch { /* token expirado */ }
        set({ isLoading: false });
        return false;
      },

      switchTenant: async (tenantId: string) => {
        const { allowedTenants } = get();
        const target = allowedTenants.find(t => t.id === tenantId);
        if (!target) throw new Error('Tenant nao permitido');
        await AuthService.getInstance().switchTenant(tenantId);
        set({ tenant: target });
        // WatermelonDB reset acontece no SyncManager
      },

      setUser: (user) => set({ user, isAuthenticated: true }),
      setLoading: (isLoading) => set({ isLoading }),
    }),
    {
      name: 'auth-store',
      storage: createJSONStorage(() => mmkvStorage),
      partialize: (state) => ({
        user: state.user,
        tenant: state.tenant,
        allowedTenants: state.allowedTenants,
      }),
    }
  )
);
```

Tokens (access_token, refresh_token) nao sao armazenados na store Zustand. Eles vivem exclusivamente no `AuthService` singleton: access_token em memoria e refresh_token no `expo-secure-store`. A store persiste apenas dados do usuario via MMKV para hidratacao rapida no boot.

## useSyncStore

Rastreia estado da sincronizacao, fila de operacoes pendentes e conflitos.

### Interface

```typescript
interface SyncConflict {
  id: string;
  entityType: 'UNIT' | 'HOLDER' | 'UNIT_HOLDER' | 'DOCUMENT';
  entityId: string;
  localData: Record<string, unknown>;
  serverData: Record<string, unknown>;
  conflictingFields: string[];
  createdAt: number;
}

type SyncStatus = 'idle' | 'pulling' | 'pushing' | 'error';

interface SyncState {
  // Estado
  lastSyncAt: number | null;     // timestamp da ultima sync bem-sucedida
  syncStatus: SyncStatus;
  pendingCount: number;           // operacoes na sync_queue
  conflicts: SyncConflict[];
  progress: number;               // 0-100 durante sync
  errorMessage: string | null;

  // Acoes
  startSync: () => Promise<void>;
  resolveConflict: (conflictId: string, resolution: 'local' | 'server' | Record<string, unknown>) => Promise<void>;
  dismissConflict: (conflictId: string) => void;
  setSyncStatus: (status: SyncStatus) => void;
  updatePendingCount: () => Promise<void>;
  resetError: () => void;
}
```

### Persistencia via WatermelonDB

A `useSyncStore` persiste dados criticos (lastSyncAt, conflicts) diretamente no WatermelonDB usando um adapter customizado:

```typescript
import { database } from '../database';

const watermelonSyncStorage = {
  getItem: async (name: string): Promise<string | null> => {
    const collection = database.get('sync_metadata');
    const records = await collection.query().fetch();
    const record = records[0];
    return record ? JSON.stringify({
      state: {
        lastSyncAt: record.lastSyncAt,
        conflicts: JSON.parse(record.conflictsJson || '[]'),
      }
    }) : null;
  },
  setItem: async (name: string, value: string) => {
    const parsed = JSON.parse(value);
    await database.write(async () => {
      // upsert sync_metadata singleton
    });
  },
  removeItem: async (name: string) => {
    // clear sync_metadata
  },
};
```

A contagem de pendentes (`pendingCount`) e calculada sob demanda a partir da collection `sync_queue` do WatermelonDB, nao persistida na store.

## useMapStore

Gerencia estado visual do mapa, layers visiveis, posicao GPS e unidade selecionada.

### Interface

```typescript
interface MapRegion {
  latitude: number;
  longitude: number;
  latitudeDelta: number;
  longitudeDelta: number;
}

type LayerId = 'ortofoto' | 'poligonos' | 'gps_marker' | 'clusters' | 'heatmap';

interface MapState {
  // Estado
  selectedCommunity: { id: string; name: string } | null;
  visibleLayers: LayerId[];
  currentPosition: { latitude: number; longitude: number; accuracy: number } | null;
  zoomLevel: number;
  selectedUnit: string | null;  // unitId selecionado no mapa
  region: MapRegion | null;

  // Acoes
  toggleLayer: (layerId: LayerId) => void;
  centerOn: (latitude: number, longitude: number) => void;
  setSelectedCommunity: (community: { id: string; name: string } | null) => void;
  setSelectedUnit: (unitId: string | null) => void;
  updatePosition: (position: { latitude: number; longitude: number; accuracy: number }) => void;
  setRegion: (region: MapRegion) => void;
  setZoomLevel: (zoom: number) => void;
}
```

### Implementacao

```typescript
export const useMapStore = create<MapState>()(
  persist(
    (set, get) => ({
      selectedCommunity: null,
      visibleLayers: ['ortofoto', 'poligonos', 'gps_marker'],
      currentPosition: null,
      zoomLevel: 16,
      selectedUnit: null,
      region: null,

      toggleLayer: (layerId) => {
        const { visibleLayers } = get();
        const updated = visibleLayers.includes(layerId)
          ? visibleLayers.filter(l => l !== layerId)
          : [...visibleLayers, layerId];
        set({ visibleLayers: updated });
      },

      centerOn: (latitude, longitude) => {
        set({
          region: { latitude, longitude, latitudeDelta: 0.005, longitudeDelta: 0.005 },
        });
      },

      setSelectedCommunity: (community) => set({ selectedCommunity: community }),
      setSelectedUnit: (unitId) => set({ selectedUnit: unitId }),
      updatePosition: (position) => set({ currentPosition: position }),
      setRegion: (region) => set({ region }),
      setZoomLevel: (zoom) => set({ zoomLevel: zoom }),
    }),
    {
      name: 'map-store',
      storage: createJSONStorage(() => mmkvStorage),
      partialize: (state) => ({
        selectedCommunity: state.selectedCommunity,
        visibleLayers: state.visibleLayers,
        zoomLevel: state.zoomLevel,
      }),
    }
  )
);
```

Apenas preferencias visuais (layers visiveis, comunidade selecionada, zoom) sao persistidas. Posicao GPS e unidade selecionada sao efemeras.

## useFormStore

Preserva rascunho do formulario wizard durante navegacao e entre sessoes.

### Interface

```typescript
interface FormDraft {
  // Step 1 - BasicInfo
  attendanceStatus?: 'PRESENTE' | 'AUSENTE' | 'NAO_QUIS';
  unitNumber?: string;
  street?: string;
  residenceTime?: string;
  unitCondition?: string;

  // Step 2 - HolderData
  holderCpf?: string;
  holderName?: string;
  holderBirthDate?: string;
  holderGender?: string;
  holderMaritalStatus?: string;

  // Step 3 - Geolocation
  latitude?: number;
  longitude?: number;
  gpsAccuracy?: number;

  // Step 4 - Photos
  photoUris?: string[];

  // Step 5 - Signature
  signaturePath?: string;
}

interface FormState {
  // Estado
  currentStep: number;         // 1 a 5
  formData: FormDraft;
  isDirty: boolean;
  errors: Record<string, string>;
  editingUnitId: string | null; // null = nova unidade

  // Acoes
  nextStep: () => void;
  prevStep: () => void;
  goToStep: (step: number) => void;
  updateFormData: (partial: Partial<FormDraft>) => void;
  setErrors: (errors: Record<string, string>) => void;
  clearError: (field: string) => void;
  submitForm: () => Promise<void>;
  resetForm: () => void;
  loadDraft: (unitId: string | null) => void;
}
```

### Persistencia de Rascunho

O rascunho persiste via MMKV com debounce de 2 segundos. Se o app for fechado antes da finalizacao, o rascunho e restaurado automaticamente ao reabrir:

```typescript
export const useFormStore = create<FormState>()(
  persist(
    (set, get) => ({
      currentStep: 1,
      formData: {},
      isDirty: false,
      errors: {},
      editingUnitId: null,

      nextStep: () => {
        const { currentStep } = get();
        if (currentStep < 5) set({ currentStep: currentStep + 1 });
      },

      prevStep: () => {
        const { currentStep } = get();
        if (currentStep > 1) set({ currentStep: currentStep - 1 });
      },

      goToStep: (step) => set({ currentStep: step }),

      updateFormData: (partial) => {
        set((state) => ({
          formData: { ...state.formData, ...partial },
          isDirty: true,
        }));
      },

      resetForm: () => set({
        currentStep: 1,
        formData: {},
        isDirty: false,
        errors: {},
        editingUnitId: null,
      }),

      submitForm: async () => {
        // Validacao final + persist no WatermelonDB + enfileirar sync_queue
        // Detalhes em 01-field-collection.md
      },

      // ... demais acoes
    }),
    {
      name: 'form-store',
      storage: createJSONStorage(() => mmkvStorage),
      partialize: (state) => ({
        currentStep: state.currentStep,
        formData: state.formData,
        editingUnitId: state.editingUnitId,
      }),
    }
  )
);
```

## Integracao com WatermelonDB Observables

WatermelonDB fornece observables reativos que emitem novos valores quando registros mudam. A integracao com componentes React usa o hook `useObservable` do `@nozbe/watermelondb/react`:

```typescript
import { useObservable } from '@nozbe/watermelondb/react';

function UnitCard({ unitId }: { unitId: string }) {
  const unit = useObservable(
    () => database.get<Unit>('units').findAndObserve(unitId),
    [unitId]
  );

  // unit atualiza automaticamente quando o registro muda no WatermelonDB
  return <Card title={unit?.code} status={unit?.attendance_status} />;
}
```

Queries complexas com filtros:

```typescript
function useUnitsForCommunity(communityId: string) {
  return useObservable(
    () => database.get<Unit>('units')
      .query(Q.where('community_id', communityId))
      .observeWithColumns(['attendance_status', 'version']),
    [communityId]
  );
}
```

## TanStack Query para Estado de Servidor

TanStack Query gerencia cache de dados remotos com estrategia otimizada para offline-first:

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: Infinity,          // dados nunca ficam stale automaticamente
      gcTime: 1000 * 60 * 60 * 24,  // cache por 24 horas
      retry: 2,
      networkMode: 'offlineFirst',  // tenta cache antes de rede
    },
  },
});
```

### Invalidacao Apos Sync

Apos sincronizacao bem-sucedida, o `SyncManager` invalida queries relevantes para forcar re-fetch dos dados atualizados:

```typescript
// No SyncManager, apos sync bem-sucedida
queryClient.invalidateQueries({ queryKey: ['units'] });
queryClient.invalidateQueries({ queryKey: ['holders'] });
queryClient.invalidateQueries({ queryKey: ['communities'] });
```

### Uso com Dados Offline

```typescript
function useSyncStatus() {
  return useQuery({
    queryKey: ['sync', 'status'],
    queryFn: () => geoApiClient.sync.getStatus(),
    enabled: isOnline,   // so executa se online
    staleTime: 30_000,   // re-fetch a cada 30s quando online
  });
}
```

## Diagrama de Fluxo de Estado

```
┌──────────────────────────────────────────────────────────┐
│                      Componente React                     │
│                                                          │
│  useAuthStore()  useSyncStore()  useMapStore()  useForm() │
│       │               │              │             │      │
└───────┼───────────────┼──────────────┼─────────────┼──────┘
        │               │              │             │
   ┌────▼────┐    ┌─────▼─────┐  ┌────▼────┐  ┌────▼────┐
   │  MMKV   │    │WatermelonDB│  │  MMKV   │  │  MMKV   │
   │(user)   │    │(sync_queue)│  │(prefs)  │  │(draft)  │
   └────┬────┘    └─────┬─────┘  └─────────┘  └─────────┘
        │               │
   ┌────▼────┐    ┌─────▼──────┐
   │SecureStr│    │TanStack Qry│
   │(tokens) │    │(server st.)│
   └─────────┘    └────────────┘
```

## Referencias

- [ADR-002 - Zustand](../ADRs/ADR-002-state-management.md)
- [WatermelonDB Schema](../DATA/01-watermelondb-schema.md)
- [Offline Sync](../FEATURES/03-offline-sync.md)
- [Conflict Resolution](../DATA/02-conflict-resolution.md)
- [AuthService Layer](../LAYERS/01-auth-service.md)
