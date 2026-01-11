# Field Data Collection Workflow

Workflow de coleta de dados cadastrais em campo via aplicativo mobile REURBCAD permitindo técnicos fiscais municipais visitarem comunidades irregulares offline capturando informações de unidades habitacionais (endereço, geometria GPS, fotos, titulares) sem necessidade de conectividade sincronizando automaticamente quando WiFi disponível com conflict detection resolution strategies garantindo zero data loss mantendo UX fluída mesmo em áreas remotas sem sinal, implementando offline-first architecture via [ADR-006: WatermelonDB](../../ARCHITECTURE/ADRs/ADR-006-offline-first-watermelondb.md) conforme [ADR-004: React Native](../../ARCHITECTURE/ADRs/ADR-004-react-native-mobile.md) mobile app sincronizando com backend GEOAPI via @carf/geoapi-client executando use case [UC-004: Coletar Dados Campo](../../REQUIREMENTS/USE-CASES/UC-004-coletar-dados-campo-mobile.md) e [UC-005: Sincronizar Offline](../../REQUIREMENTS/USE-CASES/UC-005-sincronizar-dados-offline.md).

## Atores

**Técnico de Campo (Field Agent):** Fiscal municipal funcionário equipe técnica com tablet/smartphone visitando casas coletando dados cadastrais, autorizado em Communities específicas via CommunityAuthorization vinculado a Team conforme [ADR-005: Multi-tenancy RLS](../../ARCHITECTURE/ADRs/ADR-005-multi-tenancy-rls.md).

**Morador/Posseiro:** Titular ocupante unidade fornecendo informações pessoais documentação provas posse, cadastrado como Holder vinculado a Unit via UnitHolder relacionamento.

**Sistema Mobile:** REURBCAD React Native app armazenando dados local WatermelonDB SQLite enfileirando mutations pending sync processando batch quando conectado.

**Backend API:** GEOAPI recebendo dados sincronizados persistindo PostgreSQL+PostGIS validando server-side detectando conflitos retornando resoluções.

## Steps do Workflow

### 1. Preparação Offline (Planning Phase)

**Técnico em escritório com WiFi:**
1. Abre REURBCAD mobile app autenticado via Keycloak OAuth2 PKCE flow conforme [ADR-003](../../ARCHITECTURE/ADRs/ADR-003-keycloak-autenticacao.md)
2. Seleciona [Community](../ENTITIES/04-community.md) autorizada para trabalhar (filtrado por CommunityAuthorization de seu Team)
3. Executa **PULL sync** baixando dados existentes da comunidade:
   - Units já cadastradas (geométricas, attributes)
   - Holders vinculados
   - Documents/Photos anteriores
   - Tiles mapa offline (basemap, ortofotos se disponíveis via WMS)
4. Dados salvos local WatermelonDB conforme [ADR-006](../../ARCHITECTURE/ADRs/ADR-006-offline-first-watermelondb.md)
5. App sinaliza "Pronto para campo - X unidades baixadas"

### 2. Coleta em Campo Offline (Collection Phase)

**Técnico em área SEM conectividade:**

#### 2.1 Navegar até unidade
- Visualiza mapa offline com units existentes como markers
- Usa GPS device nativo para localização atual
- Caminha até casa ainda não cadastrada ou precisa atualização

#### 2.2 Criar nova Unit
1. Toca botão "+" ou desenha polígono no mapa
2. GPS captura coordenadas atuais como GeoPoint inicial
3. Opcionalmente caminha perímetro marcando vértices gerando GeoPolygon
4. App calcula área m² automaticamente validando bounds dentro município
5. Preenche formulário Unit:
   - Code (auto-gerado sequencial offline: TEMP-001, TEMP-002, etc)
   - Address (Address VO validado)
   - Construction type (WOOD, BRICK, MIXED)
   - Status inicial: DRAFT

#### 2.3 Capturar fotos georreferenciadas
1. Toca "Adicionar Foto" usando expo-camera native
2. Camera captura foto com EXIF metadata incluindo GPS coordinates timestamp
3. Compress automático reduzindo tamanho (max 2MB) economizando storage
4. Armazena local como Document type PHOTO_FRONT, PHOTO_BACK, PHOTO_INTERIOR
5. Marca pending_upload para sync posterior

