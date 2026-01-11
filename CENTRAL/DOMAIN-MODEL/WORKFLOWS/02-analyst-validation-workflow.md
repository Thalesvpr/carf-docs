# Analyst Validation Workflow

Workflow de validação e correção em massa de dados coletados via analistas GIS usando GEOWEB portal web para edições pontuais ou GEOGIS plugin QGIS desktop para correções batch processando centenas unidades simultaneamente utilizando ortofotos drone como referência visual via WMS layers conforme [UC-010: Configurar WMS](../../REQUIREMENTS/USE-CASES/UC-010-configurar-camadas-wms.md) permitindo analistas identificar erros geometrias GPS campo (imprecisão 3-10m typical) corrigindo polígonos manualmente sobrepondo ortofoto alta resolução (precisão 10cm) validando topologia detectando overlaps gaps slivers ajustando attributes verificando CPF duplicados aprovando units para workflow legitimation implementado em backend GEOAPI conforme [Clean Architecture](../../ARCHITECTURE/PATTERNS/01-clean-architecture.md) e [CQRS pattern](../../ARCHITECTURE/PATTERNS/02-cqrs.md).

## Atores

**Analista GIS (Analyst):** Técnico especializado GIS com conhecimento QGIS PostGIS revisando dados campo desktop identificando erros corrigindo geometrias validando attributes aprovando units, autorizado via role ANALYST em Team com acesso Communities específicas via CommunityAuthorization.

**Gestor Técnico (Manager):** Coordenador equipe revisando aprovações finais resolvendo contestações duplicatas complexas definindo prioridades communities análise, role MANAGER com permissões elevadas multi-community.

## Steps do Workflow

### 1. Visualização Dados Coletados (Review Phase)

**Analista em GEOWEB:**
1. Login via Keycloak OAuth2 conforme [ADR-003](../../ARCHITECTURE/ADRs/ADR-003-keycloak-autenticacao.md)
2. Seleciona Community autorizada filtro dropdown
3. Visualiza mapa interativo react-leaflet/MapLibre renderizando:
   - Units status DRAFT (coletadas campo aguardando validação) markers amarelos
   - Units PENDING (em revisão) markers laranjas
   - Units APPROVED (validadas) markers verdes
   - Layers WMS ortofotos drone background conforme WMS workflow
4. Lista tabular paginada units com filtros avançados:
   - Status, data criação, técnico coletor, área m², conflitos detectados
5. Dashboard KPIs:
   - Total units community: X
   - Aguardando validação: Y (Z%)
   - Aprovadas: W
   - Rejeitadas: V

### 2. Identificação Erros Automáticos

**Sistema detecta automaticamente via [unit-validation](../../BUSINESS-RULES/VALIDATION-RULES/unit-validation.md):**
- **Spatial overlaps:** Geometrias units sobrepondo >10% área (PostGIS ST_Overlaps query)
- **Gaps suspeitos:** Espaços vazios entre units adjacentes sugerindo erro digitalização
- **Geometrias inválidas:** Self-intersections, polígonos não fechados (PostGIS ST_IsValid)
- **Área fora range:** <10m² ou >500m² suspeito (validação business rule REURB Lei 13.465)
- **CPF duplicado:** Mesmo titular vinculado múltiplas units sem justificativa
- **Coordenadas fora bounds:** GPS capturou fora limites município (bounding box validation)

**Units com erros marcadas status REQUIRES_CHANGES** automaticamente via [unit-status-transitions](../BUSINESS-RULES/WORKFLOW-RULES/unit-status-transitions.md), notificação enviada analista responsável via domain event UnitValidationFailedEvent conforme [ADR-010: Events](../../ARCHITECTURE/ADRs/ADR-010-event-driven-architecture.md).

### 3. Correção Web Pontual (Individual Fix)

