---
type: leaf
title: "Reports API - Geracao de Relatorios"
status: review
updated: 2026-01-21
source: "interno"
---

# Reports API - Geracao de Relatorios

API para geracao e download de relatorios em multiplos formatos.

## Import

```typescript
import { GeoApiClient } from '@carf/geoapi-client'
import type { ReportFormat, ReportJob, ExportFilters } from '@carf/tscore/types'

const api = new GeoApiClient({ baseURL: '...', auth })

// Acessar Reports API
api.reports.exportUnits()
api.reports.exportHolders()
api.reports.getCommunityStats()
api.reports.getStatus()
api.reports.download()
```

## Endpoints

```
POST /api/reports/units/export      - Solicitar exportacao de unidades
POST /api/reports/holders/export    - Solicitar exportacao de posseiros
POST /api/reports/communities/stats - Solicitar estatisticas de comunidade
GET  /api/reports/:jobId/status     - Verificar status de geracao
GET  /api/reports/:jobId/download   - Download do relatorio gerado
```

## Fluxo de Geracao

Relatorios sao gerados de forma **assincrona**:

```
1. Solicitar geracao (POST) → Retorna jobId
2. Polling de status (GET /status) → Aguardar COMPLETED
3. Download do arquivo (GET /download)
```

**Motivo:** Relatorios grandes podem demorar varios segundos para gerar.

## Methods

### exportUnits()

Solicita exportacao de unidades.

```typescript
exportUnits(
  filters: UnitsExportFilters,
  format: ReportFormat
): Promise<ReportJob>
```

#### Parametros

**filters**:
```typescript
interface UnitsExportFilters {
  communityId?: string        // Filtrar por comunidade
  status?: UnitStatus         // Filtrar por status
  occupationType?: 'RESIDENTIAL' | 'COMMERCIAL' | 'MIXED' | 'INSTITUTIONAL'
  createdAfter?: Date
  createdBefore?: Date

  // Campos a incluir no relatorio
  includeHolders?: boolean    // Incluir dados de titulares
  includeGeometry?: boolean   // Incluir coordenadas (WKT)
  includeCustomData?: boolean // Incluir campos customizados
}
```

**format**:
```typescript
type ReportFormat = 'excel' | 'pdf' | 'csv'
```

#### Retorno

```typescript
interface ReportJob {
  id: string                  // Job ID para consultas
  status: ReportJobStatus     // PENDING | PROCESSING | COMPLETED | FAILED
  format: ReportFormat
  createdAt: Date
  completedAt?: Date
  downloadUrl?: string        // Disponivel quando COMPLETED
  error?: string              // Disponivel quando FAILED
  progress?: number           // 0-100 (se disponivel)
}

type ReportJobStatus = 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED'
```

#### Exemplo

```typescript
// Solicitar relatorio
const job = await api.reports.exportUnits({
  communityId: 'comm-123',
  status: 'APPROVED',
  includeHolders: true
}, 'excel')

console.log(`Job criado: ${job.id}`)

// Aguardar conclusao
let status = job
while (status.status !== 'COMPLETED' && status.status !== 'FAILED') {
  await sleep(2000)  // Aguardar 2s
  status = await api.reports.getStatus(job.id)
  console.log(`Status: ${status.status} (${status.progress}%)`)
}

if (status.status === 'COMPLETED') {
  // Fazer download
  const blob = await api.reports.download(job.id)
  downloadFile(blob, 'unidades-aprovadas.xlsx')
} else {
  console.error('Falha:', status.error)
}
```

---

### exportHolders()

Solicita exportacao de posseiros.

```typescript
exportHolders(
  filters: HoldersExportFilters,
  format: ReportFormat
): Promise<ReportJob>
```

#### Parametros

```typescript
interface HoldersExportFilters {
  communityId?: string        // Filtrar por comunidade
  hasUnit?: boolean           // Apenas com/sem unidade vinculada
  createdAfter?: Date
  createdBefore?: Date

  // Campos a incluir
  includeUnits?: boolean      // Incluir unidades vinculadas
  includeAddress?: boolean    // Incluir endereco
  includeContact?: boolean    // Incluir telefone/email
  maskCpf?: boolean           // Mascarar CPF (***.***.***-XX)
}
```

#### Exemplo

