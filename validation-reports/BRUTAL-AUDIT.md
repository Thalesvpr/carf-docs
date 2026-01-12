# Auditoria Brutal Completa - CARF Documentation

**Data:** 2026-01-12 11:11:46
**Versão:** docs/complete-documentation-structure@63857d30
**Total Validações:** 16

## Resumo Executivo

| Validação | Status | Erros | Warnings |
|-----------|--------|-------|----------|
| Dense Paragraph | [OK] PASS | 0 | 215 |
| Isolated Files | [OK] PASS | 0 | 0 |
| Broken Links | [OK] PASS | 0 | 0 |
| Central Isolation | [FAIL] FAIL | 0 | 0 |
| UC Coverage | [FAIL] FAIL | 0 | 0 |
| Structure | [OK] PASS | 0 | 0 |
| RF Coverage | [FAIL] FAIL | 190 | 0 |
| Nomenclature | [FAIL] FAIL | 3 | 0 |
| Stack Versions | [FAIL] FAIL | 14 | 0 |
| Cross References | [FAIL] FAIL | 0 | 0 |
| Features vs Code | [OK] PASS | 0 | 0 |
| Feature Sections | [FAIL] FAIL | 61 | 0 |
| Language | [FAIL] FAIL | 292 | 0 |
| Metadata | [FAIL] FAIL | 630 | 0 |
| File Size | [FAIL] FAIL | 162 | 193 |
| File Structure | [FAIL] FAIL | 2001 | 0 |

**Resultado Final:** [FAIL] FAILED (5 passed, 11 failed)

**Total Erros:** 3353
**Total Warnings:** 408

## Detalhes por Validação

### Dense Paragraph

**Status:** [OK] PASSED

- Erros: 0
- Warnings: 215

<details>
<summary>Ver detalhes (output truncado)</summary>

```
Running CARF documentation linter...
================================================================================

[1/3] Checking CENTRAL/ for code blocks...
  [OK] No code blocks found in CENTRAL/

[2/3] Checking PROJECTS/*/DOCS/FEATURES/ word count...
  [OK] All FEATURES files have adequate content

[3/4] Checking for excessive line breaks (non-dense)...
  [OK] No excessive line breaks found

[4/4] Checking README files for excessive links...
  [WARN] Found 215 paragraphs with > 5 links

================================================================================
Errors: 0
Warnings: 215

[WARNINGS]:
  CENTRAL\README.md:para4 - 12 links (max 5 recommended)
  PROJECTS\README.md:para4 - 7 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\acorn\README.md:para67 - 7 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\address\README.md:para25 - 8 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\ajv\README.md:para4 - 7 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\ajv\README.md:para36 - 33 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\ajv\README.md:para44 - 17 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\ajv\README.md:para79 - 11 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\ajv\README.md:para91 - 8 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\ajv\README.md:para330 - 8 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\ajv\README.md:para340 - 8 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\ajv\README.md:para358 - 10 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\ajv\README.md:para360 - 25 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\ast-types\README.md:para87 - 12 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\baseline-browser-mapping\README.md:para97 - 12 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\body-parser\README.md:para8 - 6 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\braces\README.md:para11 - 9 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\braces\README.md:para181 - 6 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\browser-assert\README.md:para2 - 12 links (max 5 recommended)
  PROJECTS\LIB\TS\UI-COMPONENTS\SRC-CODE\carf-ui\node_modules\chalk\README.md:para3 - 8 links (max 5 recommended)
... (198 linhas omitidas)
```
</details>

### Isolated Files

**Status:** [OK] PASSED

<details>
<summary>Ver detalhes (output truncado)</summary>