**Analista em GEOWEB para 1-5 units:**
1. Clica unit marker mapa abrindo modal detalhes
2. Ativa modo edição "Edit Geometry"
3. Ajusta vértices polígono arrastando sobre ortofoto WMS visualizando limite real casa
4. Valida formulário attributes:
   - Address, construction type, observations
5. Valida Holders vinculados:
   - CPF correto via @carf/tscore validação
   - Vínculo titular principal único
6. Adiciona Annotation type NOTE justificando alteração: "Corrigido polígono conforme ortofoto 2025"
7. Submete PATCH /api/units/{id} via @carf/geoapi-client
8. Backend valida server-side command handler ApproveUnitCommand conforme [CQRS](../../ARCHITECTURE/PATTERNS/02-cqrs.md)
9. Status transitions DRAFT → PENDING (aguardando aprovação gestor)

### 4. Correção Massa QGIS (Batch Processing)

**Analista em GEOGIS plugin para 50-500 units:**

#### 4.1 Conexão WFS
1. Abre QGIS Desktop 3.28+ LTR
2. Menu Plugins → GEOGIS → Conectar Servidor
3. Configura conexão WFS GEOAPI:
   - URL: https://api.carf.gov.br/wfs
   - Auth: JWT token obtido Keycloak via plugin OAuth flow
4. Seleciona layer "Units - Community X" filtrando status DRAFT
5. Download vector layer QGIS temporário editing mode habilitado

#### 4.2 Configuração Basemaps
1. Adiciona WMS ortofoto drone como background conforme WMS workflow
2. Transparência 70% units overlaying ortofoto
3. Simbologia colorida por status (DRAFT amarelo, overlaps vermelho, approved verde)

#### 4.3 Correção Batch Geometrias
1. Ferramenta "Edit Multiple Features" selecionando 10-50 units vizinhas
2. Ajusta vértices batch usando ortofoto referência visual precisão 10cm
3. Topologia validation:
   - Menu Vector → Topology Checker → Check Overlaps → Fix
   - QGIS detecta overlaps automaticamente propondo snap edges
   - Analista aceita/rejeita sugestões batch
4. Simplify geometries removendo vértices redundantes threshold 0.5m mantendo formato
5. Validate geometries PostGIS ST_MakeValid corrigindo self-intersections

#### 4.4 Bulk Attributes Update
1. Abre Attribute Table filtrando units específicas
2. Field Calculator batch update:
   - Construction type: WOOD → BRICK (se identificado ortofoto)
   - Status: DRAFT → PENDING (após correções)
   - Analyst validation date: today
3. Adiciona annotation batch: "Geometrias corrigidas conforme ortofoto 2025-01-10"

#### 4.5 Sync Back to Server
1. Plugin GEOGIS menu "Sincronizar Alterações"
2. Serializa WFS-T transactions (Update features) batch 100 units
3. POST /api/wfs/Transaction para GEOAPI
4. Backend valida cada unit command handler UpdateUnitGeometryCommand
5. Persiste PostgreSQL+PostGIS via [ADR-002](../../ARCHITECTURE/ADRs/ADR-002-postgresql-postgis.md)
6. Response Success com IDs processados ou Errors detalhados
7. Plugin QGIS mostra modal "X units atualizadas, Y erros - Ver log"

### 5. Validação Topologia Avançada

**Para comunidades críticas precisão legal:**
1. Menu Processing → Toolbox → Topology Rules
2. Aplica regras OGC:
   - Must Not Overlap (units diferentes não podem sobrepor)
   - Must Not Have Gaps (units adjacentes devem fechar)
   - Must Not Have Dangles (edges devem conectar completamente)
3. Gera relatório erros topology_errors.gpkg layer
4. Fix manual ou semi-automático cada erro identificado
5. Re-valida até zero errors

### 6. Resolução Duplicatas CPF

