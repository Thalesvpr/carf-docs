---
title: "Types API - @carf/tscore"
status: review
updated: 2026-01-21
source: "CENTRAL/LIBRARIES/01-tscore.md"
---

# Types API - @carf/tscore

Referencia completa dos tipos TypeScript exportados por `@carf/tscore/types`.

## Import

```typescript
import type {
  // Entities
  Unit,
  Holder,
  Community,
  Legitimation,
  Document,

  // Enums
  UnitStatus,
  Role,
  EntityType,
  CommunityType,
  LegitimationStatus,
  DocumentType,

  // DTOs
  CreateUnitDto,
  UpdateUnitDto,
  CreateHolderDto,
  UpdateHolderDto,

  // Utils
  PaginatedResponse,
  ApiResponse,
} from '@carf/tscore/types'
```

## Entities

### Unit

Unidade habitacional em processo de regularizacao fundiaria.

```typescript
interface Unit {
  id: string
  code: string
  status: UnitStatus
  street: string
  number?: string | null
  complement?: string | null
  neighborhood?: string | null
  city: string
  state: string
  zipCode?: string | null
  geometry?: GeoJSON.Polygon | null
  area?: number | null
  builtArea?: number | null
  occupationType: 'RESIDENTIAL' | 'COMMERCIAL' | 'MIXED' | 'INSTITUTIONAL'
  residents?: number | null
  landSituation?: string | null
  observations?: string | null
  communityId: string
  blockId?: string | null
  plotId?: string | null
  customData?: Record<string, unknown> | null
  createdAt: Date
  updatedAt: Date
  deletedAt?: Date | null
  version: number
}
```

### Holder

Posseiro ou titular de unidade habitacional.

```typescript
interface Holder {
  id: string
  type: EntityType
  name: string
  cpf?: string | null
  cnpj?: string | null
  rg?: string | null
  birthDate?: Date | null
  nationality?: string | null
  maritalStatus?: MaritalStatus | null
  occupation?: string | null
  email?: string | null
  phone?: string | null
  cellphone?: string | null
  street?: string | null
  number?: string | null
  complement?: string | null
  neighborhood?: string | null
  city?: string | null
  state?: string | null
  zipCode?: string | null
  observations?: string | null
  customData?: Record<string, unknown> | null
  createdAt: Date
  updatedAt: Date
  deletedAt?: Date | null
  version: number
}
```

### Community

Comunidade ou nucleo urbano informal.

```typescript
interface Community {
  id: string
  name: string
  code?: string | null
  type: CommunityType
  status: 'ACTIVE' | 'INACTIVE' | 'ARCHIVED'
  description?: string | null
  city: string
  state: string
  neighborhood?: string | null
  region?: string | null
  zipCode?: string | null
  boundary?: GeoJSON.Polygon | null
  area?: number | null
  reurbType?: 'REURB_S' | 'REURB_E' | null
  processNumber?: string | null
  decreeNumber?: string | null
  decreeDate?: Date | null
  tenantId: string
  customData?: Record<string, unknown> | null
  createdAt: Date
  updatedAt: Date
  deletedAt?: Date | null
  version: number
}
```

### Legitimation

Processo de legitimacao fundiaria.

```typescript
interface Legitimation {
  id: string
  unitId: string
  holderId: string
  status: LegitimationStatus
  reurbType: 'REURB_S' | 'REURB_E'
  requestDate?: Date | null
  protocolNumber?: string | null
  assignedTo?: string | null
  observations?: string | null
  createdAt: Date
  updatedAt: Date
  deletedAt?: Date | null
  version: number
}
```

### Document

Documento anexado a entidade.

```typescript
interface Document {
  id: string
  type: DocumentType
  fileName: string
  fileSize: number
  mimeType: string
  storageUrl: string
  entityType: 'UNIT' | 'HOLDER' | 'COMMUNITY' | 'LEGITIMATION'
  entityId: string
  description?: string | null
  uploadedBy: string
  createdAt: Date
}
```

## Enums

### UnitStatus

Status de uma unidade no fluxo de aprovacao.

```typescript
enum UnitStatus {
  DRAFT = 'DRAFT'                       // Rascunho
  PENDING_ANALYSIS = 'PENDING_ANALYSIS' // Aguardando analise
  IN_REVIEW = 'IN_REVIEW'               // Em revisao tecnica
  APPROVED = 'APPROVED'                 // Aprovada
  REJECTED = 'REJECTED'                 // Rejeitada
  REQUIRES_CHANGES = 'REQUIRES_CHANGES' // Requer correcoes
}
```

### Role

Papeis de usuario no sistema.

```typescript
enum Role {
  SUPER_ADMIN = 'SUPER_ADMIN'
  ADMIN = 'ADMIN'
  MANAGER = 'MANAGER'
  ANALYST = 'ANALYST'
  FIELD_AGENT = 'FIELD_AGENT'
}

// Hierarquia de permissoes
const RoleHierarchy: Record<Role, number> = {
  SUPER_ADMIN: 100,
  ADMIN: 80,
  MANAGER: 60,
  ANALYST: 40,
  FIELD_AGENT: 20,
}

// Funcao utilitaria
function hasRolePermission(userRole: Role, requiredRole: Role): boolean
```