```
Found 18 completely isolated files:


## ADMIN (1 files)
--------------------------------------------------------------------------------
PROJECTS\ADMIN\SRC-CODE\carf-admin\README.md

## GEOAPI (1 files)
--------------------------------------------------------------------------------
PROJECTS\GEOAPI\SRC-CODE\carf-geoapi\README.md

## GEOGIS (1 files)
--------------------------------------------------------------------------------
PROJECTS\GEOGIS\SRC-CODE\carf-geogis\README.md

## GEOWEB (1 files)
--------------------------------------------------------------------------------
PROJECTS\GEOWEB\SRC-CODE\carf-geoweb\README.md

## LIB (2 files)
--------------------------------------------------------------------------------
PROJECTS\LIB\TS\TSCORE\SRC-CODE\carf-tscore\CHANGELOG.md
PROJECTS\LIB\TS\TSCORE\SRC-CODE\carf-tscore\README.md

## OTHER (9 files)
--------------------------------------------------------------------------------
AUDIT-PLAN.md
PROJECTS\KEYCLOAK\SRC-CODE\carf-keycloak\BUILD.md
PROJECTS\KEYCLOAK\SRC-CODE\carf-keycloak\CHANGELOG.md
PROJECTS\KEYCLOAK\SRC-CODE\carf-keycloak\README.md
PROJECTS\KEYCLOAK\SRC-CODE\carf-keycloak\tests\README.md
PROJECTS\KEYCLOAK\SRC-CODE\carf-keycloak\themes\carf\login\resources\img\README.md
PROJECTS\KEYCLOAK\SRC-CODE\carf-keycloak\themes\carf\login\resources\js\README.md
validation-reports\BRUTAL-AUDIT.md
validation-reports\SNAPSHOT-2026-01-12.md

## REURBCAD (1 files)
--------------------------------------------------------------------------------
PROJECTS\REURBCAD\SRC-CODE\carf-reurbcad\README.md

... (8 linhas omitidas)
```
</details>

### Broken Links

**Status:** [OK] PASSED

<details>
<summary>Ver detalhes (output truncado)</summary>

```
================================================================================
VERIFICADOR DE LINKS MARKDOWN - VERSAO MELHORADA
================================================================================
Raiz: C:\DEV\CARF

[*] Encontrados 975 arquivos .md

================================================================================
RESULTADOS
================================================================================
Arquivos .md encontrados: 975
Arquivos com links: 162
Links internos verificados: 2164
Links quebrados: 3
Arquivos com problemas: 2

================================================================================
DETALHES DOS LINKS QUEBRADOS
================================================================================

[ARQUIVO] VALIDATION-PLAN.md
          2 link(s) quebrado(s)

  [X] Texto: texto
      Link: caminho
      Resolve para: caminho
      Motivo: arquivo nao existe

  [X] Texto: .*\
      Link: \..*\.md
      Resolve para: ..\..\..*\.md
      Motivo: arquivo nao existe

--------------------------------------------------------------------------------

[ARQUIVO] VALIDATION-RULES.md
          1 link(s) quebrado(s)

  [X] Texto: Nome
      Link: path
... (76 linhas omitidas)
```
</details>

### Central Isolation

**Status:** [FAIL] FAILED

<details>
<summary>Ver detalhes</summary>

```
================================================================================
LINT: Central Isolation Validation
================================================================================

[1/4] Checking markdown links CENTRAL -> PROJECTS...
  [OK] No markdown links to PROJECTS/

[2/4] Checking code blocks with PROJECTS/ paths...
  [OK] No code blocks with PROJECTS/ paths

[3/4] Checking PROJECTS/*/DOCS/OVERVIEW.md exists...
  [ERROR] Missing 5 OVERVIEW.md file(s)
    - PROJECTS\GEOAPI\DOCS\OVERVIEW.md
    - PROJECTS\GEOWEB\DOCS\OVERVIEW.md
    - PROJECTS\REURBCAD\DOCS\OVERVIEW.md
    - PROJECTS\GEOGIS\DOCS\OVERVIEW.md
    - PROJECTS\ADMIN\DOCS\OVERVIEW.md

[4/4] Checking FEATURES link to CENTRAL/REQUIREMENTS...
  [WARNING] Found 21 feature(s) without CENTRAL links
    - PROJECTS\ADMIN\DOCS\FEATURES\team-management.md
    - PROJECTS\ADMIN\DOCS\FEATURES\user-management.md
    - PROJECTS\GEOGIS\DOCS\FEATURES\gis-integration.md
    - PROJECTS\GEOGIS\DOCS\FEATURES\shapefile-import.md
    - PROJECTS\GEOWEB\DOCS\FEATURES\gis-integration.md
    ... and 16 more

================================================================================
SUMMARY
================================================================================
  Errors: 5
  Warnings: 21

[FAIL] Validation failed with errors

```
</details>

