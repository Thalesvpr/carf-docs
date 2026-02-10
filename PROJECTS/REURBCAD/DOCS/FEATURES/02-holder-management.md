---
type: leaf
status: review
updated: 2026-02-08
---

# Holder Management - Gestao de Titulares

Feature de gestao de titulares implementada como CRUD completo mobile, permitindo field collectors cadastrarem, visualizarem, editarem e removerem titulares (pessoas fisicas) vinculadas a unidades habitacionais durante levantamento de campo.

## Visao Geral

O modulo de gestao de titulares abrange todo o ciclo de vida de um titular no contexto mobile: cadastro com validacao de CPF, upload de documentos, vinculacao a unidades e sincronizacao offline. Toda a persistencia local utiliza WatermelonDB com sync queue para envio ao backend quando online.

## Telas

### HoldersListScreen

`FlatList` exibindo titulares cadastrados localmente na WatermelonDB, com search filter por nome, CPF e status.

### HolderFormScreen

Formulario com inputs: nome completo, CPF, RG, data de nascimento, telefone, email e documentos (upload via camera ou galeria). Persiste localmente offline.

### HolderDetailsScreen

Exibe informacoes completas do titular com tabs:

| Tab | Conteudo |
|-----|----------|
| **Info** | Dados pessoais completos |
| **Documentos** | Documentos uploadados (RG, CPF, comprovante) |
| **Unidades Vinculadas** | Navegacao entre titulares e unidades relacionadas |

### Componentes

| Componente | Descricao |
|------------|-----------|
| `HolderCard` | Exibe avatar, nome, CPF, badge status (ativo/inativo), actions: view, edit, delete |
| `HolderSearchBar` | Input text com debounce filtering query localmente WatermelonDB `Q.where` name `Q.like` `%query%` ou cpf `Q.eq` query |
| `VincularHolderModal` | Bottom sheet listando holders disponiveis com checkboxes, permitindo vincular multiplos titulares a single unit ou vice-versa, supporting one-to-many e many-to-many relationships conforme business rules |
| `DocumentUploadWidget` | Captura photos de documentos (RG, CPF, comprovante residencia) via Expo Camera ou Image Picker, compressing e storing no local filesystem com references na WatermelonDB |

## Validacoes Zod

Schema `holderSchema` implementado via Zod:

| Campo | Tipo | Regra | Descricao |
|-------|------|-------|-----------|
| `name` | string | obrigatorio, trim, min 3, max 200, regex apenas letras/espacos/acentos (sem numeros) | Nome completo do titular |
| `cpf` | string | obrigatorio, 11 digitos, `validateCPF` helper com algoritmo Mod11, rejeita CPFs known invalid (`000.000.000-00`, `111.111.111-11`, sequential) | Documento CPF |
| `rg` | string | opcional, formato state-specific patterns ou generic alphanumeric | Documento RG |
| `data_nascimento` | Date | obrigatorio, age min 18 anos, max 120 anos, rejeita future dates e typos (01/01/1900) | Data de nascimento |
| `telefone` | string | obrigatorio, formato brasileiro `(XX) XXXXX-XXXX` ou `(XX) XXXX-XXXX` (landline e mobile) | Telefone de contato |
| `email` | string | opcional, formato RFC 5322 regex pattern | Email do titular |
| `documents` | array objects | opcional, cada document com `type` enum (`RG`, `CPF`, `COMPROVANTE_RESIDENCIA`) e `file_uri` string format | Documentos anexados |

### Validacoes Adicionais

| Validacao | Descricao |
|-----------|-----------|
| **Vinculacao** | `unit_id` UUID existencia via WatermelonDB `units` collection lookup; `holder_id` existencia impedindo orphan references |
| **Uniqueness CPF** | Async validator querying WatermelonDB `holders` collection `WHERE cpf = $cpf` excluindo current holder se editing, retornando boolean exists, impedindo duplicate CPFs no mesmo tenant |

## Tipos de Vinculacao

Relacao many-to-many entre titulares e unidades via junction table `unit_holders`:

| Tipo | Descricao |
|------|-----------|
| `PROPRIETARIO` | Proprietario da unidade |
| `COMODATARIO` | Comodatario com direito de uso |
| `LOCATARIO` | Locatario com contrato de aluguel |
| `OCUPANTE` | Ocupante irregular |

