---
type: leaf
status: review
updated: 2026-02-08
---

# Field Collection - Coleta em Campo

Feature de coleta de dados em campo implementada como formulario wizard multi-step React Native, permitindo field collectors cadastrarem unidades habitacionais e ocupacoes durante levantamento tecnico em areas sem internet.

## Visao Geral

A coleta em campo utiliza a tela `UnitFormScreen` via Expo Router stack navigation, recebendo param `unitId` para edicao de unidade existente ou `null` para criacao nova. O formulario e dividido em 5 steps sequenciais, cada step renderizado como screen separada com botoes **Proximo** e **Voltar**. Validacoes inline impedem avanco se campos obrigatorios estiverem vazios ou invalidos.

## Wizard Steps

### Step 1 - BasicInfo

Componente `FormStep1BasicInfo` com inputs controlled via React Hook Form `useForm` hook.

| Campo | Tipo | Obrigatorio | Descricao |
|-------|------|-------------|-----------|
| `nome` | string | Sim | Nome da unidade, trim nao vazio |
| `tipo` | enum | Sim | Tipo de ocupacao |
| `status` | enum | Sim | Status da unidade |
| `comunidade_id` | UUID (dropdown) | Sim | Comunidade associada |
| `caracterizacao` | enum | Sim | `CONSOLIDADA`, `PRECARIA`, `RISCO` |

A `CaracterizacaoOcupacao` e um enum validado contra valores permitidos (`CONSOLIDADA`, `PRECARIA`, `RISCO`) via Zod typed literal.

### Step 2 - Address

Componente `FormStep2Address` com inputs de endereco.

| Campo | Tipo | Obrigatorio | Descricao |
|-------|------|-------------|-----------|
| `logradouro` | string | Sim | Nome da rua |
| `numero` | string | Sim | Numero do imovel |
| `complemento` | string | Nao | Complemento |
| `bairro` | string | Sim | Bairro |
| `CEP` | string | Sim | Formato 8 digitos, regex pattern |

Oferece autocomplete via CEP API quando online, com fallback para input manual offline.

### Step 3 - AreaMeasurement

Componente `FormStep3Area` com input numerico para area em metros quadrados.

- Validacao: min 10 m², max 10.000 m² (reasonable bounds)
- Calculadora built-in permitindo field collector inserir dimensoes (largura x comprimento) com auto-calculating area total

### Step 4 - Geolocation

Componente `FormStep4Geolocation` com `MapView` (React Native Maps) exibindo marker draggable na posicao GPS atual.

- GPS obtido via `Expo Location` `getCurrentPositionAsync` com accuracy high, timeout 10s
- Botao **Obter Localizacao Atual** faz refresh das coordenadas se user moveu
- Botao **Marcar Manualmente** permite drag marker se GPS impreciso

### Step 5 - PhotoCapture

Componente `FormStep5Photos` com `FlatList` exibindo thumbnails das fotos capturadas.

- Botao **Adicionar Foto** abre `BottomSheet` com opcoes: Camera ou Galeria
- Camera: `Expo Camera` `launchCameraAsync`
- Galeria: `Image Picker` `launchImageLibraryAsync`
- Compressao via `expo-image-manipulator`: resize 1920x1080, quality 0.8, reduzindo size antes de salvar
- URIs persistidos no local filesystem via `Expo FileSystem` `documentDirectory`
- Storage references na WatermelonDB `photos` collection

## Validacoes Zod

Schema `unitSchema` implementado via Zod:

| Campo | Tipo | Regra | Mensagem/Descricao |
|-------|------|-------|---------------------|
| `name` | string | obrigatorio, trim, min 3, max 200 | Nome da unidade |
| `address` | object (nested) | obrigatorio | Objeto com `street`, `number`, `neighborhood`, `city`, `state`, `CEP` validando formato patterns |
| `area` | number | obrigatorio, min 10, max 10.000 | Reasonable bounds evitando typos absurdos (100.000 m² para residencia) |
| `geolocation` | object | obrigatorio | `latitude` (-90 a 90), `longitude` (-180 a 180) formato decimal degrees, `accuracy` meters (optional metadata) |
| `photos` | array de URI strings | opcional | Formato file path, max 10 photos limit evitando storage overflow device |
| `community_id` | UUID | obrigatorio | Existencia validada via lookup WatermelonDB `communities` collection, checando ID presente antes submit |
| `caracterizacao` | enum | obrigatorio | Validado against allowed values `CONSOLIDADA`, `PRECARIA`, `RISCO` typed literal Zod |

### Comportamento de Validacao