### UC Coverage

**Status:** [FAIL] FAILED

<details>
<summary>Ver detalhes (output truncado)</summary>

```

============================================================
UC COVERAGE VALIDATION
============================================================

Total UCs analyzed: 11
UCs covered: 0
Orphan UCs: 11

ORPHAN UCs (not linked in PROJECTS/*/FEATURES/):

  - UC-001-cadastrar-unidade-habitacional.md
    Expected in modules: GEOWEB, REURBCAD

  - UC-002-aprovar-unidade-habitacional.md
    Expected in modules: GEOWEB, REURBCAD

  - UC-003-vincular-titular-unidade.md
    Expected in modules: GEOAPI, GEOWEB, REURBCAD

  - UC-004-coletar-dados-campo-mobile.md
    Expected in modules: GEOWEB, REURBCAD

  - UC-005-sincronizar-dados-offline.md
    Expected in modules: GEOAPI, GEOWEB, REURBCAD

  - UC-006-gerar-relatorio-comunidade.md
    Expected in modules: GEOWEB

  - UC-007-exportar-dados-geograficos.md
    Expected in modules: GEOWEB, REURBCAD, GEOGIS

  - UC-008-importar-shapefile.md
    Expected in modules: GEOWEB, REURBCAD, GEOGIS

  - UC-009-gerenciar-processo-legitimacao.md
    Expected in modules: GEOWEB

  - UC-010-configurar-camadas-wms.md
    Expected in modules: GEOAPI, GEOWEB, REURBCAD
... (8 linhas omitidas)
```
</details>

### Structure

**Status:** [OK] PASSED

<details>
<summary>Ver detalhes</summary>

```
================================================================================
[VALIDATION] Project Structure
================================================================================

[[OK]] All project structures are valid
================================================================================
Errors: 0
Warnings: 0
================================================================================

```
</details>

### RF Coverage

**Status:** [FAIL] FAILED

- Erros: 190
- Warnings: 0

<details>
<summary>Ver detalhes</summary>

```
================================================================================
[VALIDATION] RF Coverage
================================================================================

[*] Found 221 Functional Requirements (RF-001 to RF-221)

Total RFs: 221
Covered: 31
Orphans: 190

[ERRORS] 190 orphan RFs (not implemented):
  [X] RF-004 not implemented in any FEATURES
  [X] RF-010 not implemented in any FEATURES
  [X] RF-011 not implemented in any FEATURES
  [X] RF-016 not implemented in any FEATURES
  [X] RF-017 not implemented in any FEATURES
  [X] RF-025 not implemented in any FEATURES
  [X] RF-027 not implemented in any FEATURES
  [X] RF-028 not implemented in any FEATURES
  [X] RF-029 not implemented in any FEATURES
  [X] RF-030 not implemented in any FEATURES
  ... and 180 more

================================================================================
Errors: 190
Warnings: 0
================================================================================

```
</details>

### Nomenclature

**Status:** [FAIL] FAILED

- Erros: 3
- Warnings: 0

<details>
<summary>Ver detalhes (output truncado)</summary>

