---
status: review
updated: 2026-01-21
---

# Units API - Gerenciamento de Unidades Habitacionais

## Visão Geral

A Units API fornece operacoes CRUD completas para gerenciamento de unidades habitacionais em processo de regularizacao fundiaria.

## Import

```typescript
import { GeoApiClient } from '@carf/geoapi-client'
import type { Unit, CreateUnitDTO, UpdateUnitDTO } from '@carf/tscore/types'

const api = new GeoApiClient({ baseURL: '...', auth })

// Acessar Units API
api.units.list()
api.units.getById()
api.units.create()
api.units.update()
api.units.delete()
```

## Endpoints

### Base URL

```
GET /api/units - Listar unidades
GET /api/units/:id - Buscar por ID
POST /api/units - Criar unidade
PUT /api/units/:id - Atualizar unidade
PATCH /api/units/:id - Atualização parcial
DELETE /api/units/:id - Deletar unidade (soft delete)
GET /api/units/:id/holders - Listar titulares da unidade
POST /api/units/:id/holders - Vincular titular
DELETE /api/units/:id/holders/:holderId - Desvincular titular
GET /api/units/:id/documents - Listar documentos anexos
POST /api/units/:id/documents - Anexar documento
GET /api/units/export - Exportar para Excel/CSV
```

## Methods

### list()

Lista unidades com filtros, busca e paginação.

```typescript
list(query?: ListUnitsQueryDTO, options?: RequestOptions): Promise<PaginatedResponse<Unit>>
```

#### Parâmetros

**query** (opcional): Filtros e paginação
```typescript
interface ListUnitsQueryDTO {
 // Paginação
 page?: number // Página (padrão: 1)
 limit?: number // Itens por página (padrão: 20, máx: 100)

 // Filtros
 communityId?: string // Filtrar por comunidade
 blockId?: string // Filtrar por quadra
 status?: UnitStatus // Filtrar por status
 occupationType?: 'RESIDENTIAL' | 'COMMERCIAL' | 'MIXED' | 'INSTITUTIONAL'

 // Busca textual (busca em code, street, neighborhood)
 search?: string

 // Ordenação
 sortBy?: 'code' | 'createdAt' | 'updatedAt' | 'status'
 sortOrder?: 'asc' | 'desc'

 // Incluir relacionamentos
 include?: Array<'community' | 'holders' | 'documents' | 'surveyPoints'>
}
```

**options** (opcional): Opções de request
```typescript
interface RequestOptions {
 cancelToken?: CancelToken
 timeout?: number
}
```

#### Retorno

```typescript
interface PaginatedResponse<Unit> {
 items: Unit[] // Array de unidades
 total: number // Total de itens (todas as páginas)
 page: number // Página atual
 limit: number // Itens por página
 totalPages: number // Total de páginas
 hasNext: boolean // Tem próxima página?
 hasPrevious: boolean // Tem página anterior?
}
```

#### Exemplos

```typescript
// Listar primeira página (20 itens)
const response = await api.units.list()
console.log(`Total: ${response.total} unidades`)
console.log(`Página ${response.page} de ${response.totalPages}`)

// Listar com filtros
const filtered = await api.units.list({
 communityId: 'comm-123',
 status: UnitStatus.APPROVED,
 page: 1,
 limit: 50
})

// Busca textual
const search = await api.units.list({
 search: 'Rua das Flores', // Busca em code, street, neighborhood
 page: 1
})

// Com relacionamentos incluídos
const withHolders = await api.units.list({
 communityId: 'comm-123',
 include: ['holders', 'documents'],
 page: 1
})

// Com ordenação
const sorted = await api.units.list({
 sortBy: 'code',
 sortOrder: 'asc',
 page: 1
})
```

---

### getById()

Busca unidade por ID.

```typescript
getById(id: string, options?: GetByIdOptions): Promise<Unit>
```

#### Parâmetros

**id** (obrigatório): UUID da unidade

**options** (opcional):
```typescript
interface GetByIdOptions {
 include?: Array<'community' | 'block' | 'plot' | 'holders' | 'documents' | 'surveyPoints' | 'annotations'>
 cancelToken?: CancelToken
}
```