- **Validacao client-side** executada `onChange` para cada field, mostrando error messages inline via `FormErrorMessage` component abaixo do input (red text, icon warning)
- **Validacao submit** executada ao final do wizard before persist, checando all steps validos e re-validando entire schema caso user navegou back e modificou fields anteriores, garantindo consistency

## Integracao API (Offline-First)

### Persistencia Local

Dados persistidos localmente na WatermelonDB `units` collection via `database.write` async action, criando `Unit` model instance com fields preenchidos do form, setando `_status` = `pending_create` indicando record novo aguardando sync.

### Sync Queue

Queueing sync operation na `sync_queue` collection, inserindo record com:

| Campo | Descricao |
|-------|-----------|
| `entity_type` | `unit` |
| `entity_id` | ID local da unidade |
| `operation` | `create` |
| `payload` | JSON serialized form data |
| `timestamp` | Timestamp de criacao para ordem de processing |

### Background Sync

Quando `NetInfo` detecta conexao online via `addEventListener` change event, triggering `syncData` function:

1. Itera `sync_queue` processando cada record sequentially
2. Chama `POST /api/units` com payload deserializado, `Authorization: Bearer` header com access token obtido via `AuthManager`
3. **Success (201 Created)**: recebe server-generated `unitId`, atualiza local record com server ID, seta `_status` = `synced`, remove da `sync_queue`
4. **Fail (4xx/5xx)**: captura response, incrementa `retry_count`. Se < 3, mantem em queue para retry posterior com exponential backoff delay
5. **409 Conflict**: detecta duplicate via server validation, oferece merge options (user escolhe: keep local, keep server, merge fields)
6. **Network timeout**: mantem em queue, retry automatico na proxima sync attempt

Background sync via `Expo Background Fetch` `registerTaskAsync` executando periodic sync attempts mesmo com app em background, garantindo dados enviados logo que conexao disponivel. Field collector nao precisa de manual intervention.

## Domain Model WatermelonDB

Mapeamento da CENTRAL Unit entity para WatermelonDB `@model` class `Unit` extending `Model`:

| Campo | Tipo | Decorador | Descricao |
|-------|------|-----------|-----------|
| `name` | string (nullable false) | `@field` | Nome da unidade |
| `address` | string (JSON serialized object nested) | `@field` | Endereco completo serializado |
| `area` | number | `@field` | Area em metros quadrados |
| `geolocation` | string (JSON serialized coords) | `@field` | Coordenadas geograficas |
| `community_id` | foreign key | `@relation('community', 'community_id')` | Many-to-one communities |
| `holder_id` | foreign key | `@field` | Relacionamento titular |
| `_status` | enum | `@field` | `local`, `synced`, `pending_create`, `pending_update`, `pending_delete` |
| `created_at` | Date | `@date` | Auto-managed via `prepareCreate` |
| `updated_at` | Date | `@date` | Auto-managed via `prepareUpdate` |

### Relacionamentos

| Relacao | Tipo | Decorador | Collection |
|---------|------|-----------|------------|
| `photos` | one-to-many | `@children('photos')` | `photos` collection |
| `community` | many-to-one | `@relation('community', 'community_id')` | `communities` collection |

## Requisitos Funcionais Implementados

Implementacao do [UC-P3-004 (Operar em Campo)](../../USE-CASES/UC-P3-004-operar-em-campo/README.md):

- Wizard multi-step formulario mobile touch-optimized com validacoes inline feedback
- Captura geolocalizacao GPS automatica com manual fallback (marker draggable)
- Captura fotografias via camera/galeria com compressao e storage local
- Persistencia offline WatermelonDB com zero data loss
- Sincronizacao automatica background queue-based com retry logic
- Cadastro unidade com campos obrigatorios: validacoes CPF, area, endereco
- Relacionamento titular via `holder_id` foreign key
- Atribuicao `community_id`
- Geolocation GPS e photos como evidencias

Rastreando requisitos: **RF-005**, **RF-006** (cadastro e coleta em campo mobile offline).

## Referencias

- [WORKFLOW-MESTRE Parte 3 - Operacao Campo](../../../../CENTRAL/WORKFLOW-MESTRE/03-operacao-campo/passo-15-fluxo-operacional.md)
- [UC-P3-004 - Operar em Campo](../../USE-CASES/UC-P3-004-operar-em-campo/README.md)
- [Offline Sync](./03-offline-sync.md)
- [Holder Management](./02-holder-management.md)
- [GEOAPI Unit Aggregate](../../../GEOAPI/DOCS/DOMAIN/AGGREGATES/01-unit-aggregate.md)
- [Offline-First Pattern](../../../GEOAPI/DOCS/PATTERNS/01-mobile-offline-first.md)