```
================================================================================
[VALIDATION] Nomenclature
================================================================================

[*] Validating nomenclature in 907 files...

[ERRORS] 765 nomenclature violations:
  [X] 724 violations of: REURB deve ser qualificado como REURB-S ou REURB-E
  [X] 2 violations of: Use 'PostgreSQL' ao invés de 'Postgres'
  [X] 39 violations of: Use 'React Native' ao invés de 'react-native' em prosa

  Rule: REURB deve ser qualificado como REURB-S ou REURB-E
  Correct: REURB-S (social) ou REURB-E (econômico)
    • CENTRAL/README.md:3
      Found: 'REURBC'
    • CENTRAL/ARCHITECTURE/README.md:3
      Found: 'REURBC'
    • CENTRAL/LIBRARIES/README.md:5
      Found: 'REURBC'
    ... and 721 more

  Rule: Use 'PostgreSQL' ao invés de 'Postgres'
  Correct: PostgreSQL
    • CENTRAL/ARCHITECTURE/DEPLOYMENT/04-cicd-pipeline.md:3
      Found: 'Postgres'
    • PROJECTS/KEYCLOAK/DOCS/HOW-TO/README.md:14
      Found: 'Postgres'

  Rule: Use 'React Native' ao invés de 'react-native' em prosa
  Correct: React Native
    • CENTRAL/REQUIREMENTS/USE-CASES/UC-004-coletar-dados-campo-mobile.md:8
      Found: 'react-native'
    • CENTRAL/REQUIREMENTS/USE-CASES/UC-004-coletar-dados-campo-mobile.md:8
      Found: 'react-native'
    • CENTRAL/REQUIREMENTS/USE-CASES/UC-004-FA-001-sincronizar-imediato.md:14
      Found: 'react-native'
    ... and 36 more

================================================================================
Errors: 3
... (3 linhas omitidas)
```
</details>

### Stack Versions

**Status:** [FAIL] FAILED

- Erros: 14
- Warnings: 0

<details>
<summary>Ver detalhes</summary>

```
================================================================================
[VALIDATION] Stack Versions
================================================================================

[ERRORS] 14 version inconsistencies:
  [X] GEOWEB: React version mismatch in PROJECTS/GEOWEB/DOCS/FEATURES/README.md - found '18.3', expected 18
  [X] GEOWEB: Vite version mismatch in PROJECTS/GEOWEB/DOCS/FEATURES/README.md - found '5.0', expected 5
  [X] GEOWEB: TypeScript version mismatch in PROJECTS/GEOWEB/DOCS/FEATURES/README.md - found '5.3', expected 5
  [X] GEOAPI: PostGIS version mismatch in PROJECTS/GEOAPI/DOCS/ARCHITECTURE/01-overview.md - found '3.4', expected 3
  [X] GEOAPI: PostGIS version mismatch in PROJECTS/GEOAPI/DOCS/ARCHITECTURE/01-overview.md - found '3.4', expected 3
  [X] GEOAPI: PostGIS version mismatch in PROJECTS/GEOAPI/DOCS/ARCHITECTURE/04-integration.md - found '3.4', expected 3
  [X] GEOAPI: PostGIS version mismatch in PROJECTS/GEOAPI/DOCS/ARCHITECTURE/README.md - found '3.4', expected 3
  [X] KEYCLOAK: Keycloak version mismatch in PROJECTS/KEYCLOAK/DOCS/README.md - found '24.0', expected 23
  [X] KEYCLOAK: Keycloak version mismatch in PROJECTS/KEYCLOAK/DOCS/ARCHITECTURE/02-theme-architecture.md - found '2', expected 23
  [X] KEYCLOAK: Keycloak version mismatch in PROJECTS/KEYCLOAK/DOCS/CONCEPTS/01-keycloak-themes.md - found '3', expected 23
  [X] KEYCLOAK: Keycloak version mismatch in PROJECTS/KEYCLOAK/DOCS/FEATURES/README.md - found '23.0', expected 23
  [X] GEOGIS: Python version mismatch in PROJECTS/GEOGIS/DOCS/README.md - found '3.9', expected 3.11
  [X] GEOGIS: Python version mismatch in PROJECTS/GEOGIS/DOCS/ARCHITECTURE/README.md - found '3', expected 3.11
  [X] GEOGIS: QGIS version mismatch in PROJECTS/GEOGIS/DOCS/README.md - found '3.28', expected 3.34

================================================================================
Errors: 14
Warnings: 0
================================================================================

```
</details>

