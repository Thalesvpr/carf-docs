# Regras de Validação - Documentação CARF

Documento define regras rígidas qualidade documentação CARF aplicadas validações automáticas garantindo consistência completude padrões estabelecidos todos tipos arquivos markdown.

## 1. READMEs (Índices e Navegação)

```yaml
type: README
min_words: 150
max_words: 500
required_sections:
  - "Descrição" # Parágrafo único denso
  - "Links estruturantes" # Bullets com [Nome](path)
required_metadata:
  - "Última atualização: YYYY-MM-DD"
max_links_per_paragraph: 5
title_pattern: "^# [A-Z]" # Título maiúscula
forbidden:
  - external_links: false # Apenas links internos preferidos
```

## 2. ADRs (Architecture Decision Records)

```yaml
type: ADR
min_words: 450
max_words: 700
structure: single_dense_paragraph # Parágrafo único
required_metadata:
  - "Data:"
  - "Status:"
  - "Decisor:"
  - "Última revisão:"
forbidden:
  - internal_links: true # ADRs auto-contidos
  - code_blocks: true # Apenas prosa
title_pattern: "^# ADR-\\d{3}:"
```

## 3. Use Cases

```yaml
type: USE_CASE
min_words: 400
max_words: 700
required_frontmatter:
  - modules: # array de strings
  - epic: # string
required_sections:
  - "Fluxos Alternativos" # Se aplicável
  - "Fluxos de Exceção" # Se aplicável
  - "Regras de Negócio"
  - "Rastreabilidade"
required_metadata:
  - "Última atualização: YYYY-MM-DD"
title_pattern: "^# UC-\\d{3}:"
required_references:
  - "RF-\\d{3}" # Pelo menos 1 RF
  - "US-\\d{3}" # Pelo menos 1 US
```

## 4. Functional Requirements

```yaml
type: FUNCTIONAL_REQUIREMENT
min_words: 100
max_words: 350
required_sections:
  - "Critérios de Aceitação"
  - "Relacionado a"
required_metadata:
  - "Última atualização: YYYY-MM-DD"
title_pattern: "^# RF-\\d{3}:"
required_references:
  - "UC-\\d{3}" # Pelo menos 1 UC
```

## 5. User Stories

```yaml
type: USER_STORY
min_words: 80
max_words: 250
structure: BDD_format
required_phrases:
  - "As a"
  - "I want"
  - "So that"
required_sections:
  - "Acceptance Criteria"
  - "Related"
title_pattern: "^# US-\\d{3}:"
```

## 6. Entities (Domain Model)

```yaml
type: ENTITY
min_words: 200
max_words: 500
structure: single_dense_paragraph
forbidden:
  - internal_links: true # Auto-contidas
required_mentions:
  - "Campos principais"
  - "Relacionamentos"
  - "Módulos"
title_pattern: "^# \\d{2}-" # Ex: 02-unit.md
filename_pattern: "^\\d{2}-[a-z-]+\\.md$"
```

## 7. FEATURES (Implementação)

```yaml
type: FEATURE
min_words: 500
max_words: 1000
required_sections:
  - "Validações" # Ou ## Validações
  - "API Integration" # Ou ## Integração API
  - "Relacionamentos" # Ou ## Domain Model
required_metadata:
  - "Última atualização: YYYY-MM-DD"
required_references:
  - "UC-\\d{3}" # Pelo menos 1 UC
  - "RF-\\d{3}" # Pelo menos 1 RF
forbidden:
  - code_blocks_in_central: true # PROJECTS pode ter exemplos
```

## 8. HOW-TOs (Guias Práticos)

```yaml
type: HOW_TO
min_words: 300
max_words: 900
required_sections:
  - "Pré-requisitos"
  - "Passos"
  - "Troubleshooting" # Opcional mas recomendado
  - "Referências"
title_pattern: "^# \\d{2}-"
filename_pattern: "^\\d{2}-[a-z-]+\\.md$"
code_blocks: allowed # Exemplos de comandos ok
```

## 9. CONCEPTS (Conceitos Técnicos)

```yaml
type: CONCEPT
min_words: 250
max_words: 550
required_sections:
  - "Como Funciona"
  - "Relacionado" # Opcional
code_blocks: allowed # Conceitos podem ter pseudocódigo
title_pattern: "^# \\d{2}-"
filename_pattern: "^\\d{2}-[a-z-]+\\.md$"
```

## 10. Business Rules

```yaml
type: BUSINESS_RULE
min_words: 300
max_words: 700
required_mentions:
  - "Algoritmo" # Se validação
  - "Referência legal" # Se aplicável
  - "Implementação"
subdirectories:
  - "VALIDATION-RULES"
  - "WORKFLOW-RULES"
  - "LEGITIMATION-RULES"
```

