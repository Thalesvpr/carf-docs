# REQUIREMENTS - Requisitos CARF

Especificação completa de requisitos funcionais, não-funcionais, casos de uso e user stories do sistema CARF organizados hierarquicamente com rastreabilidade bidirecional entre níveis permitindo navegação eficiente entre fonte atômica de requisitos (RF), perspectiva de usuário (US), fluxos completos (UC), e implementação em projetos específicos.

## Estrutura

**457 arquivos principais** organizados em 4 categorias hierárquicas:

- **[USE-CASES/](./USE-CASES/README.md)** - 11 casos de uso principais documentando fluxos completos ([index-by-epic](./USE-CASES/index-by-epic.md))
- **[FUNCTIONAL-REQUIREMENTS/](./FUNCTIONAL-REQUIREMENTS/README.md)** - 221 requisitos funcionais definindo capacidades específicas ([index-by-epic](./FUNCTIONAL-REQUIREMENTS/index-by-epic.md))
- **[USER-STORIES/](./USER-STORIES/README.md)** - 140 user stories em formato BDD ([index-by-epic](./USER-STORIES/index-by-epic.md))
- **[NON-FUNCTIONAL-REQUIREMENTS/](./NON-FUNCTIONAL-REQUIREMENTS/README.md)** - 85 requisitos não-funcionais de qualidade do sistema ([index-by-epic](./NON-FUNCTIONAL-REQUIREMENTS/index-by-epic.md))

## Índices de Navegação

**Por Épica:**
- [Use Cases por Épica](./USE-CASES/index-by-epic.md) - 11 UCs agrupados em Security (5), Performance (2), Scalability (4)
- [Requisitos Funcionais por Épica](./FUNCTIONAL-REQUIREMENTS/index-by-epic.md) - 221 RFs distribuídos em 18 épicas
- [User Stories por Épica](./USER-STORIES/index-by-epic.md) - 140 USs distribuídas em 10 épicas
- [Requisitos Não-Funcionais por Épica](./NON-FUNCTIONAL-REQUIREMENTS/index-by-epic.md) - 85 RNFs distribuídos em 7 épicas

**Por Módulo:**
- [Todos Requirements por Módulo](./index-by-module.md) - Índice completo cruzando UCs/RFs/USs/RNFs com módulos implementadores (GEOWEB, REURBCAD, GEOAPI, GEOGIS)

**Rastreabilidade:**
- [Matriz Completa UC→RF→US→RNF](./traceability-matrix.md) - Mapa bidirecional mostrando todos os 11 UCs e seus 68 RFs + 24 USs relacionados com links para implementação em PROJECTS/*/FEATURES/

## Hierarquia de Dependências

Requisitos organizados hierarquicamente onde RF Requisitos Funcionais definem O QUE fazer sendo referenciados por US User Stories especificando QUEM usa e POR QUE que por sua vez são referenciados por UC Use Cases documentando COMO fazer completo incluindo fluxos alternativos e excepcionais. Casos de uso identificam módulos implementadores via frontmatter modules resultando em implementação documentada em PROJECTS/*/DOCS/FEATURES/*.md estabelecendo rastreabilidade completa entre especificação e código.

Requirements funcionam como SOURCE NODES não linkando para implementação mas sendo linkados por PROJECTS/*/FEATURES/ estabelecendo rastreabilidade bidirecional entre especificação de produto em CENTRAL/ e código técnico em PROJECTS/.

## Épicas Principais

| Épica | UCs | RFs | USs | RNFs | Total |
|-------|-----|-----|-----|------|-------|
| performance | 2 | 38 | ~40 | ~20 | 100 |
| compatibility | 0 | 31 | ~20 | ~15 | 66 |
| security | 5 | 25 | ~25 | ~10 | 65 |
| scalability | 4 | 22 | ~20 | ~15 | 61 |
| units | 0 | 22 | ~10 | ~5 | 37 |
| usability | 0 | 21 | ~15 | ~10 | 46 |
| **TOTAL** | **11** | **221** | **140** | **85** | **457** |

## Módulos Implementadores