#### Retorno

Objeto `Unit` completo.

#### Throws

- `NotFoundError` (404) - Unidade não existe
- `UnauthorizedError` (401) - Não autenticado
- `ForbiddenError` (403) - Sem permissão para acessar esta unidade

#### Exemplos

```typescript
// Buscar unidade básica
const unit = await api.units.getById('unit-uuid-123')
console.log(unit.code, unit.street)

// Buscar com todos os relacionamentos
const fullUnit = await api.units.getById('unit-uuid-123', {
 include: ['community', 'holders', 'documents', 'surveyPoints']
})
console.log(`Titulares: ${fullUnit.holders.length}`)
console.log(`Documentos: ${fullUnit.documents.length}`)
```

---

### create()

Cria nova unidade habitacional.

```typescript
create(data: CreateUnitDTO): Promise<Unit>
```

#### Parâmetros

**data** (obrigatório):
```typescript
interface CreateUnitDTO {
 // Identificação (obrigatório)
 code: string // Código único na comunidade
 communityId: string // UUID da comunidade

 // Localização (obrigatório)
 street: string // Logradouro
 city: string // Município
 state: string // UF (2 letras)

 // Localização (opcional)
 number?: string // Número
 complement?: string // Complemento
 neighborhood?: string // Bairro
 zipCode?: string // CEP

 // Subdivisão (opcional)
 blockId?: string // UUID da quadra
 plotId?: string // UUID do lote

 // Geometria (opcional)
 geometry?: string // WKT ou GeoJSON string
 area?: number // Área em m² (calculada se geometry fornecido)

 // Ocupação (obrigatório)
 occupationType: 'RESIDENTIAL' | 'COMMERCIAL' | 'MIXED' | 'INSTITUTIONAL'

 // Ocupação (opcional)
 residents?: number // Número de moradores
 landSituation?: string // Situação fundiária

 // Observações (opcional)
 observations?: string

 // Dados customizados (opcional)
 customData?: Record<string, any>
}
```

#### Retorno

Objeto `Unit` criado com ID gerado.

#### Throws

- `ValidationError` (400) - Dados inválidos (ver `validationErrors` para detalhes)
- `ConflictError` (409) - Código já existe na comunidade
- `UnauthorizedError` (401) - Não autenticado
- `ForbiddenError` (403) - Sem permissão para criar unidade nesta comunidade

#### Exemplos

```typescript
import { CreateUnitDTO } from '@carf/tscore/types'

// Criar unidade mínima
const minimalUnit = await api.units.create({
 code: 'UN-001',
 communityId: 'comm-123',
 street: 'Rua das Flores',
 city: 'São Paulo',
 state: 'SP',
 occupationType: 'RESIDENTIAL'
})

// Criar unidade completa
const fullUnit = await api.units.create({
 code: 'UN-002',
 communityId: 'comm-123',
 street: 'Avenida Brasil',
 number: '456',
 complement: 'Casa 2',
 neighborhood: 'Centro',
 city: 'São Paulo',
 state: 'SP',
 zipCode: '01310-100',
 occupationType: 'RESIDENTIAL',
 residents: 4,
 landSituation: 'Posse',
 observations: 'Casa de alvenaria com 2 quartos',
 geometry: 'POLYGON((-46.6333 -23.5505, ...))',
 area: 120.5
})

// Tratando erros de validação
try {
 const unit = await api.units.create(data)
} catch (error) {
 if (error instanceof ValidationError) {
 // { code: ['Código já existe'], cpf: ['CPF inválido'] }
 console.error(error.validationErrors)
 } else if (error instanceof ConflictError) {
 alert('Código de unidade já cadastrado nesta comunidade')
 }
}
```

#### Regras de Validacao