### EntityType

Tipo de entidade juridica.

```typescript
enum EntityType {
  PESSOA_FISICA = 'PESSOA_FISICA'
  PESSOA_JURIDICA = 'PESSOA_JURIDICA'
  GOVERNMENT = 'GOVERNMENT'
  NGO = 'NGO'
  OTHER = 'OTHER'
}
```

### CommunityType

Tipo de comunidade.

```typescript
enum CommunityType {
  URBAN_SLUM = 'URBAN_SLUM'
  RURAL_SETTLEMENT = 'RURAL_SETTLEMENT'
  INDIGENOUS_LAND = 'INDIGENOUS_LAND'
  QUILOMBOLA = 'QUILOMBOLA'
  FISHING_COMMUNITY = 'FISHING_COMMUNITY'
  OTHER = 'OTHER'
}
```

### LegitimationStatus

Status de processo de legitimacao.

```typescript
enum LegitimationStatus {
  DRAFT = 'DRAFT'
  SUBMITTED = 'SUBMITTED'
  UNDER_REVIEW = 'UNDER_REVIEW'
  AWAITING_DOCUMENTATION = 'AWAITING_DOCUMENTATION'
  PUBLIC_NOTICE = 'PUBLIC_NOTICE'
  CONTESTED = 'CONTESTED'
  ANALYZING_CONTESTATION = 'ANALYZING_CONTESTATION'
  APPROVED = 'APPROVED'
  REJECTED = 'REJECTED'
  CERTIFICATE_ISSUED = 'CERTIFICATE_ISSUED'
  ARCHIVED = 'ARCHIVED'
}
```

### MaritalStatus

Estado civil.

```typescript
enum MaritalStatus {
  SINGLE = 'SINGLE'
  MARRIED = 'MARRIED'
  DIVORCED = 'DIVORCED'
  WIDOWED = 'WIDOWED'
  STABLE_UNION = 'STABLE_UNION'
}
```

### DocumentType

Tipo de documento.

```typescript
enum DocumentType {
  ID_DOCUMENT = 'ID_DOCUMENT'           // RG, CNH
  CPF = 'CPF'
  PROOF_OF_RESIDENCE = 'PROOF_OF_RESIDENCE'
  MARRIAGE_CERTIFICATE = 'MARRIAGE_CERTIFICATE'
  PROPERTY_TAX = 'PROPERTY_TAX'         // IPTU
  POWER_OF_ATTORNEY = 'POWER_OF_ATTORNEY'
  TECHNICAL_REPORT = 'TECHNICAL_REPORT'
  PLANT = 'PLANT'                       // Planta/croqui
  AERIAL_PHOTO = 'AERIAL_PHOTO'
  OTHER = 'OTHER'
}
```

## DTOs

### CreateUnitDto

```typescript
interface CreateUnitDto {
  code: string
  communityId: string
  street: string
  city: string
  state: string
  occupationType: 'RESIDENTIAL' | 'COMMERCIAL' | 'MIXED' | 'INSTITUTIONAL'
  number?: string
  complement?: string
  neighborhood?: string
  zipCode?: string
  blockId?: string
  plotId?: string
  geometry?: string  // WKT ou GeoJSON string
  area?: number
  builtArea?: number
  residents?: number
  landSituation?: string
  observations?: string
  customData?: Record<string, unknown>
}
```

### UpdateUnitDto

```typescript
interface UpdateUnitDto {
  code?: string
  status?: UnitStatus
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
  builtArea?: number
  occupationType?: 'RESIDENTIAL' | 'COMMERCIAL' | 'MIXED' | 'INSTITUTIONAL'
  residents?: number
  landSituation?: string
  observations?: string
  customData?: Record<string, unknown>
  version: number  // Optimistic concurrency
}
```

### CreateHolderDto

```typescript
interface CreateHolderDto {
  name: string
  cpf?: string
  cnpj?: string
  email?: string
  phone?: string
  cellphone?: string
  birthDate?: Date
  nationality?: string
  maritalStatus?: MaritalStatus
  occupation?: string
  rg?: string
  street?: string
  number?: string
  complement?: string
  neighborhood?: string
  city?: string
  state?: string
  zipCode?: string
  observations?: string
  customData?: Record<string, unknown>
}
```

### UpdateHolderDto

```typescript
interface UpdateHolderDto {
  name?: string
  cpf?: string
  cnpj?: string
  email?: string
  phone?: string
  cellphone?: string
  birthDate?: Date
  nationality?: string
  maritalStatus?: MaritalStatus
  occupation?: string
  rg?: string
  street?: string
  number?: string
  complement?: string
  neighborhood?: string
  city?: string
  state?: string
  zipCode?: string
  observations?: string
  customData?: Record<string, unknown>
  version: number
}
```

## Utils

### PaginatedResponse

```typescript
interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  limit: number
  totalPages: number
  hasNext: boolean
  hasPrevious: boolean
}
```

### ApiResponse

```typescript
interface ApiResponse<T> {
  data: T
  success: boolean
  message?: string
  timestamp: Date
}
```
