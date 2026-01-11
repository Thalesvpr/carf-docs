# TypeScript Types - Tipos Compartilhados

## Visão Geral

O @carf/tscore fornece **tipos TypeScript compartilhados** sincronizados com o [domain model](../../../../../../CENTRAL/DOMAIN-MODEL/README.md) do backend GEOAPI .NET conforme geração de código automática e usados por todos os frontends (GEOWEB, REURBCAD, ADMIN), sendo consumidos por [@carf/geoapi-client](../../../GEOAPI-CLIENT/DOCS/README.md) para tipagem de requests/responses e [@carf/ui](../../../UI-COMPONENTS/DOCS/README.md) para componentes React tipados. Garantimos type safety end-to-end com contratos de API bem definidos.

## Documentação de Referência

📖 **[CENTRAL/DOMAIN-MODEL/00-INDEX.md](../../../../../../CENTRAL/DOMAIN-MODEL/00-INDEX.md)** - Índice completo com 33 entidades e 25 value objects

📖 **[CENTRAL/API/README.md](../../../../../../CENTRAL/API/README.md)** - Especificação completa da REST API

## Princípio de Sincronização

### Backend (.NET) → Frontend (TypeScript)

Os tipos TypeScript do @carf/tscore são **gerados automaticamente** a partir dos DTOs do backend .NET usando ferramentas de code generation. Isso garante:

✅ **Contratos de API Sincronizados** - Frontend e backend sempre alinhados
✅ **Type Safety** - Erros detectados em compile-time
✅ **Refatoração Segura** - Mudanças no backend quebram o build do frontend
✅ **Autocomplete** - IDEs fornecem sugestões precisas
✅ **Documentação Viva** - Types servem como documentação

### Fluxo de Geração

```
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  GEOAPI Backend  │      │   Generator      │      │  @carf/tscore    │
│   (.NET DTOs)    │─────>│  (NSwag/OpenAPI) │─────>│ (TS interfaces)  │
└──────────────────┘      └──────────────────┘      └──────────────────┘
                                                              │
                                                              v
                          ┌──────────────────────────────────────────────────┐
                          │  Consumidores (GEOWEB, REURBCAD, ADMIN, etc.)   │
                          └──────────────────────────────────────────────────┘
```

📖 ****CENTRAL/ARCHITECTURE/CODE-GENERATION/01-type-generation.md**** - Processo de geração de types

## Tipos de Entidades

### Estrutura Base

Todas as entidades herdam campos base:

```typescript
// src/types/base.ts
export interface BaseEntity {
  id: string              // UUID v4
  createdAt: Date         // Timestamp de criação
  updatedAt: Date         // Timestamp de última atualização
  deletedAt?: Date        // Soft delete timestamp (opcional)
  version: number         // Versão para otimistic concurrency
}
```

📖 ****CENTRAL/DOMAIN-MODEL/ENTITIES/00-base-entity.md**** - Especificação da entidade base

### Unit (Unidade Habitacional)

Representa unidade habitacional em processo de regularização fundiária.

📖 **[CENTRAL/DOMAIN-MODEL/ENTITIES/02-unit.md](../../../../../../CENTRAL/DOMAIN-MODEL/ENTITIES/02-unit.md)** - Especificação completa da entidade Unit

```typescript
import type { BaseEntity } from './base'
import type { UnitStatus, CommunityType } from './enums'
import type { GeoPolygon } from './geo'

export interface Unit extends BaseEntity {
  // Identificação
  code: string                    // Código único na comunidade (ex: "UN-001")
  tenantId: string                // UUID do tenant (multi-tenancy)
  communityId: string             // UUID da comunidade
  blockId?: string                // UUID da quadra (opcional)
  plotId?: string                 // UUID do lote (opcional)

  // Endereço
  street: string                  // Logradouro
  number?: string                 // Número
  complement?: string             // Complemento
  neighborhood?: string           // Bairro
  city: string                    // Município
  state: string                   // UF (2 letras)
  zipCode?: string                // CEP (formato: 00000-000)

  // Geometria
  geometry?: GeoPolygon           // Polígono WKT/GeoJSON
  area?: number                   // Área em m² (calculada)
  perimeter?: number              // Perímetro em m (calculado)

  // Ocupação
  occupationType: 'RESIDENTIAL' | 'COMMERCIAL' | 'MIXED' | 'INSTITUTIONAL'
  residents?: number              // Número de moradores
  landSituation?: string          // Situação fundiária atual

  // Workflow
  status: UnitStatus              // Status no workflow
  observations?: string           // Observações livres

  // Dados customizados (tenant-specific)
  customData?: Record<string, any>

  // Relacionamentos (populados por joins)
  community?: Community
  block?: Block
  plot?: Plot
  holders?: Holder[]              // Titulares vinculados
  documents?: Document[]          // Documentos anexos
  surveyPoints?: SurveyPoint[]    // Pontos topográficos
  annotations?: Annotation[]      // Anotações
}
```