| Módulo | UCs | RFs | USs | RNFs | Total | Cobertura |
|--------|-----|-----|-----|------|-------|-----------|
| GEOWEB | 11 | 189 | ~130 | ~50 | 380 | 83.2% |
| REURBCAD | 8 | 112 | ~80 | ~30 | 230 | 50.3% |
| GEOAPI | 4 | 93 | ~60 | ~25 | 182 | 39.8% |
| GEOGIS | 2 | 59 | ~30 | ~20 | 111 | 24.3% |
| ADMIN | 1 | ~20 | ~10 | ~5 | 36 | 7.9% |
| KEYCLOAK | 0 | ~10 | ~5 | ~5 | 20 | 4.4% |

**Features Implementadas:**
- ✅ **GEOWEB** - 7 arquivos em FEATURES/ (Unit Management, Holder Management, GIS Integration, Reporting, Team Management, Legitimation Process, Shapefile Import)
- ✅ **REURBCAD** - 6 arquivos em FEATURES/ (Field Collection, Offline Sync, Holder Management, Team Management, Unit Management, Shapefile Import)
- ⚠️ **GEOAPI** - Sem FEATURES/ (requisitos implementados via REST API documentada em CENTRAL/API/)
- ✅ **GEOGIS** - 2 arquivos em FEATURES/ (Shapefile Import, GIS Integration)
- ✅ **ADMIN** - 2 arquivos em FEATURES/ (User Management, Tenant Management)
- N/A **KEYCLOAK** - Infraestrutura de autenticação (6 examples em CENTRAL/INTEGRATION/KEYCLOAK/examples/)

## Cobertura de Rastreabilidade

### Use Cases
✅ **100%** (11/11) dos UCs têm seção Rastreabilidade mapeando RFs e USs relacionados
✅ **100%** (11/11) dos UCs linkados em PROJECTS/*/FEATURES/ via frontmatter `modules:`

### Functional Requirements
⚠️ **30.8%** (68/221) dos RFs referenciados diretamente por UCs via rastreabilidade
⚠️ **0%** dos RFs linkados diretamente em PROJECTS/ (acessíveis via INDEXes e traceability-matrix)

### User Stories
⚠️ **17.1%** (24/140) dos USs referenciados diretamente por UCs via rastreabilidade
⚠️ **0%** dos USs linkados diretamente em PROJECTS/ (acessíveis via INDEXes e traceability-matrix)

### Non-Functional Requirements
⚠️ **0%** (0/85) dos RNFs referenciados por UCs (RNFs são transversais, aplicam-se a múltiplos UCs)
ℹ️ RNFs organizados por épica (Performance, Security, Reliability, Usability, etc.) em index-by-epic.md

## Padrões e Convenções

Frontmatter YAML obrigatório em todos arquivos de requisitos incluindo campo modules listando projetos implementadores como GEOWEB REURBCAD e campo epic identificando épica como security performance ou scalability permitindo indexação automática e rastreabilidade. Use Cases incluem seção Rastreabilidade listando RFs e USs relacionados no formato RF-049 RF-050 RF-054 e US-014 US-019 US-021 estabelecendo links explícitos entre níveis hierárquicos de requisitos.

**Estrutura de arquivos:**
- UCs: Narrativa longa (200-500 palavras) descrevendo fluxo completo
- RFs: Estrutura densa (1-3 parágrafos) com requisito específico
- USs: Formato BDD com cenários Gherkin (Given-When-Then)
- RNFs: Estrutura detalhada com métricas mensuráveis e critérios de aceitação

**Nomenclatura:**
- UC-XXX-nome-descritivo.md (11 principais + 62 FA/FE)
- RF-XXX-nome-descritivo.md (221 arquivos)
- US-XXX-nome-descritivo.md (140 arquivos)
- RNF-XXX-nome-descritivo.md (85 arquivos)

## Validação Automática

Script de validação de cobertura UC disponível em .scripts/validate-uc-coverage.py verificando que todos UCs com frontmatter modules estão linkados em PROJECTS/*/DOCS/FEATURES/*.md executado via comando python .scripts\validate-uc-coverage.py no diretório raiz do projeto retornando mensagem All UCs covered in PROJECTS/*/FEATURES/ quando validação passa confirmando rastreabilidade completa entre requirements e features implementadas.

---

**Última atualização:** 2026-01-10
