# Arquitetura

## Pipeline

O sistema executa em 4 fases sequenciais:

```
scan -> modeling -> context -> validation -> report
```

### Fase 1: Scan

Varredura do filesystem para encontrar arquivos markdown.

```python
FileScanner(config) -> Iterator[Path]
```

Configuracoes:
- `include_patterns`: `["**/*.md"]`
- `exclude_dirs`: `.git`, `.obsidian`, `.scripts`, `node_modules`, etc.

### Fase 2: Modeling

Parsing de cada arquivo para construir modelo semantico.

```python
DocumentTreeBuilder.build() -> Dict[Path, DocumentNode]
```

Cada `DocumentNode` contem:
- `path`: Path absoluto
- `relative_path`: Path relativo ao root
- `doc_type`: Tipo detectado (RF, UC, README, etc.)
- `content`: Conteudo bruto
- `frontmatter`: YAML parseado (modules, epic)
- `metadata`: Footer parseado (ultima_atualizacao, status)
- `links`: Lista de links extraidos
- `metrics`: Contagem de palavras, paragrafos, etc.

### Fase 3: Context

Construcao de indices e grafo de relacionamentos.

```python
DocumentRegistry   # Indices por path, type, identifier
RelationshipGraph  # Grafo de links entre documentos
ValidationContext  # Interface unificada para validadores
```

O grafo detecta:
- Links quebrados (target nao existe)
- Orfaos (documentos sem links entrando)
- Isolados (documentos sem links saindo)

### Fase 4: Validation

Execucao de validadores em duas categorias:

**Locais** - Operam em cada documento individualmente:
```python
class LocalValidator:
    def validate_document(self, doc, context) -> List[ValidationIssue]
```

**Globais** - Operam no grafo completo:
```python
class GlobalValidator:
    def validate(self, context) -> ValidatorResult
```

### Fase 5: Report

Consolidacao e formatacao dos resultados.

```python
ValidationReport -> ConsoleReporter | MarkdownReporter | JsonReporter
```

## Diagrama de Componentes

```
                    ┌─────────────────────────────────────────────┐
                    │              ValidationPipeline             │
                    └─────────────────────────────────────────────┘
                                         │
         ┌───────────────────────────────┼───────────────────────────────┐
         ▼                               ▼                               ▼
┌─────────────────┐            ┌─────────────────┐            ┌─────────────────┐
│     Scanner     │            │     Context     │            │   Validators    │
├─────────────────┤            ├─────────────────┤            ├─────────────────┤
│ FileScanner     │            │ DocumentRegistry│            │ LocalValidator  │
│ DocumentTree    │──────────▶ │ RelationshipGraph│──────────▶ │ GlobalValidator │
│ Parsers         │            │ ValidationContext│            │ @validator      │
└─────────────────┘            └─────────────────┘            └─────────────────┘
         │                               │                               │
         │                               │                               │
         ▼                               ▼                               ▼
┌─────────────────┐            ┌─────────────────┐            ┌─────────────────┐
│     Models      │            │    Reporters    │            │    Results      │
├─────────────────┤            ├─────────────────┤            ├─────────────────┤
│ DocumentType    │            │ ConsoleReporter │            │ ValidationIssue │
│ Frontmatter     │            │ MarkdownReporter│            │ ValidatorResult │
│ Metadata        │            │ JsonReporter    │            │ ValidationReport│
│ Link            │            │                 │            │                 │
└─────────────────┘            └─────────────────┘            └─────────────────┘
```

## Fluxo de Dados

1. `FileScanner` varre filesystem e retorna paths
2. `DocumentTreeBuilder` parseia cada arquivo em `DocumentNode`
3. `DocumentRegistry` indexa documentos por path/type/identifier
4. `RelationshipGraph` constroi grafo de links
5. `ValidationContext` expoe interface para validadores
6. Validadores produzem `ValidationIssue` para cada problema
7. `ValidationReport` consolida resultados
8. Reporter formata saida (console/markdown/json)

---

**Ultima atualizacao:** 2026-01-15

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
