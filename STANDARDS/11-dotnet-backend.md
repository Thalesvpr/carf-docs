---
type: standard
status: approved
updated: 2026-01-22
---

# STD-011: .NET 9 para Backend

## Regra

APIs backend devem usar .NET 9 com Entity Framework Core e NetTopologySuite para operacoes geoespaciais. Proibido Node.js, Python ou Java para servicos core de backend.

## Justificativa

Performance 3-5x superior em workloads PostGIS com compilacao AOT. Strong typing elimina bugs de runtime em calculos geometricos. Integracao nativa com Keycloak.

## Aplicacao

Projeto GEOAPI e qualquer novo servico backend. Excecao: scripts de automacao e ferramentas CLI podem usar outras linguagens.
