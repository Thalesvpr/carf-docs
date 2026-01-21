---
status: review
updated: 2026-01-21
---

# Integration - @carf/ui

@carf/ui é consumida por GEOWEB e ADMIN via NPM install do GitHub Packages, importando componentes individuais com tree-shaking automático (`import { Button, UnitCard } from '@carf/ui'`). Aplicações consumidoras devem configurar Tailwind CSS content paths para incluir os paths da lib no `content` do `tailwind.config.js` garantindo que classes Tailwind dos componentes sejam compiladas no bundle final. Theme customization é feita via CSS variables (`--primary`, `--radius`) definidas em `app/globals.css` seguindo convenções de instalação shadcn/ui, permitindo trocar cores, fontes e espaçamentos sem modificar código dos componentes. Para componentes de domínio (UnitCard, HolderCard), aplicações devem fornecer types de `@carf/tscore` como props e opcionalmente integrar com `@carf/geoapi-client` para data fetching, mantendo lógica de negócio fora da lib de UI.

## Setup em GEOWEB

```json
// package.json
{
  "dependencies": {
    "@carf/ui": "^0.1.0",
    "@carf/tscore": "^0.1.0"
  }
}
```

```ts
// tailwind.config.ts
export default {
  content: [
    "./app/**/*.{ts,tsx}",
    "./node_modules/@carf/ui/**/*.{ts,tsx}"  // Inclui lib
  ]
}
```

```css
/* app/globals.css */
@layer base {
  :root {
    --primary: 220 90% 56%;     /* Azul CARF */
    --radius: 0.5rem;
  }
}
```

```tsx
// app/units/page.tsx
import { UnitCard } from '@carf/ui'
import type { Unit } from '@carf/tscore/types'

export default function UnitsPage() {
  const units: Unit[] = await fetchUnits()

  return (
    <div>
      {units.map(unit => (
        <UnitCard key={unit.id} unit={unit} onEdit={handleEdit} />
      ))}
    </div>
  )
}
```

## Integração com Zustand

@carf/ui é agnóstica quanto a gerenciamento de estado. Componentes recebem dados e callbacks via props, permitindo integração com qualquer solução de estado. O padrão recomendado para GEOWEB e ADMIN é Zustand para client state.

### Store de Filtros

```tsx
// stores/filter-store.ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface FilterState {
  status: 'all' | 'pending' | 'approved' | 'rejected'
  search: string
  dateRange: { from: Date | null; to: Date | null }
  setStatus: (status: FilterState['status']) => void
  setSearch: (search: string) => void
  setDateRange: (range: FilterState['dateRange']) => void
  resetFilters: () => void
}

const initialState = {
  status: 'all' as const,
  search: '',
  dateRange: { from: null, to: null },
}

export const useFilterStore = create<FilterState>()(
  devtools(
    persist(
      (set) => ({
        ...initialState,
        setStatus: (status) => set({ status }),
        setSearch: (search) => set({ search }),
        setDateRange: (dateRange) => set({ dateRange }),
        resetFilters: () => set(initialState),
      }),
      { name: 'filter-storage' }
    )
  )
)
```

### Uso com Componentes

```tsx
// components/units-filter.tsx
import { Select, Input, DateRangePicker, Button } from '@carf/ui'
import { useFilterStore } from '@/stores/filter-store'

export function UnitsFilter() {
  const { status, search, dateRange, setStatus, setSearch, setDateRange, resetFilters } =
    useFilterStore()

  return (
    <div className="flex flex-col gap-4 md:flex-row md:items-end">
      <div className="flex-1">
        <Label>Buscar</Label>
        <Input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="CPF, endereço, protocolo..."
        />
      </div>

      <div className="w-full md:w-48">
        <Label>Status</Label>
        <Select value={status} onValueChange={setStatus}>
          <Select.Trigger>
            <Select.Value placeholder="Todos" />
          </Select.Trigger>
          <Select.Content>
            <Select.Item value="all">Todos</Select.Item>
            <Select.Item value="pending">Pendentes</Select.Item>
            <Select.Item value="approved">Aprovados</Select.Item>
            <Select.Item value="rejected">Rejeitados</Select.Item>
          </Select.Content>
        </Select>
      </div>

      <div className="w-full md:w-auto">
        <Label>Período</Label>
        <DateRangePicker value={dateRange} onChange={setDateRange} />
      </div>

      <Button variant="outline" onClick={resetFilters}>
        Limpar Filtros
      </Button>
    </div>
  )
}
```

