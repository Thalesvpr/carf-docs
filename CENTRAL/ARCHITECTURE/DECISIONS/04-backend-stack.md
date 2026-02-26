---
type: adr
status: approved
updated: 2026-02-21
---

# ADR-004: .NET 9 para Backend

## Contexto

Backend deve processar dados geoespaciais, implementar regras de negocio complexas e servir API REST para multiplos clientes. Performance e tipagem forte sao importantes para sistema critico. Equipe tem experiencia mista em diferentes stacks. Decisao impacta produtividade e contratacao futura.

## Decisao

Adotamos .NET 9 com C# como stack backend. Entity Framework Core com provider Npgsql para PostgreSQL e NetTopologySuite para geometrias. Clean Architecture organiza codigo em camadas com inversao de dependencia. MediatR implementa CQRS separando comandos de queries. O backend processa ortofotos recebidas do Operador de Drone, reduzindo tamanho e gerando versoes otimizadas, armazenando em bucket S3/MinIO segregado por tenant.

## Consequencias

Tipagem forte reduz bugs em tempo de execucao. Performance excelente do runtime .NET para processamento intensivo. Ferramentas maduras de profiling e debugging. Ecossistema menor que Node.js para bibliotecas especificas. Contratacao pode ser desafiadora em algumas regioes.

## Alternativas Rejeitadas

Node.js com TypeScript foi descartado por performance inferior em processamento geoespacial intensivo. Java Spring foi rejeitado por verbosidade e curva de aprendizado maior. Go foi descartado por ecossistema menos maduro para ORMs e falta de generics ate recentemente.