#### 2.4 Cadastrar Titular (Holder)
1. Toca "Adicionar Titular" no formulário Unit
2. Preenche dados Holder:
   - Name
   - CPF validado client-side via @carf/tscore CPF Value Object com dígitos verificadores
   - Birth date, phone, email
   - Is main titular (boolean)
3. Cria vínculo UnitHolder relacionamento N:N
4. Valida unicidade CPF local cache (aviso se duplicado em outra unit)

#### 2.5 Adicionar annotations/notas
1. Campo texto livre para observações técnico
2. Salvo como Annotation type NOTE vinculada à Unit
3. Útil para: "Precisa revisão topógrafo", "Confrontante contestou limite", etc

#### 2.6 Salvar offline
1. Toca "Salvar" persistindo local WatermelonDB
2. Unit marcada `_status: 'created'` flag sync pending
3. IDs temporários UUID v4 client-generated garantindo unicidade
4. Timestamps `created_at`, `updated_at` locais
5. App mostra "Salvo localmente - Aguardando sync"

### 3. Repetir coleta múltiplas casas
- Técnico repete steps 2.1-2.6 para 10-50 unidades no dia
- Tudo armazenado local sem necessidade WiFi
- Bateria dura ~8h campo com GPS+camera contínuo

### 4. Retorno ao escritório - Sincronização (Sync Phase)

**Técnico conecta WiFi ao final do dia:**

#### 4.1 Sync automático triggered
1. App detecta WiFi disponível (não usa dados móveis por default, configurável)
2. Background worker inicia batch sync conforme [UC-005](../../REQUIREMENTS/USE-CASES/UC-005-sincronizar-dados-offline.md)
3. Progresso indicator mostra "Sincronizando X/Y unidades"

#### 4.2 PUSH local changes para server
1. WatermelonDB query filtra records `_status: 'created' | 'updated' | 'deleted'`
2. Serializa batch 500 registros JSON payload incluindo:
   - Units com geometrias WKT
   - Holders vinculados
   - Documents/Photos base64 ou URLs
   - Annotations
   - Timestamps local created_at/updated_at para conflict detection
3. POST /api/sync/push para GEOAPI

#### 4.3 Server-side processing
Backend GEOAPI:
1. Valida JWT token tenant_id extraindo contexto via [ADR-005: RLS](../../ARCHITECTURE/ADRs/ADR-005-multi-tenancy-rls.md)
2. Para cada Unit recebida:
   - Verifica se ID já existe (update) ou novo (create)
   - Se existe: compara timestamps server vs client
     - Server newer? **CONFLICT detected**
     - Client newer? Accept update
   - Se novo: INSERT com validações server-side:
     - Geometria válida sem self-intersections
     - Não overlaps outras units (spatial query PostGIS)
     - CPF Holder único per tenant
     - Community authorization válida
3. Gera IDs definitivos server-side (UUID v7 timestamp-ordered)
4. Atribui codes definitivos sequenciais (substitui TEMP-001 → COM-A-0001)
5. Upload photos para S3/storage gerando URLs permanentes
6. Persiste PostgreSQL+PostGIS via [ADR-002](../../ARCHITECTURE/ADRs/ADR-002-postgresql-postgis.md)
7. Dispara domain events: UnitCreatedEvent, HolderLinkedEvent via [ADR-010](../../ARCHITECTURE/ADRs/ADR-010-event-driven-architecture.md)

#### 4.4 Conflict resolution
Se conflito detectado (same record editado server E client):
1. Server retorna HTTP 409 Conflict com detalhes:
   - Server version data
   - Client version data
   - Conflicting fields
   - Suggested resolution
2. Estratégias:
   - **Last-write-wins (default):** Client timestamp > server? Client vence
   - **Manual merge:** Campos críticos (geometria, titular principal) requerem UI merge
   - **Field-level merge:** Campos não-críticos (notas, fotos) merged automaticamente
3. App mobile mostra tela "Conflito detectado - Resolver manualmente" se necessário
4. Técnico escolhe versão manter ou merge campos específicos
5. Re-submit após resolução

#### 4.5 PULL server changes para local
1. GET /api/sync/pull?since=<last_sync_timestamp> busca mudanças server desde última sync
2. Backend retorna:
   - Units novas criadas por outros técnicos
   - Units atualizadas (aprovadas, rejeitadas, corrigidas)
   - Deletions soft-deleted