#### Exemplo de Uso

```typescript
import type { Unit } from '@carf/tscore/types'
import { UnitStatus } from '@carf/tscore/types'

const unit: Unit = {
  id: crypto.randomUUID(),
  code: 'UN-001',
  tenantId: 'tenant-sp-prefeitura',
  communityId: 'community-123',
  street: 'Rua das Flores',
  number: '123',
  city: 'São Paulo',
  state: 'SP',
  occupationType: 'RESIDENTIAL',
  status: UnitStatus.DRAFT,
  residents: 4,
  createdAt: new Date(),
  updatedAt: new Date(),
  version: 1
}
```

### Holder (Titular)

Representa pessoa física titular, ocupante ou interessado em unidade.

📖 **[CENTRAL/DOMAIN-MODEL/ENTITIES/03-holder.md](../../../../../../CENTRAL/DOMAIN-MODEL/ENTITIES/03-holder.md)** - Especificação completa da entidade Holder

```typescript
import type { BaseEntity } from './base'

export interface Holder extends BaseEntity {
  // Identificação
  cpf: string                     // CPF (somente números, 11 dígitos)
  cnpj?: string                   // CNPJ se pessoa jurídica
  tenantId: string                // UUID do tenant

  // Dados Pessoais
  name: string                    // Nome completo
  socialName?: string             // Nome social
  birthDate?: Date                // Data de nascimento
  gender?: 'M' | 'F' | 'O'        // Sexo/gênero
  maritalStatus?: 'SINGLE' | 'MARRIED' | 'DIVORCED' | 'WIDOWED' | 'COMMON_LAW'

  // Documentação
  rg?: string                     // RG número
  rgIssuer?: string               // Órgão emissor
  nationality?: string            // Nacionalidade
  birthPlace?: string             // Naturalidade

  // Contato
  email?: string                  // Email
  phone?: string                  // Telefone (DDD + número)

  // Socioeconômico
  monthlyIncome?: number          // Renda mensal (R$)
  occupation?: string             // Profissão
  education?: 'ELEMENTARY' | 'HIGH_SCHOOL' | 'HIGHER_EDUCATION' | 'POSTGRADUATE'
  dependents?: number             // Número de dependentes
  hasDisability?: boolean         // Possui deficiência
  disabilityType?: string         // Tipo de deficiência

  // Ocupação
  occupationTime?: number         // Tempo de ocupação (anos)
  currentlyResiding?: boolean     // Reside atualmente no imóvel

  // Documentos
  idDocumentPhoto?: string        // URL foto do documento
  photo?: string                  // URL foto pessoal

  // Observações
  observations?: string

  // Relacionamentos
  units?: UnitHolder[]            // Unidades vinculadas (N:N)
  documents?: Document[]
  annotations?: Annotation[]
}
```

#### Validação com Value Objects

```typescript
import type { Holder } from '@carf/tscore/types'
import { CPF, Email, PhoneNumber } from '@carf/tscore/validations'

function createHolder(data: any): Holder {
  // Valida CPF antes de criar
  const cpf = new CPF(data.cpf)

  // Valida email se fornecido
  const email = data.email ? new Email(data.email) : undefined

  // Valida telefone se fornecido
  const phone = data.phone ? new PhoneNumber(data.phone) : undefined

  return {
    id: crypto.randomUUID(),
    cpf: cpf.value,
    email: email?.value,
    phone: phone?.value,
    name: data.name,
    tenantId: data.tenantId,
    createdAt: new Date(),
    updatedAt: new Date(),
    version: 1
  }
}
```

### Community (Comunidade)

Representa comunidade ou assentamento que agrupa unidades geograficamente.

📖 **[CENTRAL/DOMAIN-MODEL/ENTITIES/04-community.md](../../../../../../CENTRAL/DOMAIN-MODEL/ENTITIES/04-community.md)** - Especificação completa da entidade Community

```typescript
import type { BaseEntity } from './base'
import type { CommunityType } from './enums'
import type { GeoPolygon } from './geo'

export interface Community extends BaseEntity {
  // Identificação
  code: string                    // Código único (ex: "COM-001")
  name: string                    // Nome da comunidade
  tenantId: string                // UUID do tenant

  // Geografia
  city: string                    // Município
  state: string                   // UF
  neighborhood?: string           // Bairro
  geometry?: GeoPolygon           // Polígono delimitador
  area?: number                   // Área total em m²

  // Classificação
  type: CommunityType             // URBANA, RURAL, QUILOMBOLA, etc.
  reurbType?: 'S' | 'E'           // REURB-S (social) ou REURB-E (específico)

  // Estatísticas
  totalUnits?: number             // Número total de unidades
  totalHolders?: number           // Número total de titulares
  totalArea?: number              // Área total construída

  // Observações
  description?: string
  observations?: string

  // Relacionamentos
  units?: Unit[]
  blocks?: Block[]
  authorizations?: CommunityAuthorization[]
  documents?: Document[]
  annotations?: Annotation[]
}
```

