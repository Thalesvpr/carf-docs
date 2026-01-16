# CARF Validator

Sistema de validacao estrutural e semantica para o repositorio CARF. Consolida 16+ scripts de validacao em uma arquitetura modular e extensivel.

## Quickstart

```bash
# Navega para o diretorio de scripts
cd .scripts

# Executa validacao completa
python -m carf_validator --root /caminho/para/CARF

# Lista validadores disponiveis
python -m carf_validator --list-validators

# Executa apenas validadores especificos
python -m carf_validator --only broken_links title

# Gera relatorio markdown
python -m carf_validator --format markdown --output report.md
```

## Estrutura do Pacote

```
carf_validator/
├── __init__.py          # Pipeline principal (ValidationPipeline)
├── __main__.py          # CLI entry point
├── models/              # Modelos semanticos
│   ├── base.py          # DocumentType, Frontmatter, Metadata, Link
│   └── results.py       # ValidationIssue, ValidatorResult, ValidationReport
├── scanner/             # Varredura e parsing
│   ├── traversal.py     # FileScanner
│   ├── tree.py          # DocumentTreeBuilder, DocumentNode
│   └── parsers/         # Parsers de frontmatter, links, metadata
├── context/             # Contexto global
│   ├── registry.py      # DocumentRegistry (indices)
│   ├── graph.py         # RelationshipGraph (grafo de links)
│   └── queries.py       # ValidationContext (interface para validadores)
├── validators/          # Validadores modulares
│   ├── base.py          # LocalValidator, GlobalValidator
│   ├── registry.py      # @validator decorator
│   ├── local/           # 11 validadores por arquivo
│   └── global_/         # 6 validadores de grafo
├── reporters/           # Geradores de relatorio
│   ├── console.py       # Output terminal colorido
│   ├── markdown.py      # Relatorio .md
│   └── json.py          # Relatorio .json
└── docs/                # Esta documentacao
```

## Documentacao

- [Arquitetura](./01-architecture.md) - Pipeline e componentes
- [Validadores](./02-validators.md) - Lista completa de validadores
- [Uso do CLI](./03-cli-usage.md) - Opcoes de linha de comando
- [Extensibilidade](./04-extending.md) - Como criar novos validadores
- [Referencia de Regras](./05-rules-reference.md) - Regras por tipo de documento

## Resultados

O sistema gera relatorios com tres niveis de severidade:

| Severidade | Descricao |
|------------|-----------|
| ERROR | Deve ser corrigido - falha a validacao |
| WARNING | Deveria ser corrigido |
| INFO | Informacional |

Exit codes:
- `0` - Passou (sem erros)
- `1` - Falhou (tem erros)
- `2` - Erro de execucao

---

**Ultima atualizacao:** 2026-01-15

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