### Store com Selectors

Para evitar re-renders desnecessários, use selectors para extrair apenas o estado necessário.

```tsx
// Selector granular
const status = useFilterStore((state) => state.status)
const setStatus = useFilterStore((state) => state.setStatus)

// Selector com shallow compare para objetos
import { shallow } from 'zustand/shallow'

const { from, to } = useFilterStore(
  (state) => ({ from: state.dateRange.from, to: state.dateRange.to }),
  shallow
)
```

## Integração com React Query (TanStack Query)

Para server state (dados da API), usar TanStack Query que fornece cache, refetch automático, optimistic updates e sincronização entre tabs.

### Setup do QueryClient

```tsx
// app/providers.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutos
      gcTime: 1000 * 60 * 30,   // 30 minutos
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}
```

### Query Hooks

```tsx
// hooks/use-units.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { geoApiClient } from '@carf/geoapi-client'
import type { Unit, CreateUnitInput } from '@carf/tscore/types'

export function useUnits(tenantId: string, filters?: FilterState) {
  return useQuery({
    queryKey: ['units', tenantId, filters],
    queryFn: () => geoApiClient.units.list(tenantId, {
      status: filters?.status !== 'all' ? filters?.status : undefined,
      search: filters?.search || undefined,
      fromDate: filters?.dateRange.from?.toISOString(),
      toDate: filters?.dateRange.to?.toISOString(),
    }),
    enabled: !!tenantId,
  })
}

export function useUnit(tenantId: string, unitId: string) {
  return useQuery({
    queryKey: ['unit', tenantId, unitId],
    queryFn: () => geoApiClient.units.get(tenantId, unitId),
    enabled: !!tenantId && !!unitId,
  })
}

export function useCreateUnit(tenantId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (input: CreateUnitInput) =>
      geoApiClient.units.create(tenantId, input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['units', tenantId] })
    },
  })
}

export function useUpdateUnit(tenantId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ unitId, input }: { unitId: string; input: Partial<Unit> }) =>
      geoApiClient.units.update(tenantId, unitId, input),
    onMutate: async ({ unitId, input }) => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: ['unit', tenantId, unitId] })
      const previousUnit = queryClient.getQueryData<Unit>(['unit', tenantId, unitId])

      queryClient.setQueryData<Unit>(['unit', tenantId, unitId], (old) =>
        old ? { ...old, ...input } : old
      )

      return { previousUnit }
    },
    onError: (err, { unitId }, context) => {
      // Rollback on error
      if (context?.previousUnit) {
        queryClient.setQueryData(['unit', tenantId, unitId], context.previousUnit)
      }
    },
    onSettled: (data, error, { unitId }) => {
      queryClient.invalidateQueries({ queryKey: ['unit', tenantId, unitId] })
      queryClient.invalidateQueries({ queryKey: ['units', tenantId] })
    },
  })
}
```

### Uso com Componentes

```tsx
// app/units/page.tsx
import { UnitCard, Skeleton, Alert } from '@carf/ui'
import { useUnits } from '@/hooks/use-units'
import { useFilterStore } from '@/stores/filter-store'
import { useTenant } from '@/hooks/use-tenant'

export default function UnitsPage() {
  const { tenantId } = useTenant()
  const filters = useFilterStore()
  const { data: units, isLoading, error } = useUnits(tenantId, filters)

  if (isLoading) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-48" />
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertTitle>Erro ao carregar unidades</AlertTitle>
        <AlertDescription>{error.message}</AlertDescription>
      </Alert>
    )
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {units?.map((unit) => (
        <UnitCard key={unit.id} unit={unit} />
      ))}
    </div>
  )
}
```

## Integração com React Hook Form

Formulários utilizam React Hook Form com validação Zod. Componentes @carf/ui são compatíveis via `<Controller>` ou register direto.

### Schema com Zod

