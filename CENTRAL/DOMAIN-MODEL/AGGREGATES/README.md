# AGGREGATES

Aggregates são clusters de entidades e value objects tratados como unidade coesa, onde o aggregate root controla acesso e coordena mudanças de estado, garantindo consistência transacional dentro de fronteiras bem definidas.

O [UnitAggregate](./01-unit-aggregate.md) tem Unit como root coordenando relacionamentos com Holder, Documents, Annotations e SurveyPoints. Garante invariantes como ter ao menos um titular antes de aprovar, soma de percentuais de propriedade não exceder 100%, e geometria válida sem auto-interseções.

O [CommunityAggregate](./02-community-aggregate.md) tem Community como root coordenando Blocks, autorizações de acesso e documentos. Garante que a comunidade tenha ao menos uma autorização e que geometrias de quadras estejam dentro do perímetro.

O [LegitimationRequestAggregate](./03-legitimation-request-aggregate.md) tem LegitimationRequest como root coordenando pareceres, certidão, memorial descritivo, planta técnica e contestações. Segue workflow de 11 estados conforme Lei 13.465/2017 com prazo de 120 dias.

## Aggregates

- **[01-unit-aggregate.md](./01-unit-aggregate.md)** - Unidade habitacional
- **[02-community-aggregate.md](./02-community-aggregate.md)** - Comunidade ou assentamento
- **[03-legitimation-request-aggregate.md](./03-legitimation-request-aggregate.md)** - Processo de legitimação fundiária

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Aguardando (nova geração) index gerado por script.

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (3 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-unit-aggregate](./01-unit-aggregate.md) | Unit Aggregate |
| [02-community-aggregate](./02-community-aggregate.md) | Community Aggregate |
| [03-legitimation-request-aggregate](./03-legitimation-request-aggregate.md) | LegitimationRequest Aggregate |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