### Cross References

**Status:** [FAIL] FAILED

<details>
<summary>Ver detalhes</summary>

```
================================================================================
[VALIDATION] Cross References
================================================================================


```
</details>

### Features vs Code

**Status:** [OK] PASSED

<details>
<summary>Ver detalhes</summary>

```
================================================================================
[VALIDATION] Features vs Code (Heuristic)
================================================================================

[NOTE] This is a heuristic validation based on common patterns.
[NOTE] False positives/negatives are expected.

[[OK]] Features and code appear aligned (heuristic)
================================================================================
Errors: 0
Warnings: 0
================================================================================

```
</details>

### Feature Sections

**Status:** [FAIL] FAILED

- Erros: 61
- Warnings: 0

<details>
<summary>Ver detalhes</summary>

```
================================================================================
[VALIDATION] Feature Sections
================================================================================

[*] Validating 21 feature files...

Total features: 21
Features with missing sections: 21
Total missing sections: 61

[ERRORS] 61 missing sections:
  [X] PROJECTS/ADMIN/DOCS/FEATURES/team-management.md missing required section: ## Validações
  [X] PROJECTS/ADMIN/DOCS/FEATURES/team-management.md missing required section: ## API Integration ou ## Integração API
  [X] PROJECTS/ADMIN/DOCS/FEATURES/team-management.md missing required section: ## Relacionamentos ou ## Domain Model
  [X] PROJECTS/ADMIN/DOCS/FEATURES/user-management.md missing required section: ## Validações
  [X] PROJECTS/ADMIN/DOCS/FEATURES/user-management.md missing required section: ## API Integration ou ## Integração API
  [X] PROJECTS/ADMIN/DOCS/FEATURES/user-management.md missing required section: ## Relacionamentos ou ## Domain Model
  [X] PROJECTS/GEOGIS/DOCS/FEATURES/gis-integration.md missing required section: ## Validações
  [X] PROJECTS/GEOGIS/DOCS/FEATURES/gis-integration.md missing required section: ## API Integration ou ## Integração API
  [X] PROJECTS/GEOGIS/DOCS/FEATURES/gis-integration.md missing required section: ## Relacionamentos ou ## Domain Model
  [X] PROJECTS/GEOGIS/DOCS/FEATURES/shapefile-import.md missing required section: ## Validações
  [X] PROJECTS/GEOGIS/DOCS/FEATURES/shapefile-import.md missing required section: ## API Integration ou ## Integração API
  [X] PROJECTS/GEOGIS/DOCS/FEATURES/shapefile-import.md missing required section: ## Relacionamentos ou ## Domain Model
  [X] PROJECTS/GEOWEB/DOCS/FEATURES/gis-integration.md missing required section: ## Validações
  [X] PROJECTS/GEOWEB/DOCS/FEATURES/holder-management.md missing required section: ## Validações
  [X] PROJECTS/GEOWEB/DOCS/FEATURES/holder-management.md missing required section: ## API Integration ou ## Integração API
  ... and 46 more

================================================================================
Errors: 61
Warnings: 0
================================================================================

```
</details>

### Language

**Status:** [FAIL] FAILED

- Erros: 292
- Warnings: 0

<details>
<summary>Ver detalhes</summary>

