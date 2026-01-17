# Extensibilidade

## Criando um Validador Local

Validadores locais operam em cada documento individualmente.

### Passo 1: Criar arquivo

```python
# validators/local/my_validator.py
"""Meu validador customizado."""

from typing import List

from ..base import LocalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, Severity
from ...context.queries import ValidationContext
from ...scanner.tree import DocumentNode


@validator
class MyValidator(LocalValidator):
    """Descricao do validador."""

    name = "my_validator"
    description = "Descricao curta para --list-validators"

    def validate_document(
        self, doc: DocumentNode, context: ValidationContext
    ) -> List[ValidationIssue]:
        issues = []

        # Sua logica de validacao aqui
        if some_condition:
            issues.append(ValidationIssue(
                severity=Severity.WARNING,
                code="MYVAL001",
                message="Descricao do problema",
                file_path=doc.path,
                line_number=42,
                context="texto ao redor",
                suggestion="Como corrigir",
            ))

        return issues
```

### Passo 2: Importar no __init__.py

```python
# validators/local/__init__.py
from .my_validator import MyValidator

__all__ = [
    # ... outros validadores
    "MyValidator",
]
```

### Pronto!

O decorator `@validator` registra automaticamente. O validador aparecera em:

```bash
python -m carf_validator --list-validators
python -m carf_validator --only my_validator
```

## Criando um Validador Global

Validadores globais operam no grafo completo de documentos.

```python
# validators/global_/my_global_validator.py
"""Validador global customizado."""

from typing import List

from ..base import GlobalValidator
from ..registry import validator
from ...models.results import ValidationIssue, ValidatorResult, Severity
from ...context.queries import ValidationContext


@validator
class MyGlobalValidator(GlobalValidator):
    """Valida algo no grafo."""

    name = "my_global"
    description = "Valida relacoes entre documentos"

    def validate(self, context: ValidationContext) -> ValidatorResult:
        issues: List[ValidationIssue] = []

        # Acessa todos os documentos
        for doc in context.get_all_documents():
            # Acessa links de saida
            outgoing = context.get_links_from(doc.path)

            # Acessa documentos por tipo
            all_rfs = context.get_by_type(DocumentType.RF)

            # Verifica localizacao
            if context.is_in_central(doc):
                pass

        return ValidatorResult(
            validator_name=self.name,
            issues=issues,
            stats={
                "custom_metric": 42,
            }
        )
```

## API do ValidationContext

### Documentos

```python
context.get_document(path: Path) -> DocumentNode | None
context.get_by_identifier("RF-001") -> DocumentNode | None
context.get_by_type(DocumentType.RF) -> List[DocumentNode]
context.get_all_documents() -> List[DocumentNode]
context.count_documents() -> int
```

### Relacionamentos

```python
context.get_links_from(path) -> List[Relationship]
context.get_links_to(path) -> List[Relationship]
context.get_broken_links() -> List[Relationship]
context.get_orphans() -> Set[Path]
context.get_isolated() -> Set[Path]
```

### Localizacao

```python
context.is_in_central(doc) -> bool
context.is_in_projects(doc) -> bool
context.get_project_name(doc) -> str | None
```

## Estrutura do DocumentNode

```python
doc.path           # Path absoluto
doc.relative_path  # String relativa ao root
doc.doc_type       # DocumentType enum
doc.content        # Conteudo markdown bruto
doc.title          # Titulo H1 extraido
doc.identifier     # "RF-001", "UC-002", etc.
doc.frontmatter    # Frontmatter(modules, epic, raw)
doc.metadata       # Metadata(last_update, status, ...)
doc.links          # List[Link]
doc.metrics        # ContentMetrics(word_count, ...)
```

## Severidades

```python
Severity.ERROR    # Deve ser corrigido - falha validacao
Severity.WARNING  # Deveria ser corrigido
Severity.INFO     # Informacional
```

## Convencoes de Codigo

| Elemento | Convencao | Exemplo |
|----------|-----------|---------|
| Codigo de erro | PREFIXO + 3 digitos | MYVAL001, MYVAL002 |
| Nome do validador | snake_case | my_validator |
| Nome da classe | PascalCase + Validator | MyValidator |

---

**Ultima atualizacao:** 2026-01-15

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