### LegitimationRequest (Solicitação de Legitimação)

Representa processo de legitimação fundiária conforme Lei 13.465/2017.

📖 ****CENTRAL/DOMAIN-MODEL/ENTITIES/20-legitimation-request.md**** - Especificação completa

📖 ****CENTRAL/WORKFLOWS/04-legitimation-workflow.md**** - Workflow de legitimação

```typescript
import type { BaseEntity } from './base'
import type { LegitimationStatus, Decision } from './enums'

export interface LegitimationRequest extends BaseEntity {
  // Identificação
  protocol: string                // Protocolo único (ex: "2024/000123")
  tenantId: string
  unitId: string                  // Unidade sendo legitimada

  // Workflow
  status: LegitimationStatus      // Status no workflow (11 estados)
  decision?: Decision             // Decisão final

  // Datas
  requestDate: Date               // Data da solicitação
  analysisDeadline?: Date         // Prazo para análise
  publicationDate?: Date          // Data de publicação edital
  contestationDeadline?: Date     // Prazo contestações (30 dias)
  approvalDate?: Date             // Data aprovação final
  issuanceDate?: Date             // Data emissão certidão

  // Documentação
  descriptiveMemorial?: string    // Memorial descritivo técnico
  technicalPlan?: string          // Planta técnica DWG/PDF
  certificate?: string            // Certidão de legitimação

  // Observações
  observations?: string
  justification?: string          // Justificativa decisão

  // Relacionamentos
  unit?: Unit
  responses?: LegitimationResponse[]
  contestations?: Contestation[]
  certificate?: LegitimationCertificate
}
```

## Tipos Enum

### UnitStatus

Status no workflow de validação de unidades.

📖 ****CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/11-unit-status.md**** - Especificação do VO UnitStatus

📖 **[CENTRAL/DOMAIN-MODEL/BUSINESS-RULES/WORKFLOW-RULES/unit-status-transitions.md](../../../../../../CENTRAL/DOMAIN-MODEL/BUSINESS-RULES/WORKFLOW-RULES/unit-status-transitions.md)** - State machine

```typescript
export enum UnitStatus {
  DRAFT = 'DRAFT',                       // Rascunho (coleta em andamento)
  PENDING_ANALYSIS = 'PENDING_ANALYSIS', // Aguardando análise
  IN_REVIEW = 'IN_REVIEW',               // Em revisão técnica
  APPROVED = 'APPROVED',                 // Aprovada
  REJECTED = 'REJECTED',                 // Rejeitada
  REQUIRES_CHANGES = 'REQUIRES_CHANGES'  // Requer correções
}

// Transições permitidas
const TRANSITIONS: Record<UnitStatus, UnitStatus[]> = {
  [UnitStatus.DRAFT]: [UnitStatus.PENDING_ANALYSIS],
  [UnitStatus.PENDING_ANALYSIS]: [UnitStatus.IN_REVIEW, UnitStatus.REJECTED],
  [UnitStatus.IN_REVIEW]: [UnitStatus.APPROVED, UnitStatus.REJECTED, UnitStatus.REQUIRES_CHANGES],
  [UnitStatus.REQUIRES_CHANGES]: [UnitStatus.DRAFT],
  [UnitStatus.APPROVED]: [], // Estado final
  [UnitStatus.REJECTED]: []  // Estado final
}
```

### LegitimationStatus

Status no workflow de legitimação fundiária (11 estados conforme Lei 13.465/2017).

📖 ****CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/12-legitimation-status.md**** - Especificação do VO

📖 **[CENTRAL/DOMAIN-MODEL/BUSINESS-RULES/WORKFLOW-RULES/legitimation-status-transitions.md](../../../../../../CENTRAL/DOMAIN-MODEL/BUSINESS-RULES/WORKFLOW-RULES/legitimation-status-transitions.md)** - State machine completa

