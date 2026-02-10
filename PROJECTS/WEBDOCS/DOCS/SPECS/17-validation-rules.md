---
type: leaf
status: review
updated: 2026-02-07
---

# Regras de Validacao

Regras automaticas de qualidade da documentacao WEBDOCS. Relacionado com 17-validation-scripts.md e 17-validation-ci.md.

## Validacao de Fonte

| ID | Severidade | Descricao |
|----|------------|-----------|
| SRC001 | ERROR | Source obrigatorio, exceto index e _ |
| SRC002 | ERROR | Arquivo referenciado deve existir |
| SRC003 | WARNING | Source compativel com secao (SPECS/16) |
| SRC004 | ERROR | Pattern CENTRAL/ ou PROJECTS/ .md |

## Cobertura

| ID | Severidade | Descricao |
|----|------------|-----------|
| COV001 | WARNING | Todo RF com pagina, exceto internals |
| COV002 | WARNING | Todo UC com manual, exceto tecnicos |
| COV003 | INFO | Todo workflow com guia |
| COV004 | WARNING | Toda feature com manual |

## Termos

| ID | Severidade | Correto | Incorreto |
|----|------------|---------|-----------|
| TERM001 | WARNING | Unidade Habitacional | Unit |
| TERM002 | WARNING | Em Rascunho | DRAFT |
| TERM003 | ERROR | Coordenador de Campo | field-coordinator |
| TERM004 | WARNING | GeoWeb, REURBCAD, GeoAPI | geoweb, Reurbcad |

## Conteudo

| ID | Severidade | Descricao |
|----|------------|-----------|
| CONT001 | ERROR | Description 50-160 chars |
| CONT002 | ERROR | Title obrigatorio |
| CONT003 | ERROR | Links internos validos |
| CONT004 | ERROR | Imagens existem |
| CONT005 | WARNING | Alt text em imagens |

## Execucao

ERROR bloqueia merge, WARNING reportado sem bloquear. Output JSON com rule_id, severity, file, line, message, suggestion. Ignorar regras via validate-ignore no frontmatter com IDs e justificativa.
