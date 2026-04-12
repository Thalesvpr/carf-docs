---
type: leaf
status: approved
updated: 2026-02-07
---

# Aggregates Diagram

Descricao dos aggregates e seus relacionamentos no modelo de dominio CARF, seguindo padroes de Domain-Driven Design.

## Unit Aggregate

Unit e o aggregate root. Contem tres componentes internos: Address (value object para endereco), Geometry (value object para poligono e area) e Photo (entity para fotos da unidade).

## Holder Aggregate

Holder e o aggregate root. Armazena CPF como Value Object (DOMAIN.ValueObjects.CPF, validado via algoritmo Mod11 no construtor), Contact (telefone e email como strings) e Income (renda declarada como decimal).

## Community Aggregate

Community e o aggregate root. Contem Geometry (value object para limites da area) e Contact (entity para contatos da comunidade).

## Legitimation Aggregate

Legitimation e o aggregate root. Contem Document (entity para documentos anexados) e History (entity para historico de transicoes de status).

## Composicao dos Aggregates

| Aggregate | Root | Componentes Internos | Tipo |
|-----------|------|---------------------|------|
| Unit | Unit | Address, Geometry, Photo | Value Object, Value Object, Entity |
| Holder | Holder | CPF (Value Object), Contact (strings), Income (decimal) | CPF e Value Object no DOMAIN layer; demais primitivos validados no APPLICATION layer |
| Community | Community | Geometry, Contact | Value Object, Entity |
| Legitimation | Legitimation | Document, History | Entity, Entity |

## Referencias entre Aggregates

| Origem | Destino | Mecanismo |
|--------|---------|-----------|
| Unit | Holder | Tabela junction unit_holders (por ID) |
| Unit | Community | Chave estrangeira community_id |
| Legitimation | Unit | Chave estrangeira unit_id |
| Legitimation | Holder | Lista de holder_ids |

## Regras de Aggregate

Cada aggregate possui invariantes que devem ser mantidas. Unit exige geometria valida e area maior que zero. Holder requer CPF unico por tenant e idade minima de 18 anos. Community precisa de nome unico por tenant e geometria que nao sobreponha outras comunidades. Legitimation segue state machine de workflow e exige documentos obrigatorios antes da aprovacao.

Referencias entre aggregates sao por ID apenas. Tabela unit_holders e junction table que nao pertence a nenhum aggregate. Cada aggregate e boundary de transacao. Multi-tenancy aplicado em todos via TenantId com RLS.
