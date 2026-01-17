# EXCEPTIONS

Exceções específicas de domínio representando violações de regras de negócio e condições excepcionais, mapeadas para HTTP status codes apropriados pelo Gateway layer. DomainException (HTTP 400) serve como base para todas exceções de domínio indicando regra de negócio violada genérica. ValidationException (HTTP 400) representa dados inválidos com detalhes de validação por campo. NotFoundException (HTTP 404) indica entidade não encontrada por ID ou critério de busca. AccessDeniedException (HTTP 403) sinaliza falta de permissão para operação requisitada. ConflictException (HTTP 409) representa conflitos como CPF duplicado, código de comunidade já existente ou violação de constraint única. SyncConflictException (HTTP 409) indica conflito específico de sincronização offline quando BaseVersion do dispositivo mobile difere do RowVersion atual no servidor, permitindo resolução manual ou automática dependendo dos campos alterados.

## Arquivos

- **[00-domain-exception.md](./00-domain-exception.md)** - Exceção base domínio HTTP 400
- **[01-validation-exception.md](./01-validation-exception.md)** - Exceção validação dados inválidos
- **[02-not-found-exception.md](./02-not-found-exception.md)** - Exceção entidade não encontrada HTTP 404
- **[03-access-denied-exception.md](./03-access-denied-exception.md)** - Exceção acesso negado HTTP 403
- **[04-conflict-exception.md](./04-conflict-exception.md)** - Exceção conflito HTTP 409

---

**Última atualização:** 2026-01-12

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (5 arquivos)

| ID | Titulo |
|:---|:-------|
| [00-domain-exception](./00-domain-exception.md) | DomainException |
| [01-validation-exception](./01-validation-exception.md) | ValidationException |
| [02-not-found-exception](./02-not-found-exception.md) | NotFoundException |
| [03-access-denied-exception](./03-access-denied-exception.md) | AccessDeniedException |
| [04-conflict-exception](./04-conflict-exception.md) | ConflictException |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Pronto
