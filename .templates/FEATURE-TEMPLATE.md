# {Feature Name}

{Dense paragraph descrevendo feature tecnicamente incluindo componentes principais utilizados como {ComponentName} e {OtherComponent} gerenciando fluxo de dados através de state management {Zustand/TanStack Query/Context} com forms implementados via {React Hook Form + Zod} validando entrada do usuário antes de consumir endpoints da API {/api/resource} usando HTTP client {@carf/geoapi-client ou fetch} tratando erros de rede e exibindo feedback visual ao usuário, integrando domain model do CENTRAL utilizando entidades {Entity1} e {Entity2} junto com value objects {VO1} e {VO2} para validações client-side garantindo consistência antes de submeter dados ao backend seguindo padrões estabelecidos em CENTRAL/REQUIREMENTS e CENTRAL/DOMAIN-MODEL documentados para este caso de uso específico.}

**Requirements:** [UC-XXX: Nome do Caso de Uso](../../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-XXX-nome.md), [RF-YYY: Nome Requisito](../../../../CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/RF-YYY-nome.md)

**Componentes Principais:**

{Parágrafo denso descrevendo componentes React/React Native/Backend envolvidos como {MainPage} que renderiza lista de items usando {ItemCard} com suporte a paginação via {usePagination} hook consumindo dados de TanStack Query cache, {FormDialog} modal para criação/edição com formulário controlado React Hook Form integrando validações Zod schema, {MapView} para visualização geoespacial usando Leaflet ou Google Maps com desenho interativo de polígonos e markers, {ActionButtons} para operações CRUD acionando mutations que atualizam cache otimisticamente antes de confirmar com backend.}

**State Management:**

{Descrição de como state é gerenciado incluindo Zustand store {useFeatureStore} mantendo estado global de {selectedItems, filters, viewMode} acessível por múltiplos componentes, TanStack Query hooks {useFeatureList, useFeatureDetails, useCreateFeature, useUpdateFeature} gerenciando server state com cache automático refetch e invalidation strategies, Context API {FeatureContext} provendo configurações e preferências compartilhadas, local component state via useState para UI ephemeral como modals abertos selected tabs current step em wizards, sincronização entre stores garantindo consistência de dados através de subscriptions e observers.}

**Validações:**

{Detalhamento de validações client-side implementadas com React Hook Form + Zod schemas definindo types {FeatureFormData} com regras como campos obrigatórios string().min(), email format validation email(), CPF/CNPJ validation via @carf/tscore value objects new CPF(), coordinate validation para lat/lng range checking, polygon validation garantindo no-self-intersection e minimum area, cross-field validations como data início < data fim, async validations checando unicidade de código via debounced API call, mensagens de erro customizadas em português exibidas inline no formulário.}

**API Integration:**

{Descrição de endpoints consumidos como GET /api/features para listar paginado com query params ?page=1&limit=20&filter=status:active, POST /api/features para criar novo com body JSON validado, PUT /api/features/:id para atualização parcial, DELETE /api/features/:id para soft delete, usando HTTP client @carf/geoapi-client configurado com base URL interceptors para adicionar auth token Bearer JWT retry logic em caso de network failure, error handling diferenciando 4xx client errors de 5xx server errors mostrando toast notifications apropriadas, optimistic updates modificando cache local antes de confirmar operação melhorando UX percebida, rollback automático em caso de falha restaurando estado anterior.}

**Domain Model:**

{Mapeamento de entidades e value objects do CENTRAL/DOMAIN-MODEL utilizados nesta feature como entidade [Unit](../../../../CENTRAL/DOMAIN-MODEL/ENTITIES/02-unit.md) representando unidade habitacional com propriedades code area status geometry relacionada com [Holder](../../../../CENTRAL/DOMAIN-MODEL/ENTITIES/03-holder.md) via many-to-many UnitHolder, value object [CPF](../../../../CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/01-cpf.md) validando documento titular com algoritmo módulo 11, [GeoPolygon](../../../../CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/08-geopolygon.md) encapsulando geometria polygon com validações topológicas, [Address](../../../../CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/06-address.md) normalizando endereço com CEP cidade estado, garantindo que frontend representation espelha backend domain model mantendo consistência semântica entre camadas.}

**Offline-First:** *(apenas para REURBCAD - DELETAR esta seção em outros projetos)*

{Explicação de estratégia offline-first usando WatermelonDB collections {features, holders, photos} persistindo dados localmente em SQLite durante coleta em campo sem conectividade, sync queue mantendo lista de operações pendentes create/update/delete ordenadas por timestamp, conflict detection ao sincronizar comparando updated_at timestamps entre local e remote, merge strategies aplicando last-write-wins ou manual resolution dependendo do tipo de conflito, background sync via useEffect polling quando app volta online ou manual trigger por botão, offline UI indicators mostrando badge com número de items pending sync e status icon indicando connectivity state, GPS tracking continuous salvando coordenadas georreferenciadas em background task, camera integration capturando fotos associadas com metadata location timestamp comprimindo antes de persistir economizando storage.}

---

**Última atualização:** YYYY-MM-DD
