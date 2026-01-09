# Violações de Agnosticismo - CENTRAL/TECHNICAL/

**Data:** 2025-01-05
**Total de arquivos:** 60
**Arquivos com violações:** ~30+

---

## Princípio Violado

**doc-standards**: CENTRAL/TECHNICAL/ deve descrever **O QUÊ** (conceitos, regras de negócio, fluxos) SEM mencionar **COMO** (tecnologias, bibliotecas, frameworks específicos).

---

## Categorias de Violações

### 1. Bibliotecas/Frameworks Específicos

**Violações encontradas:**
- FluentValidation (validação .NET)
- Entity Framework (ORM .NET)
- WatermelonDB (banco local mobile)
- Expo SDK (React Native)
- ASP.NET Core (middleware)
- Redis (cache)
- Zod (validação TypeScript - já corrigido em custom-data-schema.md)

**Arquivos afetados:**
- `BUSINESS-RULES/VALIDATION-RULES/business-validation.md` - menciona FluentValidation
- `BUSINESS-RULES/VALIDATION-RULES/README.md` - menciona FluentValidation
- `DATABASE/MIGRATIONS/README.md` - menciona Entity Framework
- `DOMAIN-MODEL/00-INDEX.md` - menciona Entity Framework, WatermelonDB
- `DOMAIN-MODEL/AGGREGATES/01-unit-aggregate.md` - Entity Framework navigation properties
- `DOMAIN-MODEL/ENTITIES/00-base-entity.md` - WatermelonDB Model
- `DOMAIN-MODEL/VALUE-OBJECTS/00-base-value-object.md` - FluentValidation, Zod, Pydantic
- `DOMAIN-MODEL/VALUE-OBJECTS/05-permissions-matrix.md` - ASP.NET Core, Redis
- `TESTING/TEST-CASES/E2E/README.md` - WatermelonDB, Detox, Playwright

**Como corrigir:**
```diff
- Validações FluentValidation em Application layer
+ Validações estruturais em camada de aplicação

- Entity Framework navigation properties
+ Propriedades de navegação

- WatermelonDB Model
+ Modelo de banco de dados local

- ASP.NET Core middleware
+ Middleware de autorização

- Redis cache
+ Cache em memória distribuído
```

---

### 2. Bancos de Dados e Funções Específicas

**Violações encontradas:**
- PostgreSQL (banco específico)
- PostGIS (extensão espacial)
- Funções PostGIS: ST_Overlaps, ST_Intersection, ST_Area, ST_IsValid, ST_Within, ST_Touches, ST_Azimuth, ST_Distance
- PL/pgSQL (linguagem procedural PostgreSQL)
- EXPLAIN ANALYZE (comando PostgreSQL)
- RLS Row-Level Security (feature PostgreSQL)

**Arquivos afetados:**
- `BUSINESS-RULES/README.md` - PostGIS functions
- `BUSINESS-RULES/VALIDATION-RULES/geographic-validation.md` - ST_IsValid, ST_Area, ST_Overlaps, ST_Within
- `BUSINESS-RULES/VALIDATION-RULES/README.md` - ST_IsValid, ST_Overlaps
- `DATABASE/PERFORMANCE/README.md` - PostgreSQL, PgBouncer, EXPLAIN ANALYZE, VACUUM
- `DATABASE/README.md` - PostgreSQL, PostGIS, PL/pgSQL
- `DATABASE/RLS/README.md` - PostgreSQL RLS, SET LOCAL
- `DATABASE/SCHEMA/FUNCTIONS/README.md` - PL/pgSQL, ST_Area, RLS
- `DATABASE/SCHEMA/README.md` - PostgreSQL, PostGIS ST_Area, RLS
- `DATABASE/SCHEMA/TABLES/README.md` - PostgreSQL, geography(Point,4326)
- `DATABASE/SCHEMA/TRIGGERS/README.md` - PostgreSQL triggers
- `DATABASE/SCHEMA/VIEWS/README.md` - PostgreSQL views, SECURITY DEFINER
- `DOMAIN-MODEL/ENTITIES/05-contestation.md` - PostGIS ST_Overlaps, ST_Intersection, QGIS
- `DOMAIN-MODEL/ENTITIES/06-pdf-templates.md` - ST_Azimuth, ST_Distance, ST_Touches
- `DOMAIN-MODEL/VALUE-OBJECTS/02-geo-polygon.md` - PostGIS, GEOS, JTS, Turf.js

