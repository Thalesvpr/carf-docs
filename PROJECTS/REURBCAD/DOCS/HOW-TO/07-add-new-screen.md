---
type: leaf
status: review
updated: 2026-02-08
---

# Como Adicionar uma Nova Tela

Guia passo-a-passo para adicionar uma nova tela ao REURBCAD, cobrindo desde a rota Expo Router ate a integracao com sync offline. Usa como exemplo concreto a criacao de uma tela "Edificacao" (Building) vinculada a uma unidade.

## Visao Geral dos Passos

| Passo | Acao | Arquivos Envolvidos |
|-------|------|---------------------|
| 1 | Criar rota Expo Router | `app/(tabs)/...` |
| 2 | Definir model WatermelonDB (se nova entidade) | `src/database/` |
| 3 | Criar ou atualizar Zustand store | `src/stores/` |
| 4 | Criar custom hooks | `src/hooks/` |
| 5 | Criar componentes de UI | `src/components/` |
| 6 | Adicionar validacao Zod | `src/utils/` ou `src/types/` |
| 7 | Integrar com sync queue | `src/services/SyncManager.ts` |
| 8 | Adicionar entrada de navegacao | Layout de tabs ou stack |

## Passo 1: Criar Rota Expo Router

O Expo Router usa file-based routing. Criar o arquivo no diretorio `app/` define a rota automaticamente.

Para a tela de Edificacao, que e um detalhe acessivel a partir de uma unidade:

```
app/(tabs)/mapa/[unitId]/edificacao/
  nova.tsx           # Formulario de nova edificacao
  [buildingId].tsx   # Detalhe/edicao de edificacao existente
```

Criar o arquivo da rota:

```typescript
// app/(tabs)/mapa/[unitId]/edificacao/nova.tsx
import { useLocalSearchParams } from 'expo-router';
import { ScreenErrorBoundary } from '@/components/errors/ScreenErrorBoundary';
import { BuildingFormScreen } from '@/components/domain/BuildingFormScreen';

export default function NovaBuildingScreen() {
  const { unitId } = useLocalSearchParams<{ unitId: string }>();

  return (
    <ScreenErrorBoundary screenName="NovaBuildingScreen">
      <BuildingFormScreen unitId={unitId} />
    </ScreenErrorBoundary>
  );
}
```

Criar o arquivo de detalhe:

```typescript
// app/(tabs)/mapa/[unitId]/edificacao/[buildingId].tsx
import { useLocalSearchParams } from 'expo-router';
import { ScreenErrorBoundary } from '@/components/errors/ScreenErrorBoundary';
import { BuildingFormScreen } from '@/components/domain/BuildingFormScreen';

export default function EditBuildingScreen() {
  const { unitId, buildingId } = useLocalSearchParams<{
    unitId: string;
    buildingId: string;
  }>();

  return (
    <ScreenErrorBoundary screenName="EditBuildingScreen">
      <BuildingFormScreen unitId={unitId} buildingId={buildingId} />
    </ScreenErrorBoundary>
  );
}
```

## Passo 2: Definir Model WatermelonDB

Se a nova tela representa uma entidade nova no banco local, criar model, schema e migration.

### 2.1 Adicionar tabela ao Schema

```typescript
// src/database/schema.ts
import { appSchema, tableSchema } from '@nozbe/watermelondb';

export const schema = appSchema({
  version: 8, // incrementar versao
  tables: [
    // ... tabelas existentes (units, holders, etc.)
    tableSchema({
      name: 'buildings',
      columns: [
        { name: 'server_id', type: 'string', isOptional: true },
        { name: 'tenant_id', type: 'string' },
        { name: 'unit_id', type: 'string', isIndexed: true },
        { name: 'name', type: 'string' },
        { name: 'floors', type: 'number' },
        { name: 'built_area', type: 'number' },
        { name: 'construction_type', type: 'string' },
        { name: 'condition', type: 'string' },
        { name: 'observation', type: 'string', isOptional: true },
        { name: 'created_by', type: 'string' },
        { name: 'version', type: 'number' },
        { name: 'created_at', type: 'number' },
        { name: 'updated_at', type: 'number' },
      ],
    }),
  ],
});
```

