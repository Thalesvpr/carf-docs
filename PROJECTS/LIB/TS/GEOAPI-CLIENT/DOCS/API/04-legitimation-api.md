---
type: leaf
status: review
updated: 2026-01-21
---

# Legitimation API - Processos de Legitimacao Fundiaria

## Visao Geral

A Legitimation API fornece operacoes para gerenciamento de processos de legitimacao fundiaria, permitindo controlar o fluxo de aprovacao de titulos de propriedade.

## Import

```typescript
import { GeoApiClient } from '@carf/geoapi-client'
import type {
  Legitimation,
  CreateLegitimationDTO,
  LegitimationStatus,
  WorkflowAction
} from '@carf/tscore/types'

const api = new GeoApiClient({ baseURL: '...', auth })

// Acessar Legitimation API
api.legitimation.list()
api.legitimation.getById()
api.legitimation.create()
api.legitimation.executeAction()
api.legitimation.getHistory()
```

## Endpoints

```
GET    /api/legitimations              - Listar processos
GET    /api/legitimations/:id          - Buscar por ID
POST   /api/legitimations              - Criar processo
POST   /api/legitimations/:id/actions  - Executar acao de workflow
GET    /api/legitimations/:id/history  - Historico de acoes
GET    /api/legitimations/:id/documents - Documentos do processo
POST   /api/legitimations/:id/documents - Anexar documento
```

## Methods

### list()

Lista processos de legitimacao com filtros.

```typescript
list(query?: ListLegitimationsQueryDTO): Promise<PaginatedResponse<Legitimation>>
```

#### Parametros

```typescript
interface ListLegitimationsQueryDTO {
  page?: number
  limit?: number
  communityId?: string
  unitId?: string
  holderId?: string
  status?: LegitimationStatus
  assignedTo?: string            // Usuario responsavel
  createdAfter?: Date
  createdBefore?: Date
  sortBy?: 'createdAt' | 'updatedAt' | 'status'
  sortOrder?: 'asc' | 'desc'
}
```

#### Exemplo

```typescript
// Listar pendentes atribuidos a mim
const myPending = await api.legitimation.list({
  status: 'PENDING_ANALYSIS',
  assignedTo: currentUser.id
})

// Listar por unidade
const unitProcesses = await api.legitimation.list({
  unitId: 'unit-123'
})
```

### getById()

Busca processo por ID.

```typescript
getById(id: string, options?: { include?: Array<'unit' | 'holder' | 'documents' | 'history'> }): Promise<Legitimation>
```

#### Exemplo

```typescript
const process = await api.legitimation.getById('leg-123', {
  include: ['unit', 'holder', 'history']
})

console.log(`Processo: ${process.unit.code}`)
console.log(`Status: ${process.status}`)
console.log(`Acoes: ${process.history.length}`)
```

### create()

Cria novo processo de legitimacao.

```typescript
create(data: CreateLegitimationDTO): Promise<Legitimation>
```

#### Parametros

```typescript
interface CreateLegitimationDTO {
  unitId: string                 // Unidade a legitimar
  holderId: string               // Posseiro principal
  reurbType: 'REURB_S' | 'REURB_E'  // Tipo de REURB

  // Dados do processo (opcional)
  requestDate?: Date             // Data do requerimento
  protocolNumber?: string        // Numero do protocolo
  observations?: string

  // Documentos iniciais (opcional)
  documents?: Array<{
    type: DocumentType
    fileId: string               // ID do arquivo ja uploaded
  }>
}
```

#### Regras de Validacao

1. **unitId**: Unidade deve existir e nao ter processo ativo
2. **holderId**: Posseiro deve estar vinculado a unidade
3. **reurbType**: Deve ser compativel com tipo da comunidade

#### Exemplo

```typescript
const process = await api.legitimation.create({
  unitId: 'unit-123',
  holderId: 'holder-456',
  reurbType: 'REURB_S',
  requestDate: new Date(),
  protocolNumber: 'PROT-2026-001'
})
```