**Como corrigir:**
```diff
- PostGIS ST_Overlaps
+ Operação de detecção de sobreposição espacial

- ST_Intersection
+ Operação de interseção geométrica

- ST_Area
+ Cálculo de área geométrica

- ST_IsValid
+ Validação de topologia geométrica

- PostgreSQL RLS
+ Controle de acesso por linha (row-level security)

- PL/pgSQL functions
+ Funções procedurais do banco de dados

- EXPLAIN ANALYZE
+ Análise de plano de execução de query

- geography(Point,4326)
+ Tipo geométrico de ponto geográfico
```

---

### 3. Tools e Software Específicos

**Violações encontradas:**
- QGIS (software GIS desktop)
- Grafana (monitoring dashboards)
- Prometheus (métricas)
- PagerDuty (alerting)
- Slack (notificações)
- Detox (testes mobile)
- Playwright (testes e2e)

**Arquivos afetados:**
- `DOMAIN-MODEL/ENTITIES/05-contestation.md` - QGIS
- `OPERATIONS/MONITORING/GRAFANA/` - Grafana específico
- `OPERATIONS/MONITORING/PROMETHEUS/` - Prometheus específico
- `TESTING/TEST-CASES/E2E/README.md` - Detox, Playwright

**Como corrigir:**
```diff
- ajuste de geometria via QGIS
+ ajuste de geometria via software GIS

- Grafana dashboards
+ Dashboards de monitoramento

- Prometheus metrics
+ Métricas de aplicação

- Detox React Native
+ Framework de testes mobile

- Playwright GEOWEB
+ Framework de testes e2e web
```

---

### 4. Endpoints e APIs Específicas

**Violações encontradas:**
- Endpoints REST específicos: `/api/v1/sync/pull`, `/api/v1/sync/push`
- HTTP methods explícitos: GET, POST, PUT, DELETE
- Status codes: 5xx

**Arquivos afetados:**
- Já corrigido em `WORKFLOWS/offline-sync-workflow.md`

**Como corrigir:**
```diff
- GET /api/v1/sync/pull?since={timestamp}
+ Endpoint de pull incremental com timestamp de referência

- POST /api/v1/sync/push
+ Endpoint de push de mudanças locais

- 5xx > 1%
+ Taxa de erros do servidor > 1%
```

---

### 5. Configurações e Formatos Específicos

**Violações encontradas:**
- EPSG:4674, EPSG:31981-31985 (códigos de sistema de coordenadas)
- RFC específicos (RFC 5322, RFC 7946)
- ConfigMaps Kubernetes, Docker volumes

**Arquivos afetados:**
- `DOMAIN-MODEL/VALUE-OBJECTS/02-geo-polygon.md` - EPSG codes
- `OPERATIONS/MONITORING/GRAFANA/PROVISIONING/README.md` - ConfigMaps Kubernetes

**Como corrigir:**
```diff
- SIRGAS2000 (EPSG:4674)
+ Sistema de referência geográfico brasileiro

- UTM zona apropriada (EPSG:31981-31985)
+ Sistema de referência projetado UTM

- RFC 5322
+ Padrão de formato de email

- ConfigMaps Kubernetes
+ Configurações via orquestrador de containers
```

---

## Pasta DATABASE/ - Caso Especial

**Observação:** A pasta `DATABASE/` é um caso especial porque documenta **implementação específica** de PostgreSQL/PostGIS.

**Decisão necessária:**
1. **Opção A:** Mover DATABASE/ para PROJECTS/GEOAPI/DATABASE/ (implementação específica)
2. **Opção B:** Manter em TECHNICAL/ mas renomear para DATABASE-POSTGRESQL/ deixando claro que é específico
3. **Opção C:** Criar DATABASE/ genérico conceitual + PROJECTS/GEOAPI/DATABASE-POSTGRES/ específico

**Recomendação:** Opção A - DATABASE/ deveria estar em PROJECTS/GEOAPI/ porque é implementação específica de PostgreSQL.

---

## Pasta OPERATIONS/ - Caso Especial