### 2.2 Criar Migration

```typescript
// src/database/migrations.ts
import { schemaMigrations, addColumns, createTable } from '@nozbe/watermelondb/Schema/migrations';

export const migrations = schemaMigrations({
  migrations: [
    // ... migrations anteriores
    {
      toVersion: 8,
      steps: [
        createTable({
          name: 'buildings',
          columns: [
            { name: 'server_id', type: 'string', isOptional: true },
            { name: 'tenant_id', type: 'string' },
            { name: 'unit_id', type: 'string', isIndexed: true },
            { name: 'name', type: 'string' },
            { name: 'floors', type: 'number' },
            { name: 'built_area', type: 'number' },
            { name: 'construction_type', type: 'string' },
            { name: 'condition', type: 'string' },
            { name: 'observation', type: 'string', isOptional: true },
            { name: 'created_by', type: 'string' },
            { name: 'version', type: 'number' },
            { name: 'created_at', type: 'number' },
            { name: 'updated_at', type: 'number' },
          ],
        }),
      ],
    },
  ],
});
```

### 2.3 Criar Model Class

```typescript
// src/database/models/Building.ts
import { Model } from '@nozbe/watermelondb';
import { field, date, relation, readonly } from '@nozbe/watermelondb/decorators';

export class Building extends Model {
  static table = 'buildings';

  static associations = {
    units: { type: 'belongs_to' as const, key: 'unit_id' },
  };

  @field('server_id') serverId!: string | null;
  @field('tenant_id') tenantId!: string;
  @field('unit_id') unitId!: string;
  @field('name') name!: string;
  @field('floors') floors!: number;
  @field('built_area') builtArea!: number;
  @field('construction_type') constructionType!: string;
  @field('condition') condition!: string;
  @field('observation') observation!: string | null;
  @field('created_by') createdBy!: string;
  @field('version') version!: number;
  @readonly @date('created_at') createdAt!: Date;
  @readonly @date('updated_at') updatedAt!: Date;

  @relation('units', 'unit_id') unit: any;
}
```

### 2.4 Registrar no Database

```typescript
// src/database/index.ts
import { Building } from './models/Building';

const database = new Database({
  adapter,
  modelClasses: [
    Unit, Holder, UnitHolder, Document, Community,
    Team, TeamMember, SyncQueue, SyncMetadata,
    Building, // adicionar aqui
  ],
});
```

## Passo 3: Criar ou Atualizar Zustand Store

Se a nova tela precisa de estado global (rascunho de formulario, selecao ativa), criar ou estender uma store.

Para o formulario de edificacao, estender o `useFormStore` ou criar store dedicada se a complexidade justificar:

```typescript
// src/stores/useBuildingFormStore.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { mmkvStorage } from '@/utils/mmkv-storage';

interface BuildingFormDraft {
  name?: string;
  floors?: number;
  builtArea?: number;
  constructionType?: string;
  condition?: string;
  observation?: string;
}

interface BuildingFormState {
  formData: BuildingFormDraft;
  isDirty: boolean;
  editingBuildingId: string | null;

  updateFormData: (partial: Partial<BuildingFormDraft>) => void;
  resetForm: () => void;
  loadDraft: (buildingId: string | null) => void;
}

export const useBuildingFormStore = create<BuildingFormState>()(
  persist(
    (set) => ({
      formData: {},
      isDirty: false,
      editingBuildingId: null,

      updateFormData: (partial) =>
        set((state) => ({
          formData: { ...state.formData, ...partial },
          isDirty: true,
        })),

      resetForm: () =>
        set({ formData: {}, isDirty: false, editingBuildingId: null }),

      loadDraft: (buildingId) =>
        set({ editingBuildingId: buildingId }),
    }),
    {
      name: 'building-form-store',
      storage: createJSONStorage(() => mmkvStorage),
      partialize: (state) => ({
        formData: state.formData,
        editingBuildingId: state.editingBuildingId,
      }),
    }
  )
);
```