### executeAction()

Executa acao de workflow no processo.

```typescript
executeAction(id: string, action: WorkflowActionDTO): Promise<Legitimation>
```

#### Parametros

```typescript
interface WorkflowActionDTO {
  action: WorkflowAction
  observations?: string
  documents?: Array<{
    type: DocumentType
    fileId: string
  }>
}

type WorkflowAction =
  | 'SUBMIT'           // Submeter para analise
  | 'APPROVE'          // Aprovar
  | 'REJECT'           // Rejeitar
  | 'REQUEST_DOCS'     // Solicitar documentos
  | 'RETURN'           // Devolver para correcao
  | 'CANCEL'           // Cancelar processo
  | 'REOPEN'           // Reabrir processo
```

#### Fluxo de Status

```
DRAFT -> [SUBMIT] -> PENDING_ANALYSIS
                         |
         +---------------+---------------+
         |               |               |
     [APPROVE]     [REQUEST_DOCS]    [REJECT]
         |               |               |
         v               v               v
     APPROVED    PENDING_DOCUMENTS   REJECTED
                         |
                    [SUBMIT]
                         |
                         v
                 PENDING_ANALYSIS
```

#### Exemplo

```typescript
// Submeter para analise
await api.legitimation.executeAction('leg-123', {
  action: 'SUBMIT',
  observations: 'Documentacao completa'
})

// Aprovar
await api.legitimation.executeAction('leg-123', {
  action: 'APPROVE',
  observations: 'Processo em conformidade'
})

// Solicitar documentos
await api.legitimation.executeAction('leg-123', {
  action: 'REQUEST_DOCS',
  observations: 'Falta comprovante de residencia'
})

// Rejeitar
await api.legitimation.executeAction('leg-123', {
  action: 'REJECT',
  observations: 'Documentacao inconsistente'
})
```

### getHistory()

Obtem historico de acoes do processo.

```typescript
getHistory(id: string): Promise<LegitimationHistory[]>
```

#### Retorno

```typescript
interface LegitimationHistory {
  id: string
  legitimationId: string
  action: WorkflowAction
  fromStatus: LegitimationStatus
  toStatus: LegitimationStatus
  observations?: string
  performedBy: {
    id: string
    name: string
  }
  performedAt: Date
  documents?: Document[]
}
```

#### Exemplo

```typescript
const history = await api.legitimation.getHistory('leg-123')

history.forEach(h => {
  console.log(`${h.performedAt}: ${h.action} por ${h.performedBy.name}`)
  console.log(`  ${h.fromStatus} -> ${h.toStatus}`)
  if (h.observations) {
    console.log(`  Obs: ${h.observations}`)
  }
})
```

### getDocuments()

Lista documentos do processo.

```typescript
getDocuments(id: string): Promise<Document[]>
```

### addDocument()

Anexa documento ao processo.

```typescript
addDocument(id: string, data: AddDocumentDTO): Promise<Document>
```

#### Parametros

```typescript
interface AddDocumentDTO {
  type: DocumentType
  fileId: string                 // ID do arquivo (upload separado)
  description?: string
}

type DocumentType =
  | 'ID_DOCUMENT'                // RG, CNH
  | 'CPF'
  | 'PROOF_OF_RESIDENCE'         // Comprovante de residencia
  | 'MARRIAGE_CERTIFICATE'       // Certidao de casamento
  | 'PROPERTY_TAX'               // IPTU
  | 'POWER_OF_ATTORNEY'          // Procuracao
  | 'TECHNICAL_REPORT'           // Laudo tecnico
  | 'PLANT'                      // Planta/croqui
  | 'AERIAL_PHOTO'               // Foto aerea
  | 'OTHER'
```

## Tipos TypeScript

```typescript
import type {
  Legitimation,
  CreateLegitimationDTO,
  LegitimationStatus,
  LegitimationHistory,
  WorkflowAction,
  WorkflowActionDTO,
  DocumentType,
  Document
} from '@carf/tscore/types'
```