## 11. Architecture Patterns

```yaml
type: ARCHITECTURE
min_words: 400
max_words: 900
required_sections:
  - "Explicação"
  - "Implementação"
required_references:
  - "ADR-\\d{3}" # Pelo menos 1 ADR
code_blocks: allowed # Diagramas ASCII ok
```

## Regras Globais

```yaml
global:
  encoding: UTF-8
  line_endings: LF # Unix style
  max_line_length: 2000 # Parágrafos densos podem ser longos

  metadata:
    required_all:
      - "Última atualização: YYYY-MM-DD"
    date_format: "YYYY-MM-DD"
    min_date: "2024-01-01" # Não aceitar docs muito antigos

  nomenclature:
    - pattern: "REURB[^-SE]"
      correct: "REURB-S ou REURB-E"
    - pattern: "\\bPostgres\\b"
      correct: "PostgreSQL"
    - pattern: "\\bKeyCloak\\b"
      correct: "Keycloak"
    - pattern: "\\breact-native\\b"
      correct: "React Native"

  language:
    primary: "pt-BR"
    exceptions:
      - "ARCHITECTURE/ADRs/" # Podem ter inglês
      - "code_blocks" # Código em inglês ok
    forbidden_english_words:
      - "the"
      - "and"
      - "for"
      - "with"
      - "this"
      - "that"

  structure:
    central_isolation:
      - "CENTRAL → PROJECTS links forbidden"
      - "PROJECTS → CENTRAL links required"

    project_structure:
      required_dirs:
        - "ARCHITECTURE"
        - "CONCEPTS"
        - "HOW-TO"
        - "README.md"
      optional_dirs:
        - "FEATURES"
        - "LAYERS"
        - "REFERENCE"
      exceptions:
        WEBDOCS:
          - "No FEATURES" # Site documentação
        LIB:
          - "Has API" # Biblioteca tem API reference

  markers:
    forbidden:
      - "TODO"
      - "FIXME"
      - "XXX"
      - "[WIP]"
    allowed_in:
      - "CHANGELOG.md"
      - "ROADMAP.md"
```

## Stack Versions Esperadas

```yaml
stack_versions:
  GEOWEB:
    React: "18"
    Vite: "5"
    TanStack Query: "v5"
    TypeScript: "5"

  GEOAPI:
    .NET: "9"
    EF Core: "9"
    PostgreSQL: "16"
    PostGIS: "3"

  REURBCAD:
    React Native: "0.74"
    Expo: "51"
    WatermelonDB: "0.27"

  KEYCLOAK:
    Keycloak: "23"
    Java: "17"
    Quarkus: "3"

  GEOGIS:
    Python: "3.11"
    QGIS: "3.34"

  ADMIN:
    React: "18"
    Vite: "5"

  WEBDOCS:
    VitePress: "1"
    Vue: "3"
```

## Validações por Categoria

### Críticas (Bloqueantes)
- Links quebrados
- Diretórios sem README
- Estrutura projeto inválida
- Frontmatter faltando (UC, FEATURES)
- Tamanho < 50% mínimo
- Seções obrigatórias faltando

### Importantes (Warnings)
- TODOs/FIXMEs não resolvidos
- Tamanho < mínimo mas > 50% mínimo
- Metadados desatualizados (> 1 ano)
- Nomenclatura inconsistente
- Stack versions inconsistente
- Referências faltando (UC → RF, etc)

### Menores (Melhorias)
- Tamanho > máximo (mas < 2x máximo)
- Links excessivos por parágrafo
- Seções opcionais faltando
- Arquivos isolados (sem incoming/outgoing links)

## Exceções Conhecidas

```yaml
exceptions:
  size:
    - file: "REQUIREMENTS/index-by-module.md"
      reason: "Índice consolidado 387 requirements"
      max_words: 8000

  structure:
    - dir: "WEBDOCS/DOCS/"
      missing: "FEATURES"
      reason: "Site documentação não tem features"

  isolation:
    - pattern: "SRC-CODE/**"
      reason: "Código-fonte não é documentação"

  language:
    - pattern: "ARCHITECTURE/ADRs/**"
      english_allowed: true
      reason: "ADRs podem ser em inglês"
```

## Uso das Regras

Scripts validação devem:
1. Carregar VALIDATION-RULES.md
2. Detectar tipo arquivo via pattern matching
3. Aplicar regras específicas do tipo
4. Aplicar regras globais
5. Reportar violações com severidade
6. Sugerir correções quando possível

---

**Versão:** 1.0.0
**Última atualização:** 2026-01-12
**Manutenção:** Tech Lead / Arquiteto