```typescript
export enum LegitimationStatus {
  DRAFT = 'DRAFT',                           // 1. Rascunho
  SUBMITTED = 'SUBMITTED',                   // 2. Submetido
  UNDER_ANALYSIS = 'UNDER_ANALYSIS',         // 3. Em análise
  PENDING_DOCUMENTS = 'PENDING_DOCUMENTS',   // 4. Aguardando documentos
  APPROVED_FOR_PUBLICATION = 'APPROVED_FOR_PUBLICATION', // 5. Aprovado para publicação
  PUBLISHED = 'PUBLISHED',                   // 6. Edital publicado
  CONTESTATION_PERIOD = 'CONTESTATION_PERIOD', // 7. Período de contestações (30 dias)
  UNDER_CONTESTATION_ANALYSIS = 'UNDER_CONTESTATION_ANALYSIS', // 8. Analisando contestações
  APPROVED = 'APPROVED',                     // 9. Aprovado
  REJECTED = 'REJECTED',                     // 10. Rejeitado
  CERTIFICATE_ISSUED = 'CERTIFICATE_ISSUED'  // 11. Certidão emitida (final)
}
```

### Role

Roles de autorização do sistema (RBAC).

📖 ****CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/23-role.md**** - Especificação do VO Role

📖 ****CENTRAL/SECURITY/02-authorization.md**** - Modelo RBAC

```typescript
export enum Role {
  SUPER_ADMIN = 'super-admin',       // Super administrador global
  ADMIN = 'admin',                   // Administrador do tenant
  MANAGER = 'manager',               // Gestor de processos
  ANALYST = 'analyst',               // Analista técnico
  FIELD_COLLECTOR = 'field-collector' // Coletor de campo
}
```

### CommunityType

Tipos de comunidades conforme classificação REURB.

📖 ****CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/15-community-type.md**** - Especificação do VO

```typescript
export enum CommunityType {
  URBANA = 'URBANA',           // Área urbana
  RURAL = 'RURAL',             // Área rural
  QUILOMBOLA = 'QUILOMBOLA',   // Comunidade quilombola
  INDIGENA = 'INDIGENA',       // Comunidade indígena
  RIBEIRINHA = 'RIBEIRINHA'    // Comunidade ribeirinha
}
```

## Tipos DTOs (Data Transfer Objects)

DTOs são usados para comunicação com a API, diferente das entidades completas.

### CreateUnitDTO

```typescript
export interface CreateUnitDTO {
  code: string
  communityId: string
  street: string
  number?: string
  city: string
  state: string
  occupationType: 'RESIDENTIAL' | 'COMMERCIAL' | 'MIXED' | 'INSTITUTIONAL'
  residents?: number
  geometry?: string  // WKT ou GeoJSON
}
```

### UpdateUnitDTO

```typescript
export interface UpdateUnitDTO {
  code?: string
  street?: string
  number?: string
  residents?: number
  geometry?: string
  status?: UnitStatus
  observations?: string
}
```

### ListUnitsQueryDTO

```typescript
export interface ListUnitsQueryDTO {
  page?: number           // Página (padrão: 1)
  limit?: number          // Itens por página (padrão: 20, máx: 100)
  communityId?: string    // Filtro por comunidade
  status?: UnitStatus     // Filtro por status
  search?: string         // Busca textual (code, street, etc)
  sortBy?: 'code' | 'createdAt' | 'updatedAt'
  sortOrder?: 'asc' | 'desc'
}
```

### Paginated Response

```typescript
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  limit: number
  totalPages: number
  hasNext: boolean
  hasPrevious: boolean
}
```

## Tipos Geográficos

### GeoPoint

```typescript
export interface GeoPoint {
  latitude: number   // -90 a 90
  longitude: number  // -180 a 180
  altitude?: number  // Metros (opcional)
  srid?: number      // Sistema de referência (padrão: 4326 - WGS84)
}
```

### GeoPolygon

```typescript
export interface GeoPolygon {
  type: 'Polygon'
  coordinates: number[][][]  // GeoJSON format
  srid?: number              // Sistema de referência
}

// Ou WKT (Well-Known Text)
type WKT = string  // Exemplo: "POLYGON((-46.6 -23.5, -46.5 -23.5, ...))"
```

## Type Guards

Funções para verificar tipos em runtime.

```typescript
// src/types/guards.ts

export function isUnit(obj: any): obj is Unit {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.code === 'string' &&
    typeof obj.status === 'string'
  )
}

export function isHolder(obj: any): obj is Holder {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.cpf === 'string' &&
    typeof obj.name === 'string'
  )
}

// Uso
if (isUnit(data)) {
  // TypeScript sabe que data é Unit
  console.log(data.code)
}
```

## Gerando Types do Backend

### Usando NSwag

```bash
cd PROJECTS/GEOAPI/SRC-CODE

# Gera OpenAPI spec
dotnet run --project Carf.GeoApi.Gateway --launch-profile Swagger

# Gera types TypeScript
nswag openapi2tsclient \
  /input:http://localhost:5000/swagger/v1/swagger.json \
  /output:../../../LIB/TS/TSCORE/SRC-CODE/src/types/generated.ts \
  /template:Fetch \
  /typeScriptVersion:5.3
```