```tsx
// schemas/unit-schema.ts
import { z } from 'zod'
import { cpf } from '@carf/tscore/validators'

export const unitSchema = z.object({
  address: z.string().min(10, 'Endereço deve ter pelo menos 10 caracteres'),
  neighborhood: z.string().min(2, 'Bairro é obrigatório'),
  area: z.number().positive('Área deve ser maior que zero'),
  holderCpf: z.string().refine(cpf.isValid, 'CPF inválido'),
  holderName: z.string().min(3, 'Nome deve ter pelo menos 3 caracteres'),
  holderEmail: z.string().email('Email inválido').optional().or(z.literal('')),
})

export type UnitFormValues = z.infer<typeof unitSchema>
```

### Form Component

```tsx
// components/unit-form.tsx
import { useForm, Controller } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
  Input,
  Button,
} from '@carf/ui'
import { unitSchema, type UnitFormValues } from '@/schemas/unit-schema'
import { useCpfMask } from '@carf/ui/hooks'

interface UnitFormProps {
  defaultValues?: Partial<UnitFormValues>
  onSubmit: (values: UnitFormValues) => Promise<void>
  isSubmitting?: boolean
}

export function UnitForm({ defaultValues, onSubmit, isSubmitting }: UnitFormProps) {
  const form = useForm<UnitFormValues>({
    resolver: zodResolver(unitSchema),
    defaultValues: {
      address: '',
      neighborhood: '',
      area: 0,
      holderCpf: '',
      holderName: '',
      holderEmail: '',
      ...defaultValues,
    },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <div className="grid gap-4 md:grid-cols-2">
          <FormField
            control={form.control}
            name="address"
            render={({ field }) => (
              <FormItem className="md:col-span-2">
                <FormLabel>Endereço</FormLabel>
                <FormControl>
                  <Input placeholder="Rua, número, complemento" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="neighborhood"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Bairro</FormLabel>
                <FormControl>
                  <Input {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="area"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Área (m²)</FormLabel>
                <FormControl>
                  <Input
                    type="number"
                    step="0.01"
                    {...field}
                    onChange={(e) => field.onChange(parseFloat(e.target.value))}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="border-t pt-6">
          <h3 className="text-lg font-medium mb-4">Dados do Titular</h3>
          <div className="grid gap-4 md:grid-cols-2">
            <FormField
              control={form.control}
              name="holderCpf"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>CPF</FormLabel>
                  <FormControl>
                    <CpfInput {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="holderName"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Nome Completo</FormLabel>
                  <FormControl>
                    <Input {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="holderEmail"
              render={({ field }) => (
                <FormItem className="md:col-span-2">
                  <FormLabel>Email (opcional)</FormLabel>
                  <FormControl>
                    <Input type="email" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>
        </div>

        <div className="flex justify-end gap-4">
          <Button type="button" variant="outline" onClick={() => form.reset()}>
            Limpar
          </Button>
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Salvando...' : 'Salvar'}
          </Button>
        </div>
      </form>
    </Form>
  )
}

// CPF Input com máscara
function CpfInput({ value, onChange, ...props }: React.InputHTMLAttributes<HTMLInputElement>) {
  const { maskedValue, handleChange } = useCpfMask(value as string)

  return (
    <Input
      {...props}
      value={maskedValue}
      onChange={(e) => {
        handleChange(e)
        onChange?.(e)
      }}
      placeholder="000.000.000-00"
    />
  )
}
```

## Integração com WebDocs (Astro)

WebDocs usa Astro com Starlight para documentação. Componentes @carf/ui podem ser usados em páginas MDX via islands architecture.

### Setup

```ts
// astro.config.mjs
import { defineConfig } from 'astro/config'
import starlight from '@astrojs/starlight'
import react from '@astrojs/react'
import tailwind from '@astrojs/tailwind'

export default defineConfig({
  integrations: [
    starlight({ title: 'CARF Docs' }),
    react(),
    tailwind({ applyBaseStyles: false }),
  ],
})
```

### Uso em MDX

```mdx
---
title: Componentes de Formulário
---

import { Button, Input, FormField, Label } from '@carf/ui'

# Componentes de Formulário

Exemplo interativo de FormField:

<FormField client:load>
  <Label htmlFor="demo">Campo de Exemplo</Label>
  <Input id="demo" placeholder="Digite algo..." />
</FormField>

<Button client:load onClick={() => alert('Clicado!')}>
  Clique aqui
</Button>
```

## Integração com Keycloakify