```
================================================================================
[VALIDATION] Language (Portuguese)
================================================================================

[NOTE] Ignoring ADRs, code blocks, technical terms

[*] Validating language in 885 files...

[ERRORS] 533 English word occurrences in 292 files:
  [X] CENTRAL/REQUIREMENTS/README.md contains English words: WHO, that, WHAT, WHY
  [X] CENTRAL/VERSIONING/02-github-decision.md contains English words: when
  [X] CENTRAL/WORKFLOWS/01-wms-integration-workflow.md contains English words: from
  [X] CENTRAL/VERSIONING/GIT/00-setup-guide.md contains English words: and, have, not
  [X] CENTRAL/VERSIONING/GIT/04-pr-guidelines.md contains English words: what, why
  [X] CENTRAL/VERSIONING/GIT/07-worktree-guide.md contains English words: which
  [X] CENTRAL/TESTING/TEST-STRATEGY/coverage-targets.md contains English words: not, and, are, when, being, why, The
  [X] CENTRAL/TESTING/TEST-STRATEGY/test-pyramid.md contains English words: being
  [X] CENTRAL/TESTING/TEST-CASES/API/README.md contains English words: not
  [X] CENTRAL/SECURITY/POLICIES/01-authentication-policy.md contains English words: for
  ... and 282 more files

Examples:
  • CENTRAL/REQUIREMENTS/README.md
    Word: 'that'
    Context: ...o BDD As a WHO I want WHAT So that WHY estabelecendo perspectiva...
  • CENTRAL/REQUIREMENTS/README.md
    Word: 'WHAT'
    Context: ...s formato BDD As a WHO I want WHAT So that WHY estabelecendo per...
  • CENTRAL/REQUIREMENTS/README.md
    Word: 'WHO'
    Context: ...user stories formato BDD As a WHO I want WHAT So that WHY estab...
  ... and 530 more

================================================================================
Errors: 292
Warnings: 0
================================================================================

```
</details>

### Metadata

**Status:** [FAIL] FAILED

- Erros: 630
- Warnings: 0

<details>
<summary>Ver detalhes</summary>

```
================================================================================
[VALIDATION] Metadata
================================================================================

[*] Validating metadata in 631 important files...

Total files checked: 631
Missing metadata: 630
Outdated metadata (>12 months): 0

[ERRORS] 630 files missing metadata:
  [X] PROJECTS/WEBDOCS/DOCS/ARCHITECTURE/README.md missing 'Última atualização: YYYY-MM-DD'
  [X] CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/RF-079-mesclar-unidades.md missing 'Última atualização: YYYY-MM-DD'
  [X] PROJECTS/GEOGIS/DOCS/FEATURES/shapefile-import.md missing 'Última atualização: YYYY-MM-DD'
  [X] CENTRAL/ARCHITECTURE/ADRs/ADR-020-docker-kubernetes-orchestration.md missing 'Última atualização: YYYY-MM-DD'
  [X] CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/RF-185-editar-unidade-offline.md missing 'Última atualização: YYYY-MM-DD'
  [X] CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/RF-221-proxy-de-wmswmts.md missing 'Última atualização: YYYY-MM-DD'
  [X] CENTRAL/REQUIREMENTS/NON-FUNCTIONAL-REQUIREMENTS/RNF-059-versionamento-semantico.md missing 'Última atualização: YYYY-MM-DD'
  [X] CENTRAL/REQUIREMENTS/NON-FUNCTIONAL-REQUIREMENTS/RNF-078-job-queue.md missing 'Última atualização: YYYY-MM-DD'
  [X] CENTRAL/ARCHITECTURE/PATTERNS/04-domain-events.md missing 'Última atualização: YYYY-MM-DD'
  [X] CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/RF-061-vincular-titular-a-unidade.md missing 'Última atualização: YYYY-MM-DD'
  [X] CENTRAL/REQUIREMENTS/USER-STORIES/US-139-vincular-titular-a-unidade.md missing 'Última atualização: YYYY-MM-DD'
  [X] CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/RF-022-editar-usuário.md missing 'Última atualização: YYYY-MM-DD'
  [X] CENTRAL/REQUIREMENTS/USER-STORIES/US-047-copiar-dados-da-última-unidade.md missing 'Última atualização: YYYY-MM-DD'
  [X] CENTRAL/REQUIREMENTS/USER-STORIES/US-083-gerenciar-usuários-do-tenant.md missing 'Última atualização: YYYY-MM-DD'
  [X] CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/RF-186-tirar-fotos-offline.md missing 'Última atualização: YYYY-MM-DD'
  ... and 615 more

================================================================================
Errors: 630
Warnings: 0
================================================================================

```
</details>