## Passo 4: Criar Custom Hooks

### Hook de Observacao WatermelonDB

```typescript
// src/hooks/useBuilding.ts
import { useEffect, useState } from 'react';
import { Q } from '@nozbe/watermelondb';
import { database } from '@/database';
import { Building } from '@/database/models/Building';

export function useBuilding(buildingId: string | undefined) {
  const [building, setBuilding] = useState<Building | null>(null);

  useEffect(() => {
    if (!buildingId) return;
    const subscription = database
      .get<Building>('buildings')
      .findAndObserve(buildingId)
      .subscribe(setBuilding);
    return () => subscription.unsubscribe();
  }, [buildingId]);

  return building;
}

export function useBuildingsForUnit(unitId: string) {
  const [buildings, setBuildings] = useState<Building[]>([]);

  useEffect(() => {
    const subscription = database
      .get<Building>('buildings')
      .query(Q.where('unit_id', unitId))
      .observe()
      .subscribe(setBuildings);
    return () => subscription.unsubscribe();
  }, [unitId]);

  return buildings;
}
```

### Hook de Formulario

```typescript
// src/hooks/useBuildingForm.ts
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { buildingSchema, BuildingFormData } from '@/types/building-schema';
import { useBuildingFormStore } from '@/stores/useBuildingFormStore';

export function useBuildingForm(buildingId?: string) {
  const { formData, updateFormData, resetForm } = useBuildingFormStore();

  const form = useForm<BuildingFormData>({
    resolver: zodResolver(buildingSchema),
    defaultValues: formData,
    mode: 'onChange',
  });

  const onSubmit = async (data: BuildingFormData) => {
    // Persistir no WatermelonDB + enfileirar sync
    await saveBuildingLocally(data, buildingId);
    resetForm();
  };

  return { form, onSubmit };
}
```

## Passo 5: Criar Componentes de UI

### Componente de Formulario

```typescript
// src/components/domain/BuildingFormScreen.tsx
import React from 'react';
import { ScrollView, View } from 'react-native';
import { FormErrorBoundary } from '@/components/errors/FormErrorBoundary';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Button } from '@/components/ui/Button';
import { useBuildingForm } from '@/hooks/useBuildingForm';

interface Props {
  unitId: string;
  buildingId?: string;
}

export function BuildingFormScreen({ unitId, buildingId }: Props) {
  const { form, onSubmit } = useBuildingForm(buildingId);
  const { control, handleSubmit, formState: { errors } } = form;

  return (
    <FormErrorBoundary>
      <ScrollView contentContainerStyle={styles.container}>
        <Input
          control={control}
          name="name"
          label="Nome da Edificacao"
          placeholder="Ex: Bloco A"
          error={errors.name?.message}
        />
        <Input
          control={control}
          name="floors"
          label="Numero de Pavimentos"
          keyboardType="numeric"
          error={errors.floors?.message}
        />
        <Input
          control={control}
          name="builtArea"
          label="Area Construida (m2)"
          keyboardType="decimal-pad"
          error={errors.builtArea?.message}
        />
        <Select
          control={control}
          name="constructionType"
          label="Tipo de Construcao"
          options={[
            { label: 'Alvenaria', value: 'ALVENARIA' },
            { label: 'Madeira', value: 'MADEIRA' },
            { label: 'Mista', value: 'MISTA' },
            { label: 'Metalica', value: 'METALICA' },
            { label: 'Outro', value: 'OUTRO' },
          ]}
          error={errors.constructionType?.message}
        />
        <Select
          control={control}
          name="condition"
          label="Condicao"
          options={[
            { label: 'Boa', value: 'BOA' },
            { label: 'Regular', value: 'REGULAR' },
            { label: 'Precaria', value: 'PRECARIA' },
            { label: 'Em Ruinas', value: 'RUINAS' },
          ]}
          error={errors.condition?.message}
        />
        <Input
          control={control}
          name="observation"
          label="Observacao"
          multiline
          numberOfLines={3}
        />
        <Button title="Salvar" onPress={handleSubmit(onSubmit)} />
      </ScrollView>
    </FormErrorBoundary>
  );
}
```