Para temas Keycloak, @carf/ui é consumida via Keycloakify permitindo reutilização de componentes nas páginas de login. Ver [ADR-024: Keycloakify Adoption](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-024-keycloakify-adoption.md).

### Setup no Projeto Keycloakify

```json
// package.json
{
  "dependencies": {
    "@carf/ui": "^0.1.0",
    "keycloakify": "^10.0.0"
  }
}
```

```tsx
// src/login/pages/Login.tsx
import { Button, Input, FormField, Label, Alert } from '@carf/ui'
import { useCpfMask } from '@carf/ui/hooks'
import type { KcContext } from '../kcContext'
import type { I18n } from '../i18n'

export function Login({ kcContext, i18n }: { kcContext: KcContext; i18n: I18n }) {
  const { url, realm, login, message } = kcContext
  const { msg } = i18n
  const { maskedValue, handleChange } = useCpfMask(login.username)

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="w-full max-w-md p-8 bg-card rounded-lg shadow-lg">
        <h1 className="text-2xl font-bold text-center mb-6">
          {msg('loginTitle')}
        </h1>

        {message && (
          <Alert variant={message.type === 'error' ? 'destructive' : 'default'}>
            {message.summary}
          </Alert>
        )}

        <form action={url.loginAction} method="post" className="space-y-4">
          <FormField>
            <Label htmlFor="username">{msg('username')}</Label>
            <Input
              id="username"
              name="username"
              value={maskedValue}
              onChange={handleChange}
              autoFocus
            />
          </FormField>

          <FormField>
            <Label htmlFor="password">{msg('password')}</Label>
            <Input
              id="password"
              name="password"
              type="password"
            />
          </FormField>

          <Button type="submit" className="w-full">
            {msg('doLogIn')}
          </Button>
        </form>

        {realm.registrationAllowed && (
          <p className="text-center mt-4">
            <a href={url.registrationUrl} className="text-primary hover:underline">
              {msg('doRegister')}
            </a>
          </p>
        )}
      </div>
    </div>
  )
}
```

## Testes de Integração

Testes end-to-end verificam integração correta entre @carf/ui e aplicações consumidoras.

### Playwright Config

```ts
// playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'bun run dev',
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
})
```

### Teste E2E

```ts
// e2e/unit-form.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Unit Form', () => {
  test('validates CPF and submits form', async ({ page }) => {
    await page.goto('/units/new')

    // Preenche campos obrigatórios
    await page.getByLabel('Endereço').fill('Rua das Flores, 123')
    await page.getByLabel('Bairro').fill('Centro')
    await page.getByLabel('Área').fill('150.5')
    await page.getByLabel('CPF').fill('12345678900') // CPF inválido
    await page.getByLabel('Nome Completo').fill('João Silva')

    // Tenta submeter
    await page.getByRole('button', { name: 'Salvar' }).click()

    // Verifica erro de validação
    await expect(page.getByText('CPF inválido')).toBeVisible()

    // Corrige CPF
    await page.getByLabel('CPF').clear()
    await page.getByLabel('CPF').fill('52998224725') // CPF válido

    // Submete novamente
    await page.getByRole('button', { name: 'Salvar' }).click()

    // Verifica sucesso
    await expect(page).toHaveURL(/\/units\/[a-z0-9-]+$/)
    await expect(page.getByText('Unidade criada com sucesso')).toBeVisible()
  })

  test('works on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/units/new')

    // Verifica layout mobile
    const form = page.locator('form')
    await expect(form).toBeVisible()

    // Campos empilhados verticalmente
    const addressField = page.getByLabel('Endereço')
    const neighborhoodField = page.getByLabel('Bairro')

    const addressBox = await addressField.boundingBox()
    const neighborhoodBox = await neighborhoodField.boundingBox()

    // Em mobile, bairro deve estar abaixo do endereço
    expect(neighborhoodBox!.y).toBeGreaterThan(addressBox!.y + addressBox!.height)
  })
})
```

## Referências

- [Zustand Documentation](https://docs.pmnd.rs/zustand)
- [TanStack Query Documentation](https://tanstack.com/query/latest)
- [React Hook Form Documentation](https://react-hook-form.com/)
- [Astro Islands](https://docs.astro.build/en/concepts/islands/)
- [Keycloakify Documentation](https://keycloakify.dev/)
- [Playwright Documentation](https://playwright.dev/)