### File Size

**Status:** [FAIL] FAILED

- Erros: 162
- Warnings: 193

<details>
<summary>Ver detalhes (output truncado)</summary>

```
================================================================================
[VALIDATION] File Size
================================================================================

[*] Validating file sizes in 907 files...

Total files checked: 717
Too small: 162
Too large: 193

[ERRORS] 162 files below minimum:
  [X] CENTRAL/INTEGRATION/README.md (README) too small: 69w < 150w (missing 81w)
  [X] CENTRAL/TESTING/README.md (README) too small: 144w < 150w (missing 6w)
  [X] CENTRAL/TESTING/TEST-CASES/README.md (README) too small: 116w < 150w (missing 34w)
  [X] CENTRAL/TESTING/TEST-STRATEGY/README.md (README) too small: 121w < 150w (missing 29w)
  [X] CENTRAL/TESTING/TEST-CASES/API/README.md (README) too small: 122w < 150w (missing 28w)
  [X] CENTRAL/TESTING/TEST-CASES/E2E/README.md (README) too small: 102w < 150w (missing 48w)
  [X] CENTRAL/TESTING/TEST-CASES/UNIT/README.md (README) too small: 81w < 150w (missing 69w)
  [X] CENTRAL/REQUIREMENTS/USE-CASES/UC-001-FA-001-desenhar-geometria-offline.md (UC) too small: 330w < 400w (missing 70w)
  [X] CENTRAL/REQUIREMENTS/USE-CASES/UC-001-FA-002-importar-geometria-gps.md (UC) too small: 363w < 400w (missing 37w)
  [X] CENTRAL/REQUIREMENTS/USE-CASES/UC-003-FE-001-cpf-invalido.md (UC) too small: 380w < 400w (missing 20w)
  [X] CENTRAL/REQUIREMENTS/USE-CASES/UC-003-FE-002-titular-duplicado.md (UC) too small: 337w < 400w (missing 63w)
  [X] CENTRAL/REQUIREMENTS/USE-CASES/UC-004-FA-001-sincronizar-imediato.md (UC) too small: 226w < 400w (missing 174w)
  [X] CENTRAL/REQUIREMENTS/USE-CASES/UC-004-FA-002-voice-to-text.md (UC) too small: 282w < 400w (missing 118w)
  [X] CENTRAL/REQUIREMENTS/USE-CASES/UC-004-FA-003-copiar-anterior.md (UC) too small: 267w < 400w (missing 133w)
  [X] CENTRAL/REQUIREMENTS/USE-CASES/UC-004-FE-001-gps-indisponivel.md (UC) too small: 368w < 400w (missing 32w)
  ... and 147 more

[WARNINGS] 193 files above maximum:
  [WARN] CENTRAL/LIBRARIES/README.md (README) too large: 652w > 500w (exceeds by 152w)
  [WARN] CENTRAL/REQUIREMENTS/README.md (README) too large: 510w > 500w (exceeds by 10w)
  [WARN] CENTRAL/REQUIREMENTS/USE-CASES/UC-002-FE-002-solicitar-alteracoes.md (UC) too large: 836w > 700w (exceeds by 136w)
  [WARN] CENTRAL/REQUIREMENTS/USE-CASES/UC-003-FA-001-importar-planilha.md (UC) too large: 973w > 700w (exceeds by 273w)
  [WARN] CENTRAL/REQUIREMENTS/USE-CASES/UC-003-vincular-titular-unidade.md (UC) too large: 720w > 700w (exceeds by 20w)
  [WARN] CENTRAL/REQUIREMENTS/USE-CASES/UC-004-coletar-dados-campo-mobile.md (UC) too large: 844w > 700w (exceeds by 144w)
  [WARN] CENTRAL/REQUIREMENTS/USE-CASES/UC-005-sincronizar-dados-offline.md (UC) too large: 824w > 700w (exceeds by 124w)
  [WARN] CENTRAL/REQUIREMENTS/USE-CASES/UC-007-exportar-dados-geograficos.md (UC) too large: 876w > 700w (exceeds by 176w)
  [WARN] CENTRAL/REQUIREMENTS/USE-CASES/UC-008-importar-shapefile.md (UC) too large: 1019w > 700w (exceeds by 319w)
  [WARN] CENTRAL/REQUIREMENTS/USE-CASES/UC-009-gerenciar-processo-legitimacao.md (UC) too large: 1051w > 700w (exceeds by 351w)
  ... and 183 more
... (6 linhas omitidas)
```
</details>

