# APPLICATION

Camada de aplicação do GEOAPI orquestrando use cases e coordenando fluxo entre domain e apresentação, implementando padrão CQRS separando commands para escritas e queries para leituras otimizadas. COMMANDS agrupa operações que alteram estado do sistema (CreateUnitCommand, UpdateHolderCommand) validadas via FluentValidation antes de execução, retornando Result<T> para tratamento explícito de sucesso/erro sem exceptions. QUERIES contém operações apenas-leitura projetando dados do domínio em DTOs otimizados (GetUnitByIdQuery, ListCommunitiesQuery) podendo acessar DbContext diretamente para performance ignorando agregados complexos quando apropriado. DTOS define objetos de transferência de dados imutáveis (records C#) usados para input de commands, output de queries e contratos de API evitando expor entidades de domínio diretamente. VALIDATORS contém FluentValidation validators para cada command/DTO validando regras simples (required, max length, format) e delegando validações de domínio complexas para as entidades. MAPPERS documenta estratégias de mapeamento entre domain entities e DTOs usando AutoMapper ou mapeamento manual explícito.

## Subpastas

- **[COMMANDS/](./COMMANDS/README.md)** - Commands CQRS para writes (CreateUnit, UpdateHolder, etc)
- **[QUERIES/](./QUERIES/README.md)** - Queries CQRS para reads otimizados
- **[DTOS/](./DTOS/README.md)** - Data Transfer Objects para API e transferência entre camadas
- **[VALIDATORS/](./VALIDATORS/README.md)** - FluentValidation validators para commands/DTOs
- **[MAPPERS/](./MAPPERS/README.md)** - Mapeamento Domain ↔ DTOs

---

**Última atualização:** 2026-01-12

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (0 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Commands](./COMMANDS/README.md) | 0 |
|  | [Dtos](./DTOS/README.md) | 0 |
|  | [Mappers](./MAPPERS/README.md) | 0 |
|  | [Queries](./QUERIES/README.md) | 0 |
|  | [Validators](./VALIDATORS/README.md) | 0 |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Pronto
