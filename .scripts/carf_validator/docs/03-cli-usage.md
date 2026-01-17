# Uso do CLI

## Sintaxe

```bash
python -m carf_validator [OPTIONS]
```

## Opcoes

| Opcao | Descricao |
|-------|-----------|
| `--root PATH` | Diretorio raiz do repositorio (default: diretorio atual) |
| `--format FORMAT` | Formato de saida: `console`, `markdown`, `json` (default: console) |
| `--output PATH` | Arquivo de saida (default: stdout) |
| `--only VALIDATORS` | Executar apenas estes validadores |
| `--disable VALIDATORS` | Desabilitar estes validadores |
| `--list-validators` | Lista validadores disponiveis |
| `--no-color` | Desabilita cores no output console |
| `--strict` | Exit code 1 se houver warnings |

## Exemplos

### Validacao Completa

```bash
cd .scripts
python -m carf_validator --root /c/DEV/CARF
```

### Listar Validadores

```bash
python -m carf_validator --list-validators
```

Saida:
```
Available validators:

Local validators (per-file):
  - content_bullets: Valida que bullets sao usados apenas em secoes estruturadas de footer
  - density: Valida densidade de paragrafos conforme arquitetura granular
  - file_size: Valida contagem minima e maxima de palavras por tipo de documento
  - frontmatter: Valida presenca e campos obrigatorios do frontmatter YAML
  - link_format: Valida formato de links internos
  - metadata: Valida presenca e atualidade do footer de metadata
  - nomenclature: Valida uso consistente de termos tecnicos
  - prose_continuity: Detecta quebras excessivas de prosa e paragrafos orfaos
  - readme_structure: Valida estrutura de README e proibe arquivos index
  - structure: Valida estrutura de secoes obrigatorias por tipo de documento
  - title: Valida formato do titulo H1 por tipo de documento

Global validators (graph-based):
  - broken_links: Detecta links para arquivos inexistentes
  - cross_refs: Valida que PROJECTS referencia CENTRAL (nao o inverso)
  - isolation: Valida que CENTRAL (fonte de verdade) nao depende de PROJECTS
  - orphans: Detecta arquivos sem referencias (orfaos)
  - rf_coverage: Verifica que Requisitos Funcionais sao implementados em Features
  - uc_coverage: Verifica que Use Cases sao implementados nos modulos declarados
```

### Executar Validadores Especificos

```bash
# Apenas links quebrados
python -m carf_validator --only broken_links

# Apenas validadores de titulo e estrutura
python -m carf_validator --only title structure readme_structure

# Todos exceto orphans
python -m carf_validator --disable orphans
```

### Gerar Relatorios

```bash
# Relatorio Markdown
python -m carf_validator --format markdown --output report.md

# Relatorio JSON
python -m carf_validator --format json --output report.json

# Console sem cores (para CI)
python -m carf_validator --no-color
```

### Modo Strict

```bash
# Falha se houver warnings (para CI rigoroso)
python -m carf_validator --strict
```

## Formatos de Saida

### Console

Output colorido com resumo e issues agrupados por validador.

```
============================================================
CARF Validation Report
============================================================

Summary
  Files scanned: 1161
  Errors: 570
  Warnings: 1431
  Info: 359

[broken_links]
  total_broken: 1
  X [BLINK001] /path/to/file.md:204 Link quebrado: ../../DOCS/
       Link text: 'Component Guide'
       -> Verifique se o arquivo existe

[FAIL] Validation FAILED

Errors: 570
Warnings: 1431
```

### Markdown

Relatorio formatado com tabelas e secoes colapsaveis.

### JSON

Dados estruturados para integracao com CI/CD:

```json
{
  "metadata": {
    "generated_at": "2026-01-15T15:29:56",
    "validator_version": "1.0.0"
  },
  "summary": {
    "files_scanned": 1161,
    "total_issues": 2360,
    "errors": 570,
    "warnings": 1431,
    "info": 359,
    "passed": false
  },
  "validators": [...],
  "issues_by_file": {...}
}
```

## Exit Codes

| Codigo | Significado |
|--------|-------------|
| 0 | Passou (sem erros) |
| 1 | Falhou (tem erros, ou warnings com --strict) |
| 2 | Erro de execucao |

---

**Ultima atualizacao:** 2026-01-15

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