1. **code**: Obrigatorio, unico por comunidade, 1-50 caracteres
2. **communityId**: Obrigatorio, comunidade deve existir e usuario ter acesso
3. **street**: Obrigatorio, 1-200 caracteres
4. **city**: Obrigatorio, 1-100 caracteres
5. **state**: Obrigatorio, exatamente 2 letras (UF valida)
6. **occupationType**: Obrigatorio, um dos valores do enum
7. **geometry**: Se fornecido, deve ser poligono WKT/GeoJSON valido
8. **area**: Se fornecido, deve ser > 0

---

### update()

Atualiza unidade existente (substituição completa).

```typescript
update(id: string, data: UpdateUnitDTO): Promise<Unit>
```

#### Parâmetros

**id** (obrigatório): UUID da unidade

**data** (obrigatório):
```typescript
interface UpdateUnitDTO {
 code?: string
 street?: string
 number?: string
 complement?: string
 neighborhood?: string
 city?: string
 state?: string
 zipCode?: string
 blockId?: string
 plotId?: string
 geometry?: string
 area?: number
 occupationType?: 'RESIDENTIAL' | 'COMMERCIAL' | 'MIXED' | 'INSTITUTIONAL'
 residents?: number
 landSituation?: string
 status?: UnitStatus
 observations?: string
 customData?: Record<string, any>
 version: number // Optimistic concurrency control
}
```

#### Retorno

Objeto `Unit` atualizado.

#### Throws

- `NotFoundError` (404) - Unidade não existe
- `ValidationError` (400) - Dados inválidos
- `ConflictError` (409) - Conflito de versão (outro usuário modificou)
- `UnauthorizedError` (401) - Não autenticado
- `ForbiddenError` (403) - Sem permissão para editar

#### Exemplos

```typescript
// Buscar unidade
const unit = await api.units.getById('unit-123')

// Atualizar campos específicos
const updated = await api.units.update('unit-123', {
 ...unit, // Manter campos existentes
 street: 'Rua Nova', // Atualizar street
 number: '789', // Atualizar number
 residents: 5, // Atualizar residents
 version: unit.version // Optimistic concurrency
})

// Tratar conflito de versão
try {
 const updated = await api.units.update('unit-123', data)
} catch (error) {
 if (error instanceof ConflictError) {
 alert('Outro usuário modificou esta unidade. Atualize a página.')
 // Recarregar unidade e tentar novamente
 }
}
```

#### Optimistic Concurrency Control

O campo `version` previne que dois usuários sobrescrevam mudanças um do outro:

```typescript
// Usuário A busca unidade (version = 1)
const unitA = await api.units.getById('unit-123')

// Usuário B busca mesma unidade (version = 1)
const unitB = await api.units.getById('unit-123')

// Usuário A atualiza (version 1 → 2) ✅
await api.units.update('unit-123', { ...unitA, street: 'Rua A', version: 1 })

// Usuário B tenta atualizar (version ainda é 1) ❌ Conflict!
await api.units.update('unit-123', { ...unitB, street: 'Rua B', version: 1 })
// Throws ConflictError: "Unidade foi modificada por outro usuário"
```

---

### patch()

Atualização parcial de campos específicos.

```typescript
patch(id: string, data: Partial<UpdateUnitDTO>): Promise<Unit>
```

Mais conveniente que `update()` quando quiser atualizar apenas alguns campos sem buscar a unidade inteira primeiro.

#### Exemplo

```typescript
// Atualizar apenas status e observações
const updated = await api.units.patch('unit-123', {
 status: UnitStatus.APPROVED,
 observations: 'Aprovado em 2026-01-09'
})

// Atualizar apenas geometria
const updated = await api.units.patch('unit-123', {
 geometry: 'POLYGON((...novo polígono...))',
 area: 135.7
})
```

---

### delete()

Deleta unidade (soft delete).

```typescript
delete(id: string): Promise<void>
```

#### Parâmetros

**id** (obrigatório): UUID da unidade

#### Retorno

`void` (sem retorno em caso de sucesso)

#### Throws

- `NotFoundError` (404) - Unidade não existe ou já foi deletada
- `UnauthorizedError` (401) - Não autenticado
- `ForbiddenError` (403) - Sem permissão para deletar

#### Exemplo