```typescript
const job = await api.reports.exportHolders({
  communityId: 'comm-123',
  includeUnits: true,
  maskCpf: true
}, 'csv')

// ... aguardar e baixar
```

---

### getCommunityStats()

Solicita relatorio de estatisticas de comunidade.

```typescript
getCommunityStats(
  communityId: string,
  format: ReportFormat
): Promise<ReportJob>
```

#### Conteudo do Relatorio

- Total de unidades por status
- Total de posseiros
- Area total e media
- Distribuicao por tipo de ocupacao
- Evolucao temporal (unidades por mes)
- Graficos (apenas PDF)

#### Exemplo

```typescript
const job = await api.reports.getCommunityStats('comm-123', 'pdf')

// Aguardar e baixar relatorio PDF com graficos
```

---

### getStatus()

Verifica status de um job de geracao.

```typescript
getStatus(jobId: string): Promise<ReportJob>
```

#### Exemplo

```typescript
const status = await api.reports.getStatus('job-abc-123')

if (status.status === 'COMPLETED') {
  console.log('Relatorio pronto!')
} else if (status.status === 'PROCESSING') {
  console.log(`Processando: ${status.progress}%`)
}
```

---

### download()

Faz download do relatorio gerado.

```typescript
download(jobId: string, options?: DownloadOptions): Promise<Blob>
```

#### Throws

- `NotFoundError` (404) - Job nao existe
- `BadRequestError` (400) - Job ainda nao completou

#### Exemplo

```typescript
const blob = await api.reports.download('job-abc-123')

// Download no browser
const url = window.URL.createObjectURL(blob)
const link = document.createElement('a')
link.href = url
link.download = 'relatorio.xlsx'
link.click()
```

---

## Helper: waitForCompletion()

Aguarda conclusao do job com polling automatico.

```typescript
async waitForCompletion(
  jobId: string,
  options?: WaitOptions
): Promise<ReportJob>
```

#### Parametros

```typescript
interface WaitOptions {
  pollingInterval?: number    // Intervalo em ms (padrao: 2000)
  timeout?: number            // Timeout total em ms (padrao: 300000 = 5min)
  onProgress?: (job: ReportJob) => void
}
```

#### Exemplo

```typescript
// Solicitar e aguardar
const job = await api.reports.exportUnits(filters, 'excel')

const completed = await api.reports.waitForCompletion(job.id, {
  pollingInterval: 3000,
  timeout: 60000,
  onProgress: (j) => console.log(`Progress: ${j.progress}%`)
})

const blob = await api.reports.download(completed.id)
```

---

## Helper: exportAndDownload()

Combina solicitacao, aguardo e download em uma chamada.

```typescript
async exportAndDownload(
  type: 'units' | 'holders' | 'communityStats',
  params: ExportParams,
  format: ReportFormat,
  options?: ExportOptions
): Promise<Blob>
```

#### Exemplo

```typescript
// Uma linha para exportar e baixar
const blob = await api.reports.exportAndDownload(
  'units',
  { communityId: 'comm-123', status: 'APPROVED' },
  'excel',
  { onProgress: (p) => console.log(`${p}%`) }
)

downloadFile(blob, 'unidades.xlsx')
```

---

## Formatos de Saida

### Excel (.xlsx)

- Formatacao de colunas automatica
- Headers em negrito
- Dados em tabela filtrada
- Multiplas abas (se aplicavel)

### PDF

- Cabecalho com logo e data
- Tabelas formatadas
- Graficos (estatisticas)
- Paginacao automatica

### CSV

- UTF-8 com BOM (compativel Excel)
- Separador: ponto-e-virgula (;)
- Ideal para importacao em outros sistemas

---

## Uso com React Query

```typescript
import { useQuery, useMutation } from '@tanstack/react-query'

function ExportButton({ communityId }: Props) {
  const api = useApi()

  const exportMutation = useMutation({
    mutationFn: async () => {
      const job = await api.reports.exportUnits(
        { communityId },
        'excel'
      )
      const completed = await api.reports.waitForCompletion(job.id)
      return api.reports.download(completed.id)
    },
    onSuccess: (blob) => {
      downloadFile(blob, `unidades-${communityId}.xlsx`)
    }
  })

  return (
    <button
      onClick={() => exportMutation.mutate()}
      disabled={exportMutation.isPending}
    >
      {exportMutation.isPending ? 'Gerando...' : 'Exportar Excel'}
    </button>
  )
}
```