### Componente de Card (para listagem)

```typescript
// src/components/domain/BuildingCard.tsx
import React from 'react';
import { View, Text, Pressable } from 'react-native';
import { Card } from '@/components/ui/Card';
import { StatusBadge } from '@/components/domain/StatusBadge';
import { Building } from '@/database/models/Building';

interface Props {
  building: Building;
  onPress: () => void;
}

export function BuildingCard({ building, onPress }: Props) {
  return (
    <Pressable onPress={onPress}>
      <Card>
        <Text style={styles.name}>{building.name}</Text>
        <Text style={styles.detail}>
          {building.floors} pavimento(s) - {building.builtArea} m2
        </Text>
        <StatusBadge status={building.condition} />
      </Card>
    </Pressable>
  );
}
```

## Passo 6: Adicionar Validacao Zod

Criar schema de validacao para o formulario:

```typescript
// src/types/building-schema.ts
import { z } from 'zod';

export const buildingSchema = z.object({
  name: z.string()
    .min(2, 'Nome deve ter no minimo 2 caracteres')
    .max(100, 'Nome deve ter no maximo 100 caracteres')
    .trim(),
  floors: z.number()
    .int('Numero de pavimentos deve ser inteiro')
    .min(1, 'Minimo 1 pavimento')
    .max(50, 'Maximo 50 pavimentos'),
  builtArea: z.number()
    .min(5, 'Area minima 5 m2')
    .max(50000, 'Area maxima 50.000 m2'),
  constructionType: z.enum(
    ['ALVENARIA', 'MADEIRA', 'MISTA', 'METALICA', 'OUTRO'],
    { errorMap: () => ({ message: 'Selecione o tipo de construcao' }) }
  ),
  condition: z.enum(
    ['BOA', 'REGULAR', 'PRECARIA', 'RUINAS'],
    { errorMap: () => ({ message: 'Selecione a condicao' }) }
  ),
  observation: z.string().max(500).optional(),
});

export type BuildingFormData = z.infer<typeof buildingSchema>;
```

## Passo 7: Integrar com Sync Queue

Ao salvar o formulario, persistir no WatermelonDB e enfileirar na sync_queue:

```typescript
// src/services/building-operations.ts
import { database } from '@/database';
import { Building } from '@/database/models/Building';
import { SyncQueue } from '@/database/models/SyncQueue';
import { useAuthStore } from '@/stores/useAuthStore';

export async function saveBuildingLocally(
  data: BuildingFormData,
  buildingId?: string
): Promise<void> {
  const user = useAuthStore.getState().user!;
  const tenant = useAuthStore.getState().tenant!;

  await database.write(async () => {
    if (buildingId) {
      // UPDATE existente
      const building = await database.get<Building>('buildings').find(buildingId);
      await building.update((b) => {
        b.name = data.name;
        b.floors = data.floors;
        b.builtArea = data.builtArea;
        b.constructionType = data.constructionType;
        b.condition = data.condition;
        b.observation = data.observation ?? null;
        b.version = b.version + 1;
      });

      // Enfileirar UPDATE na sync_queue
      await database.get<SyncQueue>('sync_queue').create((sq) => {
        sq.entityType = 'BUILDING';
        sq.entityId = buildingId;
        sq.operation = 'UPDATE';
        sq.payload = JSON.stringify(data);
        sq.retryCount = 0;
        sq.status = 'PENDING';
        sq.createdAt = Date.now();
      });
    } else {
      // CREATE novo
      const building = await database.get<Building>('buildings').create((b) => {
        b.tenantId = tenant.id;
        b.unitId = data.unitId;
        b.name = data.name;
        b.floors = data.floors;
        b.builtArea = data.builtArea;
        b.constructionType = data.constructionType;
        b.condition = data.condition;
        b.observation = data.observation ?? null;
        b.createdBy = user.id;
        b.version = 1;
      });

      // Enfileirar CREATE na sync_queue
      await database.get<SyncQueue>('sync_queue').create((sq) => {
        sq.entityType = 'BUILDING';
        sq.entityId = building.id;
        sq.operation = 'CREATE';
        sq.payload = JSON.stringify({ ...data, localId: building.id });
        sq.retryCount = 0;
        sq.status = 'PENDING';
        sq.createdAt = Date.now();
      });
    }
  });
}
```

