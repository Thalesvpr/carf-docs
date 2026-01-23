---
id: RNF-062
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-062: Modularidade

## Descricao

Codigo deve ser organizado em camadas desacopladas (Controller, Service, Repository) com injecao de dependencias. Separacao de responsabilidades permite manutencao e testes independentes.

## Metricas

- Camadas: Controllers sem logica de negocio, Services com regras, Repository com acesso a dados
- Dependencias: injetadas via construtor, nao criadas internamente
- Interfaces: definidas para abstracoes e pontos de integracao

## Criterios de Aceitacao

1. Controllers delegam processamento para Services
2. Services coordenam Repositories sem acesso direto a banco
3. Componentes testaveis isoladamente com mocks