Cada registro da junction contem: `unit_id`, `holder_id`, `relationship_type`.

## Integracao API (Offline-First)

### CRUD Titulares

1. Persiste holders localmente na WatermelonDB `holders` collection, criando `Holder` model instance com fields nome, cpf, rg, data_nascimento, telefone, email e `_status` = `pending_create`
2. Queueing sync operation na `sync_queue`
3. Quando online, sync pushing via `POST /api/holders` com payload holder data e `Authorization` header
4. Backend valida CPF uniqueness tenant-wide, insere na `holders` table, retorna `holderId`
5. Client atualiza local record com server ID, marca `synced`
6. Se conflict **409**: detecta duplicate CPF, oferece merge (keep local, keep server)

### Upload Documentos

1. Upload separado via `POST /api/holders/:id/documents` multipart form data
2. File photo compressed JPEG, base64 encoded ou binary stream
3. Backend armazena em blob storage (Azure Blob / AWS S3), retorna `document_url`
4. Persiste na `holders_documents` table: `holder_id`, `document_type`, `document_url`
5. Client atualiza local reference URL permitindo download posterior quando online

### Vinculacao/Desvinculacao

| Operacao | Endpoint | Metodo | Descricao |
|----------|----------|--------|-----------|
| Vincular | `/api/unit-holders` | `POST` | Body: `unit_id`, `holder_id`, `relationship_type`. Backend valida ambos IDs existem no mesmo tenant, insere junction table, retorna success |
| Desvincular | `/api/unit-holders/:id` | `DELETE` | Soft delete setando `deleted_at`, preservando historico para auditoria |

## Domain Model WatermelonDB

Mapeamento da CENTRAL Holder entity para WatermelonDB `@model` class `Holder`:

| Campo | Tipo | Decorador | Descricao |
|-------|------|-----------|-----------|
| `nome` | string | `@field` | Nome completo |
| `cpf` | string (unique index) | `@field` | CPF do titular |
| `rg` | string (nullable) | `@field` | RG do titular |
| `data_nascimento` | number (timestamp) | `@field` | Data de nascimento |
| `telefone` | string | `@field` | Telefone de contato |
| `email` | string (nullable) | `@field` | Email |
| `_status` | enum | `@field` | Tracking sync state |
| `created_at` | Date | `@date` | Timestamp criacao |
| `updated_at` | Date | `@date` | Timestamp atualizacao |

### Relacionamentos

| Relacao | Tipo | Decorador | Descricao |
|---------|------|-----------|-----------|
| `documents` | one-to-many | `@children('holder_documents')` | Documentos do titular |
| `units` | many-to-many | via junction `unit_holders` (writable false) | Unidades vinculadas |

## Requisitos Funcionais Implementados

Implementacao dos requisitos de gestao de titulares:

- **Cadastrar titular**: formulario mobile com validacoes CPF, nome, telefone
- **Vincular titular a unidade**: selecionar holder existente ou criar new inline via modal
- **Desvincular titular**: mantem holder record, apenas remove relationship junction
- **Visualizar titulares vinculados**: lista holders com relationship type badge
- **Editar informacoes titular**: preserva vinculacoes existentes
- **Remover titular**: soft delete, checando vinculacoes e impedindo delete se holder vinculado a unidades ativas (oferece desvinculacao automatica)
- **Documentacao upload**: captura via camera/galeria, storage local, sync quando online

Rastreando requisitos: **RF-007**, **RF-008** (gestao titulares, vinculacao unidades, CPF validation, documentos).

## Referencias

- [Field Collection](./01-field-collection.md)
- [Offline Sync](./03-offline-sync.md)
- [CENTRAL Holder Concept](../../../../CENTRAL/DOMAIN/CONCEPTS/03-holder.md)
- [GEOAPI Holder Management](../../../GEOAPI/DOCS/FEATURES/02-holder-management.md)
- [GEOAPI Holder Commands](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/APPLICATION/COMMANDS/02-holder-commands.md)
- [CPF Value Object](../../../GEOAPI/DOCS/DOMAIN/VALUE-OBJECTS/01-cpf.md)