### File Structure

**Status:** [FAIL] FAILED

- Erros: 2001
- Warnings: 0

<details>
<summary>Ver detalhes</summary>

```
================================================================================
[VALIDATION] File Structure
================================================================================

[*] Validating file structure in 907 files...

Total files checked: 632
Total violations: 2001

[ERRORS] 2001 structure violations:
  [X] CENTRAL/README.md (section): Missing section: ##?\s+Descrição
  [X] CENTRAL/README.md (section): Missing section: ##?\s+Links
  [X] CENTRAL/API/README.md (section): Missing section: ##?\s+Descrição
  [X] CENTRAL/API/README.md (section): Missing section: ##?\s+Links
  [X] CENTRAL/ARCHITECTURE/README.md (section): Missing section: ##?\s+Descrição
  [X] CENTRAL/ARCHITECTURE/README.md (section): Missing section: ##?\s+Links
  [X] CENTRAL/BUSINESS-RULES/README.md (section): Missing section: ##?\s+Descrição
  [X] CENTRAL/BUSINESS-RULES/README.md (section): Missing section: ##?\s+Links
  [X] CENTRAL/DOMAIN-MODEL/README.md (section): Missing section: ##?\s+Descrição
  [X] CENTRAL/DOMAIN-MODEL/README.md (section): Missing section: ##?\s+Links
  [X] CENTRAL/INTEGRATION/README.md (section): Missing section: ##?\s+Descrição
  [X] CENTRAL/INTEGRATION/README.md (section): Missing section: ##?\s+Links
  [X] CENTRAL/LIBRARIES/README.md (section): Missing section: ##?\s+Descrição
  [X] CENTRAL/LIBRARIES/README.md (section): Missing section: ##?\s+Links
  [X] CENTRAL/OPERATIONS/README.md (section): Missing section: ##?\s+Descrição
  [X] CENTRAL/OPERATIONS/README.md (section): Missing section: ##?\s+Links
  [X] CENTRAL/REQUIREMENTS/README.md (section): Missing section: ##?\s+Descrição
  [X] CENTRAL/REQUIREMENTS/README.md (section): Missing section: ##?\s+Links
  [X] CENTRAL/SECURITY/README.md (section): Missing section: ##?\s+Descrição
  [X] CENTRAL/SECURITY/README.md (section): Missing section: ##?\s+Links
  ... and 1981 more

================================================================================
Errors: 2001
Warnings: 0
================================================================================

```
</details>

## Recomendações

### Imediato (Esta Semana)
1. Revisar e corrigir erros críticos (validações FAILED)
2. Analisar warnings de alta prioridade
3. Documentar decisões sobre exceções aceitáveis

### Curto Prazo (Este Mês)
1. Resolver warnings restantes
2. Completar diretórios incompletos identificados
3. Atualizar metadados desatualizados

### Médio Prazo (Quarter)
1. Estabelecer validação automática em CI/CD
2. Criar dashboard de qualidade documentação
3. Revisar e atualizar VALIDATION-RULES.md

---
**Próxima Auditoria:** 2026-01-** (monthly)