3. Mobile aplica mudanças local WatermelonDB:
   - INSERT novos records
   - UPDATE existentes (substituindo IDs temporários por definitivos)
   - SOFT DELETE marcando `_deleted: true` sem remover database
4. UI atualiza lista units mostrando codes definitivos, status atualizados

#### 4.6 Finalização sync
1. Marca todos records local como `_status: 'synced'`
2. Limpa flags pending
3. Armazena `last_sync_timestamp` para próxima sync incremental
4. Notificação push "Sincronização completa - X unidades enviadas, Y recebidas"
5. Log sync em SyncLog table com metrics (duration, conflicts, errors)

### 5. Retry & Error Handling

**Se sync falha (network timeout, server error, validation error):**
1. App retenta automaticamente até 3x com exponential backoff (5s, 15s, 45s)
2. Se persistir, mantém dados local marcados pending
3. Notificação "Erro sincronizar - Dados salvos localmente, tentar novamente?"
4. Botão manual "Forçar Sync" disponível
5. Logs erro localmente para troubleshooting (AuditLog)

**Se conflito irresolvível automaticamente:**
1. Unit/Holder marcado `conflict: true` local
2. Badge vermelho UI "X conflitos requerem atenção"
3. Tela dedicada lista conflitos com diff visual
4. Técnico resolve manualmente ou escalona para analista desktop

## Aggregates & Entities Envolvidas

**Principais:**
- [UnitAggregate](../AGGREGATES/01-unit-aggregate.md) root coordenando Unit + UnitHolders + Documents + Annotations
- Holder entity pessoa física titular
- [Community](../ENTITIES/04-community.md) agrupamento geográfico unidades
- Team + CommunityAuthorization controle acesso

**Suporte:**
- Document fotos anexos
- Annotation notas observações
- SyncLog audit trail sincronizações

## Value Objects Utilizados

- CPF validação dígitos verificadores
- Email RFC 5322
- PhoneNumber DDD Brasil
- Address endereço estruturado
- GeoPolygon geometria unidade
- GeoPoint coordenadas GPS
- UnitStatus enum DRAFT PENDING APPROVED
- SyncStatus enum PENDING SUCCESS CONFLICT FAILED

## Business Rules Aplicadas

- [holder-validation](../../BUSINESS-RULES/VALIDATION-RULES/holder-validation.md) CPF único, LGPD compliance
- [unit-validation](../../BUSINESS-RULES/VALIDATION-RULES/unit-validation.md) geometria válida, sem overlap spatial
- [unit-status-transitions](../../BUSINESS-RULES/WORKFLOW-RULES/unit-status-transitions.md) state machine transições permitidas

## Implementação

**Mobile App:** REURBCAD React Native + Expo implementando workflow completo com WatermelonDB local database conforme [ADR-006](../../ARCHITECTURE/ADRs/ADR-006-offline-first-watermelondb.md), sync engine bidirectional pull/push, conflict resolution UI, GPS capture expo-location, camera expo-camera, maps offline react-native-maps com tiles cache.

**Backend API:** GEOAPI endpoint POST /api/sync/push e GET /api/sync/pull implementados via [CQRS handlers](../../ARCHITECTURE/PATTERNS/02-cqrs.md) validando server-side persistindo PostgreSQL+PostGIS detectando conflitos timestamps retornando resoluções.

**Deployment:** Mobile deployment via [EAS Build](../../ARCHITECTURE/DEPLOYMENT/05-mobile-deployment.md) distribuindo APK/IPA App Store Google Play, backend deployment via [Kubernetes](../../ARCHITECTURE/DEPLOYMENT/03-orchestration.md) HPA scaling conforme carga sincronizações.

## Métricas & KPIs

- **Coleta:** 10-50 units/dia per técnico (média 25)
- **Sync duration:** 2-5min para 50 units + fotos
- **Conflict rate:** <5% sync operations (maioria auto-resolved last-write-wins)
- **Data loss:** 0% (offline-first garante dados persistidos local até sync sucesso)
- **Uptime mobile:** ~8h bateria uso intensivo GPS+camera

## Próximos Workflows

Após coleta campo, dados seguem para:
- [Analyst Validation Workflow](./02-analyst-validation-workflow.md) correção massa QGIS desktop
- [Topography Workflow](./03-topography-workflow.md) levantamento GNSS profissional se necessário
- Legitimation Workflow processo administrativo Lei 13.465/2017

---

**Última atualização:** 2026-01-10