**Se [holder-validation](../../BUSINESS-RULES/VALIDATION-RULES/holder-validation.md) detecta duplicata:**
1. Query lista holders com CPF duplicado: `SELECT cpf, COUNT(*) FROM holders GROUP BY cpf HAVING COUNT(*) > 1`
2. Analista investiga:
   - Legítimo: Mesmo titular possui múltiplas casas (comum)
   - Erro: CPF digitado incorreto campo (corrigir)
   - Fraude suspeita: Escalona gestor investigação
3. Se legítimo: Adiciona annotation justificando "Titular possui 3 unidades conforme documentação"
4. Se erro: Corrige CPF via PATCH /api/holders/{id}
5. Se fraude: Marca unit status REJECTED notificando gestor domain event SuspiciousDuplicateDetectedEvent

### 7. Aprovação Final Units

**Após correções validadas:**
1. Analista marca batch units status PENDING
2. Gestor técnico revisa dashboard "Unidades Aguardando Aprovação"
3. Valida amostragem random 10% units verificando qualidade correções
4. Batch approve via command handler ApproveUnitsCommand:
   - Status transitions PENDING → APPROVED conforme [unit-status-transitions](../BUSINESS-RULES/WORKFLOW-RULES/unit-status-transitions.md)
5. Domain event UnitApprovedEvent disparado conforme [ADR-010](../../ARCHITECTURE/ADRs/ADR-010-event-driven-architecture.md)
6. Units aprovadas elegíveis próximo workflow legitimation

### 8. Rejeição Units Inválidas

**Se unit não corrigível (invasão área pública, dados insuficientes):**
1. Gestor marca status REJECTED via command RejectUnitCommand
2. Preenche motivo obrigatório: "Invasão área verde pública conforme ortofoto - não regularizável"
3. Notificação enviada técnico campo via app push notification
4. Unit permanece base dados auditoria mas excluída processos ativos
5. Estatísticas dashboard: Taxa rejeição <5% ideal, >10% indica problema campo training

## Aggregates & Entities Envolvidas

- [UnitAggregate](../AGGREGATES/01-unit-aggregate.md) root coordenando validações
- Community agrupamento geográfico
- Holder validação duplicatas CPF
- Annotation justificativas alterações audit trail
- Team + CommunityAuthorization controle acesso analistas

## Value Objects Utilizados

- UnitStatus state machine DRAFT → PENDING → APPROVED/REJECTED
- GeoPolygon geometrias corrigidas validation
- [CPF](../VALUE-OBJECTS/01-cpf.md) validação duplicatas

## Business Rules Aplicadas

- [unit-validation](../../BUSINESS-RULES/VALIDATION-RULES/unit-validation.md) spatial overlaps gaps area bounds
- [holder-validation](../../BUSINESS-RULES/VALIDATION-RULES/holder-validation.md) CPF unicidade
- [unit-status-transitions](../BUSINESS-RULES/WORKFLOW-RULES/unit-status-transitions.md) state machine allowed transitions

## Implementação

**Portal Web:** GEOWEB React Vite com maps interativos react-leaflet formulários edição validação client-side @carf/tscore consumindo [GEOAPI /api/units](../../API/UNITS/README.md) via @carf/geoapi-client.

**Plugin Desktop:** GEOGIS QGIS Python 3.9+ plugin batch processing WFS-T sync topologia validation análises espaciais [GIS patterns](../../ARCHITECTURE/PATTERNS/07-gis-spatial-patterns.md).

**Backend:** GEOAPI CQRS handlers ApproveUnitCommand RejectUnitCommand UpdateUnitGeometryCommand validando server-side PostGIS spatial queries multi-tenancy RLS conforme [ADR-005](../../ARCHITECTURE/ADRs/ADR-005-multi-tenancy-rls.md).

## Métricas

- **Throughput:** Analista processa 50-100 units/dia web, 200-500 units/dia QGIS batch
- **Error detection rate:** ~15-20% units campo requerem correção geometria
- **Approval rate:** ~95% units passam validação após correções
- **Rejection rate:** ~2-3% units inválidas não regularizáveis

---

**Última atualização:** 2026-01-10
