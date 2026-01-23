---
type: standard
status: review
updated: 2026-01-22
---

# STD-015: Clean Architecture com CQRS

## Regra

Backend deve seguir Clean Architecture com separacao Domain, Application, Infrastructure. Usar CQRS separando Commands de Queries. Domain Events para comunicacao entre aggregates.

## Justificativa

Desacoplamento permite testes unitarios sem infraestrutura. CQRS otimiza leitura e escrita independentemente. Events desacoplam dominios sem dependencias diretas.

## Aplicacao

Projeto GEOAPI. Commands para escrita, Queries para leitura, Domain Events via MediatR. Handlers em Application layer, Entities em Domain layer.
