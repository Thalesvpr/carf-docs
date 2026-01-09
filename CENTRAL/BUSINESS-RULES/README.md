# Business Rules - Regras de Negócio do Sistema

Business rules são restrições validações e políticas de negócio que governam comportamento do sistema assegurando compliance legal integridade de dados e aderência a processos estabelecidos através de regras explícitas verificáveis e rastreáveis.

## Estrutura

Regras de negócio organizadas em 3 categorias principais conforme natureza e aplicação:

### VALIDATION-RULES/ - Regras de Validação

Regras que garantem integridade e consistência de dados de entidades validando campos relacionamentos e restrições antes de persistência.

**Arquivos:**
- **holder-validation.md** - Validação de Holder (CPF/CNPJ unicidade, LGPD, UnitHolder relationships)
- **unit-validation.md** - Validação de Unit (code unicidade, geometria, área, spatial overlap)

**Aplicação:** Executadas durante criação/atualização de entidades antes de commit transacional

**Tecnologia:** Validação em múltiplas camadas (client-side, API, database constraints)

---

### WORKFLOW-RULES/ - Regras de Workflow

Regras que governam transições de status através de state machines definindo quais mudanças de estado são permitidas baseadas em status atual role de usuário e pré-condições de negócio.

**Arquivos:**
- **unit-status-transitions.md** - State machine de Unit (6 estados: DRAFT, PENDING_ANALYSIS, IN_REVIEW, APPROVED, REJECTED, REQUIRES_CHANGES)
- **legitimation-status-transitions.md** - State machine de LegitimationRequest (11 estados workflow conforme Lei 13465/2017)

**Aplicação:** Enforcement em backend validando requisições de mudança de status verificando transição permitida role adequado pré-condições atendidas registrando em AuditLog e disparando eventos de domínio

**Tecnologia:** State pattern, role-based access control, domain events

---

### LEGITIMATION-RULES/ - Regras de Legitimação Fundiária

Regras específicas de processos de legitimação fundiária conforme Lei 13465/2017 estabelecendo requisitos diferenciados por modalidade REURB-S vs REURB-E e regras de contestações administrativas.

**Arquivos:**
- **reurb-s-requirements.md** - Requisitos REURB-S (interesse social: baixa renda, área ≤250sqm, gratuito, documentação simplificada)
- **reurb-e-requirements.md** - Requisitos REURB-E (interesse específico: área ≤500sqm, taxa cobrada, documentação completa, licenças ambientais)
- **contestation-rules.md** - Regras de contestações administrativas (período 30 dias, legitimidade, análise, decisão, recursos)

**Aplicação:** Validação durante workflow de legitimação conforme modalidade selecionada verificando elegibilidade documentação obrigatória custos aplicáveis e condicionantes impostas

**Base Legal:** Lei Federal 13.465/2017 (Regularização Fundiária Urbana e Rural)

**Tecnologia:** Workflow engine, document management, notification system

---

## Enforcement de Regras

**Múltiplas Camadas de Validação:**

1. **Client-side:** Validação básica de formato em formulários web/mobile (feedback imediato ao usuário)
2. **API Layer:** Validação de negócio antes de processar requisição (garante que apenas dados válidos chegam ao domínio)
3. **Domain Layer:** Validação profunda com acesso a repositórios e serviços (regras complexas envolvendo múltiplas entidades)
4. **Database Layer:** Constraints e triggers como última linha de defesa (unicidade, foreign keys, check constraints)

**Auditoria de Violações:**

Todas violações de regras de negócio são registradas em AuditLog permitindo troubleshooting e análise de padrões de erro identificando campos problemáticos ou necessidades de treinamento.

**Mensagens de Erro User-Friendly:**

Erros de validação geram mensagens específicas orientando usuário sobre problema detectado e ação corretiva necessária facilitando correção sem necessidade de conhecimento técnico profundo.

---

## Rastreabilidade para Requisitos

Business rules implementam e asseguram compliance com requisitos funcionais e legislação:

**VALIDATION-RULES:**
- Relacionado: RF-XXX (validação de CPF), RF-XXX (validação de geometria)
- Base: Regras de integridade de dados, LGPD (Lei 13.709/2018)

**WORKFLOW-RULES:**
- Relacionado: RF-XXX (workflow de unidades), RF-XXX (workflow de legitimação)
- Base: Processo administrativo definido, rastreabilidade de decisões

**LEGITIMATION-RULES:**
- Relacionado: RF-XXX (processo REURB-S), RF-XXX (processo REURB-E), RF-XXX (contestações)
- Base Legal: Lei 13.465/2017, Decreto Municipal específico, jurisprudência

---

## Implementações

Business rules documentadas aqui têm implementação específica em:
- **Backend .NET**: `PROJECTS/GEOAPI/LAYERS/DOMAIN/RULES/` (classes validation, workflow engines)
- **Frontend React**: `PROJECTS/GEOWEB/VALIDATIONS/` (client-side validation functions)
- **Mobile React Native**: `PROJECTS/REURBCAD/VALIDATIONS/` (offline validation before sync)
- **Plugin GIS Python**: `PROJECTS/GEOGIS/validators/` (bulk validation scripts)

**Importante:** CENTRAL/BUSINESS-RULES/ documenta regras de negócio de forma technology-agnostic. Implementações específicas (bibliotecas, frameworks, patterns) pertencem a PROJECTS/[PROJECT_NAME]/DOCS/.

Ver também:
- **CENTRAL/WORKFLOWS/** - Workflows que aplicam business rules
- **CENTRAL/DOMAIN-MODEL/ENTITIES/** - Entidades sujeitas a validação
- **CENTRAL/DOMAIN-MODEL/AGGREGATES/** - Invariantes de aggregate roots
- **CENTRAL/DOMAIN-MODEL/00-INDEX.md** - Índice completo do modelo de domínio

---

**Última atualização:** 2025-01-08
