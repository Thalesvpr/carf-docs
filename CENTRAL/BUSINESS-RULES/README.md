# BUSINESS-RULES

Regras de negócio que governam o comportamento do sistema CARF, assegurando compliance legal, integridade de dados e aderência aos processos estabelecidos.

As [regras de validação](./VALIDATION-RULES/README.md) garantem integridade e consistência dos dados, validando campos como CPF, CNPJ, email, telefone, coordenadas geográficas e polígonos antes da persistência. São executadas em múltiplas camadas: client-side, API e database constraints.

As [regras de workflow](./WORKFLOW-RULES/README.md) governam transições de status através de state machines, definindo quais mudanças são permitidas baseadas no status atual, role do usuário e pré-condições de negócio. Cobrem os workflows de unidade habitacional e legitimação fundiária.

As [regras de legitimação](./LEGITIMATION-RULES/README.md) estabelecem requisitos específicos conforme Lei 13.465/2017, diferenciando as modalidades REURB-S (interesse social) e REURB-E (interesse específico) quanto a área, custos e documentação obrigatória.

## Categorias

- **[VALIDATION-RULES/](./VALIDATION-RULES/README.md)** - Validação de dados e formatos
- **[WORKFLOW-RULES/](./WORKFLOW-RULES/README.md)** - Transições de status e permissões
- **[LEGITIMATION-RULES/](./LEGITIMATION-RULES/README.md)** - Regras da Lei 13.465/2017

---

**Última atualização:** 2026-01-14
