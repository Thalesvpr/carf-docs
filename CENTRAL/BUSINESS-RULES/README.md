# BUSINESS-RULES

Regras de negócio que governam o comportamento do sistema CARF, assegurando compliance legal, integridade de dados e aderência aos processos estabelecidos.

As [regras de validação](./VALIDATION-RULES/README.md) garantem integridade e consistência dos dados, validando campos como CPF, CNPJ, email, telefone, coordenadas geográficas e polígonos antes da persistência. São executadas em múltiplas camadas: client-side, API e database constraints.

As [regras de workflow](./WORKFLOW-RULES/README.md) governam transições de status através de state machines, definindo quais mudanças são permitidas baseadas no status atual, role do usuário e pré-condições de negócio. Cobrem os workflows de unidade habitacional e legitimação fundiária.

As [regras de legitimação](./LEGITIMATION-RULES/README.md) estabelecem requisitos específicos conforme Lei 13.465/2017, diferenciando as modalidades REURB-S (interesse social) e REURB-E (interesse específico) quanto a área, custos e documentação obrigatória.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (22 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Legitimation Rules](./LEGITIMATION-RULES/README.md) | 6 |
|  | [Validation Rules](./VALIDATION-RULES/README.md) | 11 |
|  | [Workflow Rules](./WORKFLOW-RULES/README.md) | 5 |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