**Observação:** OPERATIONS/MONITORING/ documenta ferramentas específicas (Grafana, Prometheus).

**Decisão necessária:**
1. Mover para DEVELOPMENT/INFRASTRUCTURE/OPERATIONS/
2. Criar documentação conceitual de monitoring em TECHNICAL/OPERATIONS/ genérica

**Recomendação:** Mover para DEVELOPMENT/INFRASTRUCTURE/OPERATIONS/ porque é implementação específica.

---

## Resumo de Prioridades

### 🔴 CRÍTICO - Corrigir Imediatamente

1. **BUSINESS-RULES/** - Remove FluentValidation, PostGIS functions
   - Afeta: 5 arquivos
   - Impacto: Alto (regras de negócio devem ser agnósticas)

2. **DOMAIN-MODEL/ENTITIES/** - Remove PostGIS, QGIS
   - Afeta: 3 arquivos (contestation.md, pdf-templates.md, base-entity.md)
   - Impacto: Alto (entidades são conceituais)

3. **DOMAIN-MODEL/VALUE-OBJECTS/** - Remove FluentValidation, Zod, PostGIS, libraries
   - Afeta: 4 arquivos
   - Impacto: Alto (value objects são conceituais)

### 🟡 MÉDIO - Corrigir Logo

4. **TESTING/TEST-CASES/** - Remove Detox, Playwright, WatermelonDB
   - Afeta: 1 arquivo (E2E/README.md)
   - Impacto: Médio (estratégias de teste devem ser genéricas)

### 🟢 BAIXO - Decisão Arquitetural

5. **DATABASE/** - Decidir se move para PROJECTS/ ou mantém com renomeação
   - Afeta: ~15 arquivos
   - Impacto: Estrutural (requer decisão de onde colocar docs específicos)

6. **OPERATIONS/** - Mover para INFRASTRUCTURE ou criar versão conceitual
   - Afeta: ~5 arquivos
   - Impacto: Estrutural

---

## Ações Recomendadas

### Imediato (Hoje)

1. Corrigir BUSINESS-RULES/ (5 arquivos)
2. Corrigir DOMAIN-MODEL/ENTITIES/ (3 arquivos)
3. Corrigir DOMAIN-MODEL/VALUE-OBJECTS/ (4 arquivos)

### Curto Prazo (Esta Semana)

4. Corrigir TESTING/TEST-CASES/
5. Decidir destino de DATABASE/
6. Decidir destino de OPERATIONS/

### Médio Prazo (Próximo Sprint)

7. Criar script de validação automática de agnosticismo
8. Adicionar CI check que bloqueia commits com violações
9. Documentar princípio de agnosticismo em CONTRIBUTING.md

---

## Script de Validação Sugerido

```bash
#!/bin/bash
# validate-agnosticism.sh
# Valida que CENTRAL/TECHNICAL/ não menciona tecnologias específicas

VIOLATIONS=0

# Bibliotecas proibidas
FORBIDDEN=(
  "FluentValidation"
  "Entity Framework"
  "WatermelonDB"
  "Zod"
  "Expo SDK"
  "ASP.NET"
  "Redis"
  "Detox"
  "Playwright"
  "ST_Overlaps"
  "ST_Intersection"
  "ST_Area"
  "ST_IsValid"
  "PL/pgSQL"
  "QGIS"
  "Grafana"
  "Prometheus"
)

for term in "${FORBIDDEN[@]}"; do
  matches=$(grep -rn "$term" CENTRAL/TECHNICAL --include="*.md" | wc -l)
  if [ $matches -gt 0 ]; then
    echo "❌ Encontrado '$term' em CENTRAL/TECHNICAL/ ($matches ocorrências)"
    VIOLATIONS=$((VIOLATIONS + matches))
  fi
done

if [ $VIOLATIONS -gt 0 ]; then
  echo ""
  echo "Total de violações: $VIOLATIONS"
  echo "CENTRAL/TECHNICAL/ deve ser agnóstico de tecnologia!"
  exit 1
else
  echo "✅ CENTRAL/TECHNICAL/ está agnóstico!"
  exit 0
fi
```

---

**Total estimado de correções:** ~30 arquivos
**Tempo estimado:** 2-3 horas para correções críticas

