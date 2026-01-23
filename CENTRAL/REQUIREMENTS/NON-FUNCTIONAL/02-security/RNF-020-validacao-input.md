---
id: RNF-020
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-020: Validacao de Input

## Descricao

Todo input de usuarios deve ser validado e sanitizado antes de processamento. Protege contra ataques de injecao (SQL, XSS) e manipulacao maliciosa de dados.

## Metricas

- Validacao: FluentValidation para cada DTO
- ORM: Entity Framework Core com prepared statements
- Sanitizacao: escape de HTML/JS/CSS para outputs

## Criterios de Aceitacao

1. Todos os DTOs possuem validadores FluentValidation
2. Queries exclusivamente via EF Core (sem SQL concatenado)
3. Outputs sanitizados contra XSS antes de renderizacao
