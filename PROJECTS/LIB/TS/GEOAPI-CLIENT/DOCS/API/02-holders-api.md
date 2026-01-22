---
type: leaf
status: review
updated: 2026-01-21
---

# Holders API - Gerenciamento de Posseiros/Titulares

## Visao Geral

A Holders API fornece operacoes CRUD para gerenciamento de posseiros e titulares de unidades habitacionais em processo de regularizacao fundiaria.

## Import

```typescript
import { GeoApiClient } from '@carf/geoapi-client'
import type { Holder, CreateHolderDTO, UpdateHolderDTO } from '@carf/tscore/types'

const api = new GeoApiClient({ baseURL: '...', auth })

// Acessar Holders API
api.holders.list()
api.holders.getById()
api.holders.create()
api.holders.update()
api.holders.delete()
api.holders.search()
```

## Endpoints

```
GET    /api/holders           - Listar posseiros
GET    /api/holders/:id       - Buscar por ID
POST   /api/holders           - Criar posseiro
PUT    /api/holders/:id       - Atualizar posseiro
DELETE /api/holders/:id       - Deletar posseiro (soft delete)
GET    /api/holders/search    - Buscar por CPF/CNPJ/nome
GET    /api/holders/:id/units - Listar unidades do posseiro
```

## Methods

### list()

Lista posseiros com filtros e paginacao.

```typescript
list(query?: ListHoldersQueryDTO): Promise<PaginatedResponse<Holder>>
```

#### Parametros

```typescript
interface ListHoldersQueryDTO {
  page?: number              // Pagina (padrao: 1)
  limit?: number             // Itens por pagina (padrao: 20, max: 100)
  communityId?: string       // Filtrar por comunidade
  search?: string            // Busca em nome, CPF, CNPJ, email
  sortBy?: 'name' | 'createdAt' | 'updatedAt'
  sortOrder?: 'asc' | 'desc'
  include?: Array<'units'>   // Incluir relacionamentos
}
```

#### Exemplo

```typescript
// Listar com busca
const holders = await api.holders.list({
  search: 'Maria',
  page: 1,
  limit: 20
})

// Listar com unidades incluidas
const withUnits = await api.holders.list({
  include: ['units']
})
```

### getById()

Busca posseiro por ID.

```typescript
getById(id: string, options?: { include?: Array<'units'> }): Promise<Holder>
```

#### Exemplo

```typescript
const holder = await api.holders.getById('holder-123', {
  include: ['units']
})
console.log(`${holder.name} - ${holder.units.length} unidades`)
```

### create()

Cria novo posseiro.

```typescript
create(data: CreateHolderDTO): Promise<Holder>
```

#### Parametros

```typescript
interface CreateHolderDTO {
  // Identificacao (obrigatorio um dos dois)
  name: string                // Nome completo
  cpf?: string                // CPF (11 digitos, validado)
  cnpj?: string               // CNPJ (14 digitos, validado)

  // Contato (opcional)
  email?: string              // Email (validado)
  phone?: string              // Telefone
  cellphone?: string          // Celular

  // Endereco (opcional)
  address?: {
    street?: string
    number?: string
    complement?: string
    neighborhood?: string
    city?: string
    state?: string
    zipCode?: string
  }

  // Dados adicionais (opcional)
  birthDate?: Date            // Data de nascimento
  nationality?: string        // Nacionalidade
  maritalStatus?: 'SINGLE' | 'MARRIED' | 'DIVORCED' | 'WIDOWED' | 'STABLE_UNION'
  profession?: string         // Profissao
  rg?: string                 // RG
  observations?: string
}
```

#### Regras de Validacao

1. **name**: Obrigatorio, 2-200 caracteres
2. **cpf/cnpj**: Um dos dois obrigatorio, algoritmo de validacao
3. **cpf**: Deve ser unico no sistema
4. **cnpj**: Deve ser unico no sistema
5. **email**: Se fornecido, deve ser email valido

#### Exemplo

```typescript
// Criar pessoa fisica
const pf = await api.holders.create({
  name: 'Maria da Silva',
  cpf: '12345678901',
  email: 'maria@email.com',
  phone: '11999999999'
})

// Criar pessoa juridica
const pj = await api.holders.create({
  name: 'Associacao de Moradores',
  cnpj: '12345678000190',
  email: 'contato@assoc.org'
})
```

### update()

Atualiza posseiro existente.

```typescript
update(id: string, data: UpdateHolderDTO): Promise<Holder>
```

#### Exemplo

```typescript
const updated = await api.holders.update('holder-123', {
  phone: '11888888888',
  observations: 'Endereco atualizado em 2026-01-20'
})
```

### delete()

Deleta posseiro (soft delete).

```typescript
delete(id: string): Promise<void>
```

#### Regras

- Posseiro vinculado a unidades NAO pode ser deletado
- Primeiro desvincular de todas as unidades

### search()

Busca posseiro por CPF/CNPJ (busca exata).

```typescript
search(document: string): Promise<Holder | null>
```

#### Exemplo

```typescript
// Buscar por CPF antes de criar (evitar duplicatas)
const existing = await api.holders.search('12345678901')
if (existing) {
  console.log('Posseiro ja cadastrado:', existing.name)
} else {
  // Criar novo
}
```

### getUnits()

Lista unidades vinculadas ao posseiro.

```typescript
getUnits(holderId: string): Promise<UnitHolder[]>
```

#### Exemplo

```typescript
const units = await api.holders.getUnits('holder-123')
units.forEach(uh => {
  console.log(`${uh.unit.code} - ${uh.holderType}`)
})
```

## Tipos TypeScript

```typescript
import type {
  Holder,
  CreateHolderDTO,
  UpdateHolderDTO,
  ListHoldersQueryDTO,
  UnitHolder,
  MaritalStatus
} from '@carf/tscore/types'
```
