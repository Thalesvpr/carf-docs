---
type: adr
status: review
updated: 2026-01-22
---
# ADR-001: .NET 9 para Backend

## Contexto

O backend GEOAPI precisa processar workloads geoespaciais intensivos com alta concorrencia. Requisitos RNF-001 e RNF-002 exigem P99 abaixo de 50ms e suporte a 10000+ usuarios simultaneos. A equipe possui experiencia em C# e a organizacao usa ferramentas Microsoft.

## Decisao

Adotamos .NET 9 com Entity Framework Core e NetTopologySuite. A escolha se justifica por performance 3-5x superior a Node.js em operacoes PostGIS devido a compilacao AOT, strong typing eliminando bugs de runtime em calculos geometricos, e integracao nativa com Keycloak via IdentityServer sem bibliotecas third-party instaveis.

## Consequencias

Performance consistente sob alta carga atendendo requisitos nao-funcionais. Reducao de bugs por strong typing e compile-time checks. Produtividade alta com equipe familiarizada. Integracao nativa com Azure DevOps. Overhead de memoria (~30MB vs ~10MB de Go) aceitavel. Curva de aprendizado para devs junior vindos de JavaScript.

## Alternativas Rejeitadas

Node.js descartado por performance inferior em workloads CPU-intensive e tipagem fraca. Java Spring Boot rejeitado por verbosidade e configuracao complexa de spatial extensions. Python FastAPI eliminado por GIL limitando concorrencia. Go descartado por ecossistema imaturo de bibliotecas geoespaciais e ausencia de ORM robusto.
