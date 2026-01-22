---
type: leaf
status: review
updated: 2026-01-21
---

# Communities API - Gerenciamento de Comunidades/Nucleos Urbanos

## Visao Geral

A Communities API fornece operacoes para gerenciamento de comunidades e nucleos urbanos informais onde se aplicam processos de regularizacao fundiaria (REURB).

## Import

```typescript
import { GeoApiClient } from '@carf/geoapi-client'
import type { Community, CreateCommunityDTO, UpdateCommunityDTO } from '@carf/tscore/types'

const api = new GeoApiClient({ baseURL: '...', auth })

// Acessar Communities API
api.communities.list()
api.communities.getById()
api.communities.create()
api.communities.update()
api.communities.delete()
api.communities.getStatistics()
```

## Endpoints

```
GET    /api/communities              - Listar comunidades
GET    /api/communities/:id          - Buscar por ID
POST   /api/communities              - Criar comunidade
PUT    /api/communities/:id          - Atualizar comunidade
DELETE /api/communities/:id          - Deletar comunidade
GET    /api/communities/:id/stats    - Estatisticas da comunidade
GET    /api/communities/:id/units    - Listar unidades da comunidade
GET    /api/communities/:id/geometry - Obter geometria/perimetro
```

## Methods

### list()

Lista comunidades com filtros.

```typescript
list(query?: ListCommunitiesQueryDTO): Promise<PaginatedResponse<Community>>
```

#### Parametros

```typescript
interface ListCommunitiesQueryDTO {
  page?: number
  limit?: number
  status?: 'ACTIVE' | 'INACTIVE' | 'ARCHIVED'
  city?: string                  // Filtrar por municipio
  state?: string                 // Filtrar por UF
  search?: string                // Busca em nome
  sortBy?: 'name' | 'createdAt' | 'unitCount'
  sortOrder?: 'asc' | 'desc'
}
```

#### Exemplo

```typescript
// Listar comunidades ativas de SP
const communities = await api.communities.list({
  status: 'ACTIVE',
  state: 'SP',
  sortBy: 'name'
})

// Buscar por nome
const search = await api.communities.list({
  search: 'Vila'
})
```

### getById()

Busca comunidade por ID.

```typescript
getById(id: string, options?: GetCommunityOptions): Promise<Community>
```

#### Parametros

```typescript
interface GetCommunityOptions {
  include?: Array<'units' | 'blocks' | 'geometry' | 'statistics'>
}
```

#### Exemplo

```typescript
// Buscar com estatisticas
const community = await api.communities.getById('comm-123', {
  include: ['statistics', 'geometry']
})

console.log(`${community.name}: ${community.statistics.unitCount} unidades`)
```

### create()

Cria nova comunidade.

```typescript
create(data: CreateCommunityDTO): Promise<Community>
```

#### Parametros

```typescript
interface CreateCommunityDTO {
  // Identificacao (obrigatorio)
  name: string                   // Nome da comunidade
  city: string                   // Municipio
  state: string                  // UF (2 letras)

  // Localizacao (opcional)
  neighborhood?: string          // Bairro
  region?: string                // Regiao administrativa
  zipCode?: string               // CEP principal

  // Geometria (opcional)
  geometry?: string              // WKT ou GeoJSON do perimetro
  area?: number                  // Area em hectares

  // Processo REURB (opcional)
  reurbType?: 'REURB_S' | 'REURB_E'  // Tipo de REURB
  processNumber?: string         // Numero do processo
  decreeNumber?: string          // Numero do decreto
  decreeDate?: Date              // Data do decreto

  // Configuracao (opcional)
  status?: 'ACTIVE' | 'INACTIVE'
  observations?: string
}
```

#### Exemplo

```typescript
const community = await api.communities.create({
  name: 'Vila das Flores',
  city: 'Sao Paulo',
  state: 'SP',
  neighborhood: 'Zona Leste',
  reurbType: 'REURB_S',
  status: 'ACTIVE'
})
```

### update()

Atualiza comunidade existente.

```typescript
update(id: string, data: UpdateCommunityDTO): Promise<Community>
```

#### Exemplo

```typescript
const updated = await api.communities.update('comm-123', {
  processNumber: 'PROC-2026-001',
  decreeNumber: 'DEC-2026-001',
  decreeDate: new Date('2026-01-15')
})
```

### delete()

Deleta comunidade (soft delete).

```typescript
delete(id: string): Promise<void>
```

#### Regras

- Comunidade com unidades NAO pode ser deletada
- Primeiro deletar/mover todas as unidades

### getStatistics()

Obtem estatisticas da comunidade.

```typescript
getStatistics(id: string): Promise<CommunityStatistics>
```

#### Retorno

```typescript
interface CommunityStatistics {
  unitCount: number              // Total de unidades
  holderCount: number            // Total de posseiros
  totalArea: number              // Area total em m²

  // Por status
  unitsByStatus: {
    pending: number
    in_progress: number
    approved: number
    rejected: number
  }

  // Por tipo de ocupacao
  unitsByOccupationType: {
    residential: number
    commercial: number
    mixed: number
    institutional: number
  }

  // Datas
  lastUnitCreated?: Date
  lastUnitUpdated?: Date
}
```

#### Exemplo

```typescript
const stats = await api.communities.getStatistics('comm-123')

console.log(`Total: ${stats.unitCount} unidades`)
console.log(`Aprovadas: ${stats.unitsByStatus.approved}`)
console.log(`Pendentes: ${stats.unitsByStatus.pending}`)
```

### getUnits()

Lista unidades da comunidade.

```typescript
getUnits(communityId: string, query?: ListUnitsQueryDTO): Promise<PaginatedResponse<Unit>>
```

Equivalente a `api.units.list({ communityId })`.

### getGeometry()

Obtem geometria/perimetro da comunidade.

```typescript
getGeometry(id: string, format?: 'geojson' | 'wkt'): Promise<Geometry>
```

#### Exemplo

```typescript
// GeoJSON para exibir em mapa
const geojson = await api.communities.getGeometry('comm-123', 'geojson')

// WKT para integracao com GIS
const wkt = await api.communities.getGeometry('comm-123', 'wkt')
```

## Tipos TypeScript

```typescript
import type {
  Community,
  CreateCommunityDTO,
  UpdateCommunityDTO,
  ListCommunitiesQueryDTO,
  CommunityStatistics,
  ReurbType
} from '@carf/tscore/types'
```