### Atualizar SyncManager

Adicionar o handler de `BUILDING` no `SyncManager` para que o push saiba como enviar buildings ao servidor:

```typescript
// src/services/SyncManager.ts (adicionar ao switch de entity types)
case 'BUILDING':
  if (operation === 'CREATE') {
    response = await geoApiClient.buildings.create(payload);
  } else if (operation === 'UPDATE') {
    response = await geoApiClient.buildings.update(payload.serverId, payload);
  }
  break;
```

## Passo 8: Adicionar Navegacao

### Link a partir da tela de detalhe da unidade

Na tela de detalhe da unidade, adicionar botao para navegar para a nova tela:

```typescript
// No componente UnitDetail, adicionar secao de edificacoes
import { router } from 'expo-router';
import { useBuildingsForUnit } from '@/hooks/useBuilding';
import { BuildingCard } from '@/components/domain/BuildingCard';

function BuildingsSection({ unitId }: { unitId: string }) {
  const buildings = useBuildingsForUnit(unitId);

  return (
    <View>
      <Text style={styles.sectionTitle}>Edificacoes</Text>
      {buildings.map(building => (
        <BuildingCard
          key={building.id}
          building={building}
          onPress={() => router.push(
            `/(tabs)/mapa/${unitId}/edificacao/${building.id}`
          )}
        />
      ))}
      <Button
        title="Adicionar Edificacao"
        onPress={() => router.push(`/(tabs)/mapa/${unitId}/edificacao/nova`)}
      />
    </View>
  );
}
```

## Checklist Final

Antes de considerar a nova tela pronta, verificar:

| Item | Verificacao |
|------|------------|
| Rota acessivel | Navegar para a tela via app funciona |
| Formulario valida | Campos obrigatorios bloqueiam submit |
| Dados persistem offline | Criar registro sem internet, verificar no WatermelonDB |
| Sync funciona | Reconectar e verificar que dados sobem ao servidor |
| Error boundary | Simular erro de renderizacao, verificar que app nao crasha |
| Role guard | Verificar que FIELD_CADASTRATOR acessa a tela (se aplicavel) |
| Rascunho persiste | Fechar app no meio do formulario, reabrir e verificar dados |
| Tipos corretos | `tsc --noEmit` passa sem erros |
| Lint passa | `npx eslint src/` sem warnings |

## Referencias

- [Navigation Structure](../ARCHITECTURE/03-navigation-structure.md)
- [State Management](../ARCHITECTURE/04-state-management.md)
- [Project Structure](../ARCHITECTURE/06-project-structure.md)
- [WatermelonDB Schema](../DATA/01-watermelondb-schema.md)
- [Error Handling](../ARCHITECTURE/05-error-handling.md)
- [Offline Sync](../FEATURES/03-offline-sync.md)
- [Form Library ADR](../ADRs/ADR-004-form-library.md)
- [Field Collection](../FEATURES/01-field-collection.md)