```typescript
await api.units.delete('unit-123')
console.log('Unidade deletada com sucesso')

// Soft delete: unidade não é removida do banco, apenas marcada como deletada
// deletedAt timestamp é preenchido
// Unidade não aparece mais em listagens
```

---

### getHolders()

Lista titulares vinculados à unidade.

```typescript
getHolders(unitId: string): Promise<UnitHolder[]>
```

#### Retorno

```typescript
interface UnitHolder {
 id: string
 unitId: string
 holderId: string
 holderType: 'OWNER' | 'SPOUSE' | 'RESIDENT' | 'ATTORNEY' | 'HEIR'
 ownershipPercentage?: number // 0-100 (somente para OWNER)
 createdAt: Date
 holder: Holder // Dados do titular (populated)
}
```

#### Exemplo

```typescript
const holders = await api.units.getHolders('unit-123')

holders.forEach(uh => {
 console.log(`${uh.holder.name} - ${uh.holderType}`)
 if (uh.holderType === 'OWNER') {
 console.log(` Propriedade: ${uh.ownershipPercentage}%`)
 }
})
```

---

### addHolder()

Vincula titular à unidade.

```typescript
addHolder(unitId: string, data: AddHolderDTO): Promise<UnitHolder>
```

#### Parâmetros

```typescript
interface AddHolderDTO {
 holderId: string // UUID do titular
 holderType: 'OWNER' | 'SPOUSE' | 'RESIDENT' | 'ATTORNEY' | 'HEIR'
 ownershipPercentage?: number // Obrigatório se holderType = OWNER
}
```

#### Regras de Validação

1. `holderId` deve existir
2. `holderType = OWNER` → `ownershipPercentage` obrigatório (0-100)
3. Soma de `ownershipPercentage` de todos OWNER da unidade não pode exceder 100%
4. Não pode vincular mesmo titular duas vezes com mesmo `holderType`

#### Exemplo

```typescript
// Adicionar proprietário com 100% da propriedade
const owner = await api.units.addHolder('unit-123', {
 holderId: 'holder-456',
 holderType: 'OWNER',
 ownershipPercentage: 100
})

// Adicionar cônjuge
const spouse = await api.units.addHolder('unit-123', {
 holderId: 'holder-789',
 holderType: 'SPOUSE'
})

// Adicionar co-proprietários
const owner1 = await api.units.addHolder('unit-123', {
 holderId: 'holder-111',
 holderType: 'OWNER',
 ownershipPercentage: 50
})
const owner2 = await api.units.addHolder('unit-123', {
 holderId: 'holder-222',
 holderType: 'OWNER',
 ownershipPercentage: 50
})
```

---

### removeHolder()

Desvincula titular da unidade.

```typescript
removeHolder(unitId: string, holderId: string): Promise<void>
```

#### Exemplo

```typescript
await api.units.removeHolder('unit-123', 'holder-456')
```

---

### export()

Exporta unidades para Excel ou CSV.

```typescript
export(query: ListUnitsQueryDTO, format: 'excel' | 'csv'): Promise<Blob>
```

#### Exemplo

```typescript
// Exportar unidades filtradas para Excel
const blob = await api.units.export({
 communityId: 'comm-123',
 status: UnitStatus.APPROVED
}, 'excel')

// Download no browser
const url = window.URL.createObjectURL(blob)
const link = document.createElement('a')
link.href = url
link.download = 'unidades-aprovadas.xlsx'
link.click()
```

---

## Tipos TypeScript

Todos os tipos usados estão disponíveis em `@carf/tscore/types`:

```typescript
import type {
 Unit,
 CreateUnitDTO,
 UpdateUnitDTO,
 ListUnitsQueryDTO,
 UnitHolder,
 UnitStatus,
 PaginatedResponse
} from '@carf/tscore/types'
```

📖 **@carf/tscore Documentation** - Documentação completa de types (ver TSCORE/DOCS/)

## Links Relacionados

### Documentação CENTRAL

- 📖 **CENTRAL/API/UNITS/** - Especificação completa da API
- 📖 - Entidade Unit
- 📖 **CENTRAL/REQUIREMENTS/UNITS/** - Requisitos funcionais
